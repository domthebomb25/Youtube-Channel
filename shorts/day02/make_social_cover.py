"""usage: python3 make_social_cover.py <slug> [y]  -> <slug>/cover-social.png (chosen no-text thumbnail + simple 2-line title, inside the 3:4 crop y 240-1680)"""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
slug = sys.argv[1]; y0 = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
sys.path.insert(0, str(HERE.parent.parent / "videos/costco-hot-dog/shorts"))
import make_short as m
TITLES = {"kitkat-japan": ["JAPAN'S LUCKY", "KIT KAT"], "southwest-arm-wrestle": ["THE ARM-WRESTLING", "LAWSUIT"],
          "amazon-relentless": ["RELENTLESS.COM", "GOES TO AMAZON?"], "popsicle-eleven-year-old": ["AN 11-YEAR-OLD", "INVENTED THIS"],
          "movie-popcorn": ["WHY POPCORN", "COSTS SO MUCH"], "gatorade-gators": ["NAMED AFTER A", "FOOTBALL TEAM"]}
W, H = 1080, 1920
im = Image.open(HERE / slug / "thumbnail.png").convert("RGB")
s = max(W / im.width, H / im.height)
im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
x, y = (im.width - W) // 2, (im.height - H) // 2
im = im.crop((x, y, x + W, y + H)).convert("RGBA")
lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
lines = TITLES[slug]
fs = min(m.fit(t, W - 140, 112).size for t in lines); f = m.font(fs); yy = y0
for i, t in enumerate(lines):
    tw = d.textlength(t, font=f); m.outlined(d, ((W - tw) / 2, yy), t, f, m.YEL if i == 0 else m.WHITE, anchor="lm"); yy += fs * 1.08
im.alpha_composite(lay); im.convert("RGB").save(HERE / slug / "cover-social.png"); print(slug, "ok")
