from fastapi import APIRouter, Response
from pydantic import BaseModel
from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage
from io import BytesIO

router = APIRouter(prefix="/api/v1/generate")

class Rhythm808(BaseModel):
    bpm: int = 120
    pattern_length: int = 16

    # TR-808 complete instrument set
    kick: list[int] = []
    snare: list[int] = []
    hihat_closed: list[int] = []
    hihat_open: list[int] = []
    clap: list[int] = []
    rimshot: list[int] = []
    low_tom: list[int] = []
    mid_tom: list[int] = []
    high_tom: list[int] = []
    cowbell: list[int] = []
    maracas: list[int] = []
    cymbal: list[int] = []
    ride: list[int] = []
    low_conga: list[int] = []
    mid_conga: list[int] = []
    high_conga: list[int] = []
    bongo_low: list[int] = []
    bongo_high: list[int] = []

# Complete MIDI map for TR-808
MIDI_NOTES = {
    "kick": 36,
    "snare": 38,
    "hihat_closed": 42,
    "hihat_open": 46,
    "clap": 39,
    "rimshot": 37,
    "low_tom": 45,
    "mid_tom": 47,
    "high_tom": 50,
    "cowbell": 56,
    "maracas": 70,
    "cymbal": 49,
    "ride": 51,
    "low_conga": 64,
    "mid_conga": 63,
    "high_conga": 62,
    "bongo_low": 60,
    "bongo_high": 61
}


@router.post("/808")
def generate_808_rhythm(pattern: Rhythm808):
    midi = MidiFile()
    tempo = bpm2tempo(pattern.bpm)
    tick = midi.ticks_per_beat // 4  # 16 pasos = semicorcheas

    # Crear pista de tempo general
    meta_track = MidiTrack()
    meta_track.append(MetaMessage("set_tempo", tempo=tempo))
    midi.tracks.append(meta_track)

    for instrument in MIDI_NOTES.keys():
        steps = getattr(pattern, instrument)
        if not steps:
            continue

        track = MidiTrack()
        midi.tracks.append(track)
        note = MIDI_NOTES[instrument]

        for step in steps:
            if step == 1:
                # Nota activada
                track.append(Message("note_on", note=note, velocity=100, time=0))
                track.append(Message("note_off", note=note, velocity=100, time=tick))
            else:
                # Silencio
                track.append(Message("note_off", note=note, velocity=0, time=tick))

    # Guardar MIDI en memoria
    midi_io = BytesIO()
    midi.save(file=midi_io)
    midi_io.seek(0)

    return Response(
        content=midi_io.read(),
        media_type="audio/midi",
        headers={"Content-Disposition": 'attachment; filename="tr808.mid"'}
    )
