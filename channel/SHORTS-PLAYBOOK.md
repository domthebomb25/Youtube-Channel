# Shorts playbook v2 — read this first in every new chat

Started Oct 19 2026. Replaces v1 (kept at `channel/archive/SHORTS-PLAYBOOK-v1.md`). A new chat has NO memory of earlier chats; this file is the memory.
Update it whenever a test teaches us something (see "Post-mortem log").

## Goal and strategy
- Channel: The Business Stick HQ (@TheBusinessStickHQ). Shorts only. Stickman business stories.
- **ONE strong YouTube Short per day** (changed from 6/day on Oct 19). Quality and learning over volume. Same story also goes to TikTok / Instagram / Facebook.
- Monetization target: 1,000 subs + 10M Shorts views in 90 days (lower tier: 500 subs + 3M Shorts views). Needed before Feb 2027. Verify YouTube's current YPP terms before relying on the numbers.
- Reality: 10M comes from a few hits, not steady growth. Plan = many chances at a hit + learn fast from the data. Never use bought views / pods / bots (violates rules, hurts retention data).
- Rule: no near-duplicate videos. Every Short = original script, original visuals, different story.

## How a Short breaks out (what we design for)
YouTube shows a Short to a small test group first. It mainly judges: (1) viewed vs swiped away in the first 1-3 s, (2) average % viewed (over 100% = people rewatch), (3) shares/comments. Our videos that stall near 1,000 views most likely lose people in the first 2 s or at a mid-video drop. Check Studio -> Engagement to confirm.

## User rules (non-negotiable)
- **Quote the credit cost and wait for OK before spending Higgsfield credits.** Check `balance` at the start of each day.
- Every posting instruction must include **every setting in `channel/POSTING-SETTINGS.md`** (AI label ON, Identify similar products OFF, Trial reel OFF, Related video on every Short, etc.). Simple, step-by-step, iPhone first.
- **No music.** Short sound effects on the hook are approved (see Sound). **No end text** unless asked. No emojis in the big hook text unless asked.
- User prefers PDFs over .md for documents they read (make a PDF copy of anything they should read).
- Facts must be **verified with sources** (WebSearch) before scripting; keep honest caveats; 1-2 source links at the bottom of the YouTube description only.
- Show the user **every image (storyboard sheet) before rendering** and the hook clip result.
- Don't open PRs unless asked. Commit + push small text files at the end of each day.

## Format of one Short
- **Length: 25-35 s default.** Longer (up to ~45 s) only when a trending topic needs it. Log the length every time and compare average % viewed.
- 1080x1920, voice Benji, a new picture every 2-3 s (about 10-14 images), word-by-word yellow captions, big top text on key beats, an animated hook clip, no still image ever fully static (small zoom/shake at every cut).
- Story formats: "You're the company" (viewer is the CEO, problem, would-you-do-it, reveal name) and "Sounds dumb until it's genius" (weird fact -> real reason). Add new formats as tests prove them.
- Prefer everyday brands (Costco, McDonald's, Dollar Tree...), product-design secrets, marketing tricks, surprising numbers. Founder legends (FedEx, Kodak, Airbnb, Nokia, KFC, Nintendo, Play-Doh) are overused.

## Idea gate (score each 1-5; only make topics that score high)
1. Everyday brand/object the viewer already knows.
2. One surprising number or "why" that fits in the first sentence.
3. The whole story fits in one line.
4. Shareable: would a viewer send it to someone?
5. Visual: is there a striking, easy-to-understand image of the payoff?
Keep 2-3 slots a week open for timely stories (a brand in the news: recall, price change, lawsuit). Topic pool: `channel/SHORTS-TOPICS.md`.

## Hook design (the most important part)
**Payoff-first:** the viewer must know what they are watching in the first second.
1. **One line that states the payoff**, spoken and shown (example: "You could have bought Netflix for $50 million.").
2. **First image = the payoff, as striking as possible.** One clear subject, scale/contrast/impossible object. Test: with the sound off, can a viewer tell what the video is about?
3. **Big on-screen text** with the key number/claim in the first 2 s (inside the safe area, never over faces/props).
4. **Animated hook clip (first 2-4 s)** is the most visually dramatic moment of the video.
5. Open curiosity with the "how/why", not by hiding the payoff: the video answers "how did this happen?"
6. Write 3 hook options per topic (line + image idea) and pick the strongest. `channel/HOOK-TEMPLATES.md` is a source of opening words, not a rule; don't repeat the same template two videos in a row.
7. **Loop ending:** the last line lands back on the hook line so the Short replays seamlessly (rewatches raise average % viewed). Write the loop into the script from the start.
8. **Retention beat every ~8 s:** a twist, number or reveal where drop-off usually happens.

## Sound
- No music. Voice (Benji) + short sound effects: whoosh on the hook cut, hit on the big number, small pop on reveals. Keep them quiet under the voice.
- Higgsfield has no standalone sound-effect model, so SFX come from free/royalty-free files or ffmpeg-generated sounds mixed in the renderer. **Open item:** pick/make a small SFX pack in `tools/` or `videos/` (commit only tiny files) before Day 1 of the new plan.
- Narration: slightly faster delivery, stress the payoff words in the hook. Test it.

## One-a-day workflow
1. Read this file + check `balance`. Pick the topic with the idea gate.
2. Verify facts (WebSearch, 2 searches max). Write the script: payoff hook line (3 options), story, loop ending, on-screen text. Show it for one approval.
3. Quote credits, get OK. Generate narration, images, hook clip. Show the storyboard sheet and hook result. Apply fixes (0.25 credits per image fix).
4. Render with word timings, SFX, captions. Send video + cover.
5. Give posting text (title, description, tags, captions) for every platform with all settings from `POSTING-SETTINGS.md`.
6. Log it (SHORTS-LOG.md + Post-mortem table below). Commit + push. Say what to do tomorrow.
7. After 48 h: user sends Studio numbers; add the lesson here.

## Credit budget (proposed — confirm with user)
- One Short used to cost ~11.5 credits (voice 2.25 + images ~3.5 + hook 6). With one Short a day there is room to spend more on the hook: e.g. a 2nd hook clip (+6) or regenerating hook images. Quote the exact cost every time.
- Free test: Google Flow gives 50 credits/day (~7 four-second clips) but the user runs it by hand; Claude can write the prompts.

## Posting and testing
- Post time: use Studio's "when your viewers are on YouTube" chart.
- Pin a comment that asks a question. Reply to comments within the first hour; turn good comment questions into follow-up Shorts. Keep the Related video link on every Short.
- Title and description carry a clear keyword (brand name, number).
- Series identity: keep the same character and look; repeat formats that work so viewers subscribe for more.
- **One variable per batch/week** (hook type, length, topic type, SFX). Weekly review: double down on the top ~20% of formats, drop the bottom ~20%.

## Tech recipe (all proven)
- **Voice:** `generate_audio` model `text2speech_v2`, variant `elevenlabs`, voice_type `preset`, voice_id `e6f9b893-51b1-51d3-afe9-9e0482cb7ac1` (Benji). ~2.25 credits for 45 s (less for 30 s). Exact cost with `get_cost:true`.
- **Images:** `generate_image_batch`, model `gpt_image_2_5`, aspect 9:16, ONE style reference: upload `videos/costco-hot-dog/images/stickman-anchor-1.png` (media_upload -> curl PUT -> media_confirm; old media_id 2b0db06d-a086-4dcc-9ccb-cbd3415680b4 may still work) and pass as `image_references`. 0.25 credits each. **Max ~8 per batch, otherwise 429 rate_limit; retry failed ones after waiting.** Prompt style block: "Stickman cartoon explainer illustration in the exact style of the reference image: bold clean black ink outlines, flat bright cel-shaded colors, simple shapes, warm saturated background, clean comic look. Vertical 9:16. ... No logos, no brand names, no readable text." Mascot = round white head, dot eyes, thick eyebrows, white shirt, mustard-yellow tie. Fix single details by editing the image (pass it as reference, say "keep everything the same, only change X").
- **Hook clip:** `generate_video` model `kling3_0`, mode `std`, sound `off`, duration 4, aspect 9:16, start_image = image 1's job id. **6 credits.** If a "preset recommendation" notice appears, retry with `declined_preset_id`. Takes 1-3 min; poll `jobs_wait`.
- **Word timings:** `pip install pocketsphinx`; copy `videos/mcdonalds-ice-cream-short/assembly/align.py`, edit the `SUB` dict for odd words, put the narration text (numbers spelled out) in `script.txt`, run -> `word_timing.json`.
- **Render:** copy `videos/mcdonalds-ice-cream-short/assembly/build.py` (per-text y/size args, hook stretched to the first cut, year merging). Edit NARR, SHOTS (start time, image, motion), SHAKE, TEXT. Fonts/emoji from `videos/costco-hot-dog/shorts/make_short.py`. ~3 min render per Short (CPU, free). `--preview` for 540p. SFX mixing is not in build.py yet (open item).
- **Sending files:** SendUserFile limit 30 MB. Re-encode with ffmpeg `-crf 20 -preset slow -c:a copy` (~22 MB). Write temp files in the scratchpad, NOT the repo.
- **Cover image (IG/Facebook):** big 2-3 line text in the lower middle over the first image; keep text inside the 3:4 grid crop (y 240-1680). TikTok/Shorts: use opening frame.
- vidIQ (`mcp__vidIQ__*`): costs 5 credits per call; **account ran out of credits Oct 10** (a transcript call still worked Oct 19).
- Google Flow / YouTube / x.com are blocked from the cloud container (proxy 403). The user must change the environment's Network access to allow them.

## QA checklist (things the user already caught)
- Top text must not cover faces, the alarm/key props, or anything doing the emotion; keep inside y 240-1680 and centered; no emoji unless asked.
- Keep real-world layout right (McDonald's machine is BEHIND the counter, staff side; use a reference image of the same kitchen for later shots).
- Don't draw misleading outcomes (lawsuit unresolved -> tug-of-war, not a pile of money). Don't claim anything the sources don't.
- Check characters for missing parts. No cones/objects the user doesn't want in scenes.
- On-screen numbers/words are drawn by the renderer (so they're spelled right), not by the image model. No logos/brand text in images.
- Hook check: does the first image alone show the payoff? Is the loop ending written?

## Folder + git rules (repo size!)
- New Shorts go in `shorts/dayNN/<slug>/` (SCRIPT.md, assembly/ with align.py/build.py/word_timing.json). **Do not commit images, clips, mp4, mp3, png/jpg** (`.gitignore` covers `shorts/`). The user downloads files from the chat each day; the container is ephemeral.
- One-line log per Short in `channel/SHORTS-LOG.md`; mark topics used in `SHORTS-TOPICS.md`.
- Existing folders under `videos/` hold committed media from Day 0; leave them.

## Post-mortem log (fill in 48 h after posting)
| Date | Topic | Length | Views (Oct 19) | Avg watched | Avg % viewed | Lesson |
|---|---|---|---|---|---|---|
| Oct 16 | Tesla Roadster can FLY | 45 s | 1,320 | 0:27 | 61.3% | Best retention + views; everyday brand + curiosity title |
| Oct 7 | Costco co-founder threatened exec ($1.50 hot dog) | 47 s | 1,164 | 0:28 | 61.4% | Highest like rate (48 likes) |
| Oct 8 | "Business stories nobody tells you" | 23 s | 1,261 | 0:13 | 57.0% | Short (23 s) matched the 45 s ones |
| Oct 17 | Tesla "car that can fly?" | 48 s | 1,210 | 0:23 | 48.3% | Near-duplicate of Oct 16 topic; avoid repeats |
| Oct 14 | McDonald's ice cream locked | 32 s | 280 | 0:15 | 49.3% | |
| Oct 9 | Costco real money maker | 52 s | 211 | 0:25 | 48.3% | |
| Oct 13 | Relentless.com / Amazon name | 38 s | 103 | 0:20 | 53.4% | Name-story topic, weak |
| Oct 15 | Blockbuster / Netflix | 35 s | 13 | | | Founder-legend topic, weakest |
| Oct 18 | Tesla $250K loan | 43 s | 56 | | | Too new to judge |

Findings (Oct 19, 7 Shorts, small sample): Shorts holding 57-61% got ~1,200 views; those at 48-53% mostly got 100-300. People watch ~25 s regardless of length, so cutting to 28-30 s should lift % viewed to 90%+. Nobody is looping yet (best 61%). Swipe-away data still needed (Studio -> Analytics -> Engagement -> Viewed vs swiped away).

## Open items (Oct 19)
- Studio retention screenshots (best 2-3 and worst 2 Shorts) -> fill the table above and confirm where viewers leave.
- Confirm hook credit budget, and set up the SFX pack + SFX mixing in `build.py`.
- Competitor study: top 10 business-story Shorts in the last 30 days (hook line, length, visuals).
- Build 30 scored topics for the next month.
- Reusable `tools/make_short.py` (one JSON config per Short) would cut tokens per Short.

## Day starter (the user pastes this in each new chat)
"Day N: make today's Short. Read channel/SHORTS-PLAYBOOK.md and CLAUDE.md first. Pick a topic (idea gate), verify facts, show me the script with 3 hook options for approval, quote credits."
