# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chords import router
from app.api.midiblob import router as blob_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Solo registramos el router sin prefijo extra
app.include_router(router)
app.include_router(blob_router)

@app.get("/")
def root():
    return {"msg": "MIDI API running"}
