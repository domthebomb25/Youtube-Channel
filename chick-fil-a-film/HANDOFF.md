# Chick-fil-A film #1: images-only storyboard (handoff)

Read `CLAUDE.md` first. Branch: `claude/peaceful-gates-z0c750`.

## What is here
- `data/cells_v2.json`: the live storyboard (119 cells, in order). Each cell has `id`, `kind` (GEN or EDIT), `img` (image file id, defaults to `id`), `caption` (the exact line spoken while it is on screen), and `overlay` notes for edit states.
- `data/crops.json`: zoom-beat frames (2688x1520 coordinates) for the removed crop cells. `data/map6.json`: the last script map. `data/timeline-notes.txt`, `data/assembly-notes.txt`.
- `images/CF-xxx.jpg`: every current final image (JPEG q90 copies; the originals were 2688x1520 PNG). `images/CF-xxx-edit.jpg` are edit-state bases.
- `sheets/storyboard-v2-sheet-01..13.pdf`: the sheets as last built (sheet 10 is the pre-review version).
- `scripts/`: `build_v2.py` (sheet builder), `review_card.py` (one-by-one review card: image + spoken line), `overlay.py` and `overlay2.py` (perspective text composites), `wordmark015.py` + `wordmark_alpha_clean.png` (the Chick-fil-A script wordmark used on signs).
- `originals/`: the signed CF-001 master (style reference).
These scripts expect the original scratchpad paths. Re-point `S`/paths when rebuilding; images are JPEG here, so change `.png` to `.jpg`.

## Rules
- Faces: emotion only, no talking mouths. Approved face = one brow slightly raised, round eyes, short closed smile.
- No coins. Signs, tags, documents, plates are generated BLANK; text is composited. Only baked-in text allowed: "Chick-fil-A" on restaurant signs (composite the wordmark, spelled exactly).
- Quote Higgsfield credits and wait for OK before generating (gpt_image_2_5: 2k medium 1.00, 1k medium 0.50, 2k high 2.75). No rerolls.
- Text, recolors, crops, caption moves are free and local.
- Credits spent so far on this job: 159.25 (my tally).

## Workflow in use: one image at a time
Show one review card (image + exact spoken line), offer options (keep / free label / new image with a quote), apply the choice, then the next image. Rebuild and re-send the sheet when it is finished.

## State (updated)
- ALL 13 sheets are done and confirmed (sheets 1-9 earlier; 10-13 this round). Final sheets are in `sheets/` (PDF + PNG for 10-13) and one combined PDF `sheets/chick-fil-a-storyboard-all-13-sheets.pdf`.
- `data/cells_v2.json` is the live storyboard in playing order (about 117 cells). New/changed cells carry a `note` and, where generated this round, a `higgsfield_job`. `data/cells_v2.pre-v5-sheet10.json` is the pre-realignment backup.
- Retired (files kept): CF-019B, 025B, 064B, 066, 070B, 078, 084B, 089B, 094B (rides 094), 099B (rides 099). CF-065B kept.
- Sheet 10-13 order (map v5): sheet 10 = 076, 077, 079, 081, 082, 083, 080, 084. Sheet 11 = 085, 086, 087, 088, 089, 090, 092, 019 (reuse), 091, 091B. Sheet 12 = 023 (uses CF-022 image), 095, 093, 093B, 041 (reuse), 094, 095B, 096, 097. Sheet 13 = 098, 099, 100, 101.
- Alternates kept: CF-085-alt-onestore, CF-085-orig-bricks, CF-086-alt-pay, CF-086-orig-fryers, CF-091-v1-restaurant, CF-091B-v1-crown, CF-099-v1-shelf.
- CF-098 / CF-099 / CF-100 / CF-101 captions were partly inferred (098 = ten-thousand line + "not cheap" lines; 099B rides 099; 100 = last line; 101 silent). Confirm against map v5 if it ever differs.
- Credits: about 168.25 spent on this job by my tally; balance last read 1,141.46 before the later generations (expected about 1,132.46), not re-checked.
- Rebuild scripts: `scripts/build_v2.py` (original) and `scripts/build10..13.py` (per-sheet builders used this round; they expect the old scratchpad layout, so re-point paths).

## Assembly notes
CF-060: draw the envelope being set aside first, then the pile split. CF-013: chart takes no number (bars only). CF-014 carries the "$9,090,000" plate on the image.

## Higgsfield references (may be reachable in the account)
Signed CF-001 master media id 7f013de9-ae39-4b4a-ac37-b86abdc7ad74; restaurant/sign ref d3acbfe1-2023-455d-90fd-d285d0406039; counter interior (new CF-048) 217419f3-4d0c-4482-9ef2-51c0136e2451.
