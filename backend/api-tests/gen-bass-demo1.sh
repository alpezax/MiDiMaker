curl -X POST "http://127.0.0.1:8000/api/v1/generate/bass" \
-H "Content-Type: application/json" \
-d '{
    "key": "A",
    "scale": "major",
    "progression": ["I","vi","IV","V"],
    "chord_types": ["maj7","m7","maj7","7"],
    "tempo": 120,
    "duration": 2.0,
    "octave": 5,
    "style": "funk",
    "syncopation": true,
    "passing_tones": true
}' -o bassline_advanced.mid