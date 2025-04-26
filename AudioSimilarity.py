import os
import glob
import numpy as np
import librosa
import matplotlib.pyplot as plt
import soundfile as sf
import tempfile
import math
from audio_similarity import AudioSimilarity
from pydub import AudioSegment
import pyloudnorm as pyln

# ======= ONLY MODIFY THIS LINE TO CHANGE THE FOLDER =======
base_folder = './TTB/'  # Change this to your target song folder
swap_compare = True  # Specifies which is "comparison file", and should be audio of yours.

# ======= Comparitive Constants =========
sample_rate = 44100
sample_size = 1
verbose = False
TOP_DB = 40
# ======= Weight ratios =========
weights = {
    'zcr_similarity': 0.2,
    'rhythm_similarity': 0.2,
    'chroma_similarity': 0.2,
    'energy_envelope_similarity': 0.1,
    'spectral_contrast_similarity': 0.1,
    'perceptual_similarity': 0.2
}

adaptive_weights = {
    'similarity': 0.5,
    'comfort': 0.5,
    # Note here librosa score are not taken into account.
}

# ==========================================================
def convert_to_wav(input_path, wav_path):
    """
    Convert an input audio file (MP3 or MP4) to WAV.
    """
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.mp3':
        file_format = 'mp3'
        parameters = ["-f", "mp3", "-analyzeduration", "10000000", "-probesize", "5000000"]
    elif ext == '.mp4':
        file_format = 'mp4'
        parameters = []  # Default parameters for MP4
    else:
        print(f"Unsupported file extension: {ext}")
        return
    try:
        if parameters:
            audio = AudioSegment.from_file(input_path, format=file_format, parameters=parameters)
        else:
            audio = AudioSegment.from_file(input_path, format=file_format)
        audio.export(wav_path, format="wav")
        print(f"Converted {input_path} to {wav_path}")
    except Exception as e:
        print(f"Error decoding {input_path}: {e}")

def ensure_wav(file_path):
    """
    If the file is not in WAV format, convert it to WAV and return the WAV path.
    Otherwise, return the file_path unchanged.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.wav':
        return file_path
    else:
        wav_file = file_path.rsplit('.', 1)[0] + '.wav'
        convert_to_wav(file_path, wav_file)
        return wav_file

# ======= Locate Supported Audio Files =======
wav_files = sorted(glob.glob(os.path.join(base_folder, "*.wav")))
if len(wav_files) >= 2:
    original_file = wav_files[0]
    compare_file = wav_files[1]
    print("Using two WAV files found in folder.")
else:
    other_files = []
    for ext in ['mp3', 'mp4']:
        other_files.extend(glob.glob(os.path.join(base_folder, f"*.{ext}")))
    other_files = sorted(other_files)
    if len(other_files) >= 2:
        original_file = other_files[0]
        compare_file = other_files[1]
        print("Less than two WAV files found. Using first two MP3/MP4 files for conversion.")
    else:
        raise Exception("Not enough audio files found! Please drop at least two WAV files, or two MP3/MP4 files if no WAV are present.")

original_wav = ensure_wav(original_file)
compare_wav = ensure_wav(compare_file)

if swap_compare:
    original_wav, compare_wav = compare_wav, original_wav

print("\n--- Debug Info ---")
print(f"Using original file: {original_wav}")
print(f"Using comparison file: {compare_wav}")
print("------------------\n")

# ======= DTW-Based Audio Alignment =======
def plot_alignment_comparison(y_orig, y_orig_aligned, y_comp, y_comp_aligned, sr, show_seconds=5):
    plt.figure(figsize=(14, 8))
    
    # For the original file subplot, compare raw vs. aligned
    min_len_orig = min(len(y_orig), len(y_orig_aligned))
    x_axis_orig = np.arange(min_len_orig) / sr
    plt.subplot(2, 1, 1)
    plt.plot(x_axis_orig[::10], y_orig[:min_len_orig:10], alpha=0.7, label='Original (Raw)')
    plt.plot(x_axis_orig[::10], y_orig_aligned[:min_len_orig:10], alpha=0.7, label='Comparison (Aligned)')
    plt.xlim(0, show_seconds)
    plt.title("Original File: Raw vs Aligned")
    plt.ylabel("Amplitude")
    plt.legend()
    
    # For the comparison file subplot, compare raw vs. aligned
    min_len_comp = min(len(y_comp), len(y_comp_aligned))
    x_axis_comp = np.arange(min_len_comp) / sr
    plt.subplot(2, 1, 2)
    plt.plot(x_axis_comp[::10], y_comp[:min_len_comp:10], alpha=0.7, label='Comparison (Raw)')
    plt.plot(x_axis_comp[::10], y_comp_aligned[:min_len_comp:10], alpha=0.7, label='Comparison (Aligned)')
    plt.xlim(0, show_seconds)
    plt.title("Comparison File: Raw vs Aligned")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig("alignment_visualization.png")
    print("Alignment visualization saved to alignment_visualization.png")

# ======= Load and Align Audio =======
# Load the original and comparison audio files
y_orig, sr = librosa.load(original_wav, sr=sample_rate)
y_comp, sr_comp = librosa.load(compare_wav, sr=sample_rate)

y_orig_aligned, _ = librosa.effects.trim(y_orig, top_db=TOP_DB)
y_target_aligned, _ = librosa.effects.trim(y_comp, top_db=TOP_DB)

plot_alignment_comparison(y_orig, y_orig_aligned,
                          y_comp, y_target_aligned,
                          sr=sample_rate,
                          show_seconds=60)

# ======= Save the Aligned Audio to Temporary Files =======
with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as orig_temp:
    sf.write(orig_temp.name, y_orig_aligned, sample_rate)
    aligned_original = orig_temp.name

with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as comp_temp:
    sf.write(comp_temp.name, y_target_aligned, sample_rate)
    aligned_compare = comp_temp.name

# ======= Standard AudioSimilarity Analysis =======

audio_similarity = AudioSimilarity(aligned_original, aligned_compare, 
                                   sample_rate, weights,
                                   verbose=verbose, sample_size=sample_size)

zcr_score = audio_similarity.zcr_similarity() * 100
rhythm_score = audio_similarity.rhythm_similarity() * 100
chroma_score = audio_similarity.chroma_similarity() * 100
energy_score = audio_similarity.energy_envelope_similarity() * 100
spectral_score = audio_similarity.spectral_contrast_similarity() * 100
perceptual_score = audio_similarity.perceptual_similarity() * 100
overall_score = audio_similarity.stent_weighted_audio_similarity() * 100

# ======= Additional Revised Librosa Metrics =======
def compute_cosine_similarity(feature1, feature2):
    mean1 = np.mean(feature1, axis=1)
    mean2 = np.mean(feature2, axis=1)
    dot = np.dot(mean1, mean2)
    norm1 = np.linalg.norm(mean1)
    norm2 = np.linalg.norm(mean2)
    if norm1 * norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def tempogram_similarity(file1, file2, sr=sample_rate):
    y1, _ = librosa.load(file1, sr=sr)
    y2, _ = librosa.load(file2, sr=sr)
    temp1 = librosa.feature.tempogram(y=y1, sr=sr)
    temp2 = librosa.feature.tempogram(y=y2, sr=sr)
    return compute_cosine_similarity(temp1, temp2)

def mfcc_delta_similarity(file1, file2, sr=sample_rate, n_mfcc=20):
    y1, _ = librosa.load(file1, sr=sr)
    y2, _ = librosa.load(file2, sr=sr)
    mfcc1 = librosa.feature.mfcc(y=y1, sr=sr, n_mfcc=n_mfcc)
    mfcc2 = librosa.feature.mfcc(y=y2, sr=sr, n_mfcc=n_mfcc)
    delta1 = librosa.feature.delta(mfcc1)
    delta2 = librosa.feature.delta(mfcc2)
    return compute_cosine_similarity(mfcc1, mfcc2), compute_cosine_similarity(delta1, delta2)

def dtw_aligned_similarity(feat1, feat2):
    """
    Compute a DTW-aligned similarity between two feature matrices.
    """
    D, wp = librosa.sequence.dtw(feat1, feat2)
    differences = []
    for i, j in wp:
        diff = np.mean(np.abs(feat1[:, i] - feat2[:, j]))
        differences.append(diff)
    return np.mean(differences)

# (Uncomment or adjust additional metric functions as desired)
mfcc_sim, mfcc_delta_sim = mfcc_delta_similarity(aligned_original, aligned_compare)
# mfcc_delta_sim = (math.pi - math.acos(mfcc_delta_similarity(aligned_original, aligned_compare))) * 100 / math.pi 
tempogram_sim  = tempogram_similarity(aligned_original, aligned_compare) * 100

# Load audio and extract chroma features
y_comp = y_target_aligned
chroma_orig = librosa.feature.chroma_stft(y=y_orig, sr=sample_rate)
chroma_comp = librosa.feature.chroma_stft(y=y_comp, sr=sample_rate)
librosa_chroma_score = dtw_aligned_similarity(chroma_orig, chroma_comp) * 100

# Clean up temporary aligned files
os.unlink(aligned_original)
os.unlink(aligned_compare)

loudness_original = pyln.Meter(sr_comp).integrated_loudness(y_comp)


# ====== Print Results ======
print(f"ZCR Similarity: {zcr_score:.2f}%")
print(f"Rhythm Similarity: {rhythm_score:.2f}%")
print(f"Chroma Similarity: {chroma_score:.2f}%")
print(f"Energy Envelope Similarity: {energy_score:.2f}%")
print(f"Spectral Contrast Similarity: {spectral_score:.2f}%")
print(f"Perceptual Similarity: {perceptual_score:.2f}%")
print(f"Stent Weighted Audio Similarity: {overall_score:.2f}%")
print("")
print(f"MFCC Similarity: {mfcc_sim:.2f}")
print(f"MFCC Delta Similarity: {mfcc_delta_sim:.2f}")
print(f"Tempogram Similarity: {tempogram_sim:.2f}%")
print(f"Librosa Chroma Similarity (DTW): {librosa_chroma_score:.2f}%")
print(f"Integrated loudness: {loudness_original:.2f}LUFS" )