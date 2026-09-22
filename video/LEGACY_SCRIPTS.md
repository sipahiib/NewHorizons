# Historical Script Safety

The following entry points reproduce superseded cycles and are not active production tools:

- `download_approved_media.sh --legacy-2026-09-04`
- `download_stock_assets.mjs --legacy-2026-09-07 [inventory.json]`
- `render_main_motion.mjs --legacy-2026-09-07 ...`
- `render_paper_motion.mjs --legacy-2026-09-07 ...`
- `make_current_reel_covers.mjs --legacy-2026-09-10`

They fail closed without the exact legacy flag. Their outputs must not be selected by a new cycle without fresh provenance, rights, subject-correspondence and hash verification. The cover generator exists only for historical reproducibility; current policy forbids producing or delivering covers and thumbnails.
