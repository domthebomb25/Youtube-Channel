Film #2 render pipeline (local only, 0 credits). Run from the repo root with a scratch work dir W:
  python3 -I tools/render-film2/01_timeline_audio.py film2-assets W      # manifest -> timeline.json, narration.wav (exact per-line durations)
  python3 -I tools/render-film2/02_states.py film2-assets                 # builds render/states/09-50000.png, 09-100000.png, 10-1000.png
  python3 -I tools/render-film2/03_render.py film2-assets W film2-assets/render/<name>.mp4   # ffmpeg CONCAT FILTER, single encode, loudnorm two-pass
  python3 -I tools/render-film2/04_qa.py film2-assets W film2-assets/render/<name>.mp4       # QA gates -> render/QA-REPORT.txt numbers
Rules: concat FILTER only (never -c copy); never overwrite a delivered render (a re-render gets a new filename, e.g. film2-streamer-FINAL-v2.mp4).
