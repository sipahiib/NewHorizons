#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EDGE_PY="$ROOT/.tools-edge-tts/bin/python3.14"
TEXT_DIR="$ROOT/video/reels-narration"
OUT="$ROOT/build/reels/audio"
VOICE="en-GB-RyanNeural"
RATE="-2%"

mkdir -p "$OUT"

stems=(
  01-sports-biomechanics
  02-hands-on-science
  03-ai-archaeology
)

invalid=0
for stem in "${stems[@]}"; do
  [[ -n "${1:-}" && "$stem" != "$1" ]] && continue
  text_file="$TEXT_DIR/$stem.txt"
  stem="$(basename "$text_file" .txt)"
  raw="$OUT/$stem.mp3"
  wav="$OUT/$stem.wav"
  "$EDGE_PY" -m edge_tts --voice "$VOICE" --rate="$RATE" --file "$text_file" --write-media "$raw"
  ffmpeg -nostdin -y -v error -i "$raw" -af 'aresample=48000' -ac 1 -ar 48000 -c:a pcm_s16le "$wav"
  duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$wav")"
  awk -v d="$duration" 'BEGIN {if (d < 26 || d > 30) exit 1}' || {
    echo "Reel narration $stem must be 26-30 seconds at the fixed -2% voice rate; measured $duration. Revise the text, not the speed." >&2
    invalid=1
  }
  printf '%s\t%s\n' "$stem" "$duration"
done

exit "$invalid"
