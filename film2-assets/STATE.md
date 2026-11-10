# STATE — Film #2 "POV: You Became the #1 Streamer Overnight." (long-form)

Single source of truth: branch `claude/happy-mccarthy-4tfabg`, folder `film2-assets/` (this folder). Updated 2026-11-10 (end of session). Higgsfield balance: see CURRENT STATUS (Section 3 generation, 2026-11-10).

## CURRENT STATUS (Section 4 fix round, 2026-11-10)
- **Sections 1-4 are DONE: 84 shots** (Section 4 = shots 76-88). Files: `section4/76.png`-`88.png` + `section4/85-state.png`. Map: `docs/SECTION4-MAP.txt`.
- **Higgsfield balance: 789.26 credits** (790.26 after the Section 4 generation; the fix round cost 1.00: one model edit on 86). Live price re-confirmed 1.00 first.
- **Section 4 runtime: 82.7 s.** Shot 88 = VO-129 only ("And it knocks on your door — politely."), 2.7 s. **VO-130-131 ("This leads you now to the final hidden truth. But.") are the OPENING of SECTION 5**; its first shot will be shot 89, designed in the Section 5 job.
- Fix round: 86 re-edited (lead HAPPY, hands on hips, speech bubble removed; old 86 in `discarded/86-v1-bubble-sad-SUPERSEDED.png`). 85-state: tiny streamer's face repainted HAPPY locally (0.00, `tools/section4-states.py` step 5). 88: no image change.
- Open flags still standing: 78 ringing icons are phone symbols, not platform buildings; 81 one star wears a blue shirt; 76/82 right eyebrow touches the head outline. No re-rolls done.
- Storyboards: `storyboards/section4-storyboard-v4-shots-76-81`, `-82-87`, `-88-and-85-state` (.pdf/.png, rebuilt) + review tiles `section4-fix-tile-*.png`. Builder `tools/sheet-section4.py`.
- **NEXT JOB: Section 5 (Truth 3: The Catch), opening on VO-130-131, first shot = 89, new chat.** Section 6 (The Payoff) after.

## EARLIER STATUS (close-out of the Section 3 chat, 2026-11-10)
- **Sections 1-3 are DONE: 71 shots total.** Section 1 = 19 shots, Section 2 = 34 shots, Section 3 = 18 shots (58-75, including the fix round; fix-round commit `9745448`). Files: `section1/`, `section2/`, `section3/` (+ `section3/69-state.png`). Section 3 map: `docs/SECTION3-MAP.txt`.
- **Higgsfield balance: 803.26 credits.** (823.26 at the start of the Section 3 chat; 16.00 first pass + 4.00 fix round.)
- **CHARACTER COLOR LOCK: Ludwig ALWAYS wears a GREEN sweatshirt; Ninja ALWAYS wears a BLUE sweatshirt.** Neither wears a gold tie (the gold tie is the lead only).
- **NEXT JOB: Section 4 (Truth 2: The Power), shots 76-88. The map is approved: 13 generations + 1 free state, expected cost 13.00. It will run in a NEW chat; it was NOT started in this one.** Preflight before any paid call as always (masters/refs attached, live price 1.00 via get_cost; stop and report if the price differs); one generation per shot, no re-rolls without Dominick's OK.
- Section 3 fix-round summary: 59 new generation ("$6" tag retouched locally); 63 model edit (calendar removed); 65 local green recolor; 69 new full-frame generation + 69-state rebuilt locally; 70 model edit (Ninja in blue); old 71 split into 71/72/73 (VO-098/099/100, cumulative row highlight); old 72/73 renumbered 74/75.
- Storyboards: current Section 3 sheets are `storyboards/section3-fix-v4-changed-shots.pdf`/`.png` and `storyboards/section3-fix-v4-shots-71-75.pdf`/`.png`; the first-pass `section3-storyboard-v4-shots-58-67`/`-68-73` sheets are stale for the changed shots. Builders: `tools/sheet-section3.py`, `tools/sheet-section3-fix.py`, `tools/section3-states.py` (its 69-state/71 parts are superseded).
- Known nits (awaiting Dominick's review): 59's lead looks forward more than down at the coin; 69-state text is smaller than before; shot 64 room angle differs a little from shot 9.
- Video assembly: not started, only on Dominick's word.

## EARLIER STATUS (Muse process update, 2026-11-10)
- **Sections 1 and 2 are DONE.** Section 1: 19 shots final. Section 2: 34 shots final (shots 31, 45, 55 cut; shot 54 carries VO-069 2nd half-071; shot 57 is the exact shot 54 frame; shots 51 and 53 approved as-is). Storyboards for Sections 1-2 done; shots 1-57 done.
- **Sections 3-6 (VO-074 onward) run on the NEW LENIENT PACING** (fewer images, multiple lines per image, every shot under 10 s, new image only when the beat changes; Chick-fil-A standard). Full rules and process rules are in `CLAUDE.md` ("Film #2 ... standing production rules") and summarized below.
- **The drafted 28-shot Section 3 map and its 26.00 quote are VOID** (they were drafted on the old dense pacing; the files live on branch `claude/laughing-lovelace-fnekay`, not here). Do not use them.
- **NEXT JOB (do not start until told):** re-map Section 3 (VO-074-104) under the new pacing and present the map + a NEW quote. Generate nothing until the map and quote are approved.

Standing rules: quote credit cost and wait for OK before any spend; Bram voice; gpt_image_2_5 16:9 2k medium = 1.00/image;
masters 1920x1080 PNG; every delivered file under 25 MB; storyboard sheets in v4 format (DISPLAYED in chat, not just committed); documents as PDF.
Process rules (full text in CLAUDE.md):
- Sections 3-6 pacing: fewer images, several lines per image, every shot under 10 s (a single line may exceed 10 s only when it carries the hold; prefer ONE free assembly state at the payoff; flag drag in the map, never silently add images). New image only on a true beat change. Grouped lines must fit the image's meaning. VO-095 (11.60 s) = ONE image, money figure as a free state at "between twenty and thirty million dollars."
- Consistency over creativity: screen vocabulary is locked. STREAM screen = his exact-face preview + white viewer-icon column + colored chat bars. COUNTER screen = person icon + number + colored name pills/gray bars (NO white icons).
- Checks inside the prompt: exact on-screen text whitelist, LIVE on/off per timeline, digit-legibility where blur is required, face anatomy (one eyebrow per eye, connected head outline).
- Preflight before any paid call: master attached, reference attached, live price confirmed (get_cost). Local composites first; model edits only when a composite can't do it, with a stated cost.
- One prompt per job with a hard spend cap; no re-rolls without Dominick's OK; a failed check = stop and report, never auto-retry.
- Repo: commit each approved file to this branch as approved; update STATE.md at the end of every chat.
- Review bar for Sections 3-6: cartoon-good passes; only meaning failures, wrong text, broken anatomy, or wrong screen design come back.

## 1. DONE
- **Section 1 (shots 1-20, no 7):** FINAL. Shots 11 and 16 swapped to the byte-exact approved finals (11 with smiles, 16 v3) on 2026-11-10,
  from Dominick's `section1-finals-for-claude.zip`; `section1/11.png` and `section1/16.png` are byte-identical to the zip. SWAP CONFIRMED.
- **Section 2 batch 21-30:** FINAL.
  - Accepted as delivered: 21, 22, 23, 24, 25, 26, 29.
  - 27 = REUSED Section 1 shot 1 (`section1/1.png`, thumbC, unedited). No section2/27 file; the first-delivery 27 is archived in `discarded/`.
  - 28 and 30 = re-rolled, **APPROVED by Dominick** (counter much bigger, digits unreadable). No open decision.
  - Shot 31 is CUT. VO-040 plays over shot 30; shot 30 = VO-039-040, 5.9 s, slow push at assembly. No renumbering. Section 2 = 36 shots.
- **Section 2 batch 32-40:** DONE and approved. Fix round applied (one edit each, edited region pasted back, rest byte-identical):
  33 LIVE box unlit (matches 32); 36 shocked open mouth + matching preview face; 38 and 39 monitor shows his stream preview with his exact face
  (calm closed-eyes smile / beaming open mouth); 40 rebuilt from new 39 (crop (500,180)-(1460,720), x2). 32, 34, 35, 37 unchanged.
- **Merge:** everything from `claude/dreamy-goodall-axrmtw` moved into this folder; approved masters replaced the stale first-delivery copies
  (23, 24, 25, 26, 28, 30, 33, 36, 38, 39, 40 in `section2/`). The dreamy-goodall branch no longer holds Film #2 files.
- Voiceover VO-001-195 (Bram, 630.78 s), Section 2 shots 21-57 generated earlier.

- **Section 2 batch 41-50 (2026-11-10):** DONE, 0 further credits.
  - Map: shot 45 CUT (no renumbering, file `section2-cut/45-CUT.png`); shot 44 = VO-056-057 (6.56 s); shot 46 = VO-058-059 (7.05 s); Section 2 = 35 shots. 42, 43, 48, 49, 50 approved as-is.
  - Shot 41 (local, free): genuine shot-36 chat column (icons + bars) cropped from 36's master and perspective-warped onto 41's monitor panel; inset to the screen's inner rim; everything outside the panel byte-identical. Checked against 36: same icon and bar design.
  - Shot 47 (one paid edit, 1.00, plus local fix): burst replaced by his stream preview (same overwhelmed face) + established chat streaking past; screen pasted back onto the old master; viewer icons 3 and 4 repainted from clean icons in the same column (local). Known nit left alone by instruction: icon 5 has a tiny speck near its right eye.
  - Spend this chat: 2.00 total (1.00 wasted on a 41 call submitted without its references, 1.00 on the 47 edit). 823.26 left.
  - Sheet: `storyboards/section2-storyboard-v4-shots-41-50.pdf` / `.png` (45 omitted; 44 and 46 show new VO). The old 41-50 JPG in `storyboards/` is now stale. Builder: `tools/sheet-41-50.py`.

- **Section 2 batch 50-57 (2026-11-10), local composites, 0 credits:**
  - Map: shot 55 CUT (file `section2-cut/55-CUT.png`, no renumbering); shot 54 = VO-069 (2nd half)-071 (~9.0 s); shot 53 = VO-069 (1st half) 4.8 s. Section 2 = 34 shots.
  - DONE (monitor screen only, rest byte-identical): 52 (stream screen from 41: his preview + genuine chat column, perspective-matched; the chat bars fade out on the right because the real screen is wider than 41's visible part), 56 (landscape replaced: his circular head from 56 on the dark preview + genuine chat column), 57 was composited (53's counter design on the dusk monitor) but is now SUPERSEDED: shot 57 = REUSED shot 54, see below.
  - CORRECTION to 41: my earlier composite painted the chat panel over the monitor's lower bezel band (about 30 px). Redone from the original master; the panel now stops at the screen's inner rim. Same design and method.
  - 51 and 53: APPROVED AS-IS by Dominick (no chat column, no layout change). The counter fills the screen, so the 49/50 chat column cannot fit without covering the 900,000. 50 unchanged. 54 (push-in of 53) also unchanged.
  - Shot 57 = REUSED shot 54 (`section2/54.png`, unedited; VO-073 plays over the same close-up). No section2/57 file (same as shot 27); the earlier composite is archived in `discarded/57-sunset-counter-composite-SUPERSEDED.png`.
  - Sheet: `storyboards/section2-storyboard-v4-shots-50-57.pdf` / `.png` (55 omitted). Builder: `tools/sheet-50-57.py`.

## 2. IN PROGRESS / NOT STARTED
- Sections 1-2: nothing open. (The old minor items, desk-standard drift and 42 tear / 48 eye / 52 room angle, are closed by Muse's "Sections 1 and 2 are DONE".)
- Section 3: generated (58-73), awaiting review. Sections 4 (Truth 2: The Power), 5 (Truth 3: The Catch), 6 (The Payoff): not started.
- Video assembly: not started, only on Dominick's word.

## 3. FILES (all paths under `film2-assets/` on branch `claude/happy-mccarthy-4tfabg`)
### Created or changed THIS session (exact paths)
Masters (1920x1080 PNG):
- `section2/41.png` — chat column from 36 composited (fixed version, panel stops at the inner rim)
- `section2/47.png` — his stream preview + overloaded chat, icons 3 and 4 repainted
- `section2/52.png` — stream screen composited onto the wide-shot monitor
- `section2/56.png` — his head on the dark preview + chat column
- Shot 57: NO file (reuses `section2/54.png`). Shots 51, 53, 54 unchanged, approved as-is.
Moved (cut shots): `section2-cut/45-CUT.png` (from section2/45.png), `section2-cut/55-CUT.png` (from section2/55.png).
Archived, do not use: `discarded/57-sunset-counter-composite-SUPERSEDED.png`, `discarded/47-candidate-failed-icons-SUPERSEDED.png`,
  `discarded/section3-dense-draft-VOID/SECTION3-MAP-VOID.txt`, `discarded/section3-dense-draft-VOID/section3-storyboard-map-VOID.pdf` (old 28-shot Section 3 map + 26.00 quote, VOID).
Storyboards (v4): `storyboards/section2-storyboard-v4-shots-41-50.pdf`, `.png`; `storyboards/section2-storyboard-v4-shots-50-57.pdf`, `.png` (45 and 55 omitted).
Records: `docs/SECTION2-MAP.txt` (updated), `docs/SCREEN-COMPOSITE-NOTES.txt` (recipes + spend log), `STATE.md` (this file), `../CLAUDE.md` (repo root; new Film #2 standing rules).
Tools: `tools/sheet-41-50.py`, `tools/sheet-50-57.py` (sheet builders), `tools/screen-composite-lib.py` (perspective warp + mask helpers).
Reusable asset: `assets/stream-screen-asset-640x360.png` (rectified stream screen: shot 41's preview + viewer-icon column + chat bars, extended to 16:9).
### Earlier files still valid
Section 2 approved masters in `section2/`:
- `23.png`, `24.png`, `25.png`, `26.png`, `28.png`, `30.png` — approved re-roll finals. `33.png`, `36.png`, `38.png`, `39.png`, `40.png` — approved fix-round masters.
- `42.png`-`44.png`, `46.png`, `48.png`-`50.png`, `21.png`, `22.png`, `29.png`, `32.png`, `34.png`, `35.png`, `37.png`, `51.png`, `53.png`, `54.png` — approved. Shot 27 = `section1/1.png` reused.
Section 1: `section1/` shots 1-6, 8-20 (11 and 16 byte-exact approved finals). Thumbnails `thumbnails/` (thumbC locked = shot 1). Voiceover `voiceover/` (VO-001..195, `script-locked.txt`, `timing-report.md`).
Storyboards earlier: `storyboards/section2-storyboard-v4-shots-21-30.pdf`/`.png`, `...-32-40.pdf`/`.png`. The `.jpg` sheets in `storyboards/` are stale (use the v4 PDFs).
Records earlier: `docs/section2-storyboard-map.pdf`, `README.md`. Other archive: `discarded/27-*`, `discarded/28-v1-superseded.png`, `discarded/30-v1-superseded.png`, `discarded/31-asm-v1-CUT.png`, `section2-cut/31-CUT.png`.
Older tools: `tools/sheet-21-30.py`, `tools/sheet-32-40.py`.

## 4. DECISIONS WAITING ON DOMINICK
- None open on Sections 1-2 (51 and 53 approved as-is; 57 = shot 54).
- Go-ahead needed to START the Section 3 re-map (VO-074-104) under the lenient pacing. After the map + new quote are presented, approval of both is needed before any generation or spend.

## 5. NEXT STEP (superseded: see CURRENT STATUS at the top; next is Section 4, shots 76-88, in a new chat)
1. Dominick says go, then: re-map Section 3 (VO-074-104) under the lenient pacing rules (fewer images, several lines per image, every shot under 10 s, VO-095 on ONE image with the money figure as a free state) and present the map + a NEW quote (preflight: master + reference attached, live price via get_cost). Generate nothing until both are approved.
2. Sections 4-6 follow the same pacing.
