"""Evil-laugh variant of the hook: replaces the head-shake section (t < T_END) with a drawn evil laugh. Everything else is untouched."""
import cv2, numpy as np, sys, math, os
from scipy import ndimage as ndi
sys.path.insert(0, 'tools')
import tagfix2 as T
import make_hook as H

FPS = 24
T0, TEND = 0.10, 2.40
FADE_IN, FADE_OUT = 0.07, 0.09
BEAT = 0.34            # seconds per "ha"
C1 = np.array([224.1, 706.9]); R1 = 199.5   # head centre / radius in frame 1
S = 4                  # supersampling
INK = (10, 10, 14)

def openness(t):
    ph = 2 * math.pi * (t - T0) / BEAT
    return 0.62 + 0.38 * math.sin(ph - math.pi / 2)       # 0.24 .. 1.0

def weight(t):
    if t < T0 or t >= TEND: return 0.0
    if t < T0 + FADE_IN: return (t - T0) / FADE_IN
    if t > TEND - FADE_OUT: return max(0.0, (TEND - t) / FADE_OUT)
    return 1.0

def head_geom(im):
    white = (im.min(axis=2) > 236)
    lab, n = ndi.label(white)
    k = int(np.argmax(ndi.sum(white, lab, range(1, n + 1)))) + 1
    M = ndi.binary_fill_holes(lab == k)
    Min = cv2.erode(M.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(bool)
    ys, xs = np.where(M)
    return M, Min, np.array([xs.mean(), ys.mean()]), (ys.max() - ys.min()) / 2.0

def draw_face(shape, c, R, o, wob):
    """Return (ink alpha, teeth alpha) float arrays of `shape` for the laughing face."""
    h, w = shape
    ink = np.zeros((h * S, w * S), np.uint8)
    teeth = np.zeros((h * S, w * S), np.uint8)
    P = lambda u, v: np.array([(c[0] + u * R) * S, (c[1] + v * R) * S])
    I = lambda pt: (int(round(pt[0])), int(round(pt[1])))
    # brows (V shaped, angry), thick rounded strokes
    th = int(0.105 * R * S)
    for a, b in (((-0.70, -0.37 - wob), (-0.13, -0.15 - wob)), ((0.72, -0.43 - wob), (0.10, -0.19 - wob))):
        cv2.line(ink, I(P(*a)), I(P(*b)), 255, th, cv2.LINE_AA)
        cv2.circle(ink, I(P(*a)), th // 2, 255, -1, cv2.LINE_AA); cv2.circle(ink, I(P(*b)), th // 2, 255, -1, cv2.LINE_AA)
    # eyes: narrowed ovals with a slanted lid cut
    for (eu, ev, inner_right) in ((-0.37, -0.02, True), (0.39, -0.06, False)):
        ctr = P(eu, ev + wob * 0.2)
        ell = np.zeros_like(ink)
        cv2.ellipse(ell, I(ctr), (int(0.15 * R * S), int(0.17 * R * S)), 0, 0, 360, 255, -1, cv2.LINE_AA)
        slant = 0.10 * R * S
        y0 = ctr[1] - 0.045 * R * S
        pts = np.array([[ctr[0] - 0.3 * R * S, y0 - (slant if inner_right else -slant)],
                        [ctr[0] + 0.3 * R * S, y0 - (-slant if inner_right else slant)],
                        [ctr[0] + 0.3 * R * S, y0 - 0.4 * R * S], [ctr[0] - 0.3 * R * S, y0 - 0.4 * R * S]], np.int32)
        cv2.fillPoly(ell, [pts], 0)
        ink = np.maximum(ink, ell)
    # open laughing mouth
    mc = (0.14, 0.38 - 0.02 * o + wob * 0.5)
    hw = 0.50
    depth = 0.07 + 0.34 * o
    us = np.linspace(-1, 1, 60)
    top = [P(mc[0] + hw * u, mc[1] - 0.09 * (u ** 2) - 0.02 * u) for u in us]
    bot = [P(mc[0] + hw * u, mc[1] - 0.09 * (u ** 2) - 0.02 * u + depth * (1 - u ** 2) ** 0.75) for u in us[::-1]]
    poly = np.array([I(p) for p in top + bot], np.int32)
    cv2.fillPoly(ink, [poly], 255, cv2.LINE_AA)
    cv2.polylines(ink, [poly], True, 255, int(0.03 * R * S), cv2.LINE_AA)
    # teeth: a white strip under the upper lip
    td = min(0.075, depth * 0.45)
    if depth > 0.14:
        tt = [P(mc[0] + hw * 0.88 * u, mc[1] - 0.09 * (0.88 * u) ** 2 - 0.02 * 0.88 * u + 0.025) for u in us]
        tb = [P(mc[0] + hw * 0.88 * u, mc[1] - 0.09 * (0.88 * u) ** 2 - 0.02 * 0.88 * u + 0.025 + td) for u in us[::-1]]
        cv2.fillPoly(teeth, [np.array([I(p) for p in tt + tb], np.int32)], 255, cv2.LINE_AA)
    ink = cv2.resize(ink, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    teeth = cv2.resize(teeth, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return ink, teeth

def laugh_frame(im, t):
    M, Min, c, R = head_geom(im)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    alpha = np.clip((215.0 - gray) / 130.0, 0, 1) * Min
    F = cv2.dilate(((alpha > 0.03) & Min).astype(np.uint8), np.ones((9, 9), np.uint8))
    ys, xs = np.where(M)
    y0, y1, x0, x1 = max(0, ys.min() - 5), ys.max() + 5, max(0, xs.min() - 5), xs.max() + 5
    canvas = im[y0:y1, x0:x1].copy()
    canvas[~Min[y0:y1, x0:x1]] = 255
    ip = cv2.inpaint(canvas, (F[y0:y1, x0:x1] * 255).astype(np.uint8), 6, cv2.INPAINT_TELEA)
    base = im.copy()
    m_ = Min[y0:y1, x0:x1]
    base[y0:y1, x0:x1][m_] = ip[m_]
    o = openness(t)
    wob = 0.012 * math.sin(2 * math.pi * (t - T0) / BEAT)
    ink, teeth = draw_face(im.shape[:2], c, R, o, wob)
    ink *= Min; teeth *= Min
    out = base.astype(np.float32)
    out = out * (1 - ink[..., None]) + np.array(INK, np.float32) * ink[..., None]
    out = out * (1 - teeth[..., None]) + 250.0 * teeth[..., None]
    return np.clip(out, 0, 255).astype(np.uint8), M, o

def main(src_dir, out_dir, n_frames=97):
    os.makedirs(out_dir, exist_ok=True)
    for n in range(1, n_frames + 1):
        im = cv2.imread(f'{src_dir}/{n:03d}.png')
        t = (n - 1) / FPS
        out, env, hull = T.fix_tag(im)
        w = weight(t)
        if w > 0:
            im = out
            lf, M, o = laugh_frame(im, t)
            # cross-fade original face <-> laugh face inside the head
            Min = cv2.erode(M.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(bool)
            mix = im.astype(np.float32).copy()
            mix[Min] = im[Min] * (1 - w) + lf[Min] * w
            mix = np.clip(mix, 0, 255).astype(np.uint8)
            im = mix   # head stays still; only the face changes
        else:
            im = out
        cv2.imwrite(f'{out_dir}/{n:03d}.png', im)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
