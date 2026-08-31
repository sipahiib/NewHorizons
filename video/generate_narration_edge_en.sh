#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NARRATION_SOURCE="$ROOT/video/narration-en.txt" \
NARRATION_PARTS_DIR="$ROOT/build/video/narration-parts-en" \
NARRATION_OUTPUT="$ROOT/build/video/narration-en.wav" \
VOICE="en-GB-RyanNeural" \
VOICE_RATE="-2%" \
  "$ROOT/video/generate_narration_edge.sh"
