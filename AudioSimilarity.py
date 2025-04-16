import os
import glob
import numpy as np
import librosa
from audio_similarity import AudioSimilarity
from pydub import AudioSegment
import math
import pyloudnorm as pyln
import soundfile as sf


'''
File Arrangement:
Specify a folder which contains 2 different audio.
The code would look for first 2 wav, if is not enough,
it would find first 2 mp3 or mp4 to convert wav from it.
'''
# ======= ONLY MODIFY THIS LINE TO CHANGE THE FOLDER =======
base_folder = './Riaraizu/'  # Change this to your target song folder
swap_compare = False  # Specifies which is "comparison file", and should be audio of yours.

# ======= Comparitive Constants =========
IDEAL_LUFS = -20

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
    # Note here librosa score are not token into account.
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

# ======= Standard AudioSimilarity Analysis =======
sample_rate = 44100
sample_size = 1
verbose = False

audio_similarity = AudioSimilarity(original_wav, compare_wav, sample_rate, weights,
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

def mfcc_similarity(file1, file2, sr=sample_rate, n_mfcc=20):
    y1, _ = librosa.load(file1, sr=sr)
    y2, _ = librosa.load(file2, sr=sr)
    mfcc1 = librosa.feature.mfcc(y=y1, sr=sr, n_mfcc=n_mfcc)
    mfcc2 = librosa.feature.mfcc(y=y2, sr=sr, n_mfcc=n_mfcc)
    return compute_cosine_similarity(mfcc1, mfcc2)

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
    return compute_cosine_similarity(delta1, delta2)

def dtw_aligned_similarity(feat1, feat2):
    """
    Compute a DTW-aligned similarity between two feature matrices.
    
    Instead of attempting to re-sample one feature matrix to match the other,
    this function iterates over the warping path (i,j) pairs and calculates
    the average frame difference.
    
    Parameters:
        feat1: numpy array of shape (K, N)
        feat2: numpy array of shape (K, M)
    
    Returns:
        mean_diff: Mean absolute difference over all aligned frames.
    """
    # Compute DTW warping path
    D, wp = librosa.sequence.dtw(feat1, feat2)
    
    # Compute difference for each pair (i, j)
    differences = []
    for i, j in wp:
        diff = np.mean(np.abs(feat1[:, i] - feat2[:, j]))
        differences.append(diff)
    
    return np.mean(differences)


mfcc_sim       = mfcc_similarity(original_wav, compare_wav) * 100
mfcc_delta_sim = (math.pi - math.acos(mfcc_delta_similarity(original_wav, compare_wav))) * 100 / math.pi 
tempogram_sim  = tempogram_similarity(original_wav, compare_wav) * 100

# Load audio and extract chroma features (no transposition needed)
y_orig, _ = librosa.load(original_wav, sr=sample_rate)
y_comp, _ = librosa.load(compare_wav, sr=sample_rate)
chroma_orig = librosa.feature.chroma_stft(y=y_orig, sr=sample_rate)
chroma_comp = librosa.feature.chroma_stft(y=y_comp, sr=sample_rate)

# Compute DTW-aligned similarity on chroma features
librosa_chroma_score = dtw_aligned_similarity(chroma_orig, chroma_comp) * 100


print("Standard AudioSimilarity Metrics:")
print(f"ZCR Similarity: {zcr_score:.2f}%")
print(f"Rhythm Similarity: {rhythm_score:.2f}%")
print(f"Chroma Similarity: {chroma_score:.2f}%")
print(f"Energy Envelope Similarity: {energy_score:.2f}%")
print(f"Spectral Contrast Similarity: {spectral_score:.2f}%")
print(f"Perceptual Similarity: {perceptual_score:.2f}%")
print(f"Overall Stent Weighted Audio Similarity: {overall_score:.2f}%")
print("")
print("Additional Revised Librosa Metrics:")
print(f"MFCC Similarity: {mfcc_sim:.2f}%")
print(f"MFCC Delta Similarity: {mfcc_delta_sim:.2f}%")
print(f"Tempogram Similarity: {tempogram_sim:.2f}%")
print(f"Librosa Chroma Similarity (DTW): {librosa_chroma_score:.2f}%")

# ======= Ear Friendly Rating Calculation using Pyloudnorm =======
def calculate_ear_friendly_score(audio_file, ideal_lufs=IDEAL_LUFS):
    data, rate = sf.read(audio_file)
    meter = pyln.Meter(rate)
    loudness = meter.integrated_loudness(data)
    score = max(min(100, 100 - abs(loudness - ideal_lufs) * 5), 0)
    print(f"Integrated Loudness: {loudness:.2f} LUFS")
    print(f"Estimated Ear Friendly Score: {score:.2f}%")
    return score

ear_friendly_score = calculate_ear_friendly_score(compare_wav)

# ======= Adaptive Final Score Calculation =======
final_score = overall_score * adaptive_weights['similarity'] + ear_friendly_score * adaptive_weights['comfort']
print(f"\nAdaptive Final Score: {final_score:.2f}%")
