# MIDI API

Project for generate MiDi chord progressions.

* Install

```bash
pip3 install -r requirements.txt --break-system-packages
```

* Launch 

```bash
uvicorn app.main:app --reload
```

* Test API 

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/generate" \
-H "Content-Type: application/json" \
-d '{
    "key": "C",
    "scale": "major",
    "progression": ["I","vi","IV","V"],
    "chord_types": ["9","m7","9","7"],
    "tempo": 90,
    "duration": 2.0,
    "octave": 4
}' -o jazz9_progression.mid
```