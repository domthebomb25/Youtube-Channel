# STATE — Film #2 "POV: You Became the #1 Streamer Overnight." (long-form)

Last updated: 2026-11-10 · branch `claude/dreamy-goodall-axrmtw` · Higgsfield balance 825.26 credits
(838.26 at session start; spent 13.00 = 7.00 re-rolls 23–28/30 + 2.00 re-rolls 28/30 + 4.00 fix-round edits 33/36/38/39).

Standing rules are unchanged (see CLAUDE.md and the handoff): quote credit cost and wait for OK before any spend; Bram voice;
gpt_image_2_5 16:9 2k medium = 1.00/image; deliver 1920×1080; every file under 25 MB; storyboard sheets in the v4 format,
10 shots at a time; send images with display "render"; documents as PDF.

## 1. DONE

**Section 2, batch 21–30 — FINAL (decisions applied):**
- Accepted as delivered, do not touch: 21, 22, 23, 24, 25, 26, 29.
- 27 = REUSED Section 1 shot 1 (thumbC frame, byte-identical to `film2-assets/section1/1.png`). The re-rolled 27 is discarded.
- 28 and 30 re-rolled a second time (numbers much bigger, digits smeared until none can be named). Dominick's own legibility check on these two is still open (see section 4).
- Shot 31 is CUT. VO-040 ("Every time you look, it goes higher.") now plays over shot 30. Shot 30 = VO-039–040, 5.9 s
  (VO list sums to 5.82 s), slow push at assembly. No renumbering. Section 2 is now 36 shots. Do not rebuild 31.

**Section 2, batch 32–40 — DONE and approved:**
- Fix round applied, one edit each, edited region pasted back onto the master (everything else byte-identical):
  - 33: LIVE box now unlit, matches shot 32 (no red, no glow, no red cast on desk).
  - 36: shocked open mouth added; stream-preview face on the monitor is the same shocked face.
  - 38: monitor now shows his stream preview with his exact closed-eyes calm-smile face + chat column (landscape removed).
  - 39: monitor now shows his stream preview with his exact beaming open-mouth face + chat column.
- 40 rebuilt (free) from the new 39: crop (500,180)–(1460,720), scaled ×2 to 1920×1080.
- 32, 34, 35, 37 unchanged.
- Storyboard sheets: 21–30 and 32–40 built in v4 format (PDF + PNG).

**Earlier (from handoff):** voiceover VO-001–195 (Bram, 630.78 s); Section 1 shots 1–20 locked (shot 7 cut);
Section 2 shots 21–57 generated and delivered.

## 2. IN PROGRESS / NOT FINISHED
- **Section 1 swap (shots 11 and 16):** waiting for Dominick's `section1-finals-for-claude.zip` (byte-exact PNGs, 16 = v3).
  Then swap into the Section 1 masters and re-send them as two zips under 25 MB. Not started. Free.
- **Section 2 open issues from the handoff, still unresolved:**
  - Stray scenery on the monitor in shots 56 and 57 (38 is now fixed).
  - Desk-standard drift (monitor smaller/lower than shot 9) on 21, 27, 32, 34, 38, 41, 45, 55; unverified on 44, 47, 56, 57.
    Free fix = composite shot 9's desk in locally.
  - Minor: funnel shots now replaced (23–26 accepted); shot 42 shows a tear; shot 48 peeking eye; shot 52 uses a different room angle.
- **Section 2 shots 41–57:** the storyboard sheets for 41–50 and 51–57 exist only as the first-delivery JPGs on branch `claude/happy-mccarthy-4tfabg`
  (`film2-assets/storyboards/`). They have not been rebuilt in this session.
- **Sections 3 (Truth 1: The Money), 4 (Truth 2: The Power), 5 (Truth 3: The Catch), 6 (The Payoff):** not started.
  Needs the locked script lines and VO timings from Dominick, then a storyboard map + credit quote, and no generation until he approves.
- Video assembly: not started, only on Dominick's word.

## 3. FILES CREATED THIS SESSION (all committed on `claude/dreamy-goodall-axrmtw`)
Final masters, 1920×1080 PNG:
- `film2/section2-fix-round/33.png`, `36.png`, `38.png`, `39.png`, `40.png` — fix-round masters (33, 36, 38, 39 edited; 40 rebuilt).
- `film2/section2-rerolled-finals/23.png`, `24.png`, `25.png`, `26.png`, `28.png`, `30.png` — approved re-roll finals.
  The copies in `film2-assets/section2/` on the happy-mccarthy branch are FIRST-delivery versions; never assemble from those six.
- `film2/section2-rerolled-finals/27-REUSED-section1-shot1.png` — shot 27 (thumbC, unedited).

Storyboards (v4 format):
- `film2/storyboard-v4-shots-21-30.pdf` and `film2/sheets/storyboard-v4-shots-21-30.png`
- `film2/storyboard-v4-shots-32-40.pdf` and `film2/sheets/storyboard-v4-shots-32-40.png`

Records:
- `film2/SECTION2-MAP.txt` — change log + current Section 2 map (31 cut, 30 = VO-039–040).
- `STATE.md` — this file.

Superseded, kept only for the record (do not use):
- `film2/discarded/27-reroll-DISCARDED.png`, `28-v1-superseded.png`, `30-v1-superseded.png`, `31-asm-v1-CUT.png`

Tools (sheet builders; paths inside point at the session scratchpad and need adjusting):
- `film2/tools/sheet-21-30.py`, `film2/tools/sheet-32-40.py`

Not in the repo (cannot be):
- Higgsfield uploads for the fix round (32, 33, 36, 38, 39 as reference media) live only in the Higgsfield media library.

## 4. DECISIONS WAITING ON DOMINICK
1. Shots 28 and 30: does the new counter pass his legibility check (no single digit nameable)? If not, a 3rd attempt = new spend (1.00 each) and needs his OK.
2. Fix shots 56 and 57 (stray scenery on the monitor)? Local composite or re-roll at 1.00 each?
3. Apply the free desk-standard composite (shot 9's desk) to the drift shots listed in section 2?
4. Minor items (42 tear, 48 peeking eye, 52 room angle): fix or leave?
5. Where should the new masters live long-term? They are on `claude/dreamy-goodall-axrmtw` under `film2/`. The reference set `film2-assets/` is on
   `claude/happy-mccarthy-4tfabg`. Say if he wants them moved/merged there.
6. Re-send `section1-finals-for-claude.zip`.
7. Paste the locked script + VO timings for Sections 3–6 when he wants those storyboards.

## 5. NEXT STEP
1. When the zip lands: swap Section 1 shots 11 and 16 into the Section 1 masters (free) and re-send as two zips.
2. On Dominick's call on items 2–4 above: fix Section 2 shots 41–57 (quote cost first for any re-roll).
3. Then Section 3 (Truth 1: The Money): storyboard map + credit quote first, generate nothing until approved.
