"""Remove the wink from the hook clips: put the neutral right brow + open eye (from frame 1 of the flick clip) back on every frame."""
import cv2, numpy as np, sys, os
from scipy import ndimage as ndi

def head(im):
    white = (im.min(axis=2) > 236)
    lab, n = ndi.label(white)
    k = int(np.argmax(ndi.sum(white, lab, range(1, n + 1)))) + 1
    M = ndi.binary_fill_holes(lab == k)
    ys, xs = np.where(M)
    R = (ys.max() - ys.min()) / 2.0
    cy = (ys.max() + ys.min()) / 2.0
    cx = xs.min() + R if xs.min() > 3 else xs.max() - R
    return M, np.array([cx, cy]), R

REF = cv2.imread('w/001.png')
_, C1, R1 = head(REF)
# right brow + eye region in frame-1 coordinates
RX0, RX1, RY0, RY1 = 198, 322, 448, 578
gray1 = cv2.cvtColor(REF, cv2.COLOR_BGR2GRAY).astype(np.float32)
alpha1 = np.clip((215.0 - gray1) / 130.0, 0, 1)
box1 = np.zeros(REF.shape[:2], np.float32); box1[RY0:RY1, RX0:RX1] = 1
LX0, LX1, LY0, LY1 = 118, 212, 500, 569            # left brow + eye (also repaired: some frames smudge or close it)
box1[LY0:LY1, LX0:LX1] = 1
patch_alpha = alpha1 * box1                      # neutral right brow + eye (black strokes)
ebox1 = np.zeros(REF.shape[:2], np.float32); ebox1[RY0 - 34:RY1 - 34, RX0 - 14:RX1 + 45] = 1; ebox1[LY0 - 6:LY1, LX0 - 6:LX1 + 6] = 1   # larger area in which the wink marks are erased

def fix(im):
    M, C, R = head(im)
    s = R / R1
    A = np.array([[s, 0, C[0] - s * C1[0]], [0, s, C[1] - s * C1[1]]], np.float32)   # frame1 -> this frame
    h, w = im.shape[:2]
    box = cv2.warpAffine(ebox1, A, (w, h), flags=cv2.INTER_NEAREST) > 0.5
    pa = cv2.warpAffine(patch_alpha, A, (w, h), flags=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    Min = ((xx - C[0]) ** 2 + (yy - C[1]) ** 2) < (0.90 * R) ** 2     # head interior as a disk (the white blob can be broken by the envelope)
    sat = im.max(axis=2).astype(np.int16) - im.min(axis=2).astype(np.int16)
    ok = (sat < 70)                     # skip coloured pixels (the red envelope in front of the face)
    ok_paste = ~cv2.dilate((~ok).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    ok = ~cv2.dilate((~ok).astype(np.uint8), np.ones((11, 11), np.uint8)).astype(bool)   # keep the envelope and its outline untouched when erasing
    dark = ((gray < 200) & box & Min & ok).astype(np.uint8)
    dark = cv2.dilate(dark, np.ones((7, 7), np.uint8))
    ys, xs = np.where(M)
    y0, y1, x0, x1 = max(0, ys.min() - 5), min(h, ys.max() + 5), max(0, xs.min() - 5), min(w, xs.max() + 5)
    canvas = im[y0:y1, x0:x1].copy()
    canvas[~Min[y0:y1, x0:x1]] = 255
    canvas[~ok[y0:y1, x0:x1]] = 255
    ip = cv2.inpaint(canvas, (dark[y0:y1, x0:x1] * 255).astype(np.uint8), 6, cv2.INPAINT_TELEA)
    out = im.copy()
    m_ = Min[y0:y1, x0:x1] & (dark[y0:y1, x0:x1] > 0)
    out[y0:y1, x0:x1][m_] = ip[m_]
    pa = pa * (Min & ok_paste)
    res = out.astype(np.float32) * (1 - pa[..., None]) + np.array([12, 12, 16], np.float32) * pa[..., None]
    return np.clip(res, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    src, dst, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    os.makedirs(dst, exist_ok=True)
    for n in range(a, b + 1):
        cv2.imwrite(f'{dst}/{n:03d}.png', fix(cv2.imread(f'{src}/{n:03d}.png')))
