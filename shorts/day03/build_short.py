"""Shared Short renderer. usage: python3 build_short.py <slug> [--preview]
Reads <slug>/assembly/config.py (NARR, FIRST_CUT, SHOTS, TEXT, SHAKE, OUT) + word_timing.json; hook clip = <slug>/clips/hook.mp4."""
import importlib.util, json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
slug = sys.argv[1]
ROOT = HERE / slug
sys.path.insert(0, str(HERE.parent.parent / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402
spec = importlib.util.spec_from_file_location("cfg", ROOT / "assembly/config.py")
C = importlib.util.module_from_spec(spec)
C.YEL, C.WHITE = m.YEL, m.WHITE
spec.loader.exec_module(C)

W, H, FPS = 1080, 1920, 30
CAP_Y = 1330
NARR, END_SEC = C.NARR, getattr(C, "END_SEC", 0.6)
SHOTS, TEXT, SHAKE = C.SHOTS, C.TEXT, getattr(C, "SHAKE", {})
ONES = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
TEENS = {"ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}


def merge_years(ws):
    out, i = [], 0
    while i < len(ws):
        if ws[i][0] in ("nineteen", "twenty") and i + 1 < len(ws) and ws[i + 1][0] in TEENS:
            out.append((str((1900 if ws[i][0] == "nineteen" else 2000) + TEENS[ws[i + 1][0]]), ws[i][1], ws[i + 1][2])); i += 2; continue
        if ws[i][0] == "twenty" and i + 2 < len(ws) and ws[i + 1][0] == "twenty" and ws[i + 2][0] in ONES:
            out.append((str(2020 + ONES[ws[i + 2][0]]), ws[i][1], ws[i + 2][2])); i += 3; continue
        if ws[i][0] == "thirty" and i + 1 < len(ws) and ws[i + 1][0] == "thousand":
            out.append(("30,000", ws[i][1], ws[i + 1][2])); i += 2; continue
        if ws[i][0] == "nineteen" and i + 2 < len(ws) and ws[i + 1][0] == "oh" and ws[i + 2][0] in ONES:
            out.append((str(1900 + ONES[ws[i + 2][0]]), ws[i][1], ws[i + 2][2])); i += 3; continue
        if ws[i][0] == "two" and i + 2 < len(ws) and ws[i + 1][0] == "thousand" and ws[i + 2][0] in ONES:
            out.append((str(2000 + ONES[ws[i + 2][0]]), ws[i][1], ws[i + 2][2])); i += 3; continue
        if ws[i][0] == "nineteen" and i + 1 < len(ws):
            n, a, b = ws[i + 1][0], ws[i][1], ws[i + 1][2]
            if n == "forties":
                out.append(("1940s", a, b)); i += 2; continue
            if n in TENS:
                v, j = TENS[n], i + 2
                if j < len(ws) and ws[j][0] in ONES:
                    v += ONES[ws[j][0]]; b = ws[j][2]; j += 1
                out.append((str(1900 + v), a, b)); i = j; continue
        out.append(ws[i]); i += 1
    return out


def load(name):
    im = Image.open(ROOT / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def view(img, motion, p):
    e = 1 - (1 - p) ** 2
    if isinstance(motion, dict):
        z = motion["z0"] + (motion["z1"] - motion["z0"]) * e
        fx, fy = motion["at"]
    else:
        z, fx, fy = {"in": (1 + 0.10 * p, .5, .5), "out": (1.10 - 0.10 * p, .5, .5), "hold": (1.0 + 0.03 * p, .5, .5),
                     "right": (1.12, .44 + .12 * p, .5), "left": (1.12, .56 - .12 * p, .5),
                     "up": (1.12, .5, .56 - .12 * p)}[motion]
    cw, ch = W / z, H / z
    x = min(max(fx * W - cw / 2, 0), W - cw)
    y = min(max(fy * H - ch / 2, 0), H - ch)
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def title_layer(lines, top, y0, size):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - 140, size).size for t in lines)
    f = m.font(fs)
    y = y0
    for i, t in enumerate(lines):
        tw = d.textlength(t, font=f)
        m.outlined(d, ((W - tw) / 2, y), t, f, top if i == 0 else m.WHITE, anchor="lm")
        y += fs * 1.08
    return lay


def main():
    preview = "--preview" in sys.argv
    words = json.load(open(ROOT / "assembly/word_timing.json"))
    gs = m.groups(merge_years([tuple(w) for w in words]))
    titles = [(t[0], t[1], title_layer(t[2], t[3], t[4], t[5])) for t in TEXT]
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    hook = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ROOT / "clips/hook.mp4"), "-vf",
                           f"setpts=PTS*{SHOTS[1][0]}/4.04,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    hook = [Image.frombuffer("RGB", (W, H), hook[i:i + W * H * 3]) for i in range(0, len(hook), W * H * 3)]
    cap_f = m.font(92)
    total = NARR + END_SEC
    nfr = int(round(total * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else f"{slug}.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(ROOT / "clips/voiceover.mp3"), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{total:.2f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [total]
    for i in range(nfr):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t)
        t0, name, mo = SHOTS[k]
        fr = hook[min(i, len(hook) - 1)].copy() if name == "hook" else view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0))
        for st, du in SHAKE.items():
            if st <= t < st + du:
                a = 18 * (1 - (t - st) / du)
                fr = fr.transform((W, H), Image.AFFINE, (1, 0, a * math.sin(t * 90), 0, 1, a * math.cos(t * 70)), Image.BILINEAR)
        fr = fr.convert("RGBA")
        for a, b, lay in titles:
            if a <= t < b:
                fr.alpha_composite(lay)
        g = next((g for g in gs if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None) if t < NARR else None
        if g:
            d = ImageDraw.Draw(fr)
            txt = [w[0].upper() for w in g]
            cf = cap_f
            while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50:
                cf = m.font(cf.size - 4)
            widths = [d.textlength(w + " ", font=cf) for w in txt]
            x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
            for w, wd, (_, a, b) in zip(txt, widths, g):
                m.outlined(d, (x, CAP_Y), w, cf, m.YEL if a - 0.05 <= t <= b + 0.05 else m.WHITE, anchor="lm")
                x += wd
        fr = fr.convert("RGB")
        if preview:
            fr = fr.resize((ow, oh), Image.BILINEAR)
        wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait()
    print(out, round(total, 2), "s")


main()
