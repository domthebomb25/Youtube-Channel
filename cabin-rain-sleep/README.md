# Cabin rain: 10-hour sleep video

Original scene + original rain sound, built with code. No stock footage, no stock audio.

## What is here
- `art/cabin-scene.png`: AI-generated base picture (1344x752). `art/cabin-rain-thumbnail.jpg`: 1280x720 thumbnail.
- `scripts/render_seg.py`: renders one 10-minute chunk (moving rain on the glass only, swaying lantern/candle flames,
  slow smoke over the mug, lantern pulse 100%->96%, slow zoom 100%->101.5%->100%). Every chunk loops seamlessly;
  only the rain-streak layout changes per chunk number.
  `python3 render_seg.py art/cabin-scene.png out.mp4 <chunk 1-6> [seconds]`  (`CHECK=1` verifies the loop).
- `scripts/rain_audio2.py`: synthesizes forest rain from individual drop splashes + canopy drips + gentle wind.
  Version used: `DENSITY=1.8 TILT=-0.25 DROPS=0.4 CANOPY=1.3 WIND=0.35 python3 rain_audio2.py raw.wav 3620 21`
- `scripts/loopfix.py`: crossfades the end of the 3620 s file into its start, giving a 1-hour file that repeats cleanly.

## Plan
6 video chunks (10 min each, different rain layout) = 1 hour of video, 1 hour of rain audio, repeated 10x in DaVinci Resolve.
Video is cut into 2-minute pieces and audio into 20-minute pieces so each file can be sent in chat (30 MB limit).
Needs: python3, numpy, scipy, pillow, ffmpeg.

## Upload notes
Title: 10 Hours Rain Sounds for Sleeping | Cozy Cabin Forest Rain, No Thunder
Disclose altered/synthetic content = Yes (realistic AI image and synthetic sound).
