#!/bin/bash
set -e
set -x

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
KEY="A"
SCALE="major"
PROGRESSION='["I","vi","IV","V"]'
CHORD_TYPES='["maj7","m7","maj7","7"]'
TEMPO_CHORDS=90
TEMPO_BASS=120
DURATION=2.0
OCTAVE_CHORDS=4
OCTAVE_BASS=5
BASS_STYLE="funk"
SYNCOPATION=true
PASSING_TONES=true

# -----------------------------
# 1️⃣ GENERAR PROGRESIÓN DE ACORDES (jazz_progression.mid)
# -----------------------------
curl -X POST "http://127.0.0.1:8000/api/v1/generate" \
-H "Content-Type: application/json" \
-d "{
    \"key\": \"$KEY\",
    \"scale\": \"$SCALE\",
    \"progression\": $PROGRESSION,
    \"chord_types\": $CHORD_TYPES,
    \"tempo\": $TEMPO_CHORDS,
    \"duration\": $DURATION,
    \"octave\": $OCTAVE_CHORDS
}" -o jazz_progression.mid

echo "✅ Jazz progression generated: jazz_progression.mid"

# -----------------------------
# 2️⃣ GENERAR LÍNEA DE BAJO (bassline_advanced.mid)
# -----------------------------
curl -X POST "http://127.0.0.1:8000/api/v1/generate/bass" \
-H "Content-Type: application/json" \
-d "{
    \"key\": \"$KEY\",
    \"scale\": \"$SCALE\",
    \"progression\": $PROGRESSION,
    \"chord_types\": $CHORD_TYPES,
    \"tempo\": $TEMPO_BASS,
    \"duration\": $DURATION,
    \"octave\": $OCTAVE_BASS,
    \"style\": \"$BASS_STYLE\",
    \"syncopation\": $SYNCOPATION,
    \"passing_tones\": $PASSING_TONES
}" -o bassline_advanced.mid

echo "✅ Bass line generated: bassline_advanced.mid"

# -----------------------------
# 3️⃣ GENERAR PATRÓN TR-808 (tr808_pattern_demo1.mid)
# -----------------------------
curl -X POST "http://127.0.0.1:8000/api/v1/generate/808" \
-H "Content-Type: application/json" \
-d '{
    "bpm": 120,
    "kick":        [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    "snare":       [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    "hihat_closed":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
}' -o tr808_pattern_demo1.mid

echo "✅ TR-808 pattern generated: tr808_pattern_demo1.mid"

# -----------------------------
# FIN
# -----------------------------
echo "🎵 All MIDI files generated successfully!"
