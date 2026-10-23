"""IKEA maze renderer (programmatic hook). usage (from repo root):
  python3 shorts/day02/ikea-maze/tools/build_ikea.py --test 0,0.033,0.2,0.5,0.8,1.5,2.37   # save test frames to scratch dir
  python3 shorts/day02/ikea-maze/tools/build_ikea.py --render [out.mp4]
Hook (shot 1) = zoom on the exact image 1 file + animated yellow arrows racing along ONE winding path. Nothing else moves."""
import heapq, json, math, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import distance_transform_edt, binary_opening

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[3] / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402

W, H, FPS = 1080, 1920, 30
CAP_Y = 1330
YEL, WHITE = m.YEL, m.WHITE
NARR = 28.08                      # voiceover length (s); trailing silence after last word ~0.17 s, no extra tail
NFR = 841                         # frames written (28.03 s); audio is cut to the video end
SHOTS = [(0.0, "img1", "hook"), (2.4, "img2", "in"), (5.7, "img3", "right"), (9.6, "img4", "in"), (12.4, "img5", "out"),
         (14.8, "img6", "in"), (17.0, "img7", "left"), (19.1, "img8", "in"), (20.5, "img9", "in"), (22.9, "img10", "in"),
         (25.7, "img1", "pullback")]
HOOK_END = SHOTS[1][0]
DIVE_T = 0.75                     # camera has landed close on the mascot by here (<= 0.8 s)
Z_END = 3.2
FACE_SRC = (536.0, 1072.0)        # mascot head centre in 1080x1920 frame coords at zoom 1
FACE_END = (540.0, 800.0)         # where the face sits on screen once landed
HOOK_TEXT = [("WHY IS IKEA", YEL), ("BUILT LIKE", WHITE), ("A MAZE?", WHITE)]
CTA = [("FOLLOW", YEL, 56), ("New business story tomorrow.", WHITE, 44)]


def load(name):
    im = Image.open(ROOT / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


# ---------- single winding arrow path over the open floor of image 1 ----------
def compute_route(clean_png, K=4):
    im = Image.open(clean_png).convert("RGB")
    a = np.asarray(im).astype(int)
    blue = (abs(a[..., 0] - 4) < 40) & (abs(a[..., 1] - 82) < 40) & (abs(a[..., 2] - 201) < 40)
    blue[:420] = False
    blue = binary_opening(blue, iterations=3)
    dg = distance_transform_edt(blue)[::K, ::K]
    ok = dg > 10 / K
    cost = np.where(ok, 1.0 + 60.0 / (dg + 1), np.inf)

    def snap(p):
        x, y = p[0] // K, p[1] // K
        ys, xs = np.nonzero(ok); i = np.argmin((xs - x) ** 2 + (ys - y) ** 2); return int(xs[i]), int(ys[i])

    def astar(s, t):
        h = lambda p: math.dist(p, t)
        pq = [(h(s), 0, s)]; g = {s: 0}; prev = {}
        while pq:
            _, gc, u = heapq.heappop(pq)
            if u == t: break
            if gc > g[u]: continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if not dx and not dy: continue
                    v = (u[0] + dx, u[1] + dy)
                    if not (0 <= v[0] < ok.shape[1] and 0 <= v[1] < ok.shape[0]) or not np.isfinite(cost[v[1], v[0]]): continue
                    ng = gc + cost[v[1], v[0]] * math.hypot(dx, dy)
                    if ng < g.get(v, 1e18): g[v] = ng; prev[v] = u; heapq.heappush(pq, (ng + h(v), ng, v))
        p = [t]
        while p[-1] != s: p.append(prev[p[-1]])
        return p[::-1]

    via = [(20, 1300), (330, 1030), (400, 905), (490, 600)]   # bottom-left entry, up the centre corridor, beside mascot, out the top
    nodes = [snap(p) for p in via]
    route = []
    for s, t in zip(nodes, nodes[1:]): route += astar(s, t)[:-1]
    route.append(nodes[-1])
    pts = np.array([(x * K + K / 2, y * K + K / 2) for x, y in route], float)
    for _ in range(25): pts[1:-1] = (pts[:-2] + 2 * pts[1:-1] + pts[2:]) / 4
    s = max(W / im.width, H / im.height)                       # to 1080x1920 frame coordinates (same cover+crop as load())
    pts = pts * s - np.array([(math.ceil(im.width * s) - W) // 2, (math.ceil(im.height * s) - H) // 2])
    cum = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    return pts, cum


def arrow_slots(pts, cum, spacing=150, margin=70):
    out, s = [], margin
    while s < cum[-1] - margin * 0.6:
        i = max(min(np.searchsorted(cum, s), len(cum) - 1), 1)
        f = (s - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-6); p = pts[i - 1] + (pts[i] - pts[i - 1]) * f
        j, k = min(i + 3, len(pts) - 1), max(i - 4, 0); v = pts[j] - pts[k]
        out.append((p[0], p[1], math.atan2(v[1], v[0]))); s += spacing
    return out


ARROW_SHAPE = [(-.5, -.13), (.125, -.13), (.125, -.38), (.5, 0), (.125, .38), (.125, .13), (-.5, .13)]


def arrow_layer(slots, t, SS=2, L=112, SQ=0.7):
    """Arrows light up one after another (fast), then a white-hot pulse keeps racing along the path."""
    lay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    REV = 0.04                                        # seconds between arrows lighting up
    for k, (x, y, ang) in enumerate(slots):
        t_on = (k + 1) / FPS if k == 0 else (k + 1) * REV
        age = t - t_on
        if age < 0: continue
        pop = max(0.0, 1 - age / 0.12)                # short pop-in
        wave = (t - 0.5 - k * 0.045) % 0.9            # sustained racing pulse after the reveal
        flash = max(pop, (1 - wave / 0.14) if (t > 0.5 and 0 <= wave < 0.14) else 0)
        sc = 1 + 0.45 * pop + 0.18 * flash
        fill = tuple(int(c + (e - c) * flash) for c, e in zip((255, 205, 0), (255, 250, 190)))
        q = []
        for px, py in ARROW_SHAPE:
            px, py = px * L * sc, py * L * sc
            q.append(((x + px * math.cos(ang) - py * math.sin(ang)) * SS, (y + (px * math.sin(ang) + py * math.cos(ang)) * SQ) * SS))
        d.polygon(q, fill=fill + (255,)); d.line(q + [q[0]], fill=(0, 0, 0, 255), width=4 * SS)
    return lay.resize((W, H), Image.LANCZOS)


# ---------- camera ----------
def zoom_view(img, z, face_screen, face_src=FACE_SRC):
    """Crop so the point face_src (frame coords at zoom 1) lands at face_screen on screen at zoom z. z==1 -> untouched image."""
    if z <= 1.0000001: return img
    cw, ch = W / z, H / z
    x = min(max(face_src[0] - face_screen[0] / z, 0), W - cw)
    y = min(max(face_src[1] - face_screen[1] / z, 0), H - ch)
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def hook_cam(t):
    p = min(t / DIVE_T, 1.0)
    e = 1 - (1 - p) ** 2                              # fast from the very first frame, settles on landing
    z = math.exp(math.log(Z_END) * e)
    sx = FACE_SRC[0] + (FACE_END[0] - FACE_SRC[0]) * e
    sy = FACE_SRC[1] + (FACE_END[1] - FACE_SRC[1]) * e
    return z, (sx, sy)


def view(img, motion, p):
    e = 1 - (1 - p) ** 2
    z, fx, fy = {"in": (1 + 0.10 * p, .5, .5), "out": (1.10 - 0.10 * p, .5, .5), "hold": (1.0 + 0.03 * p, .5, .5),
                 "right": (1.12, .44 + .12 * p, .5), "left": (1.12, .56 - .12 * p, .5), "up": (1.12, .5, .56 - .12 * p),
                 "settle": (1.0 + 0.08 * (1 - e), .5, .5)}[motion]
    if z <= 1.0000001: return img
    cw, ch = W / z, H / z
    x = min(max(fx * W - cw / 2, 0), W - cw)
    y = min(max(fy * H - ch / 2, 0), H - ch)
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


# ---------- text layers ----------
def text_layer(lines, y0, size, gap=1.06):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - 140, size).size for t, _ in lines)
    f = m.font(fs); y = y0
    for t, col in lines:
        m.outlined(d, ((W - d.textlength(t, font=f)) / 2, y), t, f, col, anchor="lm"); y += fs * gap
    return lay


def cta_layer():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); y = 1535
    for t, col, size in CTA:
        f = m.fit(t, W - 160, size); m.outlined(d, ((W - d.textlength(t, font=f)) / 2, y), t, f, col, anchor="lm"); y += size * 1.35
    return lay


class Builder:
    def __init__(self):
        self.imgs = {n: load(n) for n in {s[1] for s in SHOTS}}
        pts, cum = compute_route(ROOT / "images/img1_clean.png")
        self.slots = arrow_slots(pts, cum)
        words = json.load(open(ROOT / "assembly/word_timing.json"))
        self.groups = m.groups([tuple(w) for w in words])
        self.hook_txt = text_layer(HOOK_TEXT, 245, 96)
        self.cta = cta_layer()
        self.cap_f = m.font(92)
        self.starts = [s[0] for s in SHOTS] + [NARR]
        self.last_t = (NFR - 1) / FPS                  # time of the final written frame (shot 11 reaches the exact wide image here)

    def frame(self, t):
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t)
        t0, name, mo = SHOTS[k]
        if mo == "hook":
            base = self.imgs[name]
            if t > 0:                                  # frame 0 stays the untouched image; arrows start on the very next frame
                base = base.copy().convert("RGBA"); base.alpha_composite(arrow_layer(self.slots, t)); base = base.convert("RGB")
            z, scr = hook_cam(t)
            fr = zoom_view(base, z, scr)
            if z > 1.5: fr = fr.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
        elif mo == "pullback":
            # continuous pull-back: the hook's landing framing -> exact wide image 1 on the very last frame; linear in log-zoom, no ease, no hold
            q = min(max((t - t0) / (self.last_t - t0), 0.0), 1.0)
            e = 1 - q
            z = math.exp(math.log(Z_END) * e)
            scr = (FACE_SRC[0] + (FACE_END[0] - FACE_SRC[0]) * e, FACE_SRC[1] + (FACE_END[1] - FACE_SRC[1]) * e)
            fr = zoom_view(self.imgs[name], z, scr)
            if z > 1.5: fr = fr.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
        else:
            end = self.last_t if k == len(SHOTS) - 1 else self.starts[k + 1]
            fr = view(self.imgs[name], mo, min(max((t - t0) / (end - t0), 0), 1))
        fr = fr.convert("RGBA")
        if t == 0: return fr.convert("RGB")             # frame 0 = the bare image 1 (identical to the last frame); text starts on frame 1
        if t < HOOK_END: fr.alpha_composite(self.hook_txt)
        if SHOTS[9][0] <= t < SHOTS[10][0]: fr.alpha_composite(self.cta)
        g = next((g for g in self.groups if g[0][1] - 0.05 <= t <= g[-1][2] + (0.0 if g is self.groups[-1] else 0.25)), None)  # last caption ends with the last word: final frames carry no text
        if g:
            d = ImageDraw.Draw(fr); txt = [w[0].upper() for w in g]; cf = self.cap_f
            while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50: cf = m.font(cf.size - 4)
            widths = [d.textlength(w + " ", font=cf) for w in txt]
            x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
            for w, wd, (_, a, b) in zip(txt, widths, g):
                m.outlined(d, (x, CAP_Y), w, cf, YEL if a - 0.05 <= t <= b + 0.05 else WHITE, anchor="lm"); x += wd
        return fr.convert("RGB")


def main():
    b = Builder()
    if "--test" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--test") + 1].split(",")]
        out = Path(sys.argv[sys.argv.index("--test") + 2]); out.mkdir(exist_ok=True, parents=True)
        for t in ts: b.frame(t).save(out / f"t{t:06.3f}.png")
        return
    out = Path(sys.argv[sys.argv.index("--render") + 1]) if len(sys.argv) > sys.argv.index("--render") + 1 else ROOT / "BS-012-ikea-maze.mp4"
    nfr = NFR
    wr =subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-i", str(ROOT / "clips/voiceover.mp3"), "-map", "0:v", "-map", "1:a", "-af", f"atrim=0:{NARR}",
                           "-c:v", "libx264", "-preset", "medium", "-qp", "19", "-pix_fmt", "yuv420p", "-profile:v", "high", "-force_key_frames", f"0,{(NFR - 1) / FPS}",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(out)], stdin=subprocess.PIPE)
    for i in range(nfr): wr.stdin.write(b.frame(i / FPS).tobytes())
    wr.stdin.close(); wr.wait(); print(out)


main()
