"""Pixel edit of approved image 1: re-center the two black eye ovals (the mascot has no pupils/whites).
Upright, same size as the originals, symmetric about the head centre line. Nothing else is touched."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); a = np.asarray(im).copy()
dark = a.sum(axis=2) < 200
def comp(box):
    x0, y0, x1, y1 = box; m = np.zeros(dark.shape, bool); m[y0:y1, x0:x1] = dark[y0:y1, x0:x1]; return m
Lm, Rm = comp((226, 440, 262, 498)), comp((300, 420, 334, 478))
def bbox(m):
    ys, xs = np.where(m); return xs.min(), ys.min(), xs.max(), ys.max()
lb, rb = bbox(Lm), bbox(Rm)
er = Image.fromarray(((Lm | Rm) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
a[np.asarray(er) > 127] = [254, 254, 254]
out = Image.fromarray(a)
SS, HEAD_CX, EYE_Y, SEP = 8, 235, 463, 74
def oval(cx, cy, w, h):
    m = Image.new('L', (w * SS, h * SS), 0)
    ImageDraw.Draw(m).ellipse([0, 0, w * SS - 1, h * SS - 1], fill=255)
    out.paste((0, 0, 0), (int(round(cx - w / 2)), int(round(cy - h / 2))), m.resize((w, h), Image.LANCZOS))
oval(HEAD_CX - SEP / 2, EYE_Y, lb[2] - lb[0] + 1, lb[3] - lb[1] + 1)
oval(HEAD_CX + SEP / 2, EYE_Y, rb[2] - rb[0] + 1, rb[3] - rb[1] + 1)
out.save(dst)
