#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EDGE_PY="$ROOT/.tools-edge-tts/bin/python3.14"
PARTS_DIR="${NARRATION_PARTS_DIR:-$ROOT/build/video/narration-parts}"
TEXT="$PARTS_DIR/text"
RAW="$PARTS_DIR/edge-raw"
CLEAN="$PARTS_DIR/clean"
VOICE="${VOICE:-tr-TR-AhmetNeural}"
VOICE_RATE="${VOICE_RATE:-+2%}"
NARRATION_SOURCE="${NARRATION_SOURCE:-$ROOT/video/narration.txt}"
NARRATION_OUTPUT="${NARRATION_OUTPUT:-$ROOT/build/video/narration.wav}"

mkdir -p "$RAW" "$CLEAN"
NARRATION_SOURCE="$NARRATION_SOURCE" NARRATION_PARTS_DIR="$PARTS_DIR" \
  node "$ROOT/video/src/extract_narration_parts.mjs"

generate() {
  local stem="$1"
  local target="$2"
  local raw="$RAW/$stem.mp3"
  local clean="$CLEAN/$stem.wav"

  "$EDGE_PY" -m edge_tts --voice "$VOICE" --rate="$VOICE_RATE" --file "$TEXT/$stem.txt" --write-media "$raw"
  local duration tempo
  duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$raw")"
  tempo="$(awk -v d="$duration" -v t="$target" 'BEGIN {v=d/t; if (v<0.82 || v>1.22) exit 2; printf "%.6f", v}')" || {
    echo "Narration section $stem is too far from target: raw=$duration target=$target" >&2
    exit 1
  }
  ffmpeg -nostdin -y -v error -i "$raw" \
    -af "atempo=$tempo,aresample=48000,apad=pad_dur=$target,atrim=duration=$target" \
    -ac 1 -ar 48000 -c:a pcm_s16le "$clean"
  printf '%s raw=%s target=%s tempo=%s\n' "$stem" "$duration" "$target" "$tempo"
}

generate roman 120
generate alpha-gal 45
generate astra 45
generate cluster 45
generate pallas 40
generate outro 10

ffmpeg -nostdin -y -v error \
  -i "$CLEAN/roman.wav" -i "$CLEAN/alpha-gal.wav" -i "$CLEAN/astra.wav" \
  -i "$CLEAN/cluster.wav" -i "$CLEAN/pallas.wav" -i "$CLEAN/outro.wav" \
  -filter_complex '[0:a][1:a][2:a][3:a][4:a][5:a]concat=n=6:v=0:a=1[outa]' \
  -map '[outa]' -ac 1 -ar 48000 -c:a pcm_s16le "$NARRATION_OUTPUT"

duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$NARRATION_OUTPUT")"
awk -v d="$duration" 'BEGIN {x=d-305; if (x<0) x=-x; if (x>0.002) exit 1}' || {
  echo "Narration duration is not exactly 305 seconds: $duration" >&2
  exit 1
}
printf 'Narration ready: %s seconds\n' "$duration"
