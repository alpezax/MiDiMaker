# app/api/midi_blob.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io

router = APIRouter(prefix="/api/v1")

@router.post("/midi-blob")
async def midi_blob(file: UploadFile = File(...)):
    midi_bytes = await file.read()
    midi_stream = io.BytesIO(midi_bytes)
    return StreamingResponse(midi_stream, media_type="audio/midi")
