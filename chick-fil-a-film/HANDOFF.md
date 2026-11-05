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

## State
- Sheets 1-9 final. Sheet 10 (CF-076 to CF-084B) in progress at CF-076.
- Retired (files kept): CF-019B, 025B, 064B, 066, 070B. CF-065B is kept.
- Remaining after sheet 10: sheets 11-13 (CF-085 to CF-101).

## Pending decision: CF-076
It is a "(carry)" cell; CF-075's line plays over 075-078. Recommended option 1: put "That is the good part of the deal. And it is real." on CF-076 and "Now here is the part that is just as real." on CF-077. (Options: 2 = free label such as "THE GOOD PART", 3 = new image at 1.00.)

## Flags for the rest of sheet 10
077 and 078 are silent carries (078 = blank pay line). 079 caption is long (3 sentences). 080 = edit state on 079, overlay LAND / BUILDING / EQUIPMENT / THE BUSINESS — CHICK-FIL-A'S. 081 is a carry. 082 and 083 pictures (sale handshake, key to kid) do not match their lines (what the company owns). 084/084B: deed with company hand; mascot hand beside empty frame.

## Assembly notes
CF-060: draw the envelope being set aside first, then the pile split. CF-013: chart takes no number (bars only). CF-014 carries the "$9,090,000" plate on the image.

## Higgsfield references (may be reachable in the account)
Signed CF-001 master media id 7f013de9-ae39-4b4a-ac37-b86abdc7ad74; restaurant/sign ref d3acbfe1-2023-455d-90fd-d285d0406039; counter interior (new CF-048) 217419f3-4d0c-4482-9ef2-51c0136e2451.
