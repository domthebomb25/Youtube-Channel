"""Credit Card Short renderer. usage: python3 build.py [--preview]
Reads word_timing.json; hook = ../clips/hook.mp4 (finalized 1.25x edit), voice = ../clips/voiceover.mp3."""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parent.parent.parent / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402

W, H, FPS = 1080, 1920, 30
CAP_Y = 1330
CAP_Y_OVERRIDE = {"img6": 1090}   # keep captions off the three mascots' faces
NARR = 25.18                # approved voiceover length
TOTAL = 25.20               # last frame sits 0.02s past the voice: trailing silence < 0.3s
HOOK_END = 2.42
# (start, image, motion). Final shot = image 1, static, pixel-exact (loop seam).
SHOTS = [(0.0, "hook", None), (HOOK_END, "img2", "in"), (4.64, "img3", "out"), (8.59, "img4A", "in"),
         (12.15, "img4B", "out"), (15.50, "img5A", "in"), (18.51, "img5B", "out"), (20.66, "img6", "in"),
         (22.84, "img7", "in"), (24.80, "img1", "static")]
BURST3 = 1.60               # hook text shakes 1.60-1.70, blasts off 1.70-1.77 (frames 51-52), gone by 1.77
ONES = {}


def load(name):
    im = Image.open(ROOT / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def view(img, motion, p):
    if motion == "static":
        return img
    z = 1 + 0.08 * p if motion == "in" else 1.08 - 0.08 * p
    cw, ch = W / z, H / z
    x, y = (W - cw) / 2, (H - ch) / 2
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def text_layer(lines, y0, size, colors):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - 120, size).size for t in lines)
    f = m.font(fs)
    y = y0
    for t, c in zip(lines, colors):
        tw = d.textlength(t, font=f)
        m.outlined(d, ((W - tw) / 2, y), t, f, c, anchor="lm")
        y += fs * 1.1
    return lay


def banner_layer(text, yc, size):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = m.fit(text, W - 200, size)
    tw = d.textlength(text, font=f)
    pad = 28
    d.rounded_rectangle(((W - tw) / 2 - pad, yc - f.size * 0.75, (W + tw) / 2 + pad, yc + f.size * 0.75), 28,
                        fill=(15, 15, 15, 215))
    m.outlined(d, ((W - tw) / 2, yc), text, f, m.YEL, anchor="lm")
    return lay


def main():
    preview = "--preview" in sys.argv
    words = json.load(open(HERE / "word_timing.json"))
    gs = m.groups([tuple(w) for w in words])
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ROOT / "clips/hook.mp4"), "-vf",
                          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    hook = [Image.frombuffer("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw), W * H * 3)]
    hook_txt = text_layer(["YOU'RE NOT", "THE CUSTOMER?!"], 330, 150, [m.WHITE, m.YEL])
    follow = text_layer(["FOLLOW FOR", "TOMORROW'S STORY"], 1560, 110, [m.WHITE, m.YEL])
    banner = banner_layer("NEW BUSINESS STORY TOMORROW", 1655, 74)
    cap_f = m.font(92)
    nfr = int(round(TOTAL * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else "BS-credit-card.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(ROOT / "clips/voiceover.mp3"), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{TOTAL:.2f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [TOTAL]
    for i in range(nfr):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t + 1e-6)
        t0, name, mo = SHOTS[k]
        fr = hook[min(i, len(hook) - 1)].copy() if name == "hook" else view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0))
        fr = fr.convert("RGBA")
        if t < BURST3 + 0.18:                      # hook text: 3-frame shake, then 2-frame blast off the top
            dx = dy = 0
            f = i - int(round(BURST3 * FPS))        # frames since burst 3 (1.60s = frame 48)
            if 0 <= f < 3:
                dx, dy = 16 * math.sin(i * 2.3), 12 * math.cos(i * 3.1)
            elif f == 3:
                dy = -260
            elif f == 4:
                dy = -700
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.paste(hook_txt, (int(dx), int(dy)))
            fr.alpha_composite(lay)
        if name == "img6":
            fr.alpha_composite(banner)
        if name == "img7":
            fr.alpha_composite(follow)
        g = next((g for g in gs if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None)
        if g:
            d = ImageDraw.Draw(fr)
            txt = [w[0].upper() for w in g]
            cf = cap_f
            while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50:
                cf = m.font(cf.size - 4)
            widths = [d.textlength(w + " ", font=cf) for w in txt]
            x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
            for w, wd, (_, a, b) in zip(txt, widths, g):
                m.outlined(d, (x, CAP_Y_OVERRIDE.get(name, CAP_Y)), w, cf, m.YEL if a - 0.05 <= t <= b + 0.05 else m.WHITE, anchor="lm")
                x += wd
        fr = fr.convert("RGB")
        if preview:
            fr = fr.resize((ow, oh), Image.BILINEAR)
        wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait()
    print(out, TOTAL, "s")


main()
