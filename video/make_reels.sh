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
  ffmpeg -nostdin -y -v error -ss "$seek" -i "$input" \
    -vf "split=2[fgsrc][bgsrc];[bgsrc]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=35,eq=brightness=-0.20:saturation=0.72[bg];[fgsrc]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709,fps=$FPS,trim=duration=$duration,setpts=PTS-STARTPTS,setsar=1" \
    -t "$duration" -an -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r "$FPS" \
    -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$output"
}

render_reel() {
  local number="$1" slug="$2" audio="$3"
  shift 3
  local -a clips=("$@")
  local audio_duration total_duration content_duration clip_duration work concat_file base cover_file title cta
  audio_duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$audio")"
  content_duration="$audio_duration"
  total_duration="$(awk -v d="$audio_duration" 'BEGIN {t=d+3; if (t<30) t=30; if (t>35) t=35; if (t-d<=0 || t-d>4) exit 2; printf "%.3f", t}')" || {
    echo "Reel $slug cannot fit 30-35 seconds with a maximum four-second closing gap: audio=$audio_duration" >&2
    exit 1
  }
  awk -v a="$audio_duration" -v t="$total_duration" 'BEGIN {g=t-a; if (g>4.0001) exit 1}' || {
    echo "Reel $slug closing gap exceeds four seconds" >&2
    exit 1
  }
  clip_duration="$(awk -v d="$content_duration" 'BEGIN {printf "%.3f", d/5}')"
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
    -t 3 -an -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r "$FPS" \
    -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$cover_file"
  printf "file '%s'\nfile '%s'\n" "$work/content.mp4" "$cover_file" > "$work/base-concat.txt"
  ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$work/base-concat.txt" -c copy "$work/base.mp4"

  title="$OUT/overlays/title$number.webp"
  cta="$OUT/overlays/cta.webp"
  ffmpeg -nostdin -y -v error -i "$work/base.mp4" -i "$audio" \
    -loop 1 -framerate "$FPS" -i "$title" -loop 1 -framerate "$FPS" -i "$cta" \
    -filter_complex "[0:v]fps=$FPS,setpts=N/($FPS*TB)[base];[2:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st=4.7:d=0.5:alpha=1,setpts=PTS-STARTPTS[title];[3:v]format=rgba,fade=t=in:st=$content_duration:d=0.35:alpha=1,setpts=PTS-STARTPTS[cta];[base][title]overlay=0:0:shortest=1:enable='between(t,0,5.2)'[tmp];[tmp][cta]overlay=0:0:shortest=1:enable='between(t,$content_duration,$total_duration)'[v];[1:a]aresample=48000,apad,atrim=duration=$total_duration,loudnorm=I=-16:LRA=7:TP=-1.5[a]" \
    -map '[v]' -map '[a]' -t "$total_duration" -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -r "$FPS" \
    -c:a aac -ar 48000 -b:a 192k -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart "$OUT/$slug.mp4"
  printf '%s audio=%s total=%s closure=%s\n' "$slug" "$audio_duration" "$total_duration" "$(awk -v a="$audio_duration" -v t="$total_duration" 'BEGIN {printf "%.3f", t-a}')"
}

case "${1:-all}" in
  1|all)
    render_reel 1 "01-roman-space-telescope" "$OUT/audio/01-roman-space-telescope.wav" \
      "assets/motion/2026-09-02/01-roman/01-launch.mp4|12" \
      "assets/motion/2026-09-02/01-roman/02-beauty-pass.mp4|7" \
      "assets/motion/2026-09-02/01-roman/03-l2-journey.mp4|3" \
      "assets/motion/2026-09-02/01-roman/04-coronagraph.mov|2" \
      "assets/motion/2026-09-02/01-roman/05-journey-to-space.mp4|16"
    [[ "${1:-all}" == 1 ]] && exit 0
    ;;
esac

case "${1:-all}" in
  remaining|all)
    render_reel 2 "02-alpha-gal-antibodies" "$OUT/audio/02-alpha-gal-antibodies.wav" \
      "assets/motion/2026-09-02/02-alpha-gal/01-cdc.mp4|24" \
      "assets/motion/2026-09-02/02-alpha-gal/02-scientific-american.mp4|10" \
      "assets/motion/2026-09-02/02-alpha-gal/03-mayo.mp4|18" \
      "assets/motion/2026-09-02/02-alpha-gal/04-tick-macro.mp4|12" \
      "assets/motion/2026-09-02/02-alpha-gal/05-lab-research.mp4|1"
    render_reel 3 "03-astra-cybersecurity" "$OUT/audio/03-astra-cybersecurity.wav" \
      "assets/motion/2026-09-02/03-astra/01-openai-defense.mp4|10" \
      "assets/motion/2026-09-02/03-astra/02-cyber-lock.mp4|2" \
      "assets/motion/2026-09-02/03-astra/03-binary-lock.mp4|0" \
      "assets/motion/2026-09-02/03-astra/04-code-screen.mp4|1" \
      "assets/motion/2026-09-02/03-astra/05-cyber-threat.mp4|6"
    render_reel 4 "04-cluster-samba" "$OUT/audio/04-cluster-samba.wav" \
      "assets/motion/2026-09-02/04-cluster/01-control-room.mp4|250" \
      "assets/motion/2026-09-02/04-cluster/02-samba-reentry.mp4|4" \
      "assets/motion/2026-09-02/04-cluster/03-reentry-explained.mp4|98" \
      "assets/motion/2026-09-02/04-cluster/04-salsa-animation.mp4|18" \
      "assets/motion/2026-09-02/04-cluster/05-draco-animation.mp4|40"
    render_reel 5 "05-pallas-one" "$OUT/audio/05-pallas-one.wav" \
      "assets/motion/2026-09-02/05-pallas/01-cctv-launch.mp4|5" \
      "assets/motion/2026-09-02/05-pallas/01-cctv-launch.mp4|55" \
      "assets/motion/2026-09-02/05-pallas/02-cctv-capability.mp4|22" \
      "assets/motion/2026-09-02/05-pallas/03-seven-engine-test.mp4|1" \
      "assets/motion/2026-09-02/05-pallas/04-second-stage-test.mp4|6"
    ;;
  1) ;;
  *) echo "Usage: $0 [1|remaining|all]" >&2; exit 2 ;;
esac

for reel in "$OUT"/[0-9][0-9]-*.mp4; do
  ffprobe -v error -show_entries format=filename,duration:stream=codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 "$reel"
done
