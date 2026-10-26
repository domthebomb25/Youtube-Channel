"""Gas-station Short renderer.  usage: python3 -I render_gas.py [--final] [--keep-frames N,N,...]
Shot 1 = programmatic hook frames (hook_frames/), shots 2-9 = storyboard stills, shot 10 = original image 1 (loop frame).
Cuts land on the first word of each beat from word_timing.json; captions are the channel style (3-word groups, current word yellow).
Composites at 1080x1920 and downsizes for the preview."""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = Path("/home/user/Youtube-Channel")
FONT = str(REPO / "videos/costco-hot-dog/assembly/fonts/LuckiestGuy.ttf")
W, H, FPS = 1080, 1920, 30
WHITE, YEL, INK = (255, 255, 255), (255, 214, 0), (15, 15, 15)
CAP_Y = 1330
FINAL = "--final" in sys.argv
KEEP = [int(x) for a in sys.argv if a.startswith("--keep=") for x in a[7:].split(",")]

font = lambda s: ImageFont.truetype(FONT, s)


def outlined(d, xy, text, f, fill, anchor="mm"):
    d.text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=max(4, f.size // 9), stroke_fill=INK)


def fit(d, text, maxw, start):
    s = start
    while d.textlength(text, font=font(s)) > maxw and s > 20:
        s -= 2
    return font(s)


# ---------------------------------------------------------------- timing from the word timings
words = json.load(open(HERE / "assembly/word_timing.json"))          # [word, start, end]
toks = [w[0] for w in words]
AUDIO = HERE / "vo_final.mp3"
NARR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(AUDIO)]))
TOTAL = round(NARR - 0.02, 3)                                  # 27.80 s: leaves a 0.27 s tail after the last word (limit 0.3 s)
NFR = int(round(TOTAL * FPS))


def start_of(seq):
    for i in range(len(toks) - len(seq) + 1):
        if toks[i:i + len(seq)] == seq:
            return words[i][1]
    raise SystemExit(f"beat not found: {seq}")


CUTS = [  # (first words of the beat, image, motion)
    (["think"], "img02", "in"),
    (["the", "station", "kept"], "img03", "in"),
    (["but", "here's", "the", "trick"], "img04", "right"),
    (13.88, "img04b", "hold"),                                         # "The gas pulls your car in." cut 0.5 s early, in the pause, so the magnet holds <= 4.5 s
    (["the", "little", "store"], "img05", "out"),
    (["about", "a", "third"], "img06", "in"),
    (["but", "seventy", "percent"], "img07", "hold"),
    (["that", "is", "why"], "img08", "in"),
    (["and", "that", "price"], "img09", "hold"),
    (["driver", "wonder"], "img10_loop", None),                            # loop frame: clean, no motion, no overlay
]
HOOK_FR = sorted((HERE / "hook_frames").glob("f*.png"))
SHOTS = [(0, "hook", None)] + [(int(round((s if isinstance(s, float) else start_of(s)) * FPS)), n, m) for s, n, m in CUTS]
LOOP_FRAME = SHOTS[-1][0]
SHOT9 = (SHOTS[-2][0], SHOTS[-1][0])


def load(path):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def view(img, motion, p):
    if motion is None:
        return img
    z, fx, fy = {"in": (1 + 0.08 * p, .5, .5), "out": (1.08 - 0.08 * p, .5, .5), "hold": (1.0 + 0.03 * p, .5, .5),
                 "right": (1.10, .45 + .10 * p, .5)}[motion]
    cw, ch = W / z, H / z
    x = min(max(fx * W - cw / 2, 0), W - cw)
    y = min(max(fy * H - ch / 2, 0), H - ch)
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


# ---------------------------------------------------------------- overlays
def hook_text_layer():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    lines = [("ALL THAT MONEY", WHITE), ("THEY KEEP 5¢?!", YEL)]
    f = min((fit(d, t, W - 140, 76) for t, _ in lines), key=lambda x: x.size)
    for (t, col), y in zip(lines, (233, 313)):   # ends above the 67.67 digits (they start at y~350)
        outlined(d, (W / 2, y), t, f, col)
    return lay


def cta_layer():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f1, f2 = font(50), font(44)
    outlined(d, (W / 2, 1530), "FOLLOW FOR TOMORROW'S STORY", f1, YEL)
    outlined(d, (W / 2, 1595), "New business story tomorrow", f2, WHITE)
    return lay


HOOK_TEXT, CTA = hook_text_layer(), cta_layer()
SHAKE_F = {27: (16, -4), 28: (-18, 5), 29: (14, -3)}                   # 0.90-0.97 s: 3-frame shake
BLAST_F = {30: -140, 31: -330, 32: -560}                               # then up and off the top, fully gone from frame 32 (1.07 s)


def hook_text_offset(i):
    if i in SHAKE_F: return SHAKE_F[i]
    if i in BLAST_F: return (0, BLAST_F[i])
    if i < 27: return (0, 0)
    return None


def groups(ws, maxn=3):
    gs, cur = [], []
    for w in ws:
        if cur and (len(cur) >= maxn or w[1] - cur[-1][2] > 0.35):
            gs.append(cur); cur = []
        cur.append(w)
    if cur: gs.append(cur)
    return gs


GS = groups(words)
CAPF = font(92)


def main():
    imgs = {n: load(HERE / f"{n}.png") for _, n, _ in SHOTS if n != "hook"}
    hook = [load(p) for p in HOOK_FR]
    ow, oh = (W, H) if FINAL else (540, 960)
    out = HERE / ("gas-station-1080.mp4" if FINAL else "preview_540.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(AUDIO), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{NFR / FPS:.3f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "17" if FINAL else "23", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [NFR]
    (HERE / "render_frames").mkdir(exist_ok=True)
    for i in range(NFR):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= i)
        f0, name, mo = SHOTS[k]
        if name == "hook":
            fr = hook[min(i, len(hook) - 1)].copy()
        else:
            fr = view(imgs[name], mo, (i - f0) / max(1, starts[k + 1] - f0))
        fr = fr.convert("RGBA")
        off = hook_text_offset(i) if name == "hook" else None
        if off is not None:
            dx, dy = off
            w, h = W - abs(dx), H - abs(dy)
            sx, sy = max(0, -dx), max(0, -dy)
            fr.alpha_composite(HOOK_TEXT, dest=(max(0, dx), max(0, dy)), source=(sx, sy, sx + w, sy + h))
        if SHOT9[0] <= i < SHOT9[1]:
            fr.alpha_composite(CTA)
        g = next((g for g in GS if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None) if t < NARR else None
        if g:
            d = ImageDraw.Draw(fr)
            txt = [w[0].upper() for w in g]
            cf = CAPF
            while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50:
                cf = font(cf.size - 4)
            widths = [d.textlength(w + " ", font=cf) for w in txt]
            x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
            for w, wd, (_, a, b) in zip(txt, widths, g):
                outlined(d, (x, CAP_Y), w, cf, YEL if a - 0.05 <= t <= b + 0.05 else WHITE, anchor="lm")
                x += wd
        fr = fr.convert("RGB")
        if i in KEEP: fr.save(HERE / "render_frames" / f"r{i:04d}.png")
        if not FINAL: fr = fr.resize((ow, oh), Image.LANCZOS)
        wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait()
    print(out, "shots (frame,name):", [(s[0], s[1]) for s in SHOTS], "frames", NFR, "=", round(NFR / FPS, 3), "s")


main()
