from midiutil import MIDIFile
from io import BytesIO
from app.utils.music_theory import degree_to_chord

def build_midi_from_progression(key, scale, progression, tempo, duration, octave, chord_types=None):
    if chord_types is None:
        chord_types = ["triad"] * len(progression)
    midi = MIDIFile(1)
    midi.addTempo(0, 0, tempo)
    t = 0
    for i, degree in enumerate(progression):
        chord_type = chord_types[i] if i < len(chord_types) else "triad"
        notes = degree_to_chord(degree, key, scale, octave, chord_type)
        for n in notes:
            midi.addNote(0, 0, n, t, duration, 100)
        t += duration
    buf = BytesIO()
    midi.writeFile(buf)
    buf.seek(0)
    return buf.read()
