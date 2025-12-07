set -x

curl -X POST "http://127.0.0.1:8000/api/v1/generate" \
-H "Content-Type: application/json" \
-d '{
    "key": "C",
    "scale": "major",
    "progression": ["I","vi","IV","V"],
    "chord_types": ["maj7","m7","maj7","7"],
    "tempo": 90,
    "duration": 2.0,
    "octave": 4
}' -o jazz_progression.mid