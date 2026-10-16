# Tesla Roadster — "can FLY" Short (Oct 16 2026)
Format: 2.2 s stickman hook (kling3_0 clip from a gpt_image_2_5 still) + the user's own event screen recording (41 s, original audio), layout A (wide footage centered over a dark blurred copy).
Hook text: "THE TESLA ROADSTER / CAN FLY" (FLY in yellow). No narration, no music, no end text.
Build: `python3 assembly/build.py HOOK_CLIP RECORDING OUT.mp4 [--preview]` (footage crop 1180x572 at y=698 of the 1180x2230 recording).
Credits: image 0.25 + hook clip 6 = ~6.25 (first hook). Extra 3 alt hooks "THE TESLA ROADSTER CAN FLY?" (driveway, night trail, ramp launch): 3 x 6.25 = 18.75. build.py supports --hook-only --texty=N --sec=S --last="FLY?".
Sources (put in YT description): electrek.co/2026/10/15/tesla-unveils-cyberfied-new-roadster-kickflip/ , techcrunch.com/2026/10/15/tesla-reveals-spacex-powered-roadster-that-flies-and-falls-with-style/
Caveats: 0-60 claims differ between sources (do not quote numbers); production date unconfirmed; price not announced.

## Viral 3 s hook (3 shots + rocket SFX)
Images: 3 key stills (gpt_image_2_5, dark bg) + shot-3 eye fix = 1.0 cr. Clips: 3 x kling3_0 std 3 s = 13.5 cr. SFX: mirelo_text_to_audio 3 s = 0.75 cr. Total ~15.25.
Build: `python3 assembly/viral_hook.py CLIP1 CLIP2 CLIP3 SFX OUT.mp4` (Anton slanted text, FLY? 3x with blue glow, shaking ?, chromatic aberration, shake, snap zoom, loop melt).

## Hook from the single fly-over clip (user's pick)
Uses the shot-2 clip (kling3_0, 716x1280, 3 s) alone: slanted Anton text, FLY? in RED, rocket SFX (trimmed 0.35 s) + synthetic sub boom on the slam. No extra credits.
Build: `cd assembly && python3 hook_single.py CLIP SFX OUT.mp4`
Benji voice for the hook ("The Tesla Roadster can... FLY?", text2speech_v2 elevenlabs) = 0.15 cr. Mixed with `hook_single.py CLIP SFX OUT.mp4 BENJI.mp3` (pause cut so FLY? lands on the slam at 1.45 s).

## FINAL (Oct 16): hook-single-benji.mp4 (3 s) + event recording in layout A, 44 s, 30 fps. Cover = frame at 2.0 s ("FLY?" text). Concat done with ffmpeg (hook fps->30, audio 48 kHz stereo).
