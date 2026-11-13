# Independent output QA — R2, 13 November 2026

**Status: BLOCKED — full independent audiovisual playback not performed.** Do not deliver or clear cleanup on this evidence. QA was independent of the render. The approved shortened narration and R2 are recorded in `APPROVAL.md`; `REVIEW.md` records a local-render pass. Main-programme checks are not applicable to this Reel.

- Actual output: `build/reels/2026-11-13/planet-earth-flow-country.mp4`. SHA-256: `c42f09259224faa163d9f077dc3d4a38e86f20c07b8201405822cf3073975cc6`.
- Full FFmpeg decode to null completed with exit 0 and no errors. FFprobe counted 2,760 video frames, H.264 1080×1920 at 60 fps, 46.000 s, and mono AAC at 96 kHz, 46.000 s. Duration and format meet the Reel specification.
- Inspected rendered frames at 1, 5.5, 6.1, 14, 21, 27, 34, 40 and 44.5 seconds. These show seven distinct landscape/satellite scenes consistent with the selected Flow Country sources and the manifest order, with full landscape frames over dark blurred backgrounds. The title is readable at 1 s and absent at 5.5 s; the final frame sample shows unboxed YouTube and Instagram calls. These samples do not prove every transition, exact CTA window, or complete visual playback. The seven selected source and narration hashes match `r2_manifest.json`; source provenance and rights are addressed in the independent pre-render review, including its distribution caveat.
- Output audio silence detection at −40 dB estimates final speech ending at 43.407 s, 2.593 s before the end. Mean level is −16.6 dB and peak −1.4 dB by FFmpeg volumedetect. These measurements cannot assess pronunciation, clipped words, pacing or perceived loudness. The user previously listened to the source audio, but independent complete listening to the rendered output was not performed.

**Remaining blocker:** independently watch and listen to the complete rendered file, checking pronunciation, missing or clipped words, pacing, sound, all imagery and transitions, mobile readability and complete CTA. Confirm exact title and CTA windows in motion. Record the playback evidence and only then set the required human-approval and machine-gate fields as described in `video/QA_CHECKLIST.md`. No persistent verification artifacts were created; the output and manifest paths above are the evidence for the commands and frame samples reported here.

## Playback confirmation — controller record

The user confirmed “onaylıyorum” after being asked to watch and listen to the complete linked 46-second rendered R2 candidate. The output SHA-256 was rechecked as `c42f09259224faa163d9f077dc3d4a38e86f20c07b8201405822cf3073975cc6`. Independent technical/sample QA above passed; user-confirmed full playback resolves its playback blocker. R2 local delivery gate: **PASS**. Publication and distribution remain unauthorised; CC BY-SA treatment remains to be resolved before external distribution. No cleanup performed.

# Main output QA — 13 November 2026

**Status: BLOCKED pending complete viewing and listening of the rendered main candidate.** Technical and sampled-frame QA performed by the controller, independent of the delegated render. The render agent's session ended with a usage-limit error after creating the candidate; the actual file was verified rather than assuming command completion.

- Candidate `build/video/2026-11-13/newhorizons.mp4`, SHA-256 `52e91a4b32151d4c280b412f728fde21e9e80142e10310ee1fefd2a95f46867f`. Full FFmpeg decode to null exited 0. FFprobe counted 10,200 frames, H.264, 1920×1080, 60 fps, 170.000 s; AAC, 48 kHz. Proposed opening 0–16 s; second story begins at 99 s; final closing occupies 160–170 s, consistent with the manifest.
- Rendered samples at 1, 5.2, 6, 12.5, 16.5, 21.5, 30, 35.6, 60, 99.5, 104.6, 120, 159, 161 and 168 s were inspected (`build/video/2026-11-13/qa/`). They show the intended contextual turbine and explicitly separate FloWave still, Hubble imagery, title and subscription windows, and the closing panel. Samples are not full-motion playback.
- FFmpeg volumedetect measured mean −16.7 dB and max −1.4 dB. Silence detection at −40 dB found 10.310–12.236, 19.534–21.242, 97.213–99.224, 158.084–162.160 and 166.878–170 s. The approximately four-second pause spanning the second-story ending and closing is explained by final speech tail plus the planned two-second closing lead-in; user evaluation of pacing remains necessary. User previously confirmed full audio preview and revised opening segments, but not this rendered audiovisual file.
- User must watch and listen to the complete candidate and assess all shots, transitions, pronunciation, pacing including the closing pause, and closing animation before the main gate can pass. No metadata or sampled frames substitute for full playback. No promotion, cleanup or publication. Hubble image third-party rights remain unresolved before any external distribution.

## Main complete playback — controller record

The user confirmed “onaylıyorum” after being asked to watch and listen to the complete linked 170-second main candidate, including its closing pause. The candidate hash was rechecked as `52e91a4b32151d4c280b412f728fde21e9e80142e10310ee1fefd2a95f46867f`. Independent controller technical/sample QA above passed, and user-confirmed complete playback resolves the playback blocker. Local main delivery gate: **PASS**. External distribution remains unauthorised; image-specific Hubble third-party rights remain unresolved. No cleanup performed.

## Post-delivery cleanup verification

At the user’s request, 35 inventoried disposable render intermediates were removed after full playback gates passed. Main, cycle-copy and R2 delivery hashes were rechecked unchanged. Inventory and hashes: `CLEANUP_MANIFEST.json`. Source inputs, manifests, verification samples and prior cycles were preserved.
