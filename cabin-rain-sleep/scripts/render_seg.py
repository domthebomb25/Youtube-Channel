"""Cabin rain scene, one 10-minute chunk. Everything repeats exactly every P seconds (so the chunk loops
seamlessly); only the rain-streak layout changes per chunk number.
Usage: render_seg.py BASE.png OUT.mp4 CHUNK_NUMBER [SECONDS] [START_SECONDS]
Set CHECK=1 to just verify that frame at t and t+600 are identical."""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter

base_path, out_path, seg = sys.argv[1], sys.argv[2], int(sys.argv[3])
secs = float(sys.argv[4]) if len(sys.argv) > 4 else 600.0
t0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
P = 600.0                      # loop length in seconds
W, H, FPS = 1920, 1080, 24
scene = np.random.default_rng(7)             # same for every chunk: flames, smoke, lantern pulse, zoom
rain_rng = np.random.default_rng(100 + seg)  # different for every chunk: where the rain streaks run

def snap(f):                   # nearest frequency that completes a whole number of cycles in P seconds
    return np.maximum(np.round(np.asarray(f) * P), 1) / P

base = np.asarray(Image.open(base_path).convert("RGB").resize((W, H), Image.LANCZOS), dtype=np.float32)
xs = np.arange(W, dtype=np.float32)
wall = np.clip((0.22 * W - xs) / (0.22 * W - 0.14 * W), 0, 1)
base = base * (1 - 0.10 * wall)[None, :, None]        # left wall 10% darker

# ---- rain on the glass only
m = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(m)
d.polygon([(442, 0), (1818, 0), (1818, 812), (700, 735), (442, 716)], fill=255)
d.rectangle((190, 310, 468, 900), fill=0)
d.rectangle((408, 658, 706, 900), fill=0)
d.rectangle((726, 716, 872, 900), fill=0)
glass_full = np.asarray(m.filter(ImageFilter.GaussianBlur(2.5)), dtype=np.float32) / 255.0
gx0, gx1, gy1 = 442, 1824, 815
glass = glass_full[0:gy1, gx0:gx1, None]
N = 340
span = gy1 + 110
sx = rain_rng.uniform(gx0, gx1 - 3, N)
sy0 = rain_rng.uniform(0, gy1, N)
spd = np.maximum(np.round(rain_rng.uniform(25, 140, N) * P / span), 1) * span / P     # whole laps per P
length = rain_rng.uniform(25, 110, N)
bright = rain_rng.uniform(0.35, 1.0, N)
wob_a = rain_rng.uniform(0, 14, N)
wob_w = 2 * np.pi * snap(rain_rng.uniform(0.2, 0.9, N) / (2 * np.pi))
wob_p = rain_rng.uniform(0, 6.28, N)
width = rain_rng.integers(1, 3, N)
RAIN_COLOR = np.array([200, 220, 255], dtype=np.float32)
OPACITY = 0.28

# ---- flames
FLAMES = [dict(x0=300, x1=372, yb=690, yt=578, amp=3.6, glow=0.10, seed=1),
          dict(x0=782, x1=818, yb=778, yt=724, amp=2.4, glow=0.12, seed=2)]
for fl in FLAMES:
    r = np.random.default_rng(fl["seed"] + 7)
    fl["fr"] = snap(r.uniform(0.7, 3.4, 6)); fl["ph"] = r.uniform(0, 6.28, 6)
    fl["ff"] = snap(r.uniform(2.0, 7.0, 4)); fl["fp"] = r.uniform(0, 6.28, 4)
    pad = 8
    y0, y1 = fl["yt"] - pad, fl["yb"] + pad
    x0, x1 = fl["x0"], fl["x1"]
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    cx, cy = (x0 + x1) / 2, (fl["yb"] + fl["yt"]) / 2
    fl["box"] = (y0, y1, x0, x1)
    fl["mask"] = np.clip(1.0 - (((xx - cx) / ((x1 - x0) / 2)) ** 2 + ((yy - cy) / ((y1 - y0) / 2)) ** 2), 0, 1) ** 0.6
    rows = np.arange(y0, y1, dtype=np.float32)
    fl["h"] = np.clip((fl["yb"] - rows) / (fl["yb"] - fl["yt"]), 0, 1) ** 1.4
    fl["cols"] = np.arange(x0, x1, dtype=np.float32)

def flame(frame, t):
    for fl in FLAMES:
        y0, y1, x0, x1 = fl["box"]
        sway = sum(np.sin(2 * np.pi * f * t + p) for f, p in zip(fl["fr"], fl["ph"])) / 3.0
        dx = fl["amp"] * sway * fl["h"]
        src = fl["cols"][None, :] - dx[:, None]
        i0 = np.clip(np.floor(src).astype(np.int32), x0 - 6, x1 + 4)
        fr = (src - np.floor(src))[..., None]
        rows = np.arange(y0, y1)[:, None]
        orig = frame[y0:y1, x0:x1].copy()
        warped = frame[rows, i0] * (1 - fr) + frame[rows, np.clip(i0 + 1, 0, W - 1)] * fr
        flut = 1 + fl["glow"] * sum(np.sin(2 * np.pi * f * t + p) for f, p in zip(fl["ff"], fl["fp"])) / 2.0
        lum = orig.mean(axis=2)
        w = (fl["mask"] * np.clip((lum - 140.0) / 80.0, 0, 1))[..., None]
        frame[y0:y1, x0:x1] = orig * (1 - w) + warped * flut * w

# ---- steam: ripple in the painted haze + slow scrolling smoke over the mug only
sy0_, sy1_, sx0_, sx1_ = 500, 668, 520, 740
_yy, _xx = np.mgrid[sy0_:sy1_, sx0_:sx1_].astype(np.float32)
STEAM_MASK = np.clip(1.0 - (((_xx - 625) / 105.0) ** 2 + ((_yy - 585) / 95.0) ** 2), 0, 1) ** 0.7
STEAM_ROWS = np.arange(sy0_, sy1_, dtype=np.float32)
STEAM_COLS = np.arange(sx0_, sx1_, dtype=np.float32)
SMOKE_BOX = (420, 668, 500, 740)
_sy, _sx = np.mgrid[SMOKE_BOX[0]:SMOKE_BOX[1], SMOKE_BOX[2]:SMOKE_BOX[3]].astype(np.float32)
_h = 668 - _sy
SMOKE_MASK = (np.exp(-(((_sx - (598 + _h * 0.20)) / (20 + _h * 0.17)) ** 2)) * np.clip(_h / 28.0, 0, 1) * np.clip((_sy - 425) / 110.0, 0, 1)).astype(np.float32)
SMOKE_Y = np.arange(SMOKE_BOX[0], SMOKE_BOX[1], dtype=np.float32)
SMOKE_X = np.arange(SMOKE_BOX[2], SMOKE_BOX[3], dtype=np.float32)
def _tex(shape, sig, seed_):
    t_ = gaussian_filter(np.random.default_rng(seed_).standard_normal(shape), sig, mode="wrap")
    lo, hi = np.percentile(t_, [3, 97])
    return np.clip((t_ - lo) / (hi - lo), 0, 1).astype(np.float32)
SMOKE = [dict(tex=_tex((1400, 700), (26, 15), 12), vy=-1400 * 5 / P, sx=14.0, k=35, ph=0.3, amt=0.17),
         dict(tex=_tex((1400, 700), (12, 8), 13), vy=-1400 * 8 / P, sx=9.0, k=55, ph=2.1, amt=0.10)]
WISP_COLOR = np.array([205, 175, 145], dtype=np.float32)

def steam(frame, t):
    dx = 2.6 * np.sin(2 * np.pi * (STEAM_ROWS / 150.0 + t * 109 / P)) + 1.4 * np.sin(2 * np.pi * (STEAM_ROWS / 63.0 + t * 194 / P))
    dx = dx * np.clip((668 - STEAM_ROWS) / 90.0, 0, 1)
    src = STEAM_COLS[None, :] - dx[:, None]
    i0 = np.clip(np.floor(src).astype(np.int32), 0, W - 2)
    fr = (src - np.floor(src))[..., None]
    rows = np.arange(sy0_, sy1_)[:, None]
    orig = frame[sy0_:sy1_, sx0_:sx1_].copy()
    warped = frame[rows, i0] * (1 - fr) + frame[rows, i0 + 1] * fr
    frame[sy0_:sy1_, sx0_:sx1_] = orig * (1 - STEAM_MASK[..., None]) + warped * STEAM_MASK[..., None]
    for layer in SMOKE:
        ys_ = (SMOKE_Y + t * layer["vy"]).astype(np.int32) % layer["tex"].shape[0]
        xs_ = (SMOKE_X + layer["sx"] * np.sin(2 * np.pi * t * layer["k"] / P + layer["ph"])).astype(np.int32) % layer["tex"].shape[1]
        dd = np.clip((layer["tex"][ys_[:, None], xs_[None, :]] - 0.50) * 3.0, 0, 1) * SMOKE_MASK
        frame[SMOKE_BOX[0]:SMOKE_BOX[1], SMOKE_BOX[2]:SMOKE_BOX[3]] += WISP_COLOR * (layer["amt"] * dd)[..., None]

# ---- lantern / candle brightness pulse (100% -> 96% -> 100%), computed on a small grid and enlarged
SW, SH = W // 4, H // 4
_fy, _fx = np.mgrid[0:SH, 0:SW].astype(np.float32) * 4
def _g(cx_, cy_, rr_):
    return np.exp(-(((_fx - cx_) ** 2 + (_fy - cy_) ** 2) / (2 * rr_ ** 2)))
G1, G2 = _g(336, 600, 190), _g(800, 750, 80)

def pulse_gain(t):
    k17 = 35
    p1 = 0.5 + 0.5 * np.sin(2 * np.pi * t / 4.0 + 0.4 + 0.6 * np.sin(2 * np.pi * t * k17 / P))
    p2 = 0.5 + 0.5 * np.sin(2 * np.pi * t * 194 / P + 1.7 + 0.6 * np.sin(2 * np.pi * t * k17 / P))
    small = (1 - 0.04 * (p1 * G1 + p2 * G2)).astype(np.float32)
    return np.asarray(Image.fromarray(small).resize((W, H), Image.BILINEAR), dtype=np.float32)[..., None]

ZOOM_MAX = 0.015

def render(t):
    frame = base.copy()
    a = np.zeros((gy1, gx1 - gx0), dtype=np.float32)
    ys = (sy0 + spd * t + wob_a * np.sin(wob_w * t + wob_p)) % span
    for k in range(N):
        head = int(ys[k]); top = max(0, head - int(length[k])); bot = min(gy1, head)
        if bot > top:
            x = int(sx[k]) - gx0
            a[top:bot, x:x + int(width[k])] += np.linspace(0, bright[k], bot - top, dtype=np.float32)[:, None]
    a = (np.clip(a, 0, 1)[..., None]) * glass
    box = frame[0:gy1, gx0:gx1]
    box[:] = box * (1 - OPACITY * a) + RAIN_COLOR * (OPACITY * a)
    flame(frame, t)
    steam(frame, t)
    frame *= pulse_gain(t)
    zs = 1.0 + ZOOM_MAX * (0.5 - 0.5 * np.cos(2 * np.pi * t / P))      # 100% -> 101.5% -> 100% over one chunk
    img = Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8))
    return img.transform((W, H), Image.AFFINE, (1 / zs, 0, W / 2 * (1 - 1 / zs), 0, 1 / zs, H / 2 * (1 - 1 / zs)), resample=Image.BILINEAR)

if os.environ.get("CHECK"):
    for tt in (0.0, 137.5, 301.0):
        a_, b_ = np.asarray(render(tt), dtype=float), np.asarray(render(tt + P), dtype=float)
        print(f"t={tt}: mean abs diff vs t+{P:.0f} = {np.abs(a_ - b_).mean():.4f}")
    sys.exit()

cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-maxrate", "800k", "-bufsize", "1600k", "-g", "48",
       "-force_key_frames", "expr:gte(t,n_forced*120)", "-pix_fmt", "yuv420p", "-threads", "2", "-movflags", "+faststart", out_path]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(int(secs * FPS)):
    proc.stdin.write(render(t0 + i / FPS).tobytes())
proc.stdin.close()
proc.wait()
