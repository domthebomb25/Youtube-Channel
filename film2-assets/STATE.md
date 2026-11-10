# STATE — Film #2 "POV: You Became the #1 Streamer Overnight." (long-form)

Single source of truth: branch `claude/happy-mccarthy-4tfabg`, folder `film2-assets/` (this folder). Updated 2026-11-10.
Higgsfield balance: 823.26 credits (825.26 before the 41-50 batch chat, which spent 2.00; see section 1).

Standing rules (unchanged, plus preflight): before ANY paid call, confirm (1) master attached, (2) reference attached, (3) live price confirmed (get_cost). Local/free fixes first when possible.
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

- **Section 2 batch 41-50 (2026-11-10):** DONE, 0 further credits.
  - Map: shot 45 CUT (no renumbering, file `section2-cut/45-CUT.png`); shot 44 = VO-056-057 (6.56 s); shot 46 = VO-058-059 (7.05 s); Section 2 = 35 shots. 42, 43, 48, 49, 50 approved as-is.
  - Shot 41 (local, free): genuine shot-36 chat column (icons + bars) cropped from 36's master and perspective-warped onto 41's monitor panel; inset to the screen's inner rim; everything outside the panel byte-identical. Checked against 36: same icon and bar design.
  - Shot 47 (one paid edit, 1.00, plus local fix): burst replaced by his stream preview (same overwhelmed face) + established chat streaking past; screen pasted back onto the old master; viewer icons 3 and 4 repainted from clean icons in the same column (local). Known nit left alone by instruction: icon 5 has a tiny speck near its right eye.
  - Spend this chat: 2.00 total (1.00 wasted on a 41 call submitted without its references, 1.00 on the 47 edit). 823.26 left.
  - Sheet: `storyboards/section2-storyboard-v4-shots-41-50.pdf` / `.png` (45 omitted; 44 and 46 show new VO). The old 41-50 JPG in `storyboards/` is now stale. Builder: `tools/sheet-41-50.py`.

- **Section 2 batch 50-57 (2026-11-10), local composites, 0 credits:**
  - Map: shot 55 CUT (file `section2-cut/55-CUT.png`, no renumbering); shot 54 = VO-069 (2nd half)-071 (~9.0 s); shot 53 = VO-069 (1st half) 4.8 s. Section 2 = 34 shots.
  - DONE (monitor screen only, rest byte-identical): 52 (stream screen from 41: his preview + genuine chat column, perspective-matched; the chat bars fade out on the right because the real screen is wider than 41's visible part), 56 (landscape replaced: his circular head from 56 on the dark preview + genuine chat column), 57 (sunset replaced by 53's counter design: person icon, 900,000, the one blurred line; darkened for dusk).
  - CORRECTION to 41: my earlier composite painted the chat panel over the monitor's lower bezel band (about 30 px). Redone from the original master; the panel now stops at the screen's inner rim. Same design and method.
  - NOT DONE: 51 and 53 (add chat column). The counter (icon + 900,000) fills the screen; the 49/50 chat column starts about 305 px into the screen, so it would sit on top of the 900,000. 50 stays unchanged. Needs Dominick's decision (section 4).
  - Sheet: `storyboards/section2-storyboard-v4-shots-50-57.pdf` / `.png` (55 omitted). Builder: `tools/sheet-50-57.py`.

## 2. IN PROGRESS / NOT STARTED
- Section 2 shots 51 and 53 and the remaining open items from the first bundle (desk-standard drift on 21, 27, 32, 34, 38, 41, 45, 55 was not
  re-checked this session; minor: 42 tear, 48 peeking eye, 52 room angle) are for the 41-57 batch chats.
- Sections 3 (Truth 1: The Money), 4 (Truth 2: The Power), 5 (Truth 3: The Catch), 6 (The Payoff): not started.
- Video assembly: not started, only on Dominick's word.

## 3. FILES (all paths under `film2-assets/`)
Section 2 approved masters, 1920x1080 PNG, in `section2/`:
- `23.png`, `24.png`, `25.png`, `26.png`, `28.png`, `30.png` — approved re-roll finals.
- `33.png`, `36.png`, `38.png`, `39.png`, `40.png` — approved fix-round masters.
- `41.png`, `47.png` — fixed masters (2026-11-10). `42.png`-`44.png`, `46.png`, `48.png`-`50.png` approved (44/46 new VO only).
- `21.png`, `22.png`, `29.png`, `32.png`, `34.png`, `35.png`, `37.png`, `51.png`, `53.png`, `54.png` — as first delivered (valid; 51 and 53 pending decision). `52.png`, `56.png`, `57.png` — screen composites (2026-11-10).
Section 1: `section1/11.png`, `section1/16.png` — byte-exact approved finals (replaced old versions). `section1/1.png` = shot 1 = thumbC = Section 2 shot 27.
Storyboards (v4 format): `storyboards/section2-storyboard-v4-shots-21-30.pdf` / `.png`, `storyboards/section2-storyboard-v4-shots-32-40.pdf` / `.png`.
  The older `.jpg` sheets in `storyboards/` for Section 1 shots 11-20 and Section 2 shots 21-30, 31-40 and 41-50 and 51-57 are stale (use the v4 PDFs).
Records: `docs/SECTION2-MAP.txt` (change log + map), `docs/section2-storyboard-map.pdf` (original map), `STATE.md` (this file), `README.md`.
Archive, do not use: `discarded/27-first-delivery-STALE.png`, `discarded/27-reroll-DISCARDED.png`, `discarded/28-v1-superseded.png`,
  `discarded/30-v1-superseded.png`, `discarded/31-asm-v1-CUT.png`; also `section2-cut/31-CUT.png`.
Tools: `tools/sheet-21-30.py`, `tools/sheet-32-40.py` (sheet builders; inner paths point at a scratch folder).

## 4. DECISIONS WAITING ON DOMINICK
- Shots 51 and 53 (chat column on the counter screen): pick one. (A) Thin sliver: chat column at the far right edge (~50 px visible), counter untouched. (B) Rebuild the 49/50 layout on these monitors: counter shrinks to 50's size on the left, chat on the right (loses the zoomed-in look). (C) Leave 51 and 53 as they are. Both are free, local.
- Note: the 49/50 chat is colored name pills + gray bars (no white icons); the white viewer icons are the 36/41 stream-screen chat. I would use the 49/50 version for 51 and 53 unless told otherwise.
For later: paste the locked script lines + VO timings for Sections 3-6 when he wants those storyboards.

## 5. NEXT STEP
1. Decide 51 and 53 (section 4). Then the desk-drift / minor items for the batch (quote cost before any re-roll).
2. Then Section 3 (Truth 1: The Money): storyboard map + credit quote first, generate nothing until Dominick approves.
