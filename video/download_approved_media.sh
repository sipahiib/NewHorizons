#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
YTDLP="/tmp/newhorizons-downloader/bin/yt-dlp"

download() {
  local relative="$1" url="$2" target
  target="$ROOT/$relative"
  mkdir -p "$(dirname "$target")"
  if [[ -s "$target" ]]; then
    printf 'Already present: %s\n' "$relative"
    return
  fi
  "$YTDLP" --impersonate chrome --no-playlist -f best --no-part -o "$target" "$url"
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate:format=duration -of csv=p=0 "$target"
}

# Main story: explainable autonomous driving
download assets/motion/2026-09-04/01-cwnet/01-las-vegas.mp4 https://www.pexels.com/video/autonomous-vehicle-on-las-vegas-street-31761705/
download assets/motion/2026-09-04/01-cwnet/02-urban.mp4 https://www.pexels.com/video/autonomous-vehicle-in-urban-setting-streets-36629601/
download assets/motion/2026-09-04/01-cwnet/03-control-screen.mp4 https://www.pexels.com/video/self-driving-electric-car-in-action-32024440/
download assets/motion/2026-09-04/01-cwnet/04-navigation.mp4 https://www.pexels.com/video/driving-with-gps-navigation-in-city-traffic-37505403/
download assets/motion/2026-09-04/01-cwnet/05-traffic.mp4 https://www.pexels.com/video/aerial-view-of-busy-urban-street-traffic-30609023/

# Cultivated tissue
download assets/motion/2026-09-04/02-tissue/01-petri.mp4 https://www.pexels.com/video/close-up-shot-of-petri-dish-with-specimen-4123377/
download assets/motion/2026-09-04/02-tissue/02-cell-culture.mp4 https://www.pexels.com/video/a-person-holding-a-petri-dish-7705427/
download assets/motion/2026-09-04/02-tissue/03-liquid-drops.mp4 https://www.pexels.com/video/drops-of-liquid-in-a-petri-dish-8392554/
download assets/motion/2026-09-04/02-tissue/04-scientists.mp4 https://www.pexels.com/video/a-man-dropping-samples-on-the-petri-dish-4120947/
download assets/motion/2026-09-04/02-tissue/05-animated-cells.mp4 https://www.pexels.com/video/animated-cells-in-motion-abstract-video-34913408/

# AMSR3 weather satellite
download assets/motion/2026-09-04/03-amsr3/01-orbit.mp4 https://www.pexels.com/video/satellite-orbiting-the-earth-854275/
download assets/motion/2026-09-04/03-amsr3/02-detailed.mp4 https://www.pexels.com/video/satellite-orbiting-planet-earth-in-space-31084229/
download assets/motion/2026-09-04/03-amsr3/03-sunrise.mp4 https://www.pexels.com/video/orbiting-satellite-over-earth-at-sunrise-34333825/
download assets/motion/2026-09-04/03-amsr3/04-panels.mp4 https://www.pexels.com/video/satellite-in-space-15164036/
download assets/motion/2026-09-04/03-amsr3/05-earth.mp4 https://www.pexels.com/video/view-from-satellite-on-earth-10409075/

# Liver fibrosis
download assets/motion/2026-09-04/04-liver/01-cells.mp4 https://www.pexels.com/video/animated-cells-in-motion-abstract-video-34913408/
download assets/motion/2026-09-04/04-liver/02-blood-mixer.mp4 https://www.pexels.com/video/a-rotating-blood-mixer-in-a-lab-8381577/
download assets/motion/2026-09-04/04-liver/03-blood-cells.mp4 https://www.pexels.com/video/dynamic-animation-of-red-blood-cells-35220823/
download assets/motion/2026-09-04/04-liver/04-microscope.mp4 https://www.pexels.com/video/young-laboratory-medicine-science-4120946/
download assets/motion/2026-09-04/04-liver/05-medical-scan.mp4 https://www.pexels.com/video/medical-equipment-855481/

# Brain-wave theory
download assets/motion/2026-09-04/05-brain/01-brain-animation.mp4 https://www.pexels.com/video/a-brain-with-a-pink-glow-in-the-dark-background-18388881/
download assets/motion/2026-09-04/05-brain/02-mri-tablet.mp4 https://www.pexels.com/video/a-brain-magnetic-resonance-imaging-result-6010766/
download assets/motion/2026-09-04/05-brain/03-mri-machine.mp4 https://www.pexels.com/video/a-mri-machine-in-a-medical-facility-7088941/
download assets/motion/2026-09-04/05-brain/04-scan-images.mp4 https://www.pexels.com/video/presenting-x-ray-images-5724101/
download assets/motion/2026-09-04/05-brain/05-concept.mp4 https://www.pexels.com/video/a-tool-squeezing-a-brain-9162016/

# Reel 1: sports biomechanics
download assets/motion/2026-09-04/reels/01-sports/01-running.mp4 https://www.pexels.com/video/knee-level-shot-of-a-runner-passing-the-starting-line-8533917/
download assets/motion/2026-09-04/reels/01-sports/02-start.mp4 https://www.pexels.com/video/tilt-shot-of-a-person-kneeling-at-a-starting-line-8533474/
download assets/motion/2026-09-04/reels/01-sports/03-basketball.mp4 https://www.pexels.com/video/basketball-falling-through-a-hoop-in-slow-motion-12787247/
download assets/motion/2026-09-04/reels/01-sports/04-football.mp4 https://www.pexels.com/video/a-man-playing-with-a-football-10349006/
download assets/motion/2026-09-04/reels/01-sports/05-skateboard.mp4 https://www.pexels.com/video/man-jumping-on-skateboard-13184995/

# Reel 2: hands-on science
download assets/motion/2026-09-04/reels/02-young-science/01-home.mp4 https://www.pexels.com/video/a-boy-doing-experiment-7605719/
download assets/motion/2026-09-04/reels/02-young-science/02-children.mp4 https://www.pexels.com/video/children-doing-science-experiment-8471232/
download assets/motion/2026-09-04/reels/02-young-science/03-girl.mp4 https://www.pexels.com/video/a-young-girl-doing-an-experiment-8926576/
download assets/motion/2026-09-04/reels/02-young-science/04-funnel.mp4 https://www.pexels.com/video/boy-experiment-at-lab-7605358/
download assets/motion/2026-09-04/reels/02-young-science/05-baking-soda.mp4 https://www.pexels.com/video/laboratory-experiment-7605356/

# Reel 3: AI and archaeology
download assets/motion/2026-09-04/reels/03-ai-archaeology/01-site.mp4 https://www.pexels.com/video/aerial-view-of-ancient-archaeological-site-34246778/
download assets/motion/2026-09-04/reels/03-ai-archaeology/02-temple.mp4 https://www.pexels.com/video/aerial-shot-of-ruins-7048573/
download assets/motion/2026-09-04/reels/03-ai-archaeology/03-amphitheatre.mp4 https://www.pexels.com/video/aerial-view-of-ancient-ruins-and-amphitheater-30616218/
download assets/motion/2026-09-04/reels/03-ai-archaeology/04-remote-sensing.mp4 https://www.pexels.com/video/aerial-view-of-ancient-archaeological-site-30485433/
download assets/motion/2026-09-04/reels/03-ai-archaeology/05-desert.mp4 https://www.pexels.com/video/stunning-aerial-view-of-ancient-ruins-in-desert-30131338/
