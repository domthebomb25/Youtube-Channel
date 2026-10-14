"""Assemble the McDonald's "It's locked" Short (1080x1920): animated hook clip, 9 stills, voiceover, word timings.

usage: python3 build.py [--preview]   ->  ../mcdonalds-locked.mp4  (--preview: 540x960, faster)
"""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent.parent.parent
sys.path.insert(0, str(REPO / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402  (fonts, outlined text, caption grouping)

W, H, FPS = 1080, 1920, 30
AUD = ROOT / "voice_final.mp3"
HOOK = ROOT / "clips/hook.mp4"
NARR = 33.52
CAP_Y = 1330
TITLE_Y = 470   # keep top text inside the 3:4 profile-grid crop (y 240-1680)
RED = (235, 50, 40)

# (start, image, motion); "hook" plays the animated clip. Cuts land on word timings.
SHOTS = [
    (0.00, "hook", None),
    (2.93, "img02", "in"),
    (6.85, "img03", "out"),
    (9.82, "img04", "in"),
    (14.09, "img05", "left"),
    (18.83, "img06", "in"),
    (22.42, "img07", "right"),
    (25.36, "img08", "in"),
    (28.91, "img09", "out"),
    (30.91, "img10", "in"),
]
PUNCH_AT = 2.27      # "locked" starts here (word_timing.json)
PUNCH_LEN = 0.20     # zoom punch length
SHAKE_LEN = 0.40     # camera shake length

# (t0, t1, [lines], colours, y, size) big on-screen text
TEXT = [
    (0.00, 2.93, ["ISN'T BROKEN.", "IT'S LOCKED."], [m.WHITE, m.YEL], 1035, 116),   # below the face, over the shirt
    (2.93, 6.85, ["151° EVERY NIGHT"], [m.YEL], 300, 112),
    (6.85, 9.82, ["IF IT FAILS: LOCKED"], [RED], 300, 112),
    (9.82, 14.09, ["UP TO $625 A DAY"], [m.YEL], 1150, 112),
    (14.09, 18.83, ["$300+ PER 15 MIN"], [m.WHITE], 1150, 112),
    (18.83, 22.42, ["KYTCH"], [m.YEL]),
    (22.42, 25.36, ["TOLD TO REMOVE IT"], [RED]),
    (25.36, 28.91, ["$900,000,000"], [m.YEL], 290, 104),
    (28.91, 30.91, ["MERITLESS?"], [m.WHITE]),
    (30.91, 33.52, ["BROKEN… OR LOCKED?"], [m.YEL], 300, 104),
]

MERGE = [(("four", "hour"), "4-HOUR"), (("one", "hundred", "fifty", "one"), "151"),
         (("six", "hundred", "twenty", "five", "dollars"), "$625"), (("three", "hundred", "dollars"), "$300"),
         (("nine", "hundred", "million", "dollars"), "$900 MILLION"), (("fifteen",), "15")]


def merge_numbers(words):
    out, i = [], 0
    while i < len(words):
        for key, rep in MERGE:
            if tuple(w[0] for w in words[i:i + len(key)]) == key:
                out.append((rep, words[i][1], words[i + len(key) - 1][2])); i += len(key); break
        else:
            out.append(words[i]); i += 1
    return out


def load(name):
    im = Image.open(ROOT / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def view(img, motion, p):
    """Ken Burns crop of a W x H image at progress p in [0,1]."""
    z, fx, fy = {"in": (1 + 0.10 * p, .5, .5), "out": (1.10 - 0.10 * p, .5, .5),
                 "right": (1.12, .44 + .12 * p, .5), "left": (1.12, .56 - .12 * p, .5)}[motion]
    cw, ch = W / z, H / z
    x = min(max(fx * W - cw / 2, 0), W - cw)
    y = min(max(fy * H - ch / 2, 0), H - ch)
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def title_layer(lines, cols, y0=None, size=130):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - 120, size).size for t in lines)
    f = m.font(fs)
    y = TITLE_Y if y0 is None else y0
    for i, t in enumerate(lines):
        m.outlined(d, (W / 2, y), t, f, cols[min(i, len(cols) - 1)], anchor="mm")
        y += fs * 1.1
    return lay


def punch_shake(fr, t):
    """0.2 s zoom punch + camera shake starting at PUNCH_AT."""
    dt = t - PUNCH_AT
    if 0 <= dt < PUNCH_LEN:
        z = 1 + 0.18 * math.sin(math.pi * dt / PUNCH_LEN)
        cw, ch = W / z, H / z
        fr = fr.transform((W, H), Image.EXTENT, ((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2), Image.BICUBIC)
    if 0 <= dt < SHAKE_LEN:
        a = 22 * (1 - dt / SHAKE_LEN)
        fr = fr.transform((W, H), Image.AFFINE, (1, 0, a * math.sin(t * 90), 0, 1, a * math.cos(t * 70)), Image.BILINEAR)
        fr = fr.resize((int(W * 1.05), int(H * 1.05))).crop((int(W * .025), int(H * .025), int(W * .025) + W, int(H * .025) + H))
    return fr


def main():
    preview = "--preview" in sys.argv
    words = merge_numbers([tuple(w) for w in json.load(open(HERE / "word_timing.json"))])
    gs = m.groups(words)
    titles = [(t[0], t[1], title_layer(t[2], t[3], *t[4:])) for t in TEXT]
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    hook = subprocess.run(["ffmpeg", "-loglevel", "error", "-t", f"{SHOTS[1][0]:.2f}", "-i", str(HOOK),
                           "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    hook = [Image.frombuffer("RGB", (W, H), hook[i:i + W * H * 3]) for i in range(0, len(hook), W * H * 3)]
    cap_f = m.font(92)
    nfr = int(round(NARR * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else "mcdonalds-locked.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(AUD), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{NARR:.2f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [NARR]
    for i in range(nfr):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t)
        t0, name, mo = SHOTS[k]
        if name == "hook":
            fr = hook[min(i, len(hook) - 1)].copy()
        else:
            fr = view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0))
        fr = fr.convert("RGBA")
        for a, b, lay in titles:
            if a <= t < b:
                fr.alpha_composite(lay)
        fr = punch_shake(fr.convert("RGB"), t)
        fr = fr.convert("RGBA")
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
                m.outlined(d, (x, CAP_Y), w, cf, m.YEL if a - 0.05 <= t <= b + 0.05 else m.WHITE, anchor="lm")
                x += wd
        fr = fr.convert("RGB")
        if preview:
            fr = fr.resize((ow, oh), Image.BILINEAR)
        wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait()
    print(out, round(NARR, 2), "s")


if __name__ == "__main__":
    main()
