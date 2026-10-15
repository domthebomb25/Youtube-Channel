"""Post fixes after make_hook.py: replace 3 undetectable tag frames with neighbours, hand-boxed tag fill for the last 4 frames."""
import cv2, numpy as np, sys, shutil
from scipy import ndimage as ndi
sys.path.insert(0, 'tools'); import tagfix2 as T
SRC, OUT = sys.argv[1], sys.argv[2]
for dst, src in ((85, 84), (89, 88), (90, 91)):
    shutil.copy(f'{OUT}/{src:03d}.png', f'{OUT}/{dst:03d}.png')
boxes = {94: (540, 612, 860, 1034), 95: (552, 624, 985, 1096), 96: (552, 610, 1003, 1172), 97: (572, 636, 1153, 1247)}
def fix_box(im, box, tol=52):
    x0, x1, y0, y1 = box
    sub = im[y0:y1, x0:x1].astype(float)
    d = np.sqrt(((sub - T.REF) ** 2).sum(axis=2))
    m = cv2.morphologyEx((d < tol).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    lab, n = ndi.label(m)
    if n == 0: return im
    sizes = ndi.sum(m, lab, range(1, n + 1))
    mm = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 40]).astype(np.uint8)
    mm = cv2.morphologyEx(mm, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    cnts, _ = cv2.findContours(mm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = np.zeros_like(mm)
    for c in cnts: cv2.fillConvexPoly(hull, cv2.convexHull(c), 1)
    hull = cv2.erode(hull, np.ones((3, 3), np.uint8)).astype(bool)
    out = im.copy(); out[y0:y1, x0:x1][hull] = T.REF.astype(np.uint8)
    return out
for n, b in boxes.items():
    cv2.imwrite(f'{OUT}/{n:03d}.png', fix_box(cv2.imread(f'{SRC}/{n:03d}.png'), b))
