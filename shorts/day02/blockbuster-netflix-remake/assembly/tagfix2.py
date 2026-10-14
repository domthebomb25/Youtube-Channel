import cv2, numpy as np
from scipy import ndimage as ndi
REF = np.array([194, 236, 249], float)  # BGR tag cream

def red_mask(im):
    b, g, r = [im[..., i].astype(int) for i in range(3)]
    return (r > 170) & (g < 110) & (b < 110) & (r - g > 80)

def find_env(im):
    red = red_mask(im)
    lab, n = ndi.label(red)
    best = None
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        a = len(ys)
        if 250 < a < 9000:
            h, w = np.ptp(ys) + 1, np.ptp(xs) + 1
            if h < 230 and w < 230 and a / (h * w) > 0.3 and (best is None or a > best[0]):
                best = (a, xs.min(), xs.max(), ys.min(), ys.max(), i, lab)
    return best

def fix_tag_once(im, tol=48, near=70, minar=120, ck=21):
    env = find_env(im)
    if env is None:
        return im, None, None
    a, x0, x1, y0, y1, idx, lab_full = env
    pad = 200
    X0, X1, Y0, Y1 = max(0, x0 - pad), min(im.shape[1], x1 + pad), max(0, y0 - pad), min(im.shape[0], y1 + pad)
    sub = im[Y0:Y1, X0:X1].astype(float)
    d = np.sqrt(((sub - REF) ** 2).sum(axis=2))
    cm = d < tol
    cm = cv2.morphologyEx(cm.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)).astype(bool)
    envm = (lab_full[Y0:Y1, X0:X1] == idx)
    near_env = ndi.binary_dilation(envm, iterations=near)
    lab, n = ndi.label(cm)
    keep = []
    for i in range(1, n + 1):
        comp = lab == i
        ar = comp.sum()
        if minar < ar < 3200 and (comp & near_env).any():
            yy, xx = np.where(comp)
            if max(np.ptp(yy), np.ptp(xx)) > 150:
                continue
            mc = sub[comp].mean(axis=0)
            if np.sqrt(((mc - REF) ** 2).sum()) > T_MC[0]:
                continue
            keep.append(i)
    if not keep:
        return im, env, None
    if len(keep) > 1:
        areas = {i: (lab == i).sum() for i in keep}
        core = max(areas, key=areas.get)
        cy_, cx_ = ndi.center_of_mass(lab == core)
        keep = [i for i in keep if i == core or np.hypot(*(np.array(ndi.center_of_mass(lab == i)) - (cy_, cx_))) < 60]
    m = np.isin(lab, keep).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ck, ck)))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = np.zeros_like(m)
    for c in cnts:
        cv2.fillConvexPoly(hull, cv2.convexHull(c), 1)
    hull = cv2.erode(hull, np.ones((3, 3), np.uint8)).astype(bool)
    out = im.copy()
    out[Y0:Y1, X0:X1][hull] = REF.astype(np.uint8)
    full = np.zeros(im.shape[:2], bool)
    full[Y0:Y1, X0:X1] = hull
    return out, env, full


def fix_tag(im):
    last = None
    for tol, mcdist, minar, ck in ((48, 32, 120, 21), (62, 45, 120, 21), (78, 60, 60, 25), (90, 85, 30, 33)):
        T_MC[0] = mcdist
        out, env, info = fix_tag_once(im, tol=tol, minar=minar, ck=ck)
        last = (out, env, info)
        if info is not None or env is None:
            return out, env, info
    return last

T_MC = [32]
