from fastapi import FastAPI
from app.api.chords import router

app=FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"msg":"MIDI API running"}
