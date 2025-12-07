from fastapi import APIRouter, Response
from app.models.chord_request import ChordRequest
from app.services.midi_generator import build_midi_from_progression

router = APIRouter(prefix="/api/v1")

@router.post("/generate")
def generate(req: ChordRequest):
    # Aseguramos que cada grado tenga su tipo de acorde
    chord_types = req.chord_types if hasattr(req, "chord_types") else ["triad"] * len(req.progression)

    # Llamamos a la función pasando la progresión y los tipos de acorde
    data = build_midi_from_progression(
        key=req.key,
        scale=req.scale,
        progression=req.progression,
        chord_types=chord_types, 
        tempo=req.tempo,
        duration=req.duration,
        octave=req.octave
    )

    return Response(
        data,
        media_type="audio/midi",
        headers={"Content-Disposition": "attachment; filename=progression.mid"}
    )
