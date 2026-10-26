"""Face fix, step 2: erase the sideways mouth and redraw it upright and symmetric on the head's centre line (x = 234.5).
Same black / coral colours, same size and vertical position as the original. Nothing outside the old mouth changes."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
CX, CY = 234.5, 536.0          # centre line of the head; vertical centre of the original mouth
A, B_TOP, B_BOT, N_BOT = 37.0, 41.0, 41.0, 3.0
CLIP_Y = CY + 41.0             # flat jaw line
TONGUE_BASE, TONGUE_H, TONGUE_HW = CY + 34.0, 30.0, 25.0
a = np.asarray(Image.open(src).convert('RGB')).copy()
dark = a.sum(axis=2) < 200
red = (a[:, :, 0] > 200) & (a[:, :, 1] < 140) & (a[:, :, 2] < 140)
box = np.zeros(dark.shape, bool); box[490:584, 238:318] = True
# the mouth is the dark blob(s) + coral tongue in that box; the head outline is not part of it (flood fill from the mouth centre)
cand = (dark | red) & box
lab = np.zeros(cand.shape, bool); stack = [(540, 282)]
while stack:
    y, x = stack.pop()
    if lab[y, x] or not cand[y, x]: continue
    lab[y, x] = True
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if 0 <= y + dy < cand.shape[0] and 0 <= x + dx < cand.shape[1]: stack.append((y + dy, x + dx))
grown = np.asarray(Image.fromarray((lab * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 127
a[grown] = (253, 253, 253)
out = Image.fromarray(a)
# --- new mouth, supersampled
SS = 8
X0, Y0, X1, Y1 = 190, 488, 280, 590
W, H = (X1 - X0) * SS, (Y1 - Y0) * SS
def P(x, y): return ((x - X0) * SS, (y - Y0) * SS)
pts = []
for k in range(720):
    t = 2 * math.pi * k / 720
    c, s = math.cos(t), math.sin(t)
    if s <= 0:                               # upper half: ellipse
        x, y = A * c, B_TOP * s
    else:                                    # lower half: squarer (superellipse) so the jaw is wide and flat
        e = 2.0 / N_BOT
        x = A * math.copysign(abs(c) ** e, c); y = B_BOT * (abs(s) ** e)
    pts.append((CX + x, min(CY + y, CLIP_Y)))
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).polygon([P(*p) for p in pts], fill=255)
tong = Image.new('L', (W, H), 0); td = ImageDraw.Draw(tong)
tp = [(CX + TONGUE_HW * math.cos(math.pi * k / 90), TONGUE_BASE - TONGUE_H * math.sin(math.pi * k / 90)) for k in range(0, 91)] + \
     [(CX - TONGUE_HW * math.cos(math.pi * k / 90), TONGUE_BASE - TONGUE_H * math.sin(math.pi * k / 90)) for k in range(90, 181)]
tp = [(CX + TONGUE_HW * math.cos(math.pi * k / 180), TONGUE_BASE - TONGUE_H * math.sin(math.pi * k / 180)) for k in range(0, 181)]
td.polygon([P(*p) for p in tp], fill=255)
small = lambda m: m.resize((X1 - X0, Y1 - Y0), Image.LANCZOS)
out.paste((0, 0, 0), (X0, Y0), small(mask))
out.paste((242, 74, 63), (X0, Y0), small(tong))
out.save(dst)
