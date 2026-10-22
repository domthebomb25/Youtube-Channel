"""Assemble the Vaseline Short (1080x1920) from the hook clip, stills, voiceover and word timings.

usage: python3 build.py [--preview]   ->  ../vaseline-short.mp4  (--preview: 540x960, faster)
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
AUD = ROOT / "clips/voiceover.mp3"
HOOK = ROOT / "clips/hook.mp4"
NARR = 29.23            # voiceover length; the video ends on the last word (loop), no end card
CAP_Y = 1330
TITLE_Y = 470

# (start, image, motion); cuts sit in the pause between sentences. Last shot = image 1 exactly (loop frame).
SHOTS = [
    (0.00, "hook", None),
    (2.99, "img2", "in"),      # It started as goo on oil pumps.
    (5.38, "img3", "in"),      # One jar lasts for years. Sold since eighteen seventy.
    (9.40, "img4", "in"),      # Workers rubbed it on cuts.
    (11.40, "img5", "in"),     # Chesebrough cleaned it, patented it.
    (13.84, "img6", "in"),     # He said he ate a spoonful a day.
    (16.52, "img7", "in"),     # You don't take a blob.
    (18.07, "img8", "in"),     # You rub a tiny bit, spread thin.
    (20.31, "img9", "in"),     # So the jar lasts.
    (22.09, "img10", "in"),    # The money is the same jelly as lip balm,
    (24.60, "img11", "in"),    # skin cream, and baby cream.
    (26.63, "img1", "still"),  # A jar like that leaves one big question —   (loop frame)
]

# (t0, t1, [lines], top colour[, y, font size])
TEXT = [
    (0.00, 2.99, ["NEVER FINISH"], m.YEL, 300, 112),
    (2.99, 5.38, ["IT STARTED AS GOO"], m.YEL, 300, 104),
    (7.45, 9.40, ["SOLD SINCE 1870"], m.YEL, 300, 112),
    (13.84, 16.52, ["HE ATE IT"], m.YEL, 300, 120),
]
CTA = (24.60, 26.63, "FOLLOW FOR TOMORROW'S STORY", "Tomorrow: Why did Yahoo say no to Google?")


def merge_years(words):
    out, i = [], 0
    while i < len(words):
        if [w[0] for w in words[i:i + 2]] == ["eighteen", "seventy"]:
            out.append(("1870", words[i][1], words[i + 1][2])); i += 2
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
    if motion == "still":
        return img
    z = 1 + 0.10 * p
    cw, ch = W / z, H / z
    x, y = (W - cw) / 2, (H - ch) / 2
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def title_layer(lines, top, y0=None, size=130):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - 140, size).size for t in lines)
    f = m.font(fs)
    y = TITLE_Y if y0 is None else y0
    for i, t in enumerate(lines):
        tw = d.textlength(t, font=f)
        m.outlined(d, ((W - tw) / 2, y), t, f, top if i == 0 else m.WHITE, anchor="lm")
        y += fs * 1.08
    return lay


def cta_layer(l1, l2):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f1, f2 = m.fit(l1, W - 120, 62), m.fit(l2, W - 120, 50)
    m.outlined(d, (W / 2, 1530), l1, f1, m.YEL)
    m.outlined(d, (W / 2, 1610), l2, f2, m.WHITE)
    return lay


def main():
    preview = "--preview" in sys.argv
    words = [(w, a, b) for w, a, b in json.load(open(HERE / "word_timing.json"))]
    gs = m.groups(merge_years(words))
    titles = [(t[0], t[1], title_layer(t[2], t[3], *t[4:])) for t in TEXT]
    cta = (CTA[0], CTA[1], cta_layer(CTA[2], CTA[3]))
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    hook = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(HOOK), "-vf",
                           f"setpts=PTS*{SHOTS[1][0]}/4.04,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    hook = [Image.frombuffer("RGB", (W, H), hook[i:i + W * H * 3]) for i in range(0, len(hook), W * H * 3)]
    cap_f = m.font(92)
    nfr = int(round(NARR * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else "vaseline-short.mp4")
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
        fr = hook[min(i, len(hook) - 1)].copy() if name == "hook" else view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0))
        fr = fr.convert("RGBA")
        for a, b, lay in titles + [cta]:
            if a <= t < b:
                fr.alpha_composite(lay)
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
