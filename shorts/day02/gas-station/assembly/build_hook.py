"""Programmatic hook for the gas-station short, built from approved image 1 (no model, no Kling).

Layers (bottom to top):
  1. plate   = image 1 with the mascot's head/shirt/tie and both black arms painted out to the flat blue
               background. Pump, car, nozzle, hose, coin, ground and legs are untouched and never move.
  2. arms    = two black arms drawn fresh with two-bone IK doing the 6-7 seesaw at hip height.
  3. body    = head + shirt + tie cut out of image 1, shifted by whole pixels per row (rigid for the head,
               sheared to zero at the hem so the feet/legs never move). Face pixels are copied, never redrawn.
"""
import json, math, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
SRC = HERE / "img01.png"
OUT = HERE / "hook_frames"
FPS = 30
DUR = 2.97            # shot 1 length = line 2 start in the trimmed voice timings
NF = int(round(FPS * DUR))
BG = np.array([0, 87, 240])

# ---- geometry (image-1 pixels, 752x1344) ----
HEAD_C, HEAD_R = (235, 480), 142
BODY_POLY = [(150, 585), (250, 580), (330, 580), (410, 640), (424, 700), (410, 760), (398, 858), (300, 860), (205, 860), (205, 785), (150, 735)]
NOZZLE_POLY = [(126, 779), (172, 762), (230, 772), (234, 796), (246, 799), (285, 817), (312, 835), (334, 852), (332, 872), (282, 884), (262, 892), (238, 894), (196, 884), (160, 856), (130, 812)]
LARM_POLY = [(166, 728), (209, 728), (209, 752), (194, 772), (166, 772)]
RARM_POLY = [(245 + 0, 350), (350, 300), (395, 380), (446, 500), (448, 610), (405, 720), (360, 800), (360, 890), (330, 900), (325, 800), (300, 640), (262, 450), (245, 370)]
RARM_POLY = [(300 + x / 4, 620 + y / 4) for x, y in RARM_POLY]
HEM_Y, NECK_Y = 852, 640
SH_L, SH_R = (190, 728), (372, 698)       # where the arms leave the cuffs
HAND_L0, HAND_R0 = (232, 768), (335, 752)  # neutral hand positions (hip height)
AMP = 28                                    # hand rise/dip in px
SWAY = 5                                    # head sway in px each way
PERIOD = 0.4                                # seconds per full seesaw cycle
L1 = L2 = 57
TILT = 16                                   # degrees of hand tilt at peak speed


def poly_mask(size, poly, ss=4):
    m = Image.new("L", (size[0] * ss, size[1] * ss), 0)
    ImageDraw.Draw(m).polygon([(x * ss, y * ss) for x, y in poly], fill=255)
    return m.resize(size, Image.LANCZOS)


def build_layers(src):
    W, H = src.size
    a = np.asarray(src).astype(int)
    notbg = (np.abs(a - BG).sum(axis=2) > 70)
    body_region = np.zeros((H, W), bool)
    head = Image.new("L", (W, H), 0)
    ImageDraw.Draw(head).ellipse([HEAD_C[0] - HEAD_R, HEAD_C[1] - HEAD_R, HEAD_C[0] + HEAD_R, HEAD_C[1] + HEAD_R], fill=255)
    body_region |= np.asarray(head) > 127
    body_region |= np.asarray(poly_mask((W, H), BODY_POLY)) > 127
    arms_region = (np.asarray(poly_mask((W, H), LARM_POLY)) > 127) | (np.asarray(poly_mask((W, H), RARM_POLY)) > 127)
    nozzle = np.asarray(poly_mask((W, H), NOZZLE_POLY)) > 127
    body = body_region & notbg & ~arms_region & ~nozzle
    # fill small gaps inside the body (white shirt vs bg tolerance) by closing, but keep out of the nozzle
    bm = Image.fromarray((body * 255).astype(np.uint8))
    bm = bm.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    body = (np.asarray(bm) > 127) & ~nozzle & body_region
    arms = arms_region & notbg & ~body & ~nozzle
    fill = Image.fromarray(((body | arms) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
    nz_grow = np.asarray(Image.fromarray((nozzle * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(19))) > 127
    fill = (np.asarray(fill) > 127) & ~nz_grow
    fill[HEM_Y + 8:] = False
    plate = a.copy()
    plate[fill] = BG
    # body layer: pixels of the original within the body mask (grown 1px so antialiased edges come along)
    grown = Image.fromarray((body * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    grown = (np.asarray(grown) > 127) & ~nozzle & body_region
    return plate.astype(np.uint8), a.astype(np.uint8), grown


def row_shift(t):
    """integer dx per row for the upper body at time t"""
    s = math.sin(2 * math.pi * t / PERIOD)
    base = SWAY * s
    dx = np.zeros(1344, int)
    for y in range(1344):
        if y <= NECK_Y:
            w = 1.0
        elif y >= HEM_Y:
            w = 0.0
        else:
            w = (HEM_Y - y) / (HEM_Y - NECK_Y)
        dx[y] = int(round(base * w))
    return dx


def ik(S, H, L1, L2, side):
    dx, dy = H[0] - S[0], H[1] - S[1]
    d = min(math.hypot(dx, dy), L1 + L2 - 1e-3)
    d = max(d, abs(L1 - L2) + 1e-3)
    a = math.atan2(dy, dx)
    cosA = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)
    A = math.acos(max(-1, min(1, cosA)))
    best = None
    for sgn in (1, -1):
        ang = a + sgn * A
        E = (S[0] + L1 * math.cos(ang), S[1] + L1 * math.sin(ang))
        score = E[0] * side  # side=-1 left arm wants smaller x, +1 right arm wants larger x
        if best is None or score > best[0]:
            best = (score, E)
    return best[1]


def hand_poly(wrist, fa, side):
    """Open palm, fingers together, slightly cupped, palm up. Local frame: +x along the forearm, +u = screen-up side."""
    n = (-math.sin(fa), math.cos(fa))
    if n[1] > 0:
        n = (-n[0], -n[1])          # make n point to screen-up
    ux, uy = math.cos(fa), math.sin(fa)
    def P(x, u):
        return (wrist[0] + ux * x + n[0] * u, wrist[1] + uy * x + n[1] * u)
    pts = []
    # fingers+palm as one cupped paddle: lower edge, then upper edge, tip curls toward 'up'
    N = 14
    low, upp = [], []
    for k in range(N + 1):
        x = 4 + 54 * k / N
        c = 8 * (k / N) ** 2                      # cup: tip lifts
        half = 19.0 - 4.0 * (k / N) ** 2          # wide flat palm, slight taper
        low.append(P(x, c - half))
        upp.append(P(x, c + half))
    # rounded fingertip
    tip = [P(58 + 6 * math.sin(th), 9 + (12.5 - 3.5) * math.cos(th) * 0.0 + 0) for th in []]
    paddle = low + upp[::-1]
    return paddle, P

def draw_hand(d, wrist, fa, side, SS, off):
    paddle, P = hand_poly(wrist, fa, side)
    pts = [((x - off[0]) * SS, (y - off[1]) * SS) for x, y in paddle]
    d.polygon(pts, fill=255)
    # rounded fingertip + wrist
    for (x, u, r) in ((55, 8, 15.0), (6, 0, 19.0)):
        cx, cy = P(x, u)
        cx, cy = (cx - off[0]) * SS, (cy - off[1]) * SS
        d.ellipse([cx - r * SS, cy - r * SS, cx + r * SS, cy + r * SS], fill=255)
    # thumb: separate capsule splaying up-and-away, with a notch between thumb and fingers
    t0, t1 = P(14, 19), P(36, 46)
    d.line([((t0[0] - off[0]) * SS, (t0[1] - off[1]) * SS), ((t1[0] - off[0]) * SS, (t1[1] - off[1]) * SS)], fill=255, width=int(13 * SS))
    for p in (t0, t1):
        cx, cy = (p[0] - off[0]) * SS, (p[1] - off[1]) * SS
        d.ellipse([cx - 6.5 * SS, cy - 6.5 * SS, cx + 6.5 * SS, cy + 6.5 * SS], fill=255)


def draw_arms(frame, t, dxrow, part):
    SS = 4
    x0, y0, x1, y1 = 60, 640, 500, 940
    w, h = (x1 - x0), (y1 - y0)
    im = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(im)
    ph = 2 * math.pi * t / PERIOD
    s, c = math.sin(ph), math.cos(ph)
    arms = [(-1, (SH_L[0] + dxrow[SH_L[1]], SH_L[1]), (HAND_L0[0], HAND_L0[1] - AMP * s), c),    # left rises when s grows
            (+1, (SH_R[0] + dxrow[SH_R[1]], SH_R[1]), (HAND_R0[0], HAND_R0[1] + AMP * s), -c)]  # right rises when s falls
    LW = 24
    for side, S, Hd, rise in arms:
        E = ik(S, Hd, L1, L2, side)
        P = lambda p: ((p[0] - x0) * SS, (p[1] - y0) * SS)
        if part == "upper":   # behind the shirt: starts well inside the sleeve so no cap shows on the cuff
            S2 = (S[0] + (E[0] - S[0]) * -0.35, S[1] + (E[1] - S[1]) * -0.35)
            d.line([P(S2), P(E)], fill=255, width=LW * SS)
            cx, cy = P(E)
            r = LW * SS / 2
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
            continue
        d.line([P(E), P(Hd)], fill=255, width=LW * SS)
        for p in (E, Hd):
            cx, cy = P(p)
            r = LW * SS / 2
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        # hand tilts with the motion: fingertips lift as the hand rises, drop as it dips
        fa = math.atan2(Hd[1] - E[1], Hd[0] - E[0])
        fa = fa - rise * math.radians(TILT) * (1 if side < 0 else -1)
        draw_hand(d, Hd, fa, side, SS, (x0, y0))
    m = np.asarray(im.resize((w, h), Image.LANCZOS)).astype(float) / 255
    out = frame.astype(float)
    reg = out[y0:y1, x0:x1]
    reg[:] = reg * (1 - m[..., None])  # black arms
    return out.astype(np.uint8)


def render_frame(i, plate, orig, body):
    t = i / FPS
    dxrow = row_shift(t)
    f = draw_arms(plate.copy(), t, dxrow, "upper")
    H, W = body.shape
    ys = np.where(body.any(axis=1))[0]
    for y in ys:
        xs = np.where(body[y])[0]
        dx = dxrow[y]
        nx = xs + dx
        ok = (nx >= 0) & (nx < W)
        f[y, nx[ok]] = orig[y, xs[ok]]
    return draw_arms(f, t, dxrow, "lower")


if __name__ == "__main__":
    src = Image.open(SRC).convert("RGB")
    plate, orig, body = build_layers(src)
    OUT.mkdir(exist_ok=True)
    Image.fromarray(plate).save(HERE / "hook_plate.png")
    Image.fromarray((body * 255).astype(np.uint8)).save(HERE / "hook_bodymask.png")
    frames = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else range(NF)
    for i in frames:
        Image.fromarray(render_frame(i, plate, orig, body)).save(OUT / f"f{i:03d}.png")
    print("frames", NF, "dur", NF / FPS)
