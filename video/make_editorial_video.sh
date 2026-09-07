#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="${EDITORIAL_BUILD:-$ROOT/build/video/editorial}"
MANIFEST="$ROOT/video/editorial_scenes.tsv"
NARRATION="${NARRATION_FILE:-$ROOT/build/video/narration.wav}"
OUTPUT="${OUTPUT_FILE:-$ROOT/build/video/newhorizons.mp4}"
TITLE_LANGUAGE="${TITLE_LANGUAGE:-tr}"
FPS=60

mkdir -p "$BUILD/segments"
EDITORIAL_BUILD="$BUILD" node "$ROOT/video/src/generate_stock_disclosures.mjs"
[[ -s "$NARRATION" ]] || { echo "Missing narration: $NARRATION" >&2; exit 1; }

audio_duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$NARRATION")"
manifest_duration="$(awk -F'|' '!/^#/ && NF {sum += $3} END {printf "%.3f", sum}' "$MANIFEST")"
awk -v a="$audio_duration" -v v="$manifest_duration" 'BEGIN {d=a-v; if (d<0) d=-d; if (d>0.02) exit 1}' || {
  echo "Scene duration mismatch: audio=$audio_duration scenes=$manifest_duration" >&2
  exit 1
}

render_still() {
  local input="$1" duration="$2" output="$3"
  [[ "$input" == "$ROOT/assets/branding/new-horizons-cover.png" ]] || {
    echo "Only the approved closing cover may be rendered as a still." >&2
    exit 1
  }
  ffmpeg -nostdin -y -v error -loop 1 -framerate "$FPS" -i "$input" \
    -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p,setrange=limited,fps=$FPS,setsar=1" \
    -t "$duration" -an -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -r "$FPS" "$output"
}

render_clip() {
  local input="$1" duration="$2" seek="$3" loop="$4" layout="$5" output="$6"
  local -a args=(-nostdin -y -v error)
  local filter
  [[ "$loop" == "yes" ]] && args+=(-stream_loop -1)
  if [[ "$loop" == "stretch" ]]; then
    local source_duration stretch
    source_duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$input")"
    stretch="$(awk -v d="$duration" -v s="$source_duration" -v t="$seek" 'BEGIN { if(s<=t) exit 1; printf "%.9f", (d+0.04)/(s-t) }')"
    args+=(-itsscale "$stretch")
  fi
  args+=(-ss "$seek" -i "$input")
  if [[ "$layout" == "contain_blur" ]]; then
    filter="split=2[fgsrc][bgsrc];[bgsrc]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=32,eq=brightness=-0.18:saturation=0.75[bg];[fgsrc]scale=1920:1080:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,eq=contrast=1.02:saturation=1.03,format=yuv420p,setrange=limited,fps=$FPS,trim=duration=$duration,setpts=PTS-STARTPTS,setsar=1"
  else
    filter="scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=contrast=1.025:saturation=1.035,format=yuv420p,setrange=limited,fps=$FPS,trim=duration=$duration,setpts=PTS-STARTPTS,setsar=1"
  fi
  local -a filter_args=(-vf "$filter")
  if [[ "$input" == */stock/* ]]; then
    local label=generic
    [[ "$input" == */M4-* ]] && label=samsung
    [[ "$input" == */M5-* ]] && label=centuria
    [[ "$input" == */M5-01.mp4 ]] && label=museum
    args+=(-loop 1 -framerate "$FPS" -i "$BUILD/disclosures/$label.webp")
    filter_args=(-filter_complex "[0:v]$filter[scene];[scene][1:v]overlay=0:0:shortest=1[outv]" -map '[outv]')
  fi
  ffmpeg "${args[@]}" \
    "${filter_args[@]}" \
    -t "$duration" -an -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -r "$FPS" "$output"
}

concat_file="$BUILD/concat.txt"
: > "$concat_file"
scene=0
while IFS='|' read -r kind relative duration seek layout; do
  [[ -z "${kind:-}" || "$kind" == \#* ]] && continue
  input="$ROOT/$relative"
  [[ "$input" != */png/* ]] || { echo "Forbidden png folder asset: $input" >&2; exit 1; }
  [[ -s "$input" ]] || { echo "Missing scene asset: $input" >&2; exit 1; }
  scene=$((scene + 1))
  output="$BUILD/segments/scene$(printf '%02d' "$scene").mp4"
  case "$kind" in
    still) render_still "$input" "$duration" "$output" ;;
    clip|outro) render_clip "$input" "$duration" "$seek" no "$layout" "$output" ;;
    cliploop) render_clip "$input" "$duration" "$seek" yes "$layout" "$output" ;;
    clipstretch) render_clip "$input" "$duration" "$seek" stretch "$layout" "$output" ;;
    *) echo "Unknown scene type: $kind" >&2; exit 1 ;;
  esac
  printf "file '%s'\n" "$output" >> "$concat_file"
  printf 'Rendered scene %02d/%02d\n' "$scene" 31
done < "$MANIFEST"

ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$concat_file" -c copy "$BUILD/visuals.mp4"
NORMALIZED_VISUALS="$BUILD/visuals-normalized.mp4"
ffmpeg -nostdin -y -v error -i "$BUILD/visuals.mp4" \
  -vf "format=yuv420p,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709,fps=$FPS" \
  -an -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -r "$FPS" \
  -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$NORMALIZED_VISUALS"

VIDEO_LANG="$TITLE_LANGUAGE" EDITORIAL_BUILD="$BUILD" \
  node "$ROOT/video/src/generate_editorial_titles.mjs"
TITLE_SEGMENTS="$BUILD/title-segments"
mkdir -p "$TITLE_SEGMENTS"
title_concat="$TITLE_SEGMENTS/concat.txt"
: > "$title_concat"

render_plain_segment() {
  local start="$1" duration="$2" output="$3"
  ffmpeg -nostdin -y -v error -ss "$start" -i "$NORMALIZED_VISUALS" -t "$duration" \
    -vf "fps=$FPS,setpts=PTS-STARTPTS" -an -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -r "$FPS" "$output"
}

render_title_segment() {
  local start="$1" duration="$2" image="$3" output="$4"
  local slide_out_start
  slide_out_start="$(awk -v d="$duration" 'BEGIN {printf "%.3f", d-0.35}')"
  ffmpeg -nostdin -y -v error -ss "$start" -i "$NORMALIZED_VISUALS" \
    -loop 1 -framerate "$FPS" -i "$image" -t "$duration" \
    -filter_complex "[0:v]fps=$FPS,setpts=PTS-STARTPTS[main];[1:v]format=rgba,fade=t=in:st=0:d=0.28:alpha=1,fade=t=out:st=$slide_out_start:d=0.35:alpha=1,setpts=PTS-STARTPTS[ov];[main][ov]overlay=x=0:y='if(lt(t,0.35),90*(0.35-t)/0.35,if(gt(t,$slide_out_start),90*(t-$slide_out_start)/0.35,0))':eof_action=repeat:shortest=1:eval=frame[outv]" \
    -map '[outv]' -an -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -r "$FPS" "$output"
}

render_glass_cta_segment() {
  local start="$1" duration="$2" image="$3" output="$4"
  local fade_out
  fade_out="$(awk -v d="$duration" 'BEGIN {printf "%.3f", d-0.55}')"
  ffmpeg -nostdin -y -v error -ss "$start" -i "$NORMALIZED_VISUALS" \
    -loop 1 -framerate "$FPS" -i "$image" \
    -loop 1 -framerate "$FPS" -i "$BUILD/title-overlays/cta-thumb.webp" \
    -loop 1 -framerate "$FPS" -i "$BUILD/title-overlays/cta-bell.webp" \
    -loop 1 -framerate "$FPS" -i "$BUILD/title-overlays/cta-glow.webp" -t "$duration" \
    -filter_complex "[0:v]fps=$FPS,setpts=PTS-STARTPTS[main];[1:v]format=rgba,fade=t=in:st=0:d=0.45:alpha=1,fade=t=out:st=$fade_out:d=0.55:alpha=1,setpts=PTS-STARTPTS[base];[2:v]format=rgba,scale=w='iw*(1+0.18*exp(-pow((t-1.15)/0.16,2)))':h='ih*(1+0.18*exp(-pow((t-1.15)/0.16,2)))':eval=frame,fade=t=in:st=0.20:d=0.35:alpha=1,fade=t=out:st=$fade_out:d=0.55:alpha=1,setpts=PTS-STARTPTS[thumb];[3:v]format=rgba,rotate='if(between(t,3,4.2),0.22*sin((t-3)*35)*(4.2-t),0)':ow=rotw(iw):oh=roth(ih):c=none,fade=t=in:st=0.25:d=0.35:alpha=1,fade=t=out:st=$fade_out:d=0.55:alpha=1,setpts=PTS-STARTPTS[bell];[4:v]format=rgba,fade=t=in:st=1.45:d=0.20:alpha=1,fade=t=out:st=1.85:d=0.45:alpha=1,setpts=PTS-STARTPTS[glow];[main][base]overlay=x=0:y='if(lt(t,0.45),55*(0.45-t)/0.45,if(gt(t,$fade_out),35*(t-$fade_out)/0.55,0))':shortest=1:eval=frame[v1];[v1][thumb]overlay=x='450+(92-overlay_w)/2':y='824+(92-overlay_h)/2':shortest=1:eval=frame[v2];[v2][bell]overlay=x='1296+(92-overlay_w)/2':y='824+(92-overlay_h)/2':shortest=1:eval=frame[v3];[v3][glow]overlay=x=617:y=817:shortest=1:eval=frame[outv]" \
    -map '[outv]' -an -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -r "$FPS" "$output"
}

segment_count=0
previous_end=0
while IFS='|' read -r title_start title_end title_path title_style; do
  gap_duration="$(awk -v s="$previous_end" -v e="$title_start" 'BEGIN {printf "%.3f", e-s}')"
  if awk -v d="$gap_duration" 'BEGIN {exit !(d>0.0001)}'; then
    segment_count=$((segment_count + 1)); gap_output="$TITLE_SEGMENTS/segment$(printf '%02d' "$segment_count").mp4"
    render_plain_segment "$previous_end" "$gap_duration" "$gap_output"; printf "file '%s'\n" "$gap_output" >> "$title_concat"
  fi
  overlay_duration="$(awk -v s="$title_start" -v e="$title_end" 'BEGIN {printf "%.3f", e-s}')"
  segment_count=$((segment_count + 1)); overlay_output="$TITLE_SEGMENTS/segment$(printf '%02d' "$segment_count").mp4"
  if [[ "$title_style" == glass_cta ]]; then render_glass_cta_segment "$title_start" "$overlay_duration" "$title_path" "$overlay_output"; else render_title_segment "$title_start" "$overlay_duration" "$title_path" "$overlay_output"; fi
  printf "file '%s'\n" "$overlay_output" >> "$title_concat"; previous_end="$title_end"
done < "$BUILD/title-overlays/manifest.tsv"

ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$title_concat" -c copy "$BUILD/titled-visuals.mp4"
ffmpeg -nostdin -y -v warning -stats_period 10 -i "$BUILD/titled-visuals.mp4" -i "$NARRATION" \
  -filter_complex '[1:a]aresample=48000,loudnorm=I=-16:LRA=7:TP=-1.5[a]' \
  -map 0:v:0 -map '[a]' -t "$audio_duration" -c:v copy -c:a aac -ar 48000 -b:a 192k -movflags +faststart "$OUTPUT"

ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 "$OUTPUT"
