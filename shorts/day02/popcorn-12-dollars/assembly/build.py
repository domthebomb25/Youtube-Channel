"""Popcorn Short renderer. usage: python3 build.py [--preview]   (run from anywhere)
Voice = ../clips/voiceover.mp3 (gap-trimmed), word timings = word_timing.json, stills = ../images/imgN.png.
Static overlays are baked into the stills at 1080x1920; shots 1 and 10 are the same file."""
import glob, json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parent.parent.parent.parent / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402

W, H, FPS, CAP_Y = 1080, 1920, 30, 1330
wt = json.load(open(HERE / "word_timing.json"))
wt_end = wt[-1][2]
NARR, END_SEC = wt_end, 0.20          # NARR = end of the last spoken word; tail = 0.20 s (limit 0.3 s)
DEJA = glob.glob("/usr/share/fonts/**/DejaVuSans-Bold.ttf", recursive=True)[0]
RED, BLACK = (150, 20, 20), (20, 20, 20)

def first(i): return wt[i][1]
CUT = [first(i) - 0.03 for i in (7, 19, 34, 47, 56, 69, 79)]      # first word of lines 2,3,4,5,6a,6b,7 (see sheet)
DIVE = {"z0": 1.0, "z1": 1.28, "at": (0.45, 0.42)}                 # starts at 1.0 so frame 0 == loop frame
STATIC = {"z0": 1.0, "z1": 1.0, "at": (0.5, 0.5)}
SHOTS = [(0.0, "hook", None), (CUT[0], "img2", "in"), (CUT[1], "img3", "up"), (CUT[2], "img4", "in"),
         (CUT[3], "img5", "out"), (CUT[4], "img6", "in"), (CUT[5], "img7", "out"), (CUT[6], "img9", "in"),
         (NARR, "img1", STATIC)]
# overlays in 752x1344 source pixels: (text, centre, px, fill, angle, font)
BRAND = m.FONT
OVERLAYS = {
    "img6": [("$12", (545, 728), 100, BLACK, 26, DEJA),
             ("under $1", (376, 1135), 62, m.WHITE, 0, BRAND)],
    "img7": [("RENT", (132, 972), 42, BLACK, 6, DEJA)],
}


def text_layer(size, text, center, px, fill, angle, fontpath):
    f = ImageFont.truetype(fontpath, px)
    t = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    sw = max(3, px // 9) if fontpath == BRAND else 0
    bb = d.multiline_textbbox((0, 0), text, font=f, stroke_width=sw, align="center")
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.multiline_text((center[0] - w / 2 - bb[0], center[1] - h / 2 - bb[1]), text, font=f, fill=fill, stroke_width=sw,
                     stroke_fill=m.INK, align="center", spacing=2)
    return t.rotate(angle, center=center, resample=Image.BICUBIC) if angle else t


def load(name):
    im = Image.open(ROOT / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    rgba = im.convert("RGBA")
    for text, (cx, cy), px, fill, ang, fp in OVERLAYS.get(name, []):
        rgba.alpha_composite(text_layer(rgba.size, text, (cx * s, cy * s), round(px * s), fill, ang, fp))
    return rgba.convert("RGB").crop((x0, y0, x0 + W, y0 + H))


def view(img, motion, p):
    e = 1 - (1 - p) ** 2
    if isinstance(motion, dict):
        z = motion["z0"] + (motion["z1"] - motion["z0"]) * e
        fx, fy = motion["at"]
    else:
        z, fx, fy = {"in": (1 + 0.10 * p, .5, .5), "out": (1.10 - 0.10 * p, .5, .5),
                     "up": (1.12, .5, .56 - .12 * p)}[motion]
    cw, ch = W / z, H / z
    x = min(max(fx * W - cw / 2, 0), W - cw)
    y = min(max(fy * H - ch / 2, 0), H - ch)
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def follow_layer():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    m.outlined(d, (W / 2, 1565), "FOLLOW", m.font(84), m.YEL)
    m.outlined(d, (W / 2, 1650), "New business story tomorrow", m.fit("New business story tomorrow", W - 160, 46), m.WHITE)
    return lay


def hook_text_layer():
    """Two-line hook text at the top, black outline: line 1 white, line 2 yellow with $12 the biggest element."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    l1 = "WHY DOES POPCORN"
    f1 = m.fit(l1, W - 110, 100)
    m.outlined(d, (W / 2, 285), l1, f1, m.WHITE)
    parts = [("COST ", m.font(96)), ("$12", m.font(200)), ("?!", m.font(120))]
    sw = lambda f: max(4, f.size // 9)
    widths = [d.textlength(t, font=f) for t, f in parts]
    x = (W - sum(widths)) / 2; base = 488                      # shared baseline
    for (t, f), wd in zip(parts, widths):
        d.text((x, base), t, font=f, fill=m.YEL, anchor="ls", stroke_width=sw(f), stroke_fill=m.INK)
        x += wd
    return lay


def hook_frames():
    """Approved Kling eruption clip, upscaled to full frame (cover + centre-crop). Frame 0 is replaced by image 1 itself."""
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ROOT / "clips/hook_v2_trim.mp4"), "-vf",
                          f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = [Image.frombuffer("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw), W * H * 3)]
    fr[0] = load("img1")
    return fr


def cap_words():
    sub = {"ninety": "90", "twelve": "12"}
    return [(sub.get(w, w), a, b) for w, a, b in wt]


def main():
    preview = "--preview" in sys.argv
    gs = m.groups(cap_words())
    imgs = {n: load(n) for n in {s[1] for s in SHOTS} - {"hook"}}
    hook, htext = hook_frames(), hook_text_layer()
    follow = follow_layer()
    total = NARR + END_SEC
    nfr = int(round(total * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = ROOT / ("preview-540p.mp4" if preview else "popcorn-12-dollars.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(ROOT / "clips/voiceover.mp3"), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{total:.3f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [total]
    cap_f = m.font(92)
    for i in range(nfr):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t)
        t0, name, mo = SHOTS[k]
        if name == "hook":
            fr = hook[min(int(t * 24), len(hook) - 1)].copy().convert("RGBA")
            fr.alpha_composite(htext)
        else:
            fr = view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0)).convert("RGBA")
        if name == "img9":
            fr.alpha_composite(follow)
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
    print(out, round(total, 3), "s")


main()
