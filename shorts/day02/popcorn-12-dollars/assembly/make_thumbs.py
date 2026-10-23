"""Covers/thumbnails (free, from existing art). A = clean image 1; B = eruption frame from the hook clip.
Outputs 1080x1920: *-youtube (no text) and *-cover (title lower middle: yellow line 1, white line 2, inside y 240-1680)."""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parent.parent.parent / "videos/costco-hot-dog/shorts"))
import make_short as m
W, H = 1080, 1920

def cover_fit(im):
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def title(im, l1, l2, y1, y2):
    im = im.convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f1, f2 = m.fit(l1, W - 120, 120), m.fit(l2, W - 120, 150)
    m.outlined(d, (W / 2, y1), l1, f1, m.YEL); m.outlined(d, (W / 2, y2), l2, f2, m.WHITE)
    im.alpha_composite(lay); return im.convert("RGB")

srcs = {"A": Image.open(ROOT / "images/img1.png").convert("RGB"), "B": Image.open(sys.argv[1]).convert("RGB")}
ypos = {"A": (1490, 1610), "B": (1420, 1570)}
out = ROOT / "thumbnails"
for k, im in srcs.items():
    base = cover_fit(im)
    base.save(out / f"popcorn-{k}-youtube-nocopy.png")
    title(base, "WHY DOES POPCORN", "COST $12?!", *ypos[k]).save(out / f"popcorn-{k}-cover.png")
