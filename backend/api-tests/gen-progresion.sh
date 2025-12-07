set -x
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -o progression.mid \
  -d '{
        "key": "C",
        "scale": "major",
        "progression": ["I","vi","IV","V"],
        "tempo": 120,
        "duration": 1.0,
        "octave": 4
      }'