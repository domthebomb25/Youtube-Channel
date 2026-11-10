# STATE — Film #2 "POV: You Became the #1 Streamer Overnight." (long-form)

Single source of truth: branch `claude/happy-mccarthy-4tfabg`, folder `film2-assets/` (this folder). Updated 2026-11-10.
Higgsfield balance: 823.26 credits (825.26 before the 41-50 batch chat; that chat spent 2.00 on shot 41 and 47 edits, neither delivered, see section 2).

Standing rules (unchanged): quote credit cost and wait for OK before any spend; Bram voice; gpt_image_2_5 16:9 2k medium = 1.00/image;
masters 1920x1080 PNG; every delivered file under 25 MB; storyboard sheets in v4 format, 10 shots at a time; documents as PDF.

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

## 2. IN PROGRESS / NOT STARTED
- **Section 2 batch 41-50 (2026-11-10):** map updated, edits NOT delivered.
  - Map: shot 45 CUT (no renumbering, file now `section2-cut/45-CUT.png`); shot 44 = VO-056-057; shot 46 = VO-058-059; Section 2 = 35 shots.
    42, 43, 48, 49, 50 approved as-is.
  - Shot 41 edit (chat -> established chat design from 36/38/39): NOT done. The one paid call was submitted without its reference images (my error), so the result was discarded. 1.00 lost.
  - Shot 47 edit (burst -> his stream preview + overloaded chat): one paid edit run, screen paste-back clean, but FAILED the check: viewer icon 3 is a malformed double blob and icon 4 has glitched eyes. Not delivered; `section2/47.png` is still the old master. Candidate kept outside the repo.
  - Needs Dominick's decision: OK for further credits (1.00 per edit) to redo 41 and re-run 47, or fix 47's two icons locally (no spend). The 2.00 approved was fully used.
  - Rebuilt 41-50 sheet NOT built (waits for the final 41 and 47 masters).
- **Shots 56 and 57** (stray scenery on the monitor): DEFERRED. No action, no spend. Belongs to the 51-57 batch chat after Muse's audit.
- Section 2 shots 41-55 and the remaining open items from the first bundle (desk-standard drift on 21, 27, 32, 34, 38, 41, 45, 55 was not
  re-checked this session; minor: 42 tear, 48 peeking eye, 52 room angle) are for the 41-57 batch chats.
- Sections 3 (Truth 1: The Money), 4 (Truth 2: The Power), 5 (Truth 3: The Catch), 6 (The Payoff): not started.
- Video assembly: not started, only on Dominick's word.

## 3. FILES (all paths under `film2-assets/`)
Section 2 approved masters, 1920x1080 PNG, in `section2/`:
- `23.png`, `24.png`, `25.png`, `26.png`, `28.png`, `30.png` — approved re-roll finals.
- `33.png`, `36.png`, `38.png`, `39.png`, `40.png` — approved fix-round masters.
- `21.png`, `22.png`, `29.png`, `32.png`, `34.png`, `35.png`, `37.png`, `41.png`-`57.png` — as first delivered (still valid; 41-57 not re-reviewed here).
Section 1: `section1/11.png`, `section1/16.png` — byte-exact approved finals (replaced old versions). `section1/1.png` = shot 1 = thumbC = Section 2 shot 27.
Storyboards (v4 format): `storyboards/section2-storyboard-v4-shots-21-30.pdf` / `.png`, `storyboards/section2-storyboard-v4-shots-32-40.pdf` / `.png`.
  The older `.jpg` sheets in `storyboards/` for Section 1 shots 11-20 and Section 2 shots 21-30 and 31-40 are stale; shots 41-50 and 51-57 JPGs are current.
Records: `docs/SECTION2-MAP.txt` (change log + map), `docs/section2-storyboard-map.pdf` (original map), `STATE.md` (this file), `README.md`.
Archive, do not use: `discarded/27-first-delivery-STALE.png`, `discarded/27-reroll-DISCARDED.png`, `discarded/28-v1-superseded.png`,
  `discarded/30-v1-superseded.png`, `discarded/31-asm-v1-CUT.png`; also `section2-cut/31-CUT.png`.
Tools: `tools/sheet-21-30.py`, `tools/sheet-32-40.py` (sheet builders; inner paths point at a scratch folder).

## 4. DECISIONS WAITING ON DOMINICK
None open for this branch. (28/30 approved; 56/57 deferred to the 51-57 chat.)
For later: paste the locked script lines + VO timings for Sections 3-6 when he wants those storyboards.

## 5. NEXT STEP
0. Finish 41 and 47 (see section 2), then rebuild the 41-50 sheet (45 omitted, 44 and 46 with new VO).
1. 51-57 batch chat (after Muse's audit): decide 56 and 57, and the desk-drift / minor items for 41-57 (quote cost before any re-roll).
2. Then Section 3 (Truth 1: The Money): storyboard map + credit quote first, generate nothing until Dominick approves.
