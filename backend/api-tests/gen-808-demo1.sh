curl -X POST "http://127.0.0.1:8000/api/v1/generate/808" \
  -H "Content-Type: application/json" \
  -d '{
        "bpm": 120,
        "kick":        [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
        "snare":       [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
        "hihat_closed":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
      }' \
  -o tr808_pattern_demo1.mid