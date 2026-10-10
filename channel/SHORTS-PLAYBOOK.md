# Shorts playbook — read this first in every new chat

Written Oct 10 2026 from the first long chat. A new chat has NO memory of that chat; this file is the memory.

## Goal
**6 YouTube Shorts per day for 30 days (180 total).** The user opens a NEW chat each day. Channel: The Business Stick HQ
(@TheBusinessStickHQ). Shorts-only strategy (no long-form for now). Aim: grow + monetize (1,000 subs + 10M Shorts views/90 days, or 500 subs + 3M for the lower tier).
Made so far: Blockbuster, McDonald's ice cream machine, LEGO tires (folders under `videos/`). Costco long video exists (use as "Related video").

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
- Credit balance 838.8 (started the day at 1,236). ~286 credits were spent by something that is NOT this workflow ("MiniMax H3 Max" video jobs and some 1.5-credit GPT images, Oct 10 10:47-14:01). User should check other chats/tabs/apps using the same Higgsfield login.
- Cost per Short with hook ~11.5 credits (voice 2.25 + images 3.5 + hook 6). 180 Shorts with hooks ~2,070; images-only ~6 each. Decide hook-vs-no-hook per Short to fit the balance.
- McDonald's Short posted with no description/tags as a test and showed zero views; tags/captions were supplied afterward.
- Reusable `tools/make_short.py` (one JSON config per Short instead of copying build.py) would cut tokens per Short a lot; worth building on Day 1 and testing on the LEGO Short.
