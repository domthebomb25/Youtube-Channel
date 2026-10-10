"""Assemble the LEGO tires Short (1080x1920) from the hook clip, stills, voiceover and word timings.

usage: python3 build.py [--preview]   ->  ../lego-tires-short.mp4  (--preview: 540x960, faster)
"""
import json, math, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parent / "costco-hot-dog/shorts"))
import make_short as m  # noqa: E402  (fonts, outlined text, emoji, caption grouping)

W, H, FPS = 1080, 1920, 30
AUD = ROOT / "clips/voiceover.mp3"
HOOK = ROOT / "clips/hook.mp4"
NARR = 47.25
END_SEC = 2.0
CAP_Y = 1330
TITLE_Y = 470   # keep top text inside the 3:4 profile-grid crop (y 240-1680)
RED = (235, 50, 40)

# (start, image, motion); image "hook" plays the animated clip. Cuts land on word timings.
SHOTS = [
    (0.00, "hook", None),
    (3.07, "img2", "in"),
    (5.47, "img3", "in"),
    (7.98, "img4", "right"),
    (11.02, "img5", "up"),
    (12.45, "img6", "in"),
    (16.01, "img7", "left"),
    (18.66, "img8", "in"),
    (22.69, "img9", "up"),
    (26.26, "img10", "right"),
    (29.86, "img11", "in"),
    (32.01, "img11", {"z0": 1.25, "z1": 1.5, "at": (0.5, 0.45)}),   # push in on the trophy
    (36.23, "img12", "up"),
    (39.04, "img13", "in"),
    (43.53, "img14", "in"),
    (NARR, "img14", "hold"),                                       # end beat
]
SHAKE = {5.64: 0.35, 24.10: 0.30}          # "LEGO" reveal, "381 million"

# (t0, t1, [lines], top colour[, y, font size]) — big on-screen text near the top
TEXT = [
    (0.00, 3.07, ["WORLD'S #1 TIRE MAKER?"], m.YEL, 360, 104),   # between the top and his head, inside every app's safe area
    (5.47, 7.05, ["LEGO?!"], RED, 170),             # above his head, face stays clear
    (19.52, 22.69, ["300,000,000+", "TIRES A YEAR"], m.YEL),
    (24.10, 26.26, ["381 MILLION", "IN 2010"], m.YEL),
    (29.86, 34.61, ["WORLD RECORD 🏆"], m.YEL, 330),   # below the spotlights, above the heads
    (41.44, 43.53, ["LEGO WINS ON COUNT"], m.WHITE),
]
DISPLAY = {"lego": "LEGO", "michelin": "Michelin", "goodyear": "Goodyear"}


def merge_years(words):
    out, i = [], 0
    while i < len(words):
        if [w[0] for w in words[i:i + 2]] == ["twenty", "ten"]:
            out.append(("2010", words[i][1], words[i + 1][2])); i += 2
        else:
            out.append(words[i]); i += 1
    return out


def load(name):
    im = Image.open(ROOT / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height) * 1.0
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def view(img, motion, p):
    """Ken Burns crop of a W x H image at progress p in [0,1]."""
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


def title_layer(lines, top, y0=None, size=130):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - 140, size).size for t in lines)
    f = m.font(fs)
    y = TITLE_Y if y0 is None else y0
    for i, t in enumerate(lines):
        emo = t[-1] if ord(t[-1]) > 0x2000 else None
        txt = t[:-1].rstrip() if emo else t
        tw = d.textlength(txt, font=f)
        ew = int(fs * 1.1) + 16 if emo else 0
        x = (W - tw - ew) / 2
        m.outlined(d, (x, y), txt, f, top if i == 0 else m.WHITE, anchor="lm")
        if emo:
            em = m.emoji_img(emo, int(fs * 1.05))
            lay.alpha_composite(em, (int(x + tw + 16), int(y - em.height / 2)))
        y += fs * 1.08
    return lay


def main():
    preview = "--preview" in sys.argv
    words = [(DISPLAY.get(w, w), a, b) for w, a, b in json.load(open(HERE / "word_timing.json"))]
    gs = m.groups(merge_years(words))
    titles = [(t[0], t[1], title_layer(t[2], t[3], *t[4:])) for t in TEXT]
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    hook = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(HOOK), "-vf", f"setpts=PTS*{SHOTS[1][0]}/4.04,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    hook = [Image.frombuffer("RGB", (W, H), hook[i:i + W * H * 3]) for i in range(0, len(hook), W * H * 3)]
    cap_f = m.font(92)
    total = NARR + END_SEC
    nfr = int(round(total * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else "lego-tires-short.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(AUD), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{total:.2f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [total]
    for i in range(nfr):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t)
        t0, name, mo = SHOTS[k]
        if name == "hook":
            fr = hook[min(i, len(hook) - 1)].copy()
        else:
            fr = view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0))
        for st, du in SHAKE.items():
            if st <= t < st + du:
                a = 18 * (1 - (t - st) / du)
                fr = fr.transform((W, H), Image.AFFINE, (1, 0, a * math.sin(t * 90), 0, 1, a * math.cos(t * 70)), Image.BILINEAR)
                fr = fr.resize((int(W * 1.04), int(H * 1.04))).crop((int(W * .02), int(H * .02), int(W * .02) + W, int(H * .02) + H))
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


if __name__ == "__main__":
    main()
