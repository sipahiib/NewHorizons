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
  01-roman-space-telescope
  02-alpha-gal-antibodies
  03-astra-cybersecurity
  04-cluster-samba
  05-pallas-one
)

invalid=0
for stem in "${stems[@]}"; do
  text_file="$TEXT_DIR/$stem.txt"
  stem="$(basename "$text_file" .txt)"
  raw="$OUT/$stem.mp3"
  wav="$OUT/$stem.wav"
  "$EDGE_PY" -m edge_tts --voice "$VOICE" --rate="$RATE" --file "$text_file" --write-media "$raw"
  ffmpeg -nostdin -y -v error -i "$raw" -af 'aresample=48000' -ac 1 -ar 48000 -c:a pcm_s16le "$wav"
  duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$wav")"
  awk -v d="$duration" 'BEGIN {if (d < 27 || d > 32.5) exit 1}' || {
    echo "Reel narration $stem must be 27-32.5 seconds; measured $duration" >&2
    invalid=1
  }
  printf '%s\t%s\n' "$stem" "$duration"
done

exit "$invalid"
