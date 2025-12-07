NOTE_ORDER = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_name_to_midi(note: str, octave: int) -> int:
    midi = 12 * (octave + 1) + NOTE_ORDER.index(note)
    print(f"[note_name_to_midi] note={note}{octave} -> MIDI={midi}")
    return midi

def build_scale(key: str, scale_type: str):
    steps = [2,2,1,2,2,2,1]  # mayor
    start = NOTE_ORDER.index(key)
    notes = [NOTE_ORDER[start]]
    idx = start
    for s in steps[:-1]:
        idx = (idx + s) % 12
        notes.append(NOTE_ORDER[idx])
    print(f"[build_scale] key={key}, scale_type={scale_type} -> {notes}")
    return notes

def degree_to_chord(degree, key, scale, octave, chord_type="triad"):
    """
    chord_type: 'triad', '7', 'maj7', 'm7', '9'
    """
    scale_notes = build_scale(key, scale)
    roman = {'I':0,'ii':1,'iii':2,'IV':3,'V':4,'vi':5,'vii':6}
    idx = roman.get(degree, 0)
    root = scale_notes[idx]

    # Extender la escala para poder tomar notas más arriba sin salir del rango
    extended_scale = scale_notes * 2

    print(f"[degree_to_chord] degree={degree}, chord_type={chord_type}, root={root}{octave}")

    # Construir acorde según tipo basado en posiciones dentro de la escala
    if chord_type == "triad":
        notes = [extended_scale[idx], extended_scale[idx+2], extended_scale[idx+4]]
    elif chord_type == "7":  # dominante 7
        notes = [extended_scale[idx], extended_scale[idx+2], extended_scale[idx+4], extended_scale[idx+6]]
    elif chord_type == "maj7":
        notes = [extended_scale[idx], extended_scale[idx+2], extended_scale[idx+4], extended_scale[idx+6]]
    elif chord_type == "m7":
        notes = [extended_scale[idx], extended_scale[idx+2], extended_scale[idx+4], extended_scale[idx+6]]
    elif chord_type == "9":  # dominante 9
        notes = [extended_scale[idx], extended_scale[idx+2], extended_scale[idx+4], extended_scale[idx+6], extended_scale[idx+8]]
    else:
        notes = [extended_scale[idx], extended_scale[idx+2], extended_scale[idx+4]]

    # Convertir a MIDI
    chord = [note_name_to_midi(n, octave) for n in notes]
    
    # Log del acorde generado
    chord_notes = [NOTE_ORDER[n % 12] + str(n // 12 - 1) for n in chord]
    print(f"[degree_to_chord] chord MIDI={chord} -> notes={chord_notes}")

    return chord
