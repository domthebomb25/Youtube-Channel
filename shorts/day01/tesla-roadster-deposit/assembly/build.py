"""Assemble the Tesla Roadster deposit Short (1080x1920) from the hook clip, stills, voiceover and word timings.

usage: python3 build.py [--preview]   ->  ../tesla-roadster-deposit-short.mp4  (--preview: 540x960, faster)
"""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parents[2] / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402  (fonts, outlined text, caption grouping)

W, H, FPS = 1080, 1920, 30
AUD = ROOT / "clips/voiceover.mp3"
HOOK = ROOT / "clips/hook.mp4"
HOOK_LEN = 4.04
NARR = 43.55
END_SEC = 0.8
CAP_Y = 1580   # lower third, still inside the 3:4 grid crop (y 240-1680)
TITLE_Y = 290   # inside the 3:4 profile-grid crop (y 240-1680)

WORDS = json.load(open(HERE / "word_timing.json"))


def t_of(word, nth=1):
    """start time of the nth occurrence of a word, minus a small lead so the cut lands just before it."""
    hits = [a for w, a, b in WORDS if w == word]
    return round(hits[nth - 1] - 0.06, 2)


# (start, image, motion); "hook" plays the animated clip. Cuts land on word starts.
ZOOM = lambda z0, z1, at: {"z0": z0, "z1": z1, "at": at}
SHOTS = [
    (0.00, "hook", None),
    (HOOK_LEN, "hook_last", "in"),                                   # 1b: stunned mascot
    (t_of("tesla", 2), "V9", ZOOM(1.0, 1.3, (0.38, 0.42))),         # 2
    (t_of("that", 1), "V13", ZOOM(1.0, 1.3, (0.50, 0.40))),           # 2b
    (t_of("thruster", 1), "V37t", "in"),                              # 3   $250,000
    (t_of("production", 1), "V44t", "in"),                            # 4   2028
    (t_of("two", 3), "V46", "in"),                                    # 4b
    (t_of("no", 1), "V57", "in"),                                     # 5
    (t_of("no", 3), "V59", "in"),                                     # 5b
    (t_of("multiply", 1), "V50", "in"),                               # 6
    (t_of("equals", 1), "V51", "in"),                                 # 6b
    (t_of("before", 1), "V55", ZOOM(1.0, 1.35, (0.40, 0.45))),         # 7
    (t_of("they", 2), "V61", "in"),                                   # 8
    (t_of("deposits", 1), "V63t", "in"),                              # 8b  $50,000 / $250,000
    (t_of("car", 2), "V66", ZOOM(1.0, 1.3, (0.5, 0.42))),             # 8c
    (t_of("that's", 1), "V60", ZOOM(1.0, 1.3, (0.5, 0.42))),         # 9
    (t_of("that's", 2), "V5", "in"),                                  # 9b
    (t_of("would", 1), "V17", "in"),                                  # 10
    (t_of("that", 2), "V17", ZOOM(1.0, 1.35, (0.5, 0.45))),           # 10b punch-in on "that won't exist for years?"
]
TOTAL_END = NARR + END_SEC

# (t0, t1, [lines], colour[, y, font size]) — big top text
TEXT = [
    (0.00, t_of("tesla", 2), ["FREE LOAN TO TESLA"], m.YEL),
    (t_of("they", 2), t_of("car", 2), ["2017"], m.YEL),
    (t_of("car", 2), t_of("that's", 1), ["2026"], m.YEL),
    (t_of("that's", 2), t_of("would", 1), ["MONEY PRINTER"], m.YEL),
]


def merge(words):
    seqs = [(("twenty", "twenty", "eight"), "2028"), (("twenty", "seventeen"), "2017"), (("twenty", "twenty", "six"), "2026"),
            (("two", "hundred", "fifty", "thousand", "dollar"), "$250,000"), (("two", "hundred", "fifty", "thousand", "dollars"), "$250,000"),
            (("p", "o", "v"), "POV")]
    out, i = [], 0
    while i < len(words):
        for seq, rep in seqs:
            n = len(seq)
            if tuple(w[0] for w in words[i:i + n]) == seq:
                out.append((rep, words[i][1], words[i + n - 1][2])); i += n; break
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
    e = 1 - (1 - p) ** 2
    if isinstance(motion, dict):
        z = motion["z0"] + (motion["z1"] - motion["z0"]) * e
        fx, fy = motion["at"]
    else:
        z, fx, fy = 1 + 0.10 * p, .5, .5
    cw, ch = W / z, H / z
    x = min(max(fx * W - cw / 2, 0), W - cw)
    y = min(max(fy * H - ch / 2, 0), H - ch)
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def title_layer(lines, top, y0=None, size=92):
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


def main():
    preview = "--preview" in sys.argv
    words = [(w, a, b) for w, a, b in WORDS]
    gs = m.groups(merge(words), maxn=2)
    titles = [(t[0], t[1], title_layer(t[2], t[3], *t[4:])) for t in TEXT]
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    hook = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(HOOK), "-vf",
                           f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    hook = [Image.frombuffer("RGB", (W, H), hook[i:i + W * H * 3]) for i in range(0, len(hook), W * H * 3)]
    cap_f = m.font(70)
    total = TOTAL_END
    nfr = int(round(total * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else "tesla-roadster-deposit-short.mp4")
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
    for s, n, _ in SHOTS: print(f"{s:6.2f} {n}")


if __name__ == "__main__":
    main()
