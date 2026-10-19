"""Covers for the '100 followers' Short: Instagram/Facebook (big text, lower middle) and TikTok (opening frame).

usage: python3 cover.py <path-to-sad-image-2.png>  ->  ../covers/*.png
"""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parents[2] / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402

W, H = 1080, 1920
OUT = ROOT / "covers"
OUT.mkdir(exist_ok=True)


def base(path):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H)).convert("RGBA")


def lines(im, items, y0, gap=1.08):
    """items: [(text, colour, size)] centred; returns the next y."""
    d = ImageDraw.Draw(im)
    y = y0
    for text, col, size in items:
        f = m.fit(text, W - 140, size)
        tw = d.textlength(text, font=f)
        m.outlined(d, ((W - tw) / 2, y), text, f, col, anchor="lm")
        y += f.size * gap
    return y


def main():
    src = sys.argv[1]
    # Instagram / Facebook: big 3-line text in the lower middle, inside the 3:4 grid crop (y 240-1680), clear of his face
    ig = base(src)
    lines(ig, [("0 TO 100", m.YEL, 200), ("FOLLOWERS", m.WHITE, 150), ("THANK YOU!", m.YEL, 150)], 1160)
    ig.convert("RGB").save(OUT / "cover-instagram-facebook.png")
    # TikTok: opening frame with the same top text as the video
    tt = base(src)
    lines(tt, [("0 TO 100", m.YEL, 112), ("IN ONE WEEK", m.WHITE, 112)], 270)
    tt.convert("RGB").save(OUT / "cover-tiktok.png")
    # optional 2nd arg: happy cake thumbnail with text over the cake body (clear of face, candles and thumbs up)
    if len(sys.argv) > 2:
        hp = base(sys.argv[2])
        lines(hp, [("THANK YOU FOR", m.WHITE, 120), ("100 FOLLOWERS", m.YEL, 150)], 1470)
        hp.convert("RGB").save(OUT / "thumbnail-happy-cake-text.png")
        hp.convert("RGB").crop((0, 240, W, 1680)).resize((540, 720)).save(OUT / "_grid-check-happy.png")
    # check preview: what the 3:4 profile grid shows of the Instagram cover
    ig.convert("RGB").crop((0, 240, W, 1680)).resize((540, 720)).save(OUT / "_grid-check.png")
    print(sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
