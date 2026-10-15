"""Evil-laugh hook, v2: eyes, brows and head stay EXACTLY as in the clip (same face as the wink/flick). Only the smirk line
opens into a laughing mouth and closes back into the same smirk line."""
import cv2, numpy as np, sys, math, os
from scipy import ndimage as ndi
sys.path.insert(0, 'tools')
import tagfix2 as T

FPS = 24
T0, TEND = 0.10, 2.40
RAMP_IN, RAMP_OUT = 0.10, 0.12
BEAT = 0.34
S = 4
INK = (10, 10, 14)

def beat(t):
    return 0.5 + 0.5 * math.sin(2 * math.pi * (t - T0) / BEAT - math.pi / 2)    # 0..1

def env(t):
    if t < T0 or t >= TEND: return 0.0
    if t < T0 + RAMP_IN: return 0.5 - 0.5 * math.cos(math.pi * (t - T0) / RAMP_IN)
    if t > TEND - RAMP_OUT: return 0.5 + 0.5 * math.cos(math.pi * (t - (TEND - RAMP_OUT)) / RAMP_OUT)
    return 1.0

def head_geom(im):
    white = (im.min(axis=2) > 236)
    lab, n = ndi.label(white)
    k = int(np.argmax(ndi.sum(white, lab, range(1, n + 1)))) + 1
    M = ndi.binary_fill_holes(lab == k)
    Min = cv2.erode(M.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(bool)
    ys, xs = np.where(M)
    return M, Min, np.array([xs.mean(), ys.mean()]), (ys.max() - ys.min()) / 2.0

def mouth_component(im, Min, c, R):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    dark = (gray < 140) & Min
    lab, n = ndi.label(dark)
    best = None
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 300: continue
        if ys.mean() > c[1] + 0.2 * R and (xs.max() - xs.min()) > 0.4 * R:
            if best is None or len(ys) > best[0]: best = (len(ys), i)
    return None if best is None else (lab == best[1])

def laugh_mouth(im, t):
    M, Min, c, R = head_geom(im)
    comp = mouth_component(im, Min, c, R)
    if comp is None: return im
    ys, xs = np.where(comp)
    xmin, xmax = xs.min(), xs.max()
    cols = np.arange(xmin, xmax + 1)
    ymid = np.array([ys[xs == x].mean() if (xs == x).any() else np.nan for x in cols])
    good = ~np.isnan(ymid)
    ymid = np.interp(cols, cols[good], ymid[good])
    ymid = np.convolve(np.pad(ymid, 6, mode='edge'), np.ones(13) / 13, mode='valid')
    th = max(6.0, len(ys) / float(len(cols)))
    # erase the original smirk line (inpaint), then redraw it as the upper lip of the laughing mouth
    F = cv2.dilate(comp.astype(np.uint8), np.ones((9, 9), np.uint8))
    y0, y1, x0, x1 = max(0, ys.min() - 40), min(im.shape[0], ys.max() + 160), max(0, xmin - 40), min(im.shape[1], xmax + 40)
    canvas = im[y0:y1, x0:x1].copy()
    ip = cv2.inpaint(canvas, (F[y0:y1, x0:x1] * 255).astype(np.uint8), 5, cv2.INPAINT_TELEA)
    base = im.copy()
    base[y0:y1, x0:x1] = np.where(Min[y0:y1, x0:x1, None], ip, canvas)
    amp = env(t) * (0.12 + 0.88 * beat(t))
    depth = 0.36 * R * amp
    h, w = y1 - y0, x1 - x0
    ink = np.zeros((h * S, w * S), np.uint8)
    teeth = np.zeros((h * S, w * S), np.uint8)
    P = lambda x, y: (int(round((x - x0) * S)), int(round((y - y0) * S)))
    u = 2 * (cols - xmin) / float(max(1, xmax - xmin)) - 1
    prof = np.clip(1 - u ** 2, 0, 1) ** 0.75
    top = [P(x, y) for x, y in zip(cols, ymid)]
    bot = [P(x, y + depth * p) for x, y, p in zip(cols[::-1], ymid[::-1], prof[::-1])]
    if depth > 1.5:
        cv2.fillPoly(ink, [np.array(top + bot, np.int32)], 255, cv2.LINE_AA)
        cv2.polylines(ink, [np.array(bot, np.int32)], False, 255, int(th * S), cv2.LINE_AA)
        if depth > 0.13 * R:
            td = min(0.075 * R, depth * 0.42)
            inner = slice(int(len(cols) * 0.1), int(len(cols) * 0.9))
            tt = [P(x, y + th * 0.5 + 1) for x, y in zip(cols[inner], ymid[inner])]
            tb = [P(x, y + th * 0.5 + 1 + min(td, depth * p * 0.8)) for x, y, p in zip(cols[inner][::-1], ymid[inner][::-1], prof[inner][::-1])]
            cv2.fillPoly(teeth, [np.array(tt + tb, np.int32)], 255, cv2.LINE_AA)
    cv2.polylines(ink, [np.array(top, np.int32)], False, 255, int(th * S), cv2.LINE_AA)
    for pt in (top[0], top[-1]):
        cv2.circle(ink, pt, int(th * S / 2), 255, -1, cv2.LINE_AA)
    ink = cv2.resize(ink, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    teeth = cv2.resize(teeth, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    mm = Min[y0:y1, x0:x1].astype(np.float32)
    ink *= mm; teeth *= mm
    reg = base[y0:y1, x0:x1].astype(np.float32)
    reg = reg * (1 - ink[..., None]) + np.array(INK, np.float32) * ink[..., None]
    reg = reg * (1 - teeth[..., None]) + 250.0 * teeth[..., None]
    base[y0:y1, x0:x1] = np.clip(reg, 0, 255).astype(np.uint8)
    return base

def main(src_dir, out_dir, n_frames=97):
    os.makedirs(out_dir, exist_ok=True)
    for n in range(1, n_frames + 1):
        im = cv2.imread(f'{src_dir}/{n:03d}.png')
        t = (n - 1) / FPS
        out, env_, hull = T.fix_tag(im)
        if env(t) > 0:
            out = laugh_mouth(out, t)
        cv2.imwrite(f'{out_dir}/{n:03d}.png', out)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
