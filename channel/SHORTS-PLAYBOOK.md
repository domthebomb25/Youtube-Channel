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
- vidIQ (`mcp__vidIQ__*`): keyword research / title scoring cost ~5 credits each; subscription bought Oct 13 (2,008 credits); `vidiq_balance` is free.

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
See the paste block the user keeps; essentials: "Day N of the 30-day plan: make 6 Shorts. Read channel/SHORTS-PLAYBOOK.md and CLAUDE.md first. Source ideas from vidIQ trending searches (top 10, no repeats of videos we made), verify facts, show scripts for approval, quote credits."

## Open items as of Oct 10
- Credit balance was 838.8 on Oct 10 (started the day at 1,236). The extra ~286 credits ("MiniMax H3 Max" jobs) were the user's own edits on another video, not a problem. Always re-check `balance` at the start of each day.
- Cost per Short with hook ~11.5 credits (voice 2.25 + images 3.5 + hook 6). 180 Shorts with hooks ~2,070; images-only ~6 each. Decide hook-vs-no-hook per Short to fit the balance.
- McDonald's Short posted with no description/tags as a test and showed zero views; tags/captions were supplied afterward.
- Reusable `tools/make_short.py` (one JSON config per Short instead of copying build.py) would cut tokens per Short a lot; worth building on Day 1 and testing on the LEGO Short.

## Lessons from Day 01 (Oct 11)
- Style reference: don't use the Costco anchor (red-stripe background leaks). Use a plain-background earlier shot as reference ("art style only, not background"). Max ~7 images per batch; resubmit stalled batches.
- Use `shorts/day01/build_short.py <slug>` (per-short `assembly/config.py` with NARR, SHOTS, TEXT) instead of copying build.py. Pocketsphinx needs a SUB entry for out-of-vocab words (e.g. pequod).
- Storyboard sheets with A/B/C options side by side let the user pick fast.

## CURRENT STATUS (last updated after Day 01, Oct 11 2026; the day's chat must update this block at the end of its day) — read this to continue
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

**Credits:** balance was 808.95 before the Day-01 hooks; spent 24 (hooks) + 2 (thumbnails) -> about 783 (re-check with `balance`). vidIQ: subscribed Oct 13, 2,008 credits at that time (check `vidiq_balance`).

**Topic pool:** `channel/SHORTS-TOPICS.md`. Used so far: Blockbuster, McDonald's ice cream machine, LEGO tires, Starbucks/Moby Dick, Bubble Wrap, Kleenex, Mountain Dew (the user supplied the last four scripts). Remaining ideas: Pepsi navy, Southwest arm-wrestle, American Airlines olive, Kit Kat Japan, Heinz 57, Coca-Cola coca leaves, Toblerone Matterhorn, PEZ smoking, Burger King Whopper Detour, Apple Ron Wayne, Nike swoosh $35, Oswald/Mickey, YouTube dating site, Doritos Disneyland, M&M's soldiers, Amazon "Relentless", Game Boy bombing, Arizona 99 cents, Tic Tac 0 calories, IKEA maze, 50 Cent Vitaminwater, Dolly Parton/Elvis, Hollister dark stores, Michael Jackson Beatles songs. Prefer everyday brands the user's audience knows. Hook templates: `channel/HOOK-TEMPLATES.md` (rotate).

**Any-day start:** user says "Day N: make 6 Shorts" (add catch-up Shorts if the log shows a shortfall). Do: read this file + CLAUDE.md + `channel/SHORTS-LOG.md`, run Higgsfield `balance`, then do the TOPIC SOURCING below, verify, write all scripts at once for approval (the user may paste his own scripts instead), quote credits, wait for OK, then follow the flow above. Use `shorts/dayNN/<slug>/`; copy `shorts/day01/build_short.py` and a per-short `assembly/` (align.py, script.txt, config.py) as the template (media is gitignored and the container is ephemeral, so scripts/configs must be committed). At the end of the day: append to `channel/SHORTS-LOG.md`, update this STATUS block, commit + push, and tell the user to merge the branch (or open a PR if asked) so tomorrow's chat sees it.

## TOPIC SOURCING (user rule, every day): ideas come from vidIQ trending searches
1. Check `vidiq_balance` first (free call). vidIQ tools cost credits (keyword/title tools ~5 each). The user bought the monthly subscription on Oct 13 2026: 2,008 credits then (renewable plan of 2,000, resets about the 10th of each month). Spend what the research needs, report credits used. If the balance is ever empty, say so and ask before falling back to WebSearch (state clearly that the list is not vidIQ-based).
2. Use vidIQ (`vidiq_trending_videos`, `vidiq_trend_categories`, `vidiq_outliers`, `vidiq_keyword_research`, `vidiq_youtube_search`; check what is available) to find the top TRENDING business / brand-origin / "hidden story behind a company or product" searches and outlier Shorts right now. Focus: everyday brands and products anyone recognizes, surprising origin facts, marketing tricks, product design secrets, surprising numbers. Avoid the saturated founder legends (FedEx, Kodak, Airbnb, Nokia, KFC, Nintendo, Play-Doh).
3. Generate the TOP 10 ideas vidIQ surfaces, ranked, each with: working title, one-line hook, search/trend evidence (volume, views of outliers), and the format (weird fact / sounds dumb until it's genius / you're the company).
4. NEVER repeat a video already made: compare every idea against `channel/SHORTS-LOG.md`, the "Made so far" list above and the folders under `videos/` and `shorts/`. Drop duplicates and near-duplicates (same company + same angle) and replace them until 10 fresh ideas remain.
5. Show the 10 to the user, who picks the day's 6 (or says "use your top 6"). Then WebSearch-verify each chosen fact (2 searches max each) before scripting, and keep only claims the sources support.
6. Append unused ideas to `channel/SHORTS-TOPICS.md` with the date, and mark used ones.

