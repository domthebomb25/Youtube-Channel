"""Hotel Short renderer. usage: python3 build_hotel.py [--preview] [--debug DIR]
Hook clip = clips/hook.mp4 (speed-matched to line 1), stills in images/, voice in clips/voiceover.mp3, config in config.py.
Frame 0 and the final loop frame are built from the SAME image-1 file with no transform, so the loop is pixel-exact."""
import importlib.util, json, math, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[2]
sys.path.insert(0, str(REPO / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402
spec = importlib.util.spec_from_file_location("cfg", HERE / "config.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

W, H, FPS = 1080, 1920, 30
CAP_Y = 1330
CAP_Y_SHOT = getattr(C, "CAP_Y_SHOT", {})  # per-shot caption y overrides (keep props readable)
NARR, SHOTS = C.NARR, C.SHOTS
DEBUG = Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None


def merge_numbers(ws):
    out, i = [], 0
    while i < len(ws):
        if ws[i][0] == "one" and i + 1 < len(ws) and ws[i + 1][0] == "hundred":
            if i + 2 < len(ws) and ws[i + 2][0] == "ten":
                out.append(("110", ws[i][1], ws[i + 2][2])); i += 3; continue
            out.append(("100", ws[i][1], ws[i + 1][2])); i += 2; continue
        out.append(tuple(ws[i])); i += 1
    return out


def load(name):
    im = Image.open(ROOT / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def view(img, motion, p):
    if motion == "static":
        return img.copy()
    e = 1 - (1 - p) ** 2
    z = {"in": 1 + 0.08 * e, "out": 1.08 - 0.08 * e, "hold": 1.0 + 0.03 * p}[motion]
    cw, ch = W / z, H / z
    x, y = (W - cw) / 2, (H - ch) / 2
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def probe_dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def load_hook():
    dur = probe_dur(ROOT / "clips/hook.mp4")
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ROOT / "clips/hook.mp4"), "-vf",
                          f"setpts=PTS*{C.HOOK_END / dur:.5f},scale={W}:{H}:force_original_aspect_ratio=increase,"
                          f"crop={W}:{H},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return [Image.frombuffer("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw), W * H * 3)]


def find_spark(frames):
    """First frame with the big white-yellow star flash (the key cards touching)."""
    for i, f in enumerate(frames):
        a = np.asarray(f)[350:1300].astype(int)
        n = int(((a[..., 0] > 245) & (a[..., 1] > 240) & (a[..., 2] > 190) & (a[..., 2] < 235)).sum())
        if n > 1000:
            return i, n
    raise SystemExit("spark not found")


def hook_layers():
    lines, y1, y2, size = C.HOOK_TEXT
    f = min((m.fit(t, W - 140, size) for t in lines), key=lambda x: x.size)
    out = []
    for t, y, col in zip(lines, (y1, y2), (m.WHITE, m.YEL)):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        m.outlined(ImageDraw.Draw(lay), (W / 2, y), t, f, col)
        out.append(lay)
    return out, f.size


def shifted(lay, dx, dy):
    return lay.transform((W, H), Image.AFFINE, (1, 0, -dx, 0, 1, -dy), Image.BILINEAR)


def main():
    preview = "--preview" in sys.argv
    words = merge_numbers([tuple(w) for w in json.load(open(ROOT / "assembly/word_timing.json"))])
    gs = m.groups(words)
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    hook = load_hook()
    spark, cnt = find_spark(hook)
    print("hook frames", len(hook), "spark frame", spark, f"t={spark / FPS:.2f}s", "px", cnt)
    layers, tsize = hook_layers()
    cap_f = m.font(92)
    cta_a, cta_b, cta_lines = C.CTA
    fa, fb = m.font(40), m.font(30)
    nfr = int(round(NARR * FPS))
    starts = [s[0] for s in SHOTS] + [NARR]

    def base(i):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t)
        t0, name, mo = SHOTS[k]
        if name == "hook":
            if i == 0:
                return imgs["img01"].copy()
            fr = hook[min(i, len(hook) - 1)]
            if i < 4:
                return Image.blend(imgs["img01"], fr, i / 4)
            return fr.copy()
        return view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0))

    assert np.array_equal(np.asarray(base(0)), np.asarray(base(nfr - 1))), "loop frames differ"
    print("loop check: frame 0 and last frame (no overlays) are pixel-identical")

    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else "hotel-overbooking.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(ROOT / "clips/voiceover.mp3"), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{NARR:.3f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    dbg = {0, nfr - 1, *range(spark - 2, spark + 14), *[int(a * FPS) + 25 for a, _, _ in SHOTS], int(26.0 * FPS)}
    for i in range(nfr):
        t = i / FPS
        fr = base(i).convert("RGBA")
        if t < C.HOOK_END:  # hook text from frame 0; shakes 3 frames at the spark, then blasts up and is gone
            if i < spark:
                for lay in layers: fr.alpha_composite(lay)
            elif i < spark + 3:
                s = 1 if (i - spark) % 2 == 0 else -1
                for lay in layers: fr.alpha_composite(shifted(lay, 16 * s, -6 * s))
            else:
                k = i - (spark + 2)
                dy = -(k * k) * 40
                if dy > -(C.HOOK_TEXT[1] + tsize):
                    for lay in layers: fr.alpha_composite(shifted(lay, 0, dy))
        if cta_a <= t < cta_b:
            d = ImageDraw.Draw(fr)
            m.outlined(d, (W / 2, 1858), cta_lines[0], fa, m.YEL)
            m.outlined(d, (W / 2, 1898), cta_lines[1], fb, m.WHITE)
        g = next((g for g in gs if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None) if t < NARR else None
        if g:
            d = ImageDraw.Draw(fr)
            cy = CAP_Y_SHOT.get(next(n for a, n, _ in reversed(SHOTS) if a <= t), CAP_Y)
            txt = [w[0].upper() for w in g]
            cf = cap_f
            while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50:
                cf = m.font(cf.size - 4)
            widths = [d.textlength(w + " ", font=cf) for w in txt]
            x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
            for w, wd, (_, a, b) in zip(txt, widths, g):
                m.outlined(d, (x, cy), w, cf, m.YEL if a - 0.05 <= t <= b + 0.05 else m.WHITE, anchor="lm")
                x += wd
        fr = fr.convert("RGB")
        if DEBUG and i in dbg:
            DEBUG.mkdir(parents=True, exist_ok=True)
            fr.save(DEBUG / f"f{i:04d}.png")
        if preview:
            fr = fr.resize((ow, oh), Image.BILINEAR)
        wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait()
    print(out, round(nfr / FPS, 2), "s video")


main()
