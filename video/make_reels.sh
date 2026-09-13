#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/build/reels"
FPS=60
mkdir -p "$OUT/work"
node "$ROOT/video/src/generate_reel_overlays.mjs"

render_vertical_clip() {
  local input="$1" duration="$2" disclosure="$3" output="$4"
  local filter="split=2[fgsrc][bgsrc];[bgsrc]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=35,eq=brightness=-0.20:saturation=0.72[bg];[fgsrc]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709,fps=$FPS,trim=duration=$duration,setpts=PTS-STARTPTS,setsar=1"
  ffmpeg -nostdin -y -v error -i "$input" -loop 1 -framerate "$FPS" -i "$disclosure" \
    -filter_complex "[0:v]$filter[scene];[scene][1:v]overlay=0:0:shortest=1[v]" -map '[v]' \
    -t "$duration" -an -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r "$FPS" \
    -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$output"
}

render_reel() {
  local number="$1" slug="$2" audio="$3" disclosure_name="$4"
  shift 4
  local -a clips=("$@")
  [[ "${#clips[@]}" -eq 7 ]] || { echo "Reel $slug requires exactly seven clips" >&2; exit 1; }
  [[ -s "$audio" ]] || { echo "Missing Reel narration: $audio" >&2; exit 1; }

  local audio_duration speech_end total_duration closing_gap clip_duration work concat_file
  audio_duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$audio")"
  speech_end="$(node "$ROOT/video/measure_reel_audio.mjs" "$audio")"
  awk -v d="$audio_duration" -v s="$speech_end" 'BEGIN {if(d<35 || d>45.02 || s>45.02) exit 1}' || {
    echo "Reel narration must finish within 45 seconds: $slug audio=$audio_duration speech_end=$speech_end" >&2
    exit 1
  }
  total_duration="$(awk -v s="$speech_end" 'BEGIN {t=s+3; if(t<45)t=45; if(t>50)exit 1; printf "%.3f",t}')"
  closing_gap="$(awk -v s="$speech_end" -v t="$total_duration" 'BEGIN {printf "%.3f",t-s}')"
  awk -v g="$closing_gap" 'BEGIN {if(g<=0 || g>4.001)exit 1}' || { echo "Invalid post-speech gap: $closing_gap" >&2; exit 1; }
  clip_duration="$(awk -v t="$total_duration" 'BEGIN {printf "%.6f",t/7}')"

  work="$OUT/work/$slug"
  mkdir -p "$work"
  concat_file="$work/concat.txt"
  : > "$concat_file"
  local index=0 input source_duration segment
  for input in "${clips[@]}"; do
    index=$((index+1))
    source_duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$ROOT/$input")"
    awk -v s="$source_duration" -v d="$clip_duration" 'BEGIN {if(s+0.01<d)exit 1}' || { echo "Source too short: $input ($source_duration < $clip_duration)" >&2; exit 1; }
    segment="$work/clip$(printf '%02d' "$index").mp4"
    render_vertical_clip "$ROOT/$input" "$clip_duration" "$OUT/overlays/$disclosure_name.webp" "$segment"
    printf "file '%s'\n" "$segment" >> "$concat_file"
  done

  ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$concat_file" -c copy "$work/base.mp4"
  ffmpeg -nostdin -y -v error -i "$work/base.mp4" -i "$audio" \
    -loop 1 -framerate "$FPS" -i "$OUT/overlays/title$number.webp" \
    -loop 1 -framerate "$FPS" -i "$OUT/overlays/cta.webp" \
    -filter_complex "[0:v]fps=$FPS,setpts=N/($FPS*TB)[base];[2:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st=4.7:d=0.30:alpha=1,setpts=PTS-STARTPTS[title];[3:v]format=rgba,fade=t=in:st=$(awk -v t="$total_duration" 'BEGIN {printf "%.3f",t-3}'):d=0.35:alpha=1,setpts=PTS-STARTPTS[cta];[base][title]overlay=0:0:enable='between(t,0,5)'[v1];[v1][cta]overlay=0:0:enable='between(t,$(awk -v t="$total_duration" 'BEGIN {printf "%.3f",t-3}'),$total_duration)'[v];[1:a]aresample=48000,apad,atrim=duration=$total_duration,loudnorm=I=-16:LRA=7:TP=-1.5[a]" \
    -map '[v]' -map '[a]' -t "$total_duration" -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r "$FPS" \
    -c:a aac -ar 48000 -b:a 192k -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart "$OUT/$slug.mp4"
  printf '%s audio=%s speech_end=%s total=%s closing_gap=%s clips=7\n' "$slug" "$audio_duration" "$speech_end" "$total_duration" "$closing_gap"
}

render_r1() {
  render_reel 1 "01-sports-biomechanics" "$OUT/audio/01-sports-biomechanics.wav" sports \
    "assets/motion/2026-09-10/reels/R1-01.mp4" "assets/motion/2026-09-10/reels/R1-02.mp4" \
    "assets/motion/2026-09-10/reels/R1-03.mp4" "assets/motion/2026-09-10/reels/R1-04.mp4" \
    "assets/motion/2026-09-10/reels/R1-05.mp4" "assets/motion/2026-09-10/reels/R1-06.mp4" \
    "assets/motion/2026-09-10/reels/R1-07.mp4"
}

render_r2() {
  render_reel 2 "02-planet-earth" "$OUT/audio/02-planet-earth.wav" earth \
    "assets/motion/2026-09-10/reels/R3-01.mp4" "assets/motion/2026-09-10/reels/R3-02.mp4" \
    "assets/motion/2026-09-10/reels/R3-03.mp4" "assets/motion/2026-09-10/reels/R3-04.mp4" \
    "assets/motion/2026-09-10/reels/R3-05.mp4" "assets/motion/2026-09-10/reels/R3-06.mp4" \
    "assets/motion/2026-09-10/reels/R3-07.mp4"
}

case "${1:-ready}" in
  1) render_r1 ;;
  2) render_r2 ;;
  ready) render_r1; render_r2 ;;
  *) echo "Usage: $0 [1|2|ready]" >&2; exit 2 ;;
esac
