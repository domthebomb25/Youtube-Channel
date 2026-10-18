"""Assemble the '100 followers' thank-you Short (1080x1920, ~10 s) from 4 animated clips, voiceover and word timings.

usage: python3 build.py [--preview]   ->  ../100-followers-short.mp4  (--preview: 540x960, faster)
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
TOTAL = 9.94          # four 3.04 s clips; voiceover is 9.87 s
CAP_Y = 1460          # below the "100" candles; still above the bottom 20% UI zone (y 1536)

# (start, clip, source offset, speed). Cuts land on the voiceover words.
SHOTS = [
    (0.00, "c1", 0.00, 1.09),   # "A week ago, this channel had zero followers."
    (2.80, "c2", 0.10, 1.30),   # "Today, a hundred of you showed up."
    (5.00, "c3", 0.00, 1.45),   # "Thank you, truly."
    (6.90, "c4", 0.00, 1.00),   # "Stick around, this stickman is just getting started."
]

# (t0, t1, [lines], top colour, y, font size)
TEXT = [
    (0.00, 2.80, ["0 TO 100", "IN ONE WEEK"], m.YEL, 270, 112),
]
POP = (3.44, 5.00, "100", m.YEL, 330, 230)   # "100" pops in on the word "hundred"


def text_layer(lines, top, y0, size, scale=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - 140, size).size for t in lines)
    f = m.font(max(8, int(fs * scale)))
    y = y0
    for i, t in enumerate(lines):
        tw = d.textlength(t, font=f)
        m.outlined(d, ((W - tw) / 2, y), t, f, top if i == 0 else m.WHITE, anchor="lm")
        y += f.size * 1.08
    return lay


def pop_scale(t, t0):
    """Quick overshoot pop-in over 0.25 s."""
    p = min(max((t - t0) / 0.25, 0), 1)
    return 0.5 + 0.5 * p + 0.18 * math.sin(p * math.pi)


def decode(name, src, speed, n):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(src), "-i", str(ROOT / f"clips/{name}.mp4"),
                          "-vf", f"setpts=(PTS-STARTPTS)/{speed},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = [Image.frombuffer("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw), W * H * 3)]
    return fr


def main():
    preview = "--preview" in sys.argv
    words = [tuple(w) for w in json.load(open(HERE / "word_timing.json"))]
    gs = m.groups(words)
    titles = [(t[0], t[1], text_layer(t[2], t[3], t[4], t[5])) for t in TEXT]
    cap_f = m.font(92)
    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else "100-followers-short.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(AUD), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{TOTAL:.2f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    nfr = int(round(TOTAL * FPS))
    starts = [s[0] for s in SHOTS] + [TOTAL]
    for k, (t0, name, src, speed) in enumerate(SHOTS):
        i0, i1 = int(round(t0 * FPS)), int(round(starts[k + 1] * FPS)) if k + 1 < len(SHOTS) else nfr
        clip = decode(name, src, speed, i1 - i0)
        for i in range(i0, i1):
            t = i / FPS
            fr = clip[min(i - i0, len(clip) - 1)].convert("RGBA")
            for a, b, lay in titles:
                if a <= t < b:
                    fr.alpha_composite(lay)
            if POP[0] <= t < POP[1]:
                fr.alpha_composite(text_layer([POP[2]], POP[3], POP[4], POP[5], pop_scale(t, POP[0])))
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
    print(out, TOTAL, "s")


if __name__ == "__main__":
    main()
