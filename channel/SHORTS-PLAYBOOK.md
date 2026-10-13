# Shorts playbook — read this first in every new chat

Written Oct 10 2026 from the first long chat. A new chat has NO memory of that chat; this file is the memory.

## Goal
**6 YouTube Shorts per day for 30 days (180 total).** The user opens a NEW chat each day. Channel: The Business Stick HQ
(@TheBusinessStickHQ). Shorts-only strategy (no long-form for now). Aim: grow + monetize (1,000 subs + 10M Shorts views/90 days, or 500 subs + 3M for the lower tier).
Made so far: Blockbuster, McDonald's ice cream machine, LEGO tires (folders under `videos/`), plus Day 01: Starbucks/Moby Dick, Bubble Wrap, Kleenex, Mountain Dew (folders under `shorts/day01/`). Costco long video exists (use as "Related video" on every YouTube Short).

## User rules (non-negotiable)
- **Quote the credit cost and wait for OK before spending Higgsfield credits** (also in CLAUDE.md). Check `balance` at the start of each day.
- Every posting instruction must include **every setting in `channel/POSTING-SETTINGS.md`** (AI label ON, Identify similar products OFF, Trial reel OFF, Related video on every Short, etc.). Simple, step-by-step, iPhone first.
- Hooks start from `channel/HOOK-TEMPLATES.md`. Rotate them; don't repeat the same hook two videos in a row.
- **No music in the video** (user decided). **No end text** unless asked. No emojis in the big hook text unless asked.
- User prefers PDFs over .md for documents they read.
- Facts must be **verified with sources** (WebSearch) before scripting; never claim unverified things; keep honest caveats in the script. Put 1-2 source links at the bottom of the YouTube description only.
- Show the user **every image (storyboard sheet) before rendering**, and the hook clip result. They catch real problems (see QA list).
- Don't open PRs unless asked. Commit + push small text files at the end of each day (a stop hook complains about uncommitted files).

## Format of one Short (what works)
- 45-50 s, 1080x1920, voice Benji, 14-15 stickman images (new picture every 2-4 s), word-by-word yellow captions, big top text on key beats, a 4 s animated hook.
- Story formats: "You're the company" (viewer becomes the CEO, problem, would-you-do-it, reveal company name at end) and "Sounds dumb until it's genius" (weird fact -> real reason).
- Topic pool: `channel/SHORTS-TOPICS.md` (~29 unused ideas). The founder legends (FedEx, Kodak, Airbnb, Nokia, KFC, Nintendo, Play-Doh) are overused; prefer everyday brands, product-design secrets, marketing tricks, surprising numbers. Need ~150 more topics over the 30 days; research them (WebSearch; vidIQ if credits).
- Quality bar for monetization review: every Short = original script, original visuals, different story. Never near-duplicates.

## Token-lean daily workflow (batch, don't chat back and forth)
1. Read this file + `balance`. Pick today's 6 topics from `SHORTS-TOPICS.md` (mix formats and hook templates).
2. WebSearch-verify each (2 searches max each). Write 6 scripts (narration + on-screen text). **Show all 6 at once for one approval.**
3. Quote total credits; get OK. Generate 6 narrations + 6x14 images in batches (see limits), build 6 storyboards, show them (one sheet per Short).
4. Apply the user's image fixes (0.25 credits each), then make the 6 hook clips, render, send videos + covers.
5. Give posting text (title, description, tags, captions) for all 6 in one message. Commit scripts. Say what to do tomorrow.

## Tech recipe (all proven)
- **Voice:** `generate_audio` model `text2speech_v2`, variant `elevenlabs`, voice_type `preset`, voice_id `e6f9b893-51b1-51d3-afe9-9e0482cb7ac1` (Benji). ~2.25 credits for 45 s. Get exact cost with `get_cost:true`.
- **Images:** `generate_image_batch`, model `gpt_image_2_5`, aspect 9:16, ONE style reference: upload `videos/costco-hot-dog/images/stickman-anchor-1.png` (media_upload -> curl PUT -> media_confirm; old media_id 2b0db06d-a086-4dcc-9ccb-cbd3415680b4 may still work) and pass as `image_references`. 0.25 credits each. **Max ~8 per batch, otherwise 429 rate_limit; retry the failed ones after waiting.** Prompt style block: "Stickman cartoon explainer illustration in the exact style of the reference image: bold clean black ink outlines, flat bright cel-shaded colors, simple shapes, warm saturated background, clean comic look. Vertical 9:16. ... No logos, no brand names, no readable text." Mascot = round white head, dot eyes, thick eyebrows, white shirt, mustard-yellow tie. Fix single details by editing the image (pass it as reference, say "keep everything the same, only change X").
- **Hook clip:** `generate_video` model `kling3_0`, mode `std`, sound `off`, duration 4, aspect 9:16, start_image = image 1's job id. **6 credits.** If a "preset recommendation" notice appears, retry with `declined_preset_id`. Takes 1-3 min; poll `jobs_wait`.
- **Word timings:** `pip install pocketsphinx`; copy `videos/mcdonalds-ice-cream-short/assembly/align.py`, edit the `SUB` dict for odd words, put the narration text (numbers spelled out) in `script.txt`, run -> `word_timing.json`.
- **Render:** copy `videos/mcdonalds-ice-cream-short/assembly/build.py` (most current: per-text y/size args, hook stretched to the first cut, year merging). Edit NARR, SHOTS (start time, image, motion), SHAKE, TEXT. Fonts/emoji come from `videos/costco-hot-dog/shorts/make_short.py`. Render takes ~3 min per Short (CPU only, free). `--preview` for 540p.
- **Sending files:** SendUserFile limit 30 MB. Re-encode with ffmpeg `-crf 20 -preset slow -c:a copy` (~22 MB looks identical after app compression). Write temp files in the scratchpad, NOT the repo (a stray tmp.mp4 triggered the stop hook once).
- **Cover image (IG/Facebook):** big 2-3 line text in the lower middle over the first image; keep text inside the 3:4 grid crop (y 240-1680). TikTok/Shorts: use opening frame.
- vidIQ (`mcp__vidIQ__*`): keyword research / title scoring cost 5 credits each; **account ran out of vidIQ credits Oct 10**.

## QA checklist (things the user already caught)
- Top text must not cover faces, the alarm/key props, or anything doing the emotion; keep inside y 240-1680 and centered; no emoji unless asked.
- Keep real-world layout right (McDonald's machine is BEHIND the counter, staff side; use a reference image of the same kitchen for later shots).
- Don't draw misleading outcomes (lawsuit unresolved -> tug-of-war, not a pile of money). Don't claim anything the sources don't.
- Check characters for missing parts (a missing foot was fixed). No cones/objects the user doesn't want in scenes.
- On-screen numbers/words are drawn by the renderer (so they're spelled right), not by the image model. No logos/brand text in images.

## Folder + git rules (repo size!)
- New Shorts go in `shorts/dayNN/<slug>/` (SCRIPT.md, assembly/ with align.py/build.py/word_timing.json). **Do not commit images, clips, mp4, mp3, png/jpg** (`.gitignore` covers `shorts/`); 180 Shorts of media would be many GB. The user downloads files from the chat each day; the container is ephemeral.
- Keep a one-line log per Short in `channel/SHORTS-LOG.md` (date, slug, title, credits) and mark topics used in `SHORTS-TOPICS.md`.
- Existing folders under `videos/` hold committed media from Day 0; leave them.

## Day starter (the user pastes this in each new chat)
"Day N of the 30-day plan: make 6 Shorts. Read channel/SHORTS-PLAYBOOK.md and CLAUDE.md first. Pick topics from SHORTS-TOPICS.md, verify facts, show me all 6 scripts for approval, quote credits."

## Open items as of Oct 10
- Credit balance was 838.8 on Oct 10 (started the day at 1,236). The extra ~286 credits ("MiniMax H3 Max" jobs) were the user's own edits on another video, not a problem. Always re-check `balance` at the start of each day.
- Cost per Short with hook ~11.5 credits (voice 2.25 + images 3.5 + hook 6). 180 Shorts with hooks ~2,070; images-only ~6 each. Decide hook-vs-no-hook per Short to fit the balance.
- McDonald's Short posted with no description/tags as a test and showed zero views; tags/captions were supplied afterward.
- Reusable `tools/make_short.py` (one JSON config per Short instead of copying build.py) would cut tokens per Short a lot; worth building on Day 1 and testing on the LEGO Short.

## Lessons from Day 01 (Oct 11)
- Style reference: don't use the Costco anchor (red-stripe background leaks). Use a plain-background earlier shot as reference ("art style only, not background"). Max ~7 images per batch; resubmit stalled batches.
- Use `shorts/day01/build_short.py <slug>` (per-short `assembly/config.py` with NARR, SHOTS, TEXT) instead of copying build.py. Pocketsphinx needs a SUB entry for out-of-vocab words (e.g. pequod).
- Storyboard sheets with A/B/C options side by side let the user pick fast.

## STATUS AFTER DAY 01 (Oct 11 2026) — read this to continue
**Done and posted-ready (4 of the day's 6; the other 2 were not made, so Day 02 should make 6 plus ideally 2 catch-up = 8, or just 6 if credits are tight):**
| # | Short | Format | Hook (first 3-5 s, animated) | Length |
|---|---|---|---|---|
| 1 | Starbucks named after Moby Dick | Weird fact -> real reason | "Did you know ___ exists thanks to ___?" | 29 s |
| 2 | Bubble Wrap was wallpaper | Sounds dumb until it's genius | "Pause for a second... ___?" | 33 s |
| 3 | Kleenex wasn't made for noses | Sounds dumb until it's genius | "You're not going to agree with this..." | 34 s |
| 4 | Mountain Dew wasn't meant to be a soda | Weird fact | "Nobody talks about this..." (no on-screen title) | 28 s |
Earlier (Day 0): Blockbuster (47 s CEO format), McDonald's ice cream machine (49 s), LEGO tires (47 s). All 7 Shorts are posted/ready on YT/TikTok/IG/FB. McDonald's had zero views when posted with no description/tags (test); always use title + description + tags from now on.

**Day-01 production flow that worked (copy it):**
1. User pasted 4 scripts; I quoted cost; user approved. Voiceovers (Benji) 1.35-1.8 credits each; 12 images per Short at 0.25 = 3 credits (shorter Shorts = 12 images, not 14-15); 4 s hook 6 credits. ~11 credits per Short with hook.
2. Storyboard sheet per Short (PIL contact sheet: 4 columns, shot number + narration caption under each image) sent via SendUserFile. Where the user wants choices, show 3 options side by side (A red / B blue / C green borders) in one sheet and ask for letters. The user then lists fixes; fixes cost 0.25 each.
3. Hook clips from the shot-1 image (Kling std, sound off, 4 s). Check a frame strip, then render.
4. `shorts/day01/build_short.py <slug>` renders from `<slug>/assembly/config.py` (NARR, SHOTS list of (start, image, motion), TEXT list of (t0, t1, [lines], color, y, size)) + `word_timing.json` from pocketsphinx (`assembly/align.py` + `script.txt`, numbers spelled out, add `SUB` entries for words the dictionary lacks e.g. pequod). Year words merge into digits on captions. Hook is stretched to the first cut. Cut times come from word_timing.json (cut on the first word of each narration beat). Titles on hook at y=300 size 100, inside safe area. Render takes ~3-5 min for 4 in parallel; files come out 20-26 MB (under the 30 MB send limit).
5. Covers/thumbnails: IG/FB/TikTok cover = chosen image with 2-line title text (yellow line 1, white line 2) at y~1500 (lower middle, inside 3:4 crop, not over faces; Starbucks used smaller text at y~1590). YouTube thumbnail = no-text version. For thumbnails ask the user to pick from 2 generated options per Short (0.25 each). Thumbnail prompts: close-up, shocked/smirking stickman, one strong focal prop, vivid contrast background, "no text".
6. Then give posting text: YouTube title (<=100 chars + 2 hashtags), description (facts + sources named, not invented URLs), tags, TikTok caption (with #businesstok), IG/FB caption (without). Then step-by-step posting for the app the user asks for, including every setting from POSTING-SETTINGS.md.

**Image rules learned (user feedback):** style reference = a plain-background earlier shot (not the Costco anchor) with "art style only, not background"; keep character outfits consistent between shots; founders/people consistent across shots; props/text must be right (sign says OPEN); no emojis unless asked; characters need all body parts; keep original real-world layout right; user may want 3 options for a hero shot; every shot must match its narration line. Remove shots the user calls unnecessary (e.g. a 1 s shot) and let the hook run longer instead.

**Voice rules:** narration approved by user line by line; keep honest wording ("As the story goes", "thanks to", no unverified claims); numbers spelled out for the voice and shown as digits on screen.

**Credits:** balance was 808.95 before the Day-01 hooks; spent 24 (hooks) + 2 (thumbnails) -> about 783 (re-check with `balance`). vidIQ account out of credits (keyword tools cost 5).

**Topic pool:** `channel/SHORTS-TOPICS.md`. Used so far: Blockbuster, McDonald's ice cream machine, LEGO tires, Starbucks/Moby Dick, Bubble Wrap, Kleenex, Mountain Dew (the user supplied the last four scripts). Remaining ideas: Pepsi navy, Southwest arm-wrestle, American Airlines olive, Kit Kat Japan, Heinz 57, Coca-Cola coca leaves, Toblerone Matterhorn, PEZ smoking, Burger King Whopper Detour, Apple Ron Wayne, Nike swoosh $35, Oswald/Mickey, YouTube dating site, Doritos Disneyland, M&M's soldiers, Amazon "Relentless", Game Boy bombing, Arizona 99 cents, Tic Tac 0 calories, IKEA maze, 50 Cent Vitaminwater, Dolly Parton/Elvis, Hollister dark stores, Michael Jackson Beatles songs. Prefer everyday brands the user's audience knows. Hook templates: `channel/HOOK-TEMPLATES.md` (rotate).

**Day 02 start:** user says "Day 2: make 6 Shorts" (or 8). Do: read this file + CLAUDE.md, run `balance`, pick topics, WebSearch-verify each (2 searches), write all scripts at once for approval (user may paste his own scripts instead), quote credits, wait for OK, then follow the flow above. Use `shorts/day02/<slug>/`, copy `shorts/day01/build_short.py` and the per-short `assembly/` files as the template (media is gitignored; the container is ephemeral so scripts/configs must be in git).

## STATUS AFTER DAY 02 (Oct 12 2026) — read this to continue
**Made (6):** Kit Kat Japan, Southwest arm-wrestle, Amazon "Relentless", Popsicle, movie-theater popcorn, Gatorade. Folders `shorts/day02/<slug>/` (SCRIPT.md, assembly/config.py, shots.json, word_timing.json). Posting text: `shorts/day02/POSTING-TEXT.md`. Thumbnails chosen: Kit Kat B, Southwest A, Amazon A, Popsicle A, Popcorn B, Gatorade B. Cost ~75.7 credits (balance 707.25 after thumbnails). Day 01 had only 4, so 10 of the first 13 Shorts exist plus Day 0's 3.
**Flow that worked (copy it):** pick ideas -> WebSearch verify -> user edits scripts line by line -> quote credits -> voices (batch of 6, Benji) -> 12 images each (style ref = LEGO img3 plain yellow, upload via media_upload; role `image_references`; 6 per batch, retry any 429s) -> storyboard sheets (12 shots, narration under each) -> user lists fixes by Short + shot (0.25 each; edit by passing the old job id as image_references with "keep everything the same, only change X") -> where the user wants choices show A/B/C inline in the sheet (red/blue/green borders) -> hooks with `generate_video_batch` kling3_0 std, sound off, 4 s, retry with `declined_preset_id` -> `build_short.py <slug>` (6 in parallel, ~6-8 min) -> `make_cover.py <slug>` -> send videos + covers -> 2 no-text thumbnails each -> posting text.
**Lessons:** (1) fact-check every number and caveat again before voicing; drop unverified claims (Pepsi navy, Wansink cereal study were dropped; blog-only percentages replaced by CNBC/SEC figures). (2) If the user adds narration, re-record the voice (get_cost first), re-run `align.py`, and recompute `shots.json`. (3) Text drawn inside images (signs, address bars) came out spelled right with gpt_image_2_5 when the exact string is given; always eyeball it. (4) Image model sometimes returns split two-panel images: say "ONE single full-frame scene, no panels". (5) Add `oh`/`two thousand` year merging is in build_short.py; year overlays go at y=1620, hook title y=300. (6) Kit Kat flavor count and Popsicle patent year were left out because sources disagree.
**Topic pool left:** Toblerone Matterhorn, PEZ, Burger King Whopper Detour, Coca-Cola coca leaves, Apple Ron Wayne, YouTube dating site, Arizona 99 cents, 50 Cent Vitaminwater, Pringles, Chick-fil-A Sundays, Post-it, Slinky, Velcro, Red Bull, Rolex, Dolly Parton, Monopoly, WD-40, Listerine, Hawaiian pizza, Nintendo cards, Bic cap hole, Tesla patents, Crocs, Google/Excite, prices ending in .99, milk at the back of the store, Dollar Tree $1, Wendy's square patty, Cracker Jack, Chuck E. Cheese tokens, Apple Store, Crayola, Subway footlong. Used on Day 02: Kit Kat, Southwest, Amazon, Popsicle, popcorn, Gatorade.

## STATUS AFTER DAY 03 (Oct 13 2026) — read this to continue
**Made (6):** chip bag nitrogen, Coke contour bottle, Crumbl weekly menu, Hollister dim lights, Dubai chocolate, airplane window breather hole (airplane has 11 shots, others 12). Folders `shorts/day03/<slug>/` (SCRIPT.md, assembly/config.py, shots.json, word_timing.json). Cost ~72 credits (balance 635.15 after hooks and thumbnails). Thumbnails: 2 no-text options per Short generated; picks and posting text (`shorts/day03/POSTING-TEXT.md`) were still pending when this was written.
**Flow changes that worked:** vidIQ had credits again (outliers search 5 credits each; the 'rising keywords' feed was useless for business, outliers by keyword was the useful tool). Topic list built from vidIQ outlier Shorts. Fact check twice: the second pass caught Crumbl (menu rotation was cut in Jan 2026), Coke bottle contest year (1914 vs 1915), and Dubai chocolate (shortage also caused by a weak US harvest). Storyboard sheets show A/B/C options inline with full-size options below. Shot-1 hook is stretched/trimmed to the first cut; short opening lines get the hook extended to the next word (2.8-4.3 s).
**Lessons:** (1) WebFetch could not reach any site; rely on WebSearch summaries and say so. (2) Keep sheet captions aligned to the real narration line per shot (a caption offset confused the airplane sheet once). (3) A shop that only sells cookies must show only cookies (no croissants, muffins). (4) Pane/window characters need no grid and the hole at the bottom center. (5) The year merging in build_short.py now handles 'nineteen fifteen', 'twenty seventeen', 'twenty twenty five' and 'thirty thousand'.
**Topic pool left:** see the Day 03 section in channel/SHORTS-TOPICS.md.
