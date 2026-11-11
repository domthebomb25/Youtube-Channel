# Frame-check: compare each of the 91 storyboard-PDF tiles to the repo master planned for that position.
import sys, os, glob, json, numpy as np
from PIL import Image
A, SB = sys.argv[1], sys.argv[2]
FINAL = A + "/section2-final/"
def sf(n):
    for d in ("section1","section2","section3","section4","section5","section6"):
        p=f"{A}/{d}/{n}.png"
        if os.path.exists(p): return p
POS = [1,2,3,4,5,6,8,9,10,11,13,52,17,18,19,20, 22,23,24,25,26,1,"CHAIR",FINAL+"ninja-blue-hoodie.png",FINAL+"ludwig-monitorback-fix2.png",FINAL+"kai-red-hoodie-v2.png",56,26,
       59,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,
       76,77,78,79,80,81,82,83,84,85,86,87,88,89,
       90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,106,107,108,104,105,109,110,111,
       112,113,114,115,87,118,119,120,121]
POS[22] = A + "/section2-v2/chair-empty.png"
assert len(POS) == 91, len(POS)
def path(x): return x if isinstance(x, str) else sf(x)
def small(im): return np.asarray(im.convert("RGB").resize((96, 54), Image.BILINEAR), np.float32)
def corr(a, b):
    a = a.ravel() - a.mean(); b = b.ravel() - b.mean(); return float((a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
pages = sorted(glob.glob(SB + "/p-*.png")); assert len(pages) == 31, len(pages)
res = []
for k in range(91):
    pg = Image.open(pages[k // 3]).convert("RGB"); W = pg.size[0]; c = k % 3
    s = W / 2000.0
    x0 = int((15 + 664 * c) * s); y0 = int(52 * s); tw = int(642 * s); th = int(360 * s)
    tile = pg.crop((x0, y0, x0 + tw, y0 + th))
    p = path(POS[k]); ref = Image.open(p)
    r = corr(small(tile), small(ref)); d = float(np.abs(small(tile) - small(ref)).mean())
    res.append((k + 1, os.path.relpath(p, A), r, d))
bad = [r for r in res if r[2] < 0.93]
for r in res: print("%3d %-42s corr %.3f  meanabs %5.1f %s" % (r[0], r[1], r[2], r[3], "<-- CHECK" if r[2] < 0.93 else ""))
print("flagged:", [(r[0], r[1], round(r[2], 3)) for r in bad])
