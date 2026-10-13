"""usage: python3 make_cover.py <slug>  -> <slug>/cover.png (shot-1 image + 2-line title, lower middle, inside the 3:4 crop)"""
import importlib.util, math, sys
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
slug = sys.argv[1]
sys.path.insert(0, str(HERE.parent.parent / "videos/costco-hot-dog/shorts"))
import make_short as m
W, H = 1080, 1920
spec = importlib.util.spec_from_file_location("cfg", HERE / slug / "assembly/config.py")
C = importlib.util.module_from_spec(spec); C.YEL, C.WHITE = m.YEL, m.WHITE; spec.loader.exec_module(C)
lines = C.TEXT[0][2]
im = Image.open(HERE / slug / "images/img1.png").convert("RGB")
s = max(W / im.width, H / im.height)
im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
x, y = (im.width - W) // 2, (im.height - H) // 2
im = im.crop((x, y, x + W, y + H)).convert("RGBA")
lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
fs = min(m.fit(t, W - 140, 104).size for t in lines); f = m.font(fs); yy = 1490
for i, t in enumerate(lines):
    tw = d.textlength(t, font=f); m.outlined(d, ((W - tw) / 2, yy), t, f, m.YEL if i == 0 else m.WHITE, anchor="lm"); yy += fs * 1.08
im.alpha_composite(lay); im.convert("RGB").save(HERE / slug / "cover.png"); print(slug, "cover ok")
