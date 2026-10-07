# Reproduction — 2026-10-07

Run from the repository root after current approval. Source downloads/TTS need network access. Retained originals and source pages support provenance; selected derivatives and manifests are cycle-local. Never substitute a historical manifest.

```sh
python3 video/cycles/2026-10-07/fetch_pages.py
python3 video/cycles/2026-10-07/fetch_media.py
python3 video/cycles/2026-10-07/fetch_context.py
.tools-edge-tts/bin/python video/cycles/2026-10-07/prepare_audio.py
/Users/is9565/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 video/cycles/2026-10-07/prepare_visuals.py
python3 video/cycles/2026-10-07/prepare_audit.py
```

Source-composed pre-render samples can be generated with `render.py OUTPUT --preview`. Independent review must set each output's gate to PASS before rendering:

```sh
python3 video/cycles/2026-10-07/render.py main
python3 video/cycles/2026-10-07/render.py r1
python3 video/cycles/2026-10-07/render.py r2
```

Actual-output evidence:

```sh
/Users/is9565/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 video/cycles/2026-10-07/qa_outputs.py main
/Users/is9565/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 video/cycles/2026-10-07/qa_outputs.py r1
/Users/is9565/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 video/cycles/2026-10-07/qa_outputs.py r2
```

Complete perceptual listening and continuous viewing are required separately; evidence scripts cannot pass those gates. Candidate paths remain cycle-local until full audiovisual acceptance. Shared main output promotion and cleanup remain blocked while any playback gate is pending. Publishing requires separate authorisation.
