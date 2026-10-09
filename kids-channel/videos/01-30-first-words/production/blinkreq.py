"""Closed / half-closed eye edits of each hold frame: python3 blinkreq.py 000 002 ..."""
import json, sys
ids = dict(l.split() for l in open('hold_media.txt'))
KEEP = ("Edit the reference image. Keep EVERYTHING exactly identical: same framing, same camera, same pose, same head position "
        "and angle, same mouth expression, same hair, headband, toy or item in her hands, hands, clothes, lighting, colors and "
        "background, pixel for pixel. The ONLY change: ")
CLOSED = ("both of her eyes are gently and fully CLOSED in a natural mid-blink, upper eyelids down meeting the lower lids, lashes "
          "resting closed, smooth eyelid skin matching her skin tone. Eyebrows stay in the same place. No other changes at all.")
HALF = ("both of her eyes are HALF closed, as in the middle of a quick blink, upper eyelids lowered halfway over the irises. "
        "Eyebrows stay in the same place. No other changes at all.")
out = []
for n in sys.argv[1:]:
    for k, txt in ((0, CLOSED), (1, HALF)):
        out.append({"index": int(n) * 10 + k, "params": {"model": "gpt_image_2_5", "aspect_ratio": "16:9", "quality": "high",
            "resolution": "1k", "use_unlim": False, "medias": [{"value": ids[n], "role": "image_references"}], "prompt": KEEP + txt}})
print(json.dumps(out))
