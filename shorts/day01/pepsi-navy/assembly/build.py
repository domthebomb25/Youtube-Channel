"""Assemble the Pepsi / Soviet warships Short (1080x1920): hook clip + still shots, voiceover, SFX, word timings.

usage: MEDIA=/path/to/media python3 build.py [--preview]   ->  $MEDIA/pepsi-navy-short.mp4  (--preview: 540x960, faster)
MEDIA must hold: hook4.mp4, s1.png, s3_eyes.png, s4_fixed.png, new03.png, rubles_new.png, img05..img10.png, s10_new.png, voice_final.mp3
"""
import json, math, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
MEDIA = Path(os.environ.get("MEDIA", HERE))
sys.path.insert(0, str(REPO / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402  (fonts, outlined text, caption grouping)

W, H, FPS, SR = 1080, 1920, 30, 48000
AUD = MEDIA / "voice_final.mp3"
HOOK = MEDIA / "hook7.mp4"              # one continuous 4 s animated hook (fixed can); used as is, no added effects
PLAIN = os.environ.get("PLAIN_HOOK") == "1"       # no SFX / shake / bursts / flash / punch-in on the hook
HOOK_ONLY = os.environ.get("HOOK_ONLY") == "1"    # render just the first seconds
TOTAL = 4.6 if HOOK_ONLY else 33.45               # narration ends 33.28 on the unfinished loop line
CAP_Y_BOT, CAP_Y_TOP = 1500, 300  # captions go where they cover nothing important (per shot, see CAPPOS)
CAPPOS = {"hook": "bot", "new03": "top", "rubles_new": 690, "img05": "bot", "img06": "top", "img07": "top",
          "img08": "bot", "img09": "top", "img10": "bot", "s10_new": "bot", "s1": "bot"}
TITLE_Y = 330
RED = (235, 50, 40)
SLOT = (0.375, 0.49)             # coin slot position in the hook frame (fraction of W, H)

# hook timeline (seconds): clip 0-SWALLOW (strain), white-flash cut, clip CLIP_AFTER.. (celebrate), then two still beats
SWALLOW, CLIP_AFTER, CAN_AT, HAND_AT = 2.25, 2.85, 3.00, 3.55

# (start, image, motion); "hook" = animated clip handled in code. Cuts land just before the words.
SHOTS = [
    (0.00, "hook", None),
    (4.09, "new03", "in"),
    (7.80, "rubles_new", "right"),
    (9.78, "img05", "in"),
    (12.30, "img06", "left"),
    (14.88, "img07", "out"),
    (18.10, "img08", "in"),
    (22.62, "img09", "right"),
    (23.88, "img10", "in"),
    (26.80, "s10_new", {"z0": 1.0, "z1": 1.12, "at": (0.5, 0.42)}),
    (31.95, "s1", "in"),                                                  # same picture as the hook -> seamless loop
]
SHAKE = {23.88: 0.35, 26.80: 0.25}

# (t0, t1, [lines], top colour[, y, font size]) big on-screen text; kept off faces
TEXT = [
    (0.00, 4.09, ["PAID IN WARSHIPS"], m.YEL, TITLE_Y, 118),      # the only header: the payoff, from frame 0
]
CUTS = [s[0] for s in SHOTS[1:]]
THUDS = []                                   # voice only: no hit sounds


def merge_years(words):
    out, i = [], 0
    while i < len(words):
        if [w[0] for w in words[i:i + 3]] == ["nineteen", "eighty", "nine"]:
            out.append(("1989", words[i][1], words[i + 2][2])); i += 3
        else:
            out.append(words[i]); i += 1
    return out


# ---------- sound effects (synthesised, quiet under the voice) ----------
def _env(n, decay): return np.exp(-np.arange(n) / (SR * decay))


def _add(buf, snd, t):
    i = int(t * SR)
    if i < 0 or i >= len(buf): return
    j = min(len(buf), i + len(snd)); buf[i:j] += snd[:j - i]


def boom(rng):
    n = int(0.9 * SR); t = np.arange(n) / SR
    f = 95 - 60 * np.minimum(t / 0.5, 1)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.28)
    nz = np.convolve(rng.standard_normal(n), np.ones(60) / 60, "same") * _env(n, 0.12)
    return 0.55 * s + 0.35 * nz


def whoosh(rng, dur=0.35, amp=0.16):
    n = int(dur * SR); nz = rng.standard_normal(n)
    nz = np.convolve(nz, np.ones(24) / 24, "same")
    win = np.sin(np.linspace(0, np.pi, n)) ** 2
    return amp * nz * win * 3


def thud(rng):
    n = int(0.25 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(130 - 80 * np.minimum(t / 0.15, 1)) / SR) * _env(n, 0.07)
    return 0.45 * s + 0.1 * rng.standard_normal(n) * _env(n, 0.01)


def clunk(rng):
    n = int(0.3 * SR); t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 180 * t) + 0.6 * np.sin(2 * np.pi * 275 * t)) * _env(n, 0.07)
    return 0.4 * s + 0.15 * rng.standard_normal(n) * _env(n, 0.008)


def pop(rng):
    n = int(0.12 * SR); t = np.arange(n) / SR
    return 0.38 * np.sin(2 * np.pi * np.cumsum(700 + 900 * t / 0.12) / SR) * _env(n, 0.03)


def clank(rng):
    n = int(0.25 * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) for f in (820, 1330, 2100)) * _env(n, 0.06)
    return 0.12 * s + 0.1 * rng.standard_normal(n) * _env(n, 0.005)


def make_audio():
    rng = np.random.default_rng(7)
    voice = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(AUD), "-ac", "1", "-ar", str(SR),
                                          "-f", "f32le", "-"], capture_output=True, check=True).stdout, dtype=np.float32).copy()
    n = int(TOTAL * SR)
    mix = np.zeros(n, dtype=np.float64)
    mix[:min(n, len(voice))] += voice[:n]
    sfx = np.zeros(n)
    for t in THUDS: _add(sfx, thud(rng), t)
    mix += sfx
    mix = np.clip(mix, -0.98, 0.98)
    wav = HERE / "mix.raw"
    wav.write_bytes(mix.astype(np.float32).tobytes())
    return wav


# ---------- picture ----------
def load(name):
    im = Image.open(MEDIA / f"{name}.png").convert("RGB")
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
        z, fx, fy = {"in": (1 + 0.10 * p, .5, .5), "out": (1.10 - 0.10 * p, .5, .5),
                     "right": (1.12, .44 + .12 * p, .5), "left": (1.12, .56 - .12 * p, .5)}[motion]
    cw, ch = W / z, H / z
    x = min(max(fx * W - cw / 2, 0), W - cw)
    y = min(max(fy * H - ch / 2, 0), H - ch)
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def title_layer(lines, top, y0, size):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - 120, size).size for t in lines)
    f = m.font(fs)
    y = y0
    for i, t in enumerate(lines):
        tw = d.textlength(t, font=f)
        m.outlined(d, ((W - tw) / 2, y), t, f, top if i == 0 else m.WHITE, anchor="lm")
        y += fs * 1.08
    return lay


def burst(size):
    """Yellow-white radial impact burst (RGBA), used as flashes at the slot."""
    yy, xx = np.mgrid[-1:1:complex(size), -1:1:complex(size)]
    r = np.sqrt(xx ** 2 + yy ** 2)
    a = np.clip(1 - r, 0, 1) ** 1.6
    ang = np.arctan2(yy, xx)
    a = a * (0.75 + 0.25 * np.cos(ang * 9))                     # spiky rays
    img = np.zeros((size, size, 4), dtype=np.uint8)
    img[..., 0] = 255; img[..., 1] = 235 - (r * 60).astype(np.uint8); img[..., 2] = (120 * r).astype(np.uint8)
    img[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def shake(fr, amp, t):
    fr = fr.transform((W, H), Image.AFFINE, (1, 0, amp * math.sin(t * 90), 0, 1, amp * math.cos(t * 70)), Image.BILINEAR)
    return fr.resize((int(W * 1.04), int(H * 1.04))).crop((int(W * .02), int(H * .02), int(W * .02) + W, int(H * .02) + H))


def hook_frame(clip, t, bursts=None):
    """The animated hook is used exactly as generated (no shake, bursts, flash or zoom)."""
    return clip[min(int(t * FPS), len(clip) - 1)].copy()


def main():
    preview = "--preview" in sys.argv
    words = json.load(open(HERE / "word_timing.json"))
    gs = m.groups(merge_years([(w, a, b) for w, a, b in words]))
    titles = [(t[0], t[1], title_layer(t[2], t[3], *t[4:])) for t in TEXT]
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(HOOK), "-vf",
                          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    clip = [Image.frombuffer("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw), W * H * 3)]
    bursts = burst(520)
    mix = make_audio()
    cap_f = m.font(76)
    nfr = int(round(TOTAL * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = MEDIA / ("pepsi-hook-plain.mp4" if HOOK_ONLY else "pepsi-preview5-540p.mp4" if preview else "pepsi-navy-short.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", str(mix),
                           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [TOTAL]
    for i in range(nfr):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t)
        t0, name, mo = SHOTS[k]
        if name == "hook":
            fr = hook_frame(clip, t, bursts)
        else:
            fr = view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0))
        for st, du in SHAKE.items():
            if st <= t < st + du and name != "hook":
                fr = shake(fr, 18 * (1 - (t - st) / du), t)
        fr = fr.convert("RGBA")
        for a, b, lay in titles:
            if a <= t < b:
                fr.alpha_composite(lay)
        g = next((g for g in gs if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None)
        if g:
            d = ImageDraw.Draw(fr)
            txt = [w[0].upper() for w in g]
            cf = cap_f
            while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 160 and cf.size > 44:
                cf = m.font(cf.size - 4)
            widths = [d.textlength(w + " ", font=cf) for w in txt]
            x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
            pos = CAPPOS.get(name, "bot")
            cy = pos if isinstance(pos, (int, float)) else (CAP_Y_TOP if pos == "top" else CAP_Y_BOT)
            for w, wd, (_, a, b) in zip(txt, widths, g):
                m.outlined(d, (x, cy), w, cf, m.YEL if a - 0.05 <= t <= b + 0.05 else m.WHITE, anchor="lm")
                x += wd
        fr = fr.convert("RGB")
        if preview:
            fr = fr.resize((ow, oh), Image.BILINEAR)
        wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait()
    mix.unlink()
    print(out, round(TOTAL, 2), "s")


if __name__ == "__main__":
    main()
