"""Face fix as a still: erase both eye ovals from ORIGINAL image 1 and redraw TWO IDENTICAL ovals (one oval pasted twice),
symmetric about the head's vertical centre line (x = 234.5), tops at the same height. Nothing else is touched."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
EYE_W, EYE_H = 24, 45          # one size for both eyes
TOP = 447                      # same top for both
XL, XR = 188, 258              # XL + XR + EYE_W - 1 = 2 * 234.5  -> mirror images about the centre line
a = np.asarray(Image.open(src).convert('RGB')).copy()
dark = a.sum(axis=2) < 200
def comp(box):
    x0, y0, x1, y1 = box; m = np.zeros(dark.shape, bool); m[y0:y1, x0:x1] = dark[y0:y1, x0:x1]; return m
eyes = comp((226, 440, 262, 494)) | comp((300, 420, 334, 478))   # the two eye ovals only (brows and mouth are outside these boxes)
grown = np.asarray(Image.fromarray((eyes * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 127
white = np.median(a[grown == False][:0].reshape(-1, 3), axis=0) if False else np.array([253, 253, 253])
grown[494:] = False                                      # never reach the mouth (its top edge starts at y=495)
a[grown] = white
out = Image.fromarray(a)
SS = 8
m = Image.new('L', (EYE_W * SS, EYE_H * SS), 0)
ImageDraw.Draw(m).ellipse([0, 0, EYE_W * SS - 1, EYE_H * SS - 1], fill=255)
oval = m.resize((EYE_W, EYE_H), Image.LANCZOS)            # ONE oval
patch = Image.new('RGB', (EYE_W + 6, EYE_H + 4), (253, 253, 253))   # identical flat white under each eye so the two copies match to the pixel
for x in (XL, XR):
    out.paste(patch, (x - 3, TOP - 2))
    out.paste((0, 0, 0), (x, TOP), oval)                                # the same oval, twice
out.save(dst)
