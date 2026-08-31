#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EDITORIAL_BUILD="$ROOT/build/video/editorial-en" \
NARRATION_FILE="$ROOT/build/video/narration-brian.wav" \
OUTPUT_FILE="$ROOT/build/video/newhorizons.mp4" \
TITLE_LANGUAGE="en" \
  "$ROOT/video/make_editorial_video.sh"
