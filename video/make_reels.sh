#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/build/reels"
COVER="$ROOT/assets/branding/new-horizons-cover.png"
FPS=60

mkdir -p "$OUT/work"
node "$ROOT/video/src/generate_reel_overlays.mjs"

render_vertical_clip() {
  local input="$1" seek="$2" duration="$3" output="$4"
  local filter="split=2[fgsrc][bgsrc];[bgsrc]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=35,eq=brightness=-0.20:saturation=0.72[bg];[fgsrc]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709,fps=$FPS,trim=duration=$duration,setpts=PTS-STARTPTS,setsar=1"
  local -a input_args=(-nostdin -y -v error -ss "$seek" -i "$input")
  local -a filter_args=(-vf "$filter")
  if [[ "$input" == */stock/* ]]; then
    local label=stock
    [[ "$input" == */R1-* ]] && label=sports
    [[ "$input" == */R3-0[123].mp4 ]] && label=athens
    input_args+=(-loop 1 -framerate "$FPS" -i "$OUT/overlays/$label.webp")
    filter_args=(-filter_complex "[0:v]$filter[scene];[scene][1:v]overlay=0:0:shortest=1[v]" -map '[v]')
  fi
  ffmpeg "${input_args[@]}" "${filter_args[@]}" \
    -t "$duration" -an -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r "$FPS" \
    -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$output"
}

render_reel() {
  local number="$1" slug="$2" audio="$3"
  shift 3
  local -a clips=("$@")
  local audio_duration speech_end narration_delay delay_ms total_duration content_duration closing_duration clip_duration work concat_file base cover_file title cta
  audio_duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$audio")"
  awk -v d="$audio_duration" 'BEGIN {if (d < 26 || d > 30) exit 1}' || {
    echo "Reel $slug requires 26-30 seconds of narration; measured $audio_duration. Revise narration text without changing the approved voice rate." >&2
    exit 1
  }
  speech_end="$(node "$ROOT/video/measure_reel_audio.mjs" "$audio")"
  # A sub-second opening breath keeps very short speech inside the minimum
  # 30-second delivery without exceeding four seconds after the last word.
  narration_delay="$(awk -v e="$speech_end" 'BEGIN {d=26.1-e; if(d<0)d=0; if(d>1)exit 1; printf "%.3f", d}')"
  delay_ms="$(awk -v d="$narration_delay" 'BEGIN {printf "%.0f", d*1000}')"
  speech_end="$(awk -v e="$speech_end" -v d="$narration_delay" 'BEGIN {if(e+d>30)exit 1; printf "%.3f", e+d}')"
  content_duration="$(awk -v a="$audio_duration" -v d="$narration_delay" 'BEGIN {printf "%.3f", a+d}')"
  total_duration="$(awk -v d="$speech_end" 'BEGIN {t=d+3; if (t<30) t=30; if (t>35) t=35; if (t-d<=0 || t-d>4) exit 2; printf "%.3f", t}')" || {
    echo "Reel $slug cannot fit 30-35 seconds with a maximum four-second closing gap: audio=$audio_duration" >&2
    exit 1
  }
  awk -v a="$speech_end" -v t="$total_duration" 'BEGIN {g=t-a; if (g>4.0001) exit 1}' || {
    echo "Reel $slug closing gap exceeds four seconds" >&2
    exit 1
  }
  clip_duration="$(awk -v d="$content_duration" 'BEGIN {printf "%.3f", d/5}')"
  closing_duration="$(awk -v a="$content_duration" -v t="$total_duration" 'BEGIN {printf "%.3f", t-a}')"
  work="$OUT/work/$slug"
  mkdir -p "$work"
  concat_file="$work/concat.txt"
  : > "$concat_file"

  local i=0 spec input seek segment
  for spec in "${clips[@]}"; do
    i=$((i + 1))
    input="${spec%%|*}"
    seek="${spec##*|}"
    segment="$work/clip$(printf '%02d' "$i").mp4"
    render_vertical_clip "$ROOT/$input" "$seek" "$clip_duration" "$segment"
    printf "file '%s'\n" "$segment" >> "$concat_file"
  done
  [[ "$i" -eq 5 ]] || { echo "Reel $slug requires exactly five source clips" >&2; exit 1; }

  ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$concat_file" -c copy "$work/content.mp4"
  cover_file="$work/cover.mp4"
  ffmpeg -nostdin -y -v error -loop 1 -framerate "$FPS" -i "$COVER" \
    -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1920:0:(oh-ih)/2:black,format=yuv420p,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709,fps=$FPS,setsar=1" \
    -t "$closing_duration" -an -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r "$FPS" \
    -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$cover_file"
  printf "file '%s'\nfile '%s'\n" "$work/content.mp4" "$cover_file" > "$work/base-concat.txt"
  ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$work/base-concat.txt" -c copy "$work/base.mp4"

  title="$OUT/overlays/title$number.webp"
  cta="$OUT/overlays/cta.webp"
  ffmpeg -nostdin -y -v error -i "$work/base.mp4" -i "$audio" \
    -loop 1 -framerate "$FPS" -i "$title" -loop 1 -framerate "$FPS" -i "$cta" \
    -filter_complex "[0:v]fps=$FPS,tpad=stop_mode=clone:stop_duration=0.1,setpts=N/($FPS*TB)[base];[2:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st=4.7:d=0.5:alpha=1,setpts=PTS-STARTPTS[title];[3:v]format=rgba,fade=t=in:st=$content_duration:d=0.35:alpha=1,setpts=PTS-STARTPTS[cta];[base][title]overlay=0:0:shortest=1:enable='between(t,0,5.2)'[tmp];[tmp][cta]overlay=0:0:shortest=1:enable='between(t,$content_duration,$total_duration)'[v];[1:a]aresample=48000,adelay=${delay_ms}:all=1,apad,atrim=duration=$total_duration,loudnorm=I=-16:LRA=7:TP=-1.5[a]" \
    -map '[v]' -map '[a]' -t "$total_duration" -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r "$FPS" \
    -c:a aac -ar 48000 -b:a 192k -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart "$OUT/$slug.mp4"
  printf '%s audio=%s speech_end=%s opening_delay=%s total=%s closure=%s\n' "$slug" "$audio_duration" "$speech_end" "$narration_delay" "$total_duration" "$(awk -v a="$speech_end" -v t="$total_duration" 'BEGIN {printf "%.3f", t-a}')"
}

case "${1:-all}" in
  1|all)
    render_reel 1 "01-sports-biomechanics" "$OUT/audio/01-sports-biomechanics.wav" \
      "assets/motion/2026-09-07/stock/R1-01.mp4|0" \
      "assets/motion/2026-09-07/stock/R1-02.mp4|0" \
      "assets/motion/2026-09-07/stock/R1-03.mp4|0" \
      "assets/motion/2026-09-07/stock/R1-04.mp4|0" \
      "assets/motion/2026-09-07/stock/R1-05.mp4|0"
    [[ "${1:-all}" == 1 ]] && exit 0
    ;;
esac

case "${1:-all}" in
  remaining|all|2)
    render_reel 2 "02-hands-on-science" "$OUT/audio/02-hands-on-science.wav" \
      "assets/motion/2026-09-07/reels/paper-illustrative/01-rotor-drop.mp4|0" \
      "assets/motion/2026-09-07/reels/paper-illustrative/02-cut-lines.mp4|0" \
      "assets/motion/2026-09-07/reels/paper-illustrative/03-opposite-folds.mp4|0" \
      "assets/motion/2026-09-07/reels/paper-illustrative/04-equal-height.mp4|0" \
      "assets/motion/2026-09-07/reels/paper-illustrative/05-repeat-and-time.mp4|0"
    [[ "${1:-all}" == 2 ]] && exit 0
    ;;
esac

case "${1:-all}" in
  remaining|all|3)
    render_reel 3 "03-ai-archaeology" "$OUT/audio/03-ai-archaeology.wav" \
      "assets/motion/2026-09-07/stock/R3-01.mp4|0" \
      "assets/motion/2026-09-07/stock/R3-02.mp4|0" \
      "assets/motion/2026-09-07/stock/R3-03.mp4|0" \
      "assets/motion/2026-09-07/stock/R3-04.mp4|0" \
      "assets/motion/2026-09-07/stock/R3-05.mp4|0"
    ;;
  1) ;;
  *) echo "Usage: $0 [1|2|3|remaining|all]" >&2; exit 2 ;;
esac

for reel in "$OUT"/[0-9][0-9]-*.mp4; do
  ffprobe -v error -show_entries format=filename,duration:stream=codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 "$reel"
done
