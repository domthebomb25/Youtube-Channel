import cv2, numpy as np
from scipy import ndimage as ndi

def find_env(im):
    b, g, r = [im[..., i].astype(int) for i in range(3)]
    red = (r > 170) & (g < 100) & (b < 100) & (r - g > 90)
    # ignore sunset area: keep blobs with solid red (large components) in lower 2/3 where envelope lives is not guaranteed -> use components
    lab, n = ndi.label(red)
    best = None
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        a = len(ys)
        if 300 < a < 9000:
            h, w = np.ptp(ys) + 1, np.ptp(xs) + 1
            if h < 220 and w < 220 and a / (h * w) > 0.35:
                if best is None or a > best[0]:
                    best = (a, xs.min(), xs.max(), ys.min(), ys.max())
    return best

def cream_mask(im):
    b, g, r = [im[..., i].astype(int) for i in range(3)]
    return (r > 205) & (g > 185) & (b > 120) & (b < 232) & (r - b > 22) & (r - b < 90)

def fix_tag(im, dbg=False):
    env = find_env(im)
    if env is None:
        return im, None
    a, x0, x1, y0, y1 = env
    pad = 170
    X0, X1, Y0, Y1 = max(0, x0 - pad), min(im.shape[1], x1 + pad), max(0, y0 - pad), min(im.shape[0], y1 + pad)
    sub = im[Y0:Y1, X0:X1]
    cm = cream_mask(sub)
    cm = cv2.morphologyEx(cm.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)).astype(bool)
    lab, n = ndi.label(cm)
    ex0, ex1, ey0, ey1 = x0 - X0, x1 - X0, y0 - Y0, y1 - Y0
    out = im.copy()
    found = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        ar = len(ys)
        if not (250 < ar < 7000):
            continue
        # distance from the envelope bbox
        dx = max(ex0 - xs.max(), xs.min() - ex1, 0)
        dy = max(ey0 - ys.max(), ys.min() - ey1, 0)
        if max(dx, dy) > 90:
            continue
        found.append(i)
    if not found:
        return im, env
    m = np.isin(lab, found).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = np.zeros_like(m)
    for c in cnts:
        cv2.fillConvexPoly(hull, cv2.convexHull(c), 1)
    hull = cv2.erode(hull, np.ones((3, 3), np.uint8))
    px = sub[cm & (lab > 0)]
    col = np.median(px, axis=0) if len(px) else np.array([200, 225, 245])
    s = out[Y0:Y1, X0:X1]
    s[hull.astype(bool)] = col
    return out, env
