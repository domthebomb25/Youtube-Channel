# STATE — Film #2 "POV: You Became the #1 Streamer Overnight." (long-form)

Single source of truth: branch `claude/happy-mccarthy-4tfabg`, folder `film2-assets/` (this folder). Updated 2026-11-10 (CLOSE-OUT of the Section 6 chat).

## FILM RENDERED (2026-11-11): `render/film2-streamer-FINAL.mp4`
- Rendered locally in this chat from the repo (0 credits spent by this chat; balance was 749.71 when the render started): 1920x1080, 30 fps cfr, H.264 High yuv420p (bt709), CRF 18, AAC-LC 192 kbps stereo 48 kHz, ffmpeg CONCAT FILTER (never -c copy), 117 shots + 5 state splits = 122 segments, 18,939 frames. **Duration 631.300 s**, size 82,857,437 bytes (79.0 MB, committed; under 100 MB).
- QA (all gates PASS, numbers in `render/QA-REPORT.txt`): full linear decode OK (18,939 frames, no decoder errors); dual-mono L/R correlation min 0.99973 over 64 ten-second windows; quietest/loudest window RMS -19.8 / -16.3 dBFS (none silent); integrated loudness -14.1 LUFS, true peak -1.1 dBTP, LRA 3.6 LU; the 8 required frames verified (shot 9 50,000 / 100,000, shot 10 1,000 GIFTED SUBS, shot 35 LIVE bright, shot 50 900,000, shot 69 figure after trigger, shot 85 flood after trigger, final frame = shot 121 plain monitor back).
- Built locally (no file existed): shot 9 counter flips and shot 10 banner flip (`render/states/`); cues from audio analysis: 69-state at 7.85 s into VO-095, 85-state at 8.01 s into VO-124. Existing state files used for 35, 40, 50, 54, 69, 85.
- Deviations (in the QA report): loudnorm true-peak target -1.5 (a -1.0 target measured -0.7 dBTP after AAC and failed the gate; the first render was never delivered); shot 40 follows the manifest (39 on VO-051, 40 push-in on VO-052); total is 631.30 s because per-line timing-report durations are rounded (exact VO total 631.22 s).
- Reproducible: `tools/render-film2/` (01..04 scripts + README), `render/build-info/`. Any re-render gets a NEW filename (`film2-streamer-FINAL-v2.mp4`); never overwrite.
- BALANCE NOTE: the balance now reads **741.96**. This chat made NO paid calls during the render; the transaction log shows 7 x 0.25 GPT Image 2.5 (01:02 UTC) + 1 x 6.00 Kling v3.0 (01:10 UTC) = 7.75 charged by another session/tool on the same account (Shorts-recipe prices), exactly 749.71 -> 741.96.
- NEXT: Dominick's review of the final film.

## ASSEMBLY HANDOFF (2026-11-11): BUNDLE REBUILT, VERIFIED AND HANDED OFF FOR RENDERING
- All six `assembly/sectionN-assembly.zip` rebuilt from the current canonical state and verified against `assembly/MANIFEST.txt` with `tools/verify-assembly.py`: **117 masters, 194 played VO files**, each file byte-identical to the repo (S1 19/27, S2 34/46, S3 18/31 + 069-state, S4 13/25 + 085-state, S5 23/47, S6 10/18). Fixes inside: composited 32-35, fixed 93, accepted 101, awake 113, fixed 121; new VO-178, VO-179, VO-195; ORIGINAL VO-193. No OLD/UNUSED take and no VO-194 in any zip. (35 is a numbered master in section 2; 69-state and 85-state are separate state files.) Zip contents were byte-identical to the already-committed zips, so those were not re-pushed.
- Sent to Dominick as attachments (zips 1-6, then MANIFEST.txt) for Muse to assemble and render locally. **Balance 749.71 (unchanged; 0 credits spent).**
- NEXT: Muse assembles/renders; nothing else open.

## FINAL-REVIEW UPDATES (2026-11-11, this chat) — Job log
### SHOT 113 REGENERATED AWAKE (1.00)
- New line VO-179 ("And you woke up...") needs him awake: shot 113 regenerated once (gpt_image_2_5 16:9 2k medium, 1.00, price confirmed via get_cost, refs = old 113 + stream-screen asset, job 2c6a463d-29c2-4851-9f6d-6d4ec75f16b8). He is awake (eyes open, raised brows, crown), the monitor preview shows his awake face (locked stream design), bright morning light. Self-check passed (flag: wide open-mouth smile, not "small"). Old image archived `discarded/113-original.png`. Duration unchanged 3.5 s. Map, sheets (full-film 19, section 6 sheet 1) and `assembly/section6-assembly.zip` rebuilt.
- **Balance 749.71 credits** (754.81 at the end of the last job; this chat's spend = 1.00). NOTE: the balance read 750.71 BEFORE this generation, i.e. 4.10 lower than 754.81: the transaction log shows eight 0.25 GPT Image 2.5 charges and three Voiceover charges at 00:32-00:33 UTC that this chat did not make (another session/tool spending on the same account). Expected 753.81; actual 749.71.

### JOB 3 DONE: end-line change (0.15)
- Ending is now VO-193 "You became the #1 streamer overnight." (original take, untouched) + NEW VO-195 "Staying at #1 is just as hard." VO-194 ("Staying there?") is RETIRED: `voiceover/VO-194-UNUSED-staying-there.mp3` (never assemble; not counted). Old VO-195 = `voiceover/VO-195-OLD-real-job.mp3`. New `voiceover/VO-195.mp3` = 2.769 s (2.77); cost 0.15; **balance 754.81**. Shot 121 = 2.69 + 2.77 = 5.46 s. Film VO total **631.22 s** (194 played files). Shot 121's image unchanged. Script, timing report, SECTION6 map, README, MANIFEST, full-film sheet 21, section 6 sheets and `assembly/section6-assembly.zip` rebuilt (zip has original VO-193 + new VO-178/179/195, no VO-194).

### JOB 2 DONE: VO-179 line change (0.15)
- VO-179 is now "And you woke up as the biggest show on Earth." (was "You went to sleep as the biggest show on Earth."). Bram, same route/settings as the VO-178 change; cost 0.15; **balance 754.96**. Old file `voiceover/VO-179-OLD-went-to-sleep.mp3` (3.71 s); new `voiceover/VO-179.mp3` = 3.474 s (3.47). Shot 113 = 3.47 s (was 3.71). Film VO total 631.17 s (10:31.17). Shot 113's image unchanged. `script-locked.txt`, timing report (row + total), `docs/SECTION6-MAP.txt`, README, MANIFEST (regenerated), sheet 19 updated. Section 6 zip is rebuilt in Job 3.

### JOB 1 DONE: shots 32-35 monitor fix (local composite, 0.00)
- The dead/black desk monitor in `section2/32.png`, `33.png`, `34.png`, `35.png` now shows shot 28's dashboard screen (person icon, motion-blurred UNREADABLE number box, graph off-frame to the right), perspective-warped to each monitor's inner rim, glow toned for the morning light. 28's face occluder was patched from the screen's own dark margin first. Number stays blurred (no sharpening, no invented digits).
- Only the screen area changed in each shot (verified by pixel diff: 0 changed pixels outside the screen polygon). LIVE states unchanged (unlit 32, 33, 34; bright 35). 35 = same composite as 34 on 35's own original; 34 vs 35 differ only at the LIVE light (and its glow on the bezel corner, max 15 levels).
- Originals archived: `discarded/32-original.png` ... `35-original.png`. Tool: `tools/fix-shots-32-35.py`. Full-film sheet 6 and `assembly/section2-assembly.zip` rebuilt with the fixed masters.
- Notes: the monitor's right edge is off-frame in 32, 33, 34 and 35, so the right part of the screen (graph) is not visible; the quad's off-frame corners were extrapolated.

## CURRENT STATUS — FULL-FILM STORYBOARD + ASSEMBLY BUNDLE BUILT (2026-11-10)
### DONE (0.00 spent; no generations, no re-records)
- **FULL-FILM STORYBOARD BUILT, awaiting Dominick's final review before assembly.** All 117 shots in playing order (7, 31, 45, 55 cut), final masters (fixed 93 and 121, accepted 101), final voice timings (VO-178 = 2.12 s, shot 112 = 7.6 s, quote "You went to sleep as nobody."). 122 tiles = 117 shots + 5 free state tiles (9 -> 50,000, 9 -> 100,000, 10 -> 1,000 GIFTED SUBS, 69-state, 85-state), 6 tiles per sheet, **21 sheets**: `storyboards/full-film/fullfilm-storyboard-v4-sheet-01-of-21.png` ... `-21-of-21.png`. Builders: `tools/fullfilm-data.py`, `tools/sheet-fullfilm.py`, `tools/fullfilm-crosscheck.py`.
- Shots 18, 35, 40, 50 and 54 are NUMBERED shots whose own file is an assembly state; they play in their place and carry the ASSEMBLY STATE label (yellow frame), no duplicate tiles.
- **ASSEMBLY HANDOFF BUNDLE built:** `assembly/section1-assembly.zip` ... `section6-assembly.zip` + `assembly/MANIFEST.txt` (shot, image, VO files, duration, state + trigger). Zips hold masters in shot order (`masters/NNN.png`), that section's VO mp3s, and the state files (069-state in section 3, 085-state in section 4). Builder `tools/build-assembly.py`.
- Balance unchanged: **755.11 credits.**
### FLAGS FROM THE CROSS-CHECK (nothing silently fixed)
- Shots 9 and 10 state flips (50,000, 100,000, 1,000 GIFTED SUBS) have NO files in the repo; the tiles show the base image with a badge, and the manifest says "text swap at assembly". Nothing generated.
- `docs/SECTION2-MAP.txt` MAP block is stale vs its own change log (it lists 44 = VO-056, 45 = VO-057-058, 46 = VO-059); the change log (44 = VO-056-057, 45 CUT, 46 = VO-058-059) is used, as on the Section 2 sheets.
- `docs/SECTION3-MAP.txt` labels for 71/72/73 ("Every viewer pays." etc.) do not match locked VO-098/099/100 text; the VO ranges match. Tiles use the locked lines.
- Durations (timing report vs map): every shot is within 0.15 s; the two largest: shot 30 = 5.82 s vs map 5.9 (map rounds up for the push), shot 59 = 8.21 s vs map 8.1. Shot 69 = 11.65 s (map 11.6). Per-row timing-report sum is 631.48 s vs exact 631.41 s (row rounding).
- Zip sizes exceed the 25 MB standing limit except section 6 (S1 41.2, S2 75.7, S3 36.2, S4 29.3, S5 49.4, S6 22.8 MB) because the masters are PNG; they are repo files under GitHub's 100 MB cap, not file cards.
### NEXT STEP
- Dominick's final review of the 21 sheets; then assembly (Muse, locally, from the zips).

## EARLIER STATUS — CLOSE-OUT OF THE SECTION 6 CHAT (2026-11-10)
### DONE
- **ALL 117 SHOTS OF THE FILM ARE NOW GENERATED.** Section 6 (The Payoff) = shots 112-121 (VO-177-195), generated, AWAITING REVIEW. Totals: S1 19, S2 34, S3 18, S4 13, S5 23, S6 10 = 117.
- Section 6 spend: exactly 10.00 (10 x gpt_image_2_5 16:9 2k medium at 1.00; live price confirmed 1.00 via get_cost first). No re-rolls. Two submissions (112, 121) were rejected with a 429 rate limit before any job existed (balance showed only 8.00 charged), and were resubmitted unchanged.
- **Higgsfield balance: 755.11 credits** after Fix 2 (755.26 after the shots; 765.26 at the start of the chat).
- Masters: `section6/112.png`-`121.png` (1920x1080). Map: `docs/SECTION6-MAP.txt` (job ids, self-check, flags). Storyboards (v4): `storyboards/section6-storyboard-v4-shots-112-117` and `-118-121` (.png and .pdf); builder `tools/sheet-section6.py`.
- Self-check passed on all ten (whitelist text = only the locked #1 and LIVE props, STREAM screen only on 113/121, gold tie = lead only, one brow per eye, LIVE bright on 113/121). Flags in the map (116 smug smile, 121 determined rather than calm, 118 lead seen from behind, 119 challenger missing one brow).
- Script wording: the sheets use the LOCKED lines; the shot brief paraphrased some (e.g. VO-179 locked = "biggest show on Earth").
### COMBINED FIX ROUND (same chat): VO-178 line change (0.15) + shot 121 monitor back (local, 0.00)
- Total fix-round spend 0.15. **Balance 755.11 credits (confirmed).** No new generations.
- Shot 121: the stream screen on the monitor's back panel was removed and repainted as a plain dark monitor back (local edit, `tools/fix121-monitor-back.py`; original at `discarded/121-original.png`; outside the panel the file is pixel-identical). Sheet 2 (118-121) rebuilt.
- Housekeeping: Bram voice_id now in `CLAUDE.md`; Section 6 runtime corrected to 53.6 s in `docs/SECTION6-MAP.txt`.
- Details: `docs/SECTION6-MAP.txt` (combined fix-round entry at the bottom).
### FIX 2 (same chat): VO-178 LINE CHANGE
- Approved change to the locked script: VO-178 is now "You went to sleep as nobody." (was "You woke up as nobody."). `voiceover/script-locked.txt`, `voiceover/timing-report.md` (row + total 631.41 s / 10:31.41), `README.md`, `docs/SECTION6-MAP.txt` and sheet 1 updated.
- Re-recorded with Bram (text2speech_v2 / elevenlabs / preset 549ff70a-3ee7-4f04-a4d9-89a24fab7709), cost 0.15, one take. Old file kept as `voiceover/VO-178-OLD-woke-up.mp3` (1.49 s). New `voiceover/VO-178.mp3` = 2.12 s (+0.63). Shot 112 = 5.49 + 2.12 = 7.60 s (was 7.0). Section 6 runtime 52.6 s.
- **Higgsfield balance: 755.11 credits.** (755.26 - 0.15.) Shot 112's picture unchanged; flag if "just woken" no longer fits the new words.
- The "shot 121 monitor fix" mentioned in the instruction never reached this chat: nothing run (0.00).
### IN PROGRESS
- Nothing. Section 6 awaits Dominick's review (only meaning failures, wrong text, broken anatomy or wrong screen design come back for fixes).
### NEXT STEP
- Dominick reviews Section 6 (and any standing flags). Fixes only on his word, with a stated cost. Then video assembly (not started; only on Dominick's word).

## EARLIER STATUS (close-out of the Section 5 chat, 2026-11-10)
### DONE
- **Sections 1-5 are COMPLETE: 107 shots** (S1 19, S2 34, S3 18, S4 13, S5 23; shot numbers run 1-111 because of the cut/reused numbers in S1-S2). Section 5 = shots 89-111 (VO-130-176), fix round included.
- **Higgsfield balance: 765.26 credits.** (789.26 at the start; 23.00 first pass, exactly 1.00 each; +1.00 for the 101 regeneration; 93 local, 0.00.) Live price re-confirmed 1.00 before every paid call.
- Section 5 fix round: **93** = local edit, 0.00 (the two scattered red Xs on Ninja's wall calendar erased and redrawn as TWO CONSECUTIVE squares in one row; everything else byte-identical). **101** = regenerated once, 1.00, ACCEPTED AS-IS by Dominick: five ghost gift boxes + one solid box, a plain gray-hoodie viewer holding up a coin (no re-roll; his smile stays). The old theater-seats 101 is archived.
- Standing flags (cartoon-good, accepted): 105 calendar grid has 24 squares and 108 has 20 (not 30); 94 Ninja's right eyebrow is tight to the head outline. Full list at the bottom of `docs/SECTION5-MAP.txt`.
- CHARACTER COLOR LOCK unchanged: Ludwig GREEN, Ninja BLUE; gold tie = the lead only. 102-103 record holder = unnamed generic gray-hoodie stickman; 106 Kai Cenat = plain generic stickman, label only.
- Section 5 storyboards (v4, up to date): `storyboards/section5-storyboard-v4-shots-89-94`, `-95-100`, `-101-106`, `-107-111` (.png and .pdf). Note: the displayed-in-chat requirement could not be met with inline images in this chat (my tools can only send file cards); the four PNGs were sent as file cards.
### IN PROGRESS
- Nothing.
### EVERY FILE CREATED OR CHANGED IN THIS CHAT (paths under `film2-assets/`)
- Masters: `section5/89.png` ... `section5/111.png` (23 files, 1920x1080). `section5/93.png` = locally edited. `section5/101.png` = regenerated and accepted.
- Archived originals: `discarded/93-original.png` (scattered-X version), `discarded/101-original.png` (theater-seats version).
- Records: `docs/SECTION5-MAP.txt` (new), `STATE.md` (this file).
- Storyboards: `storyboards/section5-storyboard-v4-shots-89-94.png`/`.pdf`, `storyboards/section5-storyboard-v4-shots-95-100.png`/`.pdf`, `storyboards/section5-storyboard-v4-shots-101-106.png`/`.pdf`, `storyboards/section5-storyboard-v4-shots-107-111.png`/`.pdf`.
- Tools: `tools/sheet-section5.py` (sheet builder), `tools/crop-section5.py` (raw 2688x1520 -> 16:9 1920x1080 masters), `tools/fix93-calendar.py` (shot 93 local edit; reads `discarded/93-original.png`, writes `section5/93.png`).
- Not in the repo: the raw 2688x1520 Higgsfield outputs (kept only in the session scratchpad). Generated assets live on Higgsfield by job id; the job ids are in `docs/SECTION5-MAP.txt`.
### DECISIONS STILL WAITING
- None for Section 5.
### NEXT STEP
- **Section 6 (The Payoff), shots 112-121 (VO-177 onward, "So that is what it really means...", to the end of the film at VO-195). It runs in a NEW chat, from the map in Muse's message (that map is NOT stored in this repo).** Start of that chat: read `CLAUDE.md` and this file, give production standing, then preflight (references attached, live price 1.00 via get_cost; stop and report if not); one generation per shot, no re-rolls without an OK, quote the credit cost and wait for OK before spending. Useful references: shot 9 (room + style), shot 75 (dusk room), stream-screen asset `assets/stream-screen-asset-640x360.png`, shot 50 or 99 (counter screen), shots 90 and 109 (staircase/throne), shot 100 (gift box).

## EARLIER STATUS (close-out of the Section 4 chat, 2026-11-10)


- **Sections 1-4 are DONE: 84 shots** (S1 19, S2 34, S3 18 = shots 58-75, S4 13 = shots 76-88 plus its fix rounds). Files: `section4/76.png`-`88.png` + `section4/85-state.png`. Map: `docs/SECTION4-MAP.txt`. Committed through the Section 4 fix rounds.
- **Higgsfield balance: 789.26 credits.** (803.26 at the start of Section 4; 13.00 generation + 1.00 fix-round edit on 86; everything else local.)
- **FINAL, matter closed:** `section4/85-state.png` (tiny streamer's face repainted quietly happy, closed smile + soft brows, to match shot 88's suited figure; local, 0.00; `tools/section4-states.py` step 5). `section4/86.png` = fix-round edit (happy, hands on hips, no bubble).
- **STANDING RULINGS:** 78's phone icons and 81's blue-shirt star stand as delivered (no fixes). 76/82 eyebrow nit stands. Shot 88 ends at VO-129 (2.7 s); Section 4 runtime 82.7 s. **VO-130-131 ("This leads you now to the final hidden truth. But.") open Section 5 as shot 89.**
- CHARACTER COLOR LOCK unchanged: Ludwig GREEN, Ninja BLUE; gold tie = the lead only.
- Storyboards: `storyboards/section4-storyboard-v4-shots-76-81`, `-82-87`, `-88-and-85-state` (.pdf/.png) + `section4-fix-tile-*.png`. Builders `tools/sheet-section4.py`, `tools/section4-states.py`.
- **NEXT JOB: Section 5 (Truth 3: The Catch), shots 89-111, map approved, 23 generations, expected cost 23.00 (expected balance after: 766.26). It will run in a NEW chat; it was NOT started here.** Preflight as always (references attached, live price 1.00, stop and report if not); one generation per shot, no re-rolls without an OK. Section 6 (The Payoff) after.

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
- Voiceover VO-001-195 (Bram, 631.41 s after the VO-178 re-record), Section 2 shots 21-57 generated earlier.

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
