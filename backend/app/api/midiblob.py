from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

@app.post("/api/v1/midi-blob")
async def midi_blob(file: UploadFile = File(...)):
    # Leer el contenido del archivo MIDI en memoria
    midi_bytes = await file.read()
    midi_stream = io.BytesIO(midi_bytes)

    # Retornar como stream (Blob)
    return StreamingResponse(midi_stream, media_type="audio/midi")
