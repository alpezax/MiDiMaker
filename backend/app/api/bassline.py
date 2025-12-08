# app/routes/bass_generator.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Literal, Optional
from mido import MidiFile, MidiTrack, Message, bpm2tempo
import random

# ---------------------------
# MODELO DE PETICIÓN
# ---------------------------
class BassRequest(BaseModel):
    key: str
    scale: str
    progression: List[str]
    chord_types: Optional[List[str]] = None  # útil para inversiones/arpegios
    tempo: int
    duration: float
    octave: int = 4
    style: Literal["simple", "walking", "funk", "arpeggio"] = "simple"
    syncopation: bool = False
    passing_tones: bool = False

# ---------------------------
# CONSTANTES MUSICALES
# ---------------------------
NOTES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
ROMAN_TO_SCALE_DEGREES = {"I":1,"ii":2,"iii":3,"IV":4,"V":5,"vi":6,"vii":7}
SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
}

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def note_to_midi(note: str, octave: int) -> int:
    return NOTES_SHARP.index(note) + (octave + 1) * 12

def generate_scale_notes(key: str, scale_type: str):
    root_index = NOTES_SHARP.index(key)
    intervals = SCALES[scale_type]
    return [(root_index + interval) % 12 for interval in intervals]

def roman_to_note(key: str, scale: str, roman: str, octave: int):
    scale_notes = generate_scale_notes(key, scale)
    degree = ROMAN_TO_SCALE_DEGREES.get(roman)
    if not degree:
        raise HTTPException(status_code=400, detail=f"Roman numeral {roman} not recognized")
    note_semitone = scale_notes[degree - 1]
    root_note = NOTES_SHARP[note_semitone]
    return note_to_midi(root_note, octave)

# ---------------------------
# GENERACIÓN DE PATRÓN DE BAJO
# ---------------------------
def generate_bass_pattern(req: BassRequest):
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    track.append(Message("program_change", program=32, time=0))  # Acoustic Bass

    ticks_per_beat = midi.ticks_per_beat
    note_ticks = int(req.duration * ticks_per_beat)
    bass_octave = req.octave - 2

    for idx, roman in enumerate(req.progression):
        chord_root = roman_to_note(req.key, req.scale, roman, bass_octave)
        notes = []

        # -------------------------
        # 1. Selección de notas según estilo
        # -------------------------
        if req.style == "simple":
            notes = [chord_root]

        elif req.style == "walking":
            if idx == 0:
                prev_note = chord_root
            else:
                prev_note = roman_to_note(req.key, req.scale, req.progression[idx-1], bass_octave)
            step = 1 if chord_root > prev_note else -1
            notes = list(range(prev_note, chord_root + step, step))

        elif req.style == "funk":
            fifth = chord_root + 7
            notes = [chord_root, fifth]

        elif req.style == "arpeggio":
            # Arpegio simple basado en mayor; puede mejorarse según chord_types
            third = chord_root + 4
            fifth = chord_root + 7
            notes = [chord_root, third, fifth]

        # -------------------------
        # 2. Añadir passing tones
        # -------------------------
        if req.passing_tones and len(notes) > 0:
            new_notes = []
            for i in range(len(notes)-1):
                new_notes.append(notes[i])
                mid = (notes[i] + notes[i+1]) // 2
                new_notes.append(mid)
            new_notes.append(notes[-1])
            notes = new_notes

        # -------------------------
        # 3. Añadir síncopas
        # -------------------------
        times = [0] * len(notes)
        if req.syncopation:
            times = [0 if i % 2 == 0 else note_ticks // 2 for i in range(len(notes))]

        # -------------------------
        # 4. Añadir notas al track
        # -------------------------
        for note, t in zip(notes, times):
            track.append(Message("note_on", note=note, velocity=90, time=t))
            track.append(Message("note_off", note=note, velocity=40, time=note_ticks))

    output_path = "bassline_advanced.mid"
    midi.save(output_path)
    return output_path

# ---------------------------
# ROUTER
# ---------------------------
router = APIRouter(prefix="/api/v1")

@router.post("/generate/bass")
def generate_bass(req: BassRequest):
    path = generate_bass_pattern(req)
    return FileResponse(path, media_type="audio/midi", filename="bassline_advanced.mid")
