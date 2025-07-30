license = """
MIT License

Copyright (c) 2025 OctoFlare

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from mido import MidiFile, tempo2bpm
from tkinter import filedialog
from dataclasses import dataclass, field
from pathlib import Path
import pynbs
import math
import statistics

@dataclass
class MNote:
	x: int = 0
	note: int = 0
	vel: float = 0.0
	channel: int = 0
	until: int = -1

@dataclass
class MPerc:
	note: int = 0
	ins: int = 0
	pitch: float = 0.0

@dataclass
class MTrack:
	name: str = ""
	notes: list[MNote] = field(default_factory=list)
	amount: int = 0
	length: int = -1

def note_exists(x, y, song):
	for note in song.notes:
		if note.tick == x and note.layer == y:
			return True
	return False

def replace_note(x, y, song, ins, key, vel, pan, pit):
	for note in song.notes:
		if note.tick == x and note.layer == y:
			note.instrument = ins
			note.key = key
			note.velocity = vel
			note.panning = pan
			note.pitch = pit
			return

def main():

	print(license)

	midi_ins = []

	# Piano
	midi_ins.append({"name": "Acoustic Grand Piano", "shortName": "Piano 1", "instrument": 0, "pitch": 0})
	midi_ins.append({"name": "Bright Acoustic Piano", "shortName": "Piano 2", "instrument": 15, "pitch": 0})
	midi_ins.append({"name": "Electric Grand Piano", "shortName": "Piano 3", "instrument": 15, "pitch": 0})
	midi_ins.append({"name": "Honky-tonk Piano", "shortName": "Honky-tonk", "instrument": 15, "pitch": 0})
	midi_ins.append({"name": "Electric Piano 1", "shortName": "E.Piano 1", "instrument": 0, "pitch": 0})
	midi_ins.append({"name": "Electric Piano 2", "shortName": "E.Piano 2", "instrument": 0, "pitch": 0})
	midi_ins.append({"name": "Harpsichord", "shortName": "", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "Clavinet", "shortName": "", "instrument": 14, "pitch": 0})

	# Chromatic Percussion
	midi_ins.append({"name": "Celesta", "shortName": "", "instrument": 7, "pitch": -2})
	midi_ins.append({"name": "Glockenspiel", "shortName": "", "instrument": 7, "pitch": -2})
	midi_ins.append({"name": "Music Box", "shortName": "", "instrument": 7, "pitch": -2})
	midi_ins.append({"name": "Vibraphone", "shortName": "", "instrument": 10, "pitch": 0})
	midi_ins.append({"name": "Marimba", "shortName": "", "instrument": 10, "pitch": 0})
	midi_ins.append({"name": "Xylophone", "shortName": "", "instrument": 9, "pitch": -2})
	midi_ins.append({"name": "Tubular Bells", "shortName": "", "instrument": 7, "pitch": -2})
	midi_ins.append({"name": "Dulcimer", "shortName": "", "instrument": 5, "pitch": 1})

	# Organ
	midi_ins.append({"name": "Drawbar Organ", "shortName": "Organ 1", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Percussive Organ", "shortName": "Organ 2", "instrument": 10, "pitch": 0})
	midi_ins.append({"name": "Rock Organ", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Church Organ", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Reed Organ", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Accordion", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Harmonica", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Bandoneon", "shortName": "", "instrument": 6, "pitch": -1})

	# Guitar
	midi_ins.append({"name": "Acoustic Guitar (nylon)", "shortName": "Nylon-str.Gt", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "Acoustic Guitar (steel)", "shortName": "Steel-str.Gt", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "Electric Guitar (jazz)", "shortName": "Jazz Guitar", "instrument": 0, "pitch": 0})
	midi_ins.append({"name": "Electric Guitar (clean)", "shortName": "Clean Guitar", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "Electric Guitar (muted)", "shortName": "Muted Guitar", "instrument": 1, "pitch": 2})
	midi_ins.append({"name": "Overdriven Guitar", "shortName": "Overdrive Gt", "instrument": 12, "pitch": 2})
	midi_ins.append({"name": "Distortion Guitar", "shortName": "Distortion Gt", "instrument": 12, "pitch": 2})
	midi_ins.append({"name": "Guitar Harmonics", "shortName": "Gt Harmonics", "instrument": 5, "pitch": 3})

	# Bass
	midi_ins.append({"name": "Acoustic Bass", "shortName": "", "instrument": 1, "pitch": 2})
	midi_ins.append({"name": "Electric Bass (finger)", "shortName": "Fingered Bass", "instrument": 1, "pitch": 2})
	midi_ins.append({"name": "Electric Bass (pick)", "shortName": "Picked Bass", "instrument": 1, "pitch": 2})
	midi_ins.append({"name": "Fretless Bass", "shortName": "", "instrument": 1, "pitch": 2})
	midi_ins.append({"name": "Slap Bass 1", "shortName": "", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "Slap Bass 2", "shortName": "", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "Synth Bass 1", "shortName": "", "instrument": 1, "pitch": 2})
	midi_ins.append({"name": "Synth Bass 2", "shortName": "", "instrument": 15, "pitch": 0})

	# Strings
	midi_ins.append({"name": "Violin", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Viola", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Cello", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Contrabass", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Tremolo Strings", "shortName": "Tremolo aStr.", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Pizzicato Strings", "shortName": "Pizzicato", "instrument": 1, "pitch": 2})
	midi_ins.append({"name": "Orchestral Harp", "shortName": "Harp", "instrument": 0, "pitch": 0})
	midi_ins.append({"name": "Timpani", "shortName": "", "instrument": 3, "pitch": 0})

	# Ensemble
	midi_ins.append({"name": "String Ensemble 1", "shortName": "Strings 1", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "String Ensemble 2", "shortName": "Strings 2", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Synth Strings 1", "shortName": "Syn.Strings1", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Synth Strings 2", "shortName": "Syn.Strings2", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Choir Aahs", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Voice Oohs", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Synth Voice", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Orchestra Hit", "shortName": "", "instrument": 3, "pitch": -1})

	# Brass
	midi_ins.append({"name": "Trumpet", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Trombone", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Tuba", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Muted Trumpet", "shortName": "", "instrument": 12, "pitch": 2})
	midi_ins.append({"name": "French Horn", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Brass Section", "shortName": "Brass", "instrument": 12, "pitch": 2})
	midi_ins.append({"name": "Synth Brass 1", "shortName": "", "instrument": 12, "pitch": 2})
	midi_ins.append({"name": "Synth Brass 2", "shortName": "", "instrument": 6, "pitch": -1})

	# Reed
	midi_ins.append({"name": "Soprano Sax", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Alto Sax", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Tenor Sax", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Baritone Sax", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Oboe", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "English Horn", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Bassoon", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Clarinet", "shortName": "", "instrument": 6, "pitch": -1})

	# Pipe
	midi_ins.append({"name": "Piccolo", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Flute", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Recorder", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Pan Flute", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Blown Bottle", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Shakuhachi", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Whistle", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Ocarina", "shortName": "", "instrument": 6, "pitch": -1})

	# Synth Lead
	midi_ins.append({"name": "Lead 1 (square)", "shortName": "Square Lead", "instrument": 13, "pitch": 0})
	midi_ins.append({"name": "Lead 2 (sawtooth)", "shortName": "Saw Lead", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Lead 3 (calliope)", "shortName": "Calliope", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Lead 4 (chiff)", "shortName": "Chiff Lead", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Lead 5 (charang)", "shortName": "Charang", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "Lead 6 (voice)", "shortName": "Voice Lead", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Lead 7 (fifths)", "shortName": "Fifth Lead", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Lead 8 (bass + lead)", "shortName": "Bass+Lead", "instrument": 1, "pitch": 2})

	# Synth Pad
	midi_ins.append({"name": "Pad 1 (new age)", "shortName": "Fantasia", "instrument": 7, "pitch": -2})
	midi_ins.append({"name": "Pad 2 (warm)", "shortName": "Warm Pad", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Pad 3 (polysynth)", "shortName": "Polysynth", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Pad 4 (choir)", "shortName": "Space Choir", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Pad 5 (bowed)", "shortName": "Bowed Glass", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Pad 6 (metallic)", "shortName": "Metal Pad", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Pad 7 (halo)", "shortName": "Halo Pad", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Pad 8 (sweep)", "shortName": "Sweep Pad", "instrument": 8, "pitch": -2})

	# Synth Effects
	midi_ins.append({"name": "FX 1 (rain)", "shortName": "Rain Drop", "instrument": 8, "pitch": -2})
	midi_ins.append({"name": "FX 2 (soundtrack)", "shortName": "Soundtrack", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "FX 3 (crystal)", "shortName": "Crystal", "instrument": 8, "pitch": -2})
	midi_ins.append({"name": "FX 4 (atmosphere)", "shortName": "Atmosphere", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "FX 5 (brightness)", "shortName": "Brightness", "instrument": 15, "pitch": 0})
	midi_ins.append({"name": "FX 6 (goblins)", "shortName": "Goblins", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "FX 7 (echoes)", "shortName": "Echoes", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "FX 8 (sci-fi)", "shortName": "SF", "instrument": 5, "pitch": 1})

	# Ethnic
	midi_ins.append({"name": "Sitar", "shortName": "", "instrument": 14, "pitch": 0})
	midi_ins.append({"name": "Banjo", "shortName": "", "instrument": 14, "pitch": 0})
	midi_ins.append({"name": "Shamisen", "shortName": "", "instrument": 14, "pitch": 0})
	midi_ins.append({"name": "Koto", "shortName": "", "instrument": 5, "pitch": 1})
	midi_ins.append({"name": "Kalimba", "shortName": "", "instrument": 10, "pitch": 0})
	midi_ins.append({"name": "Bag pipe", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Fiddle", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Shanai", "shortName": "", "instrument": 6, "pitch": -1})

	# Percussive
	midi_ins.append({"name": "Tinkle Bell", "shortName": "", "instrument": 8, "pitch": -2})
	midi_ins.append({"name": "Agogo", "shortName": "", "instrument": 11, "pitch": -1})
	midi_ins.append({"name": "Steel Drums", "shortName": "", "instrument": 10, "pitch": 0})
	midi_ins.append({"name": "Woodblock", "shortName": "", "instrument": 9, "pitch": -2})
	midi_ins.append({"name": "Taiko Drum", "shortName": "", "instrument": 2, "pitch": 0})
	midi_ins.append({"name": "Melodic Tom", "shortName": "", "instrument": 3, "pitch": 0})
	midi_ins.append({"name": "Synth Drum", "shortName": "", "instrument": 3, "pitch": 0})
	midi_ins.append({"name": "Reverse Cymbal", "shortName": "Reverse Cym.", "instrument": 3, "pitch": 10})

	# Sound Effects
	midi_ins.append({"name": "Guitar Fret Noise", "shortName": "Gt Fret Noise", "instrument": 4, "pitch": 1})
	midi_ins.append({"name": "Breath Noise", "shortName": "", "instrument": 6, "pitch": -1})
	midi_ins.append({"name": "Seashore", "shortName": "", "instrument": 8, "pitch": -2})
	midi_ins.append({"name": "Bird Tweet", "shortName": "Bird", "instrument": 6, "pitch": 1})
	midi_ins.append({"name": "Telephone Ring", "shortName": "Telephone", "instrument": 7, "pitch": 2})
	midi_ins.append({"name": "Helicopter", "shortName": "", "instrument": 2, "pitch": 0})
	midi_ins.append({"name": "Applause", "shortName": "", "instrument": 3, "pitch": 0})
	midi_ins.append({"name": "Gunshot", "shortName": "", "instrument": 3, "pitch": 0})

	midi_drum = []
	for i in range(24):
		midi_drum.append({})

	# Percussion
	midi_drum.append({"name": "Cutting Noise(SFX)", "instrument": 13, "pitch": 39})
	midi_drum.append({"name": "Snare Roll", "instrument": 3, "pitch": 8})
	midi_drum.append({"name": "Finger Snap", "instrument": 4, "pitch": 25})
	midi_drum.append({"name": "High Q", "instrument": 3, "pitch": 18})
	midi_drum.append({"name": "Slap", "instrument": 3, "pitch": 27})
	midi_drum.append({"name": "Scratch Push", "instrument": 4, "pitch": 16})
	midi_drum.append({"name": "Scratch Pull", "instrument": 4, "pitch": 13})
	midi_drum.append({"name": "Sticks", "instrument": 4, "pitch": 9})
	midi_drum.append({"name": "Square Click", "instrument": 4, "pitch": 6})
	midi_drum.append({"name": "Metronome Click", "instrument": 4, "pitch": 2})
	midi_drum.append({"name": "Metronome Bell", "instrument": 8, "pitch": 17})

	# 35
	midi_drum.append({"name": "Bass Drum 2", "instrument": 2, "pitch": 10})
	midi_drum.append({"name": "Bass Drum 1", "instrument": 2, "pitch": 6})
	midi_drum.append({"name": "Side Stick", "instrument": 4, "pitch": 6})
	midi_drum.append({"name": "Snare Drum 1", "instrument": 3, "pitch": 8})
	midi_drum.append({"name": "Hand Clap", "instrument": 4, "pitch": 6})
	midi_drum.append({"name": "Snare Drum 2", "instrument": 3, "pitch": 4})
	midi_drum.append({"name": "Low Tom 2", "instrument": 2, "pitch": 6})

	# 42
	midi_drum.append({"name": "Closed Hi-hat", "instrument": 3, "pitch": 22})
	midi_drum.append({"name": "Low Tom 1", "instrument": 2, "pitch": 13})
	midi_drum.append({"name": "Pedal Hi-hat", "instrument": 3, "pitch": 22})
	midi_drum.append({"name": "Mid Tom 2", "instrument": 2, "pitch": 15})
	midi_drum.append({"name": "Open Hi-hat", "instrument": 3, "pitch": 18})
	midi_drum.append({"name": "Mid Tom 1", "instrument": 2, "pitch": 20})
	midi_drum.append({"name": "High Tom 2", "instrument": 2, "pitch": 23})

	# 49
	midi_drum.append({"name": "Crash Cymbal 1", "instrument": 3, "pitch": 17})
	midi_drum.append({"name": "High Tom 1", "instrument": 2, "pitch": 23})
	midi_drum.append({"name": "Ride Cymbal 1", "instrument": 3, "pitch": 24})
	midi_drum.append({"name": "Chinese Cymbal", "instrument": 3, "pitch": 8})
	midi_drum.append({"name": "Ride Bell", "instrument": 3, "pitch": 13})
	midi_drum.append({"name": "Tambourine", "instrument": 4, "pitch": 18})
	midi_drum.append({"name": "Splash Cymbal", "instrument": 3, "pitch": 18})

	# 56
	midi_drum.append({"name": "Cowbell", "instrument": 11, "pitch": 5})
	midi_drum.append({"name": "Crash Cymbal 2", "instrument": 3, "pitch": 13})
	midi_drum.append({"name": "Vibraslap", "instrument": 4, "pitch": 2})
	midi_drum.append({"name": "Ride Cymbal 2", "instrument": 3, "pitch": 13})
	midi_drum.append({"name": "High Bongo", "instrument": 4, "pitch": 9})
	midi_drum.append({"name": "Low Bongo", "instrument": 4, "pitch": 2})
	midi_drum.append({"name": "Mute High Conga", "instrument": 4, "pitch": 8})

	# 63
	midi_drum.append({"name": "Open High Conga", "instrument": 2, "pitch": 22})
	midi_drum.append({"name": "Low Conga", "instrument": 2, "pitch": 15})
	midi_drum.append({"name": "High Timbale", "instrument": 3, "pitch": 13})
	midi_drum.append({"name": "Low Timbale", "instrument": 3, "pitch": 8})
	midi_drum.append({"name": "High Agogo", "instrument": 9, "pitch": 12})
	midi_drum.append({"name": "Low Agogo", "instrument": 9, "pitch": 5})
	midi_drum.append({"name": "Cabasa", "instrument": 4, "pitch": 20})

	# 70
	midi_drum.append({"name": "Maracas", "instrument": 4, "pitch": 23})
	midi_drum.append({"name": "Short Whistle", "instrument": 6, "pitch": 34})
	midi_drum.append({"name": "Long Whistle", "instrument": 6, "pitch": 33})
	midi_drum.append({"name": "Short Guiro", "instrument": 4, "pitch": 17})
	midi_drum.append({"name": "Long Guiro", "instrument": 4, "pitch": 11})
	midi_drum.append({"name": "Claves", "instrument": 4, "pitch": 18})
	midi_drum.append({"name": "High Wood Block", "instrument": 4, "pitch": 10})

	# 77
	midi_drum.append({"name": "Low Wood Block", "instrument": 4, "pitch": 5})
	midi_drum.append({"name": "Mute Cuica", "instrument": 12, "pitch": 25})
	midi_drum.append({"name": "Open Cuica", "instrument": 12, "pitch": 26})
	midi_drum.append({"name": "Mute Triangle", "instrument": 4, "pitch": 16})
	midi_drum.append({"name": "Open Triangle", "instrument": 8, "pitch": 19})
	midi_drum.append({"name": "Shaker", "instrument": 3, "pitch": 22})
	midi_drum.append({"name": "Jingle Bell", "instrument": 8, "pitch": 6})

	# 84
	midi_drum.append({"name": "Bell Tree", "instrument": 8, "pitch": 15})
	midi_drum.append({"name": "Castanets", "instrument": 4, "pitch": 21})
	midi_drum.append({"name": "Mute Surdo", "instrument": 2, "pitch": 14})
	midi_drum.append({"name": "Open Surdo", "instrument": 2, "pitch": 7})

	midiPrecision = 1 # 0, 1, 3, 7
	midiVel = 1
	midiRemoveSilent = 1
	midiOctave = 0
	midiMaxHeight = 20
	midiName = 1
	midiNamePatch = 1
	extendNotes = 1 # whether to represent note off events or not
	tempoChanger = 1 # whether to include tempo changes or not
	tempoChangerX = []
	tempoChangerTempo = []
	tempoChangerCount = 0
	deltaPerTick = 0
	midiTempo = 0
	midiCopyright = ""
	midiTracks = []
	midiMinPos = -1
	midiMaxPos = -1
	midiChannels = -1
	midiPercs = []
	midiChannelPatch = []
	midiChannelIns = []
	midiChannelOctave = []
	for i in range(128):
		midiChannelIns.append(0)
		midiChannelOctave.append(0)
		midiChannelPatch.append(0)

	midiPath = filedialog.askopenfilename(
		title="Select a MIDI File",
		filetypes=[("MIDI Files", "*.mid *.midi")]
	)

	print("Converting, please wait...")

	midiFile = MidiFile(midiPath)

	midiTempo = midiFile.ticks_per_beat

	for i, track in enumerate(midiFile.tracks):
		p = 0
		delta = 0
		midiTracks.append(MTrack("", []))
		for msg in track:
			delta = msg.time
			p += delta
			if msg.is_meta:
				if msg.type == 'copyright':
					midiCopyright = msg.text
				elif msg.type == 'track_name':
					midiTracks[i].name = msg.name
				elif msg.type == 'set_tempo':
					tempoChangerX.append(p)
					tempoChangerTempo.append(60000000.0 / msg.tempo)
					#print(msg.tempo)
					#print(60000000.0 / msg.tempo)
					#print(tempoChangerTempo)
					tempoChangerCount += 1
			else:
				if msg.type == 'note_off':
					if msg.channel != 9 and extendNotes == 1:
						if p < midiMinPos or midiMinPos == -1:
							midiMinPos = p
						for aaa in reversed(midiTracks[i].notes):
							if msg.note == aaa.note and msg.channel == aaa.channel:
								if aaa.until == -1:
									aaa.until = p
								break
						midiMaxPos = max(midiMaxPos, p)
				elif msg.type == 'note_on':
					if (msg.velocity == 0):
						if msg.channel != 9:
							if p < midiMinPos or midiMinPos == -1:
								midiMinPos = p
							for aaa in reversed(midiTracks[i].notes):
								if msg.note == aaa.note and msg.channel == aaa.channel:
									if aaa.until == -1:
										aaa.until = p
									break
							midiMaxPos = max(midiMaxPos, p)
					else:
						if msg.channel != 9 or (msg.note >= 24 and msg.note <= 84):
							if p < midiMinPos or midiMinPos == -1:
								midiMinPos = p
							midiMaxPos = max(midiMaxPos, p)
							midiTracks[i].notes.append(MNote(p, msg.note, msg.velocity, msg.channel))
							midiTracks[i].amount += 1
							midiTracks[i].length = max(midiTracks[i].length, p)
							midiChannels = max(midiChannels, msg.channel)
							if msg.channel == 9:
								exist = 0
								for perc in midiPercs:
									if perc.note == msg.note:
										exist = 1
										break
								if exist == 0:
									midiPercs.append(MPerc(msg.note, 0, 0))
				elif msg.type == 'program_change':
					midiChannelPatch[msg.channel] = msg.program

	midiPercIns = []
	midiPercPitch = []
	for i in range(len(midiPercs)):
		midiPercIns.append(-1)
		midiPercPitch.append(33)

	midiChannels += 1
	for i in range(16):
		try:
			midiChannelIns[i] = midi_ins[midiChannelPatch[i]]["instrument"]
			midiChannelOctave[i] = midi_ins[midiChannelPatch[i]]["pitch"]
		except:
			midiChannelIns.append(-1)
			midiChannelOctave.append(0)
	for i in range(len(midiPercs)):
		try:
			midiPercIns[i] = midi_drum[midiPercs[i].note]["instrument"]
			midiPercPitch[i] = midi_drum[midiPercs[i].note]["pitch"] + 33
		except:
			midiPercIns.append(-1)
			midiPercPitch.append(33)
	midiLength = 0

	nbsFile = pynbs.new_file()

	nbsFile.header.tempo = tempoChangerTempo[0] * (midiPrecision + 1) / 15

	deltaPerTick = (midiTempo & 0x7FFF) / 4 / (midiPrecision + 1)

	channelHeight = []
	posamount = []
	ins1notes = []
	ins2notes = []
	ins3notes = []
	ins4notes = []
	ins5notes = []
	ins6notes = []
	ins7notes = []
	ins8notes = []
	ins9notes = []
	ins10notes = []

	onNotes = []

	if tempoChanger == 1:
		nbsFile.instruments.append(pynbs.Instrument(id = 16, name = "Tempo Changer", file = ""))

	for i in range(midiChannels + 1):
		channelHeight.append(0)
		posamount.append([])
		for j in range(math.floor((midiMaxPos - midiMinPos * midiRemoveSilent) / deltaPerTick) + 1):
			posamount[i].append(0)

	for i in range(88):
		ins1notes.append([])
		ins2notes.append([])
		ins3notes.append([])
		ins4notes.append([])
		ins5notes.append([])
		ins6notes.append([])
		ins7notes.append([])
		ins8notes.append([])
		ins9notes.append([])
		ins10notes.append([])
		for j in range(math.floor((midiMaxPos - midiMinPos * midiRemoveSilent) / deltaPerTick) + 1):
			ins1notes[i].append(0)
			ins2notes[i].append(0)
			ins3notes[i].append(0)
			ins4notes[i].append(0)
			ins5notes[i].append(0)
			ins6notes[i].append(0)
			ins7notes[i].append(0)
			ins8notes[i].append(0)
			ins9notes[i].append(0)
			ins10notes[i].append(0)

	for track in midiTracks:
		for note in track.notes:
			channel = note.channel
			anote = statistics.median([0, note.note - 21, 87])
			vel = 100
			if midiVel:
				vel = note.vel
			pos = math.floor((note.x - midiMinPos * midiRemoveSilent) / deltaPerTick)
			until = math.floor((note.until - midiMinPos * midiRemoveSilent) / deltaPerTick)
			stop = 0
			if (channel == 9):
				a = 0
				while a < len(midiPercs):
					if (midiPercs[a].note == note.note):
						if midiPercs[a].ins == -1:
							stop = 1
							break
					a += 1
				a -= 1
				anote = statistics.median([0, midiPercs[a].pitch, 87])
			else:
				if midiChannelIns[channel] == -1:
					stop = 1
				anote += 12 * midiChannelOctave[channel]
				anote = statistics.median([0, anote, 87])
			if midiOctave == 1:
				while anote < 33:
					anote += 12
				while anote > 57:
					anote -= 12
			if stop == 0:
				if (channel == 9 or note.until == -1 or pos - until == 0):
					if channelHeight[channel] < midiMaxHeight or midiMaxHeight == 20:
						if (midiChannelIns[channel] == 0):
							ins1notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 1):
							ins2notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 2):
							ins3notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 3):
							ins4notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 4):
							ins5notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 5):
							ins6notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 6):
							ins7notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 7):
							ins8notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 8):
							ins9notes[anote][pos] = 1
						elif (midiChannelIns[channel] == 9):
							ins10notes[anote][pos] = 1
						posamount[channel][pos] += 1
						channelHeight[channel] = max(channelHeight[channel], posamount[channel][pos])
				else:
					for i in range(pos, until):
						if channelHeight[channel] < midiMaxHeight or midiMaxHeight == 20:
							if (midiChannelIns[channel] == 0):
								ins1notes[anote][i] = 1
							elif (midiChannelIns[channel] == 1):
								ins2notes[anote][i] = 1
							elif (midiChannelIns[channel] == 2):
								ins3notes[anote][i] = 1
							elif (midiChannelIns[channel] == 3):
								ins4notes[anote][i] = 1
							elif (midiChannelIns[channel] == 4):
								ins5notes[anote][i] = 1
							elif (midiChannelIns[channel] == 5):
								ins6notes[anote][i] = 1
							elif (midiChannelIns[channel] == 6):
								ins7notes[anote][i] = 1
							elif (midiChannelIns[channel] == 7):
								ins8notes[anote][i] = 1
							elif (midiChannelIns[channel] == 8):
								ins9notes[anote][i] = 1
							elif (midiChannelIns[channel] == 9):
								ins10notes[anote][i] = 1
							posamount[channel][i] += 1
							channelHeight[channel] = max(channelHeight[channel], posamount[channel][i])
	for i in range(math.floor((midiMaxPos - midiMinPos * midiRemoveSilent) / deltaPerTick) + 1):
		for j in range(88):
			ins1notes[j][i] = 0
			ins2notes[j][i] = 0
			ins3notes[j][i] = 0
			ins4notes[j][i] = 0
			ins5notes[j][i] = 0
			ins6notes[j][i] = 0
			ins7notes[j][i] = 0
			ins8notes[j][i] = 0
			ins9notes[j][i] = 0
			ins10notes[j][i] = 0

	# Place blocks
	for track in midiTracks:
		for note in track.notes:
			channel = note.channel
			pos = math.floor((note.x - midiMinPos * midiRemoveSilent) / deltaPerTick)
			until = math.floor((note.until - midiMinPos * midiRemoveSilent) / deltaPerTick)
			anote = note.note - 21
			vel = 100
			if midiVel:
				vel = note.vel
			if vel >= 100:
				vel = 100
			yy = 0
			stop = 0
			ins = -1
			if (channel == 9):
				a = 0
				while a < len(midiPercs):
					if (midiPercs[a].note == note.note):
						break
					a += 1
				ins = midiPercIns[a]
				anote = statistics.median([0, midiPercPitch[a], 87])
			else:
				ins = midiChannelIns[channel]
				anote += 12 * midiChannelOctave[channel]
				anote = statistics.median([0, anote, 87])
			if midiOctave == 1:
				while anote < 33:
					anote += 12
				while anote > 57:
					anote -= 12
			if ins > -1 and stop == 0:
				if (channel == 9 or note.until == -1 or pos - until == 0):
					if (midiChannelIns[channel] == 0):
						ins1notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 1):
						ins2notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 2):
						ins3notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 3):
						ins4notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 4):
						ins5notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 5):
						ins6notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 6):
						ins7notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 7):
						ins8notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 8):
						ins9notes[anote][pos] = 1
					elif (midiChannelIns[channel] == 9):
						ins10notes[anote][pos] = 1
				else:
					for i in range(pos, until):
						if (midiChannelIns[channel] == 0):
							ins1notes[anote][i] = 1
						elif (midiChannelIns[channel] == 1):
							ins2notes[anote][i] = 1
						elif (midiChannelIns[channel] == 2):
							ins3notes[anote][i] = 1
						elif (midiChannelIns[channel] == 3):
							ins4notes[anote][i] = 1
						elif (midiChannelIns[channel] == 4):
							ins5notes[anote][i] = 1
						elif (midiChannelIns[channel] == 5):
							ins6notes[anote][i] = 1
						elif (midiChannelIns[channel] == 6):
							ins7notes[anote][i] = 1
						elif (midiChannelIns[channel] == 7):
							ins8notes[anote][i] = 1
						elif (midiChannelIns[channel] == 8):
							ins9notes[anote][i] = 1
						elif (midiChannelIns[channel] == 9):
							ins10notes[anote][i] = 1
			for i in range(channel):
				yy += channelHeight[i]
			if tempoChanger == 1:
				yy += 1
			tempy = yy
			forValue = pos + 1
			if (channel != 9 and note.until != -1 and pos - until != 0):
				forValue = until
			if midi_ins[midiChannelPatch[channel]]["name"] == "Reverse Cymbal":
				for i in range(pos, forValue):
					a = 0
					yy = tempy
					at = i - pos
					tempvel = 100
					length = until - pos
					if length != 0:
						tempvel = math.floor(vel * (at / length))
					while True:
						if not note_exists(i, yy, nbsFile):
							if ins >= 0:
								nbsFile.notes.append(pynbs.Note(tick = i, layer = yy, instrument = ins, key = anote, velocity = tempvel, panning = 0, pitch = 0))
							#print(i)
							break
						yy += 1
						a += 1
						if a >= midiMaxHeight and midiMaxHeight < 20:
							break
			else:
				for i in range(pos, forValue):
					a = 0
					yy = tempy
					tempvel = vel
					temppan = 0
					at = i - pos
					if (at != 0):
						tempvel = math.floor(vel * 0.5)
						if (at % 2 == 0):
							temppan = 50
						else:
							temppan = -50
					while True:
						if not note_exists(i, yy, nbsFile):
							if ins >= 0:
								nbsFile.notes.append(pynbs.Note(tick = i, layer = yy, instrument = ins, key = anote, velocity = tempvel, panning = temppan, pitch = 0))
							#print(i)
							break
						yy += 1
						a += 1
						if a >= midiMaxHeight and midiMaxHeight < 20:
							break
	if tempoChanger == 1:
		for i in range(tempoChangerCount):
			pos = math.floor((tempoChangerX[i] - midiMinPos * midiRemoveSilent) / deltaPerTick)
			if pos < 0:
				pos = 0
			if not note_exists(pos, 0, nbsFile):
				nbsFile.notes.append(pynbs.Note(tick = pos, layer = 0, instrument = 16, key = 39, velocity = 100, panning = 0, pitch = math.floor(tempoChangerTempo[i] * (midiPrecision + 1))))
			else:
				replace_note(pos, 0, nbsFile, 16, 39, 100, 100, math.floor(tempoChangerTempo[i] * (midiPrecision + 1)))

	if midiName == 1:
		yy = 0
		if tempoChanger == 1:
			nbsFile.layers[yy].name = "TempoChgr"
			yy += 1
		for i in range(midiChannels + 1):
			for j in range(channelHeight[i]):
				nbsFile.layers.append(pynbs.Layer(yy))
				nbsFile.layers[yy].panning = 100
				nbsFile.layers[yy].name = "Channel " + str(i + 1)
				if midiNamePatch == 1:
					try:
						nbsFile.layers[yy].name = midi_ins[midiChannelPatch[i]]["shortName"]
						if nbsFile.layers[yy].name == "":
							nbsFile.layers[yy].name = midi_ins[midiChannelPatch[i]]["name"]
					except:
						nbsFile.layers[yy].name = "Unknown"
					if i == 9:
						nbsFile.layers[yy].name = "Percussion"
				nbsFile.layers[yy].lock = False
				nbsFile.layers[yy].volume = 100
				yy += 1

	nbsFile.notes.sort(key=lambda note: (note.tick, note.layer))

	nbsPath = filedialog.asksaveasfilename(
			title="Save NBS file",
			filetypes=[("NBS File", "*.nbs")],
			initialfile=Path(midiPath).stem + "_converted"
		)
	nbsFile.save(nbsPath)

if __name__ == "__main__":
	main()
