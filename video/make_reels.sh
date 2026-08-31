#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VISUALS="$ROOT/build/video/editorial-en/visuals-normalized.mp4"
AUDIO="$ROOT/build/video/narration-brian-source.wav"
COVER="$ROOT/assets/branding/new-horizons-cover.png"
OUT="$ROOT/build/reels"
mkdir -p "$OUT"
node "$ROOT/video/src/generate_reel_overlays.mjs"

render_reel() {
  local number="$1" slug="$2" visual_start="$3" audio_start="$4"
  local reel_audio="$OUT/audio/$slug.wav"
  local total_duration=30
  local content_duration=25
  local cta_start=25
  local source_duration=29
  local clean_select="null"
  local narration_args=(-ss "$audio_start" -t 25 -i "$AUDIO")
  local audio_filter="[2:a]atrim=duration=25,asetpts=PTS-STARTPTS[a0];[3:a]apad=pad_dur=0.136,atrim=duration=5,asetpts=PTS-STARTPTS[a1];[a0][a1]concat=n=2:v=0:a=1,loudnorm=I=-16:LRA=7:TP=-1.5[a]"
  if [[ -f "$reel_audio" ]]; then
    total_duration=32
    content_duration=27
    cta_start=27
    source_duration=31
    narration_args=(-i "$reel_audio")
    audio_filter="[2:a]apad,atrim=duration=$total_duration,asetpts=PTS-STARTPTS,loudnorm=I=-16:LRA=7:TP=-1.5[a]"
  fi
  if [[ "$number" == "3" ]]; then
    clean_select="select='not(between(t,7.60,9.00)+between(t,14.95,15.60)+between(t,20.25,20.85))',setpts=N/(60*TB)"
  elif [[ "$number" == "5" ]]; then
    clean_select="select='not(between(t,8.03,9.00))',setpts=N/(60*TB)"
  fi
  ffmpeg -nostdin -y -v error \
    -ss "$visual_start" -t "$source_duration" -i "$VISUALS" \
    -loop 1 -framerate 60 -t 5 -i "$COVER" \
    "${narration_args[@]}" \
    -ss 203.376 -t 4.864 -i "$AUDIO" \
    -loop 1 -framerate 60 -i "$OUT/overlays/title$number.webp" \
    -loop 1 -framerate 60 -i "$OUT/overlays/cta.webp" \
    -filter_complex "[0:v]$clean_select,split=2[fgsrc][bgsrc];[bgsrc]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=35,eq=brightness=-0.18:saturation=0.72[bg];[fgsrc]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=60,trim=duration=$content_duration,setpts=PTS-STARTPTS[v0];[1:v]scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1920:0:(oh-ih)/2:black,setsar=1,fps=60,trim=duration=5,setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.35[v1];[v0][v1]concat=n=2:v=1:a=0[base];[4:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st=4.4:d=0.4:alpha=1,setpts=PTS-STARTPTS[title];[5:v]format=rgba,trim=duration=5,fade=t=in:st=0:d=0.45:alpha=1,setpts=PTS-STARTPTS+$cta_start/TB[cta];[base][title]overlay=0:0:shortest=1[tmp];[tmp][cta]overlay=0:0:eof_action=pass[v];$audio_filter" \
    -map '[v]' -map '[a]' -t "$total_duration" -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r 60 \
    -c:a aac -ar 48000 -b:a 192k -movflags +faststart "$OUT/$slug.mp4"
}

case "${1:-all}" in
  1) render_reel 1 "01-libre-duo" 5 14.557 ;;
  remaining)
    render_reel 2 "02-nasa-pandora" 55 55.752
    render_reel 3 "03-future-collider" 110 87.275
    render_reel 4 "04-double-higgs" 155 126.421
    render_reel 5 "05-ai-6g-factories" 210 168.087
    ;;
  all)
    render_reel 1 "01-libre-duo" 5 14.557
    render_reel 2 "02-nasa-pandora" 55 55.752
    render_reel 3 "03-future-collider" 110 87.275
    render_reel 4 "04-double-higgs" 155 126.421
    render_reel 5 "05-ai-6g-factories" 210 168.087
    ;;
  *) echo "Usage: $0 [1|remaining|all]" >&2; exit 2 ;;
esac

for reel in "$OUT"/*.mp4; do
  ffprobe -v error -show_entries format=filename,duration:stream=codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 "$reel"
done
