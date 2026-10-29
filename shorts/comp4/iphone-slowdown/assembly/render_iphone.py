"""iPhone Slowdown Short (Compilation #4, posting #1) renderer.
usage: python3 render_iphone.py [--preview]     (preview = 540x960; final = 1080x1920, run once after preview approval)
Inputs (all APPROVED, not regenerated here): clips/hook.mp4 (Kling take 2, natural speed), clips/voice_norm.wav
(voiceover_v2 at -14 LUFS), images/img01..img10.png, assembly/align_tokens.json (pocketsphinx word timings)."""
import json, math, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent.parent.parent
sys.path.insert(0, str(REPO / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402  (font, outlined, fit, groups, YEL, WHITE)

W, H, FPS = 1080, 1920, 30
CAP_Y = 1330
PREVIEW = "--preview" in sys.argv

# ---- timeline (seconds on the approved voiceover_v2 timeline) ----
LINE_END = [2.83, 5.15, 8.84, 11.74, 15.06, 18.04, 23.34, 26.18]      # approved line ends
TOTAL_FR = 792                                                          # 26.40 s (audio 26.38 s)
LOOP_T = 25.70                                                          # loop frame (image 1) start, ~0.7 s
tok = json.load(open(HERE / "align_tokens.json"))                       # [name, start, end, line_index]
def tok_start(line, name):
    return next(t[1] for t in tok if t[3] == line and re.sub(r"\(\d+\)$", "", t[0]) == name)
SPLIT_TO = tok_start(4, "to")        # L5: image 6 starts at "to stop"
SPLIT_A = tok_start(5, "a")          # L6: image 8 starts at "a fresh battery"
SHOTS = [(0.0, "hook"), (LINE_END[0], "img02"), (LINE_END[1], "img03"), (LINE_END[2], "img04"), (LINE_END[3], "img05"),
         (SPLIT_TO, "img06"), (LINE_END[4], "img07"), (SPLIT_A, "img08"), (LINE_END[5], "img09"),
         (LINE_END[6], "img10"), (LOOP_T, "img01")]
HOOK_LEN = LINE_END[0]
STATIC = {"hook", "img01"}           # no push-in on the hook and the loop frame
CTA = (LINE_END[6], LOOP_T)          # FOLLOW + tomorrow tease on image 10, gone before the loop frame

# ---- caption words (locked script; numerals in caption form) ----
MERGES = [(("five", "hundred"), "$500"), (("million", "dollars"), "million"), (("seventy", "nine", "dollars"), "$79"),
          (("twenty", "nine", "dollars"), "$29"), (("i", "phone"), "iPhone"), (("i", "phones"), "iPhones")]
def caption_words():
    toks = [(re.sub(r"\(\d+\)$", "", t[0]), t[1], t[2]) for t in tok]
    out, i = [], 0
    while i < len(toks):
        for seq, rep in MERGES:
            n = len(seq)
            if tuple(t[0] for t in toks[i:i + n]) == seq:
                out.append((rep, toks[i][1], toks[i + n - 1][2])); i += n; break
        else:
            out.append(toks[i]); i += 1
    return out
CAPS = caption_words()
json.dump(CAPS, open(HERE / "word_timing.json", "w"))
GROUPS = m.groups(CAPS)
CAP_F = m.font(92)

# ---- images / hook ----
def load(name):
    im = Image.open(ROOT / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def push(img, p):                    # gentle 3% push-in
    z = 1.0 + 0.03 * p
    cw, ch = W / z, H / z
    x, y = (W - cw) / 2, (H - ch) / 2
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)

def decode_hook():
    n = int(round(HOOK_LEN * FPS))                       # trim (not speed-change) the natural 3.04 s clip to 2.83 s
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ROOT / "clips/hook.mp4"), "-vf",
                          f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS}",
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return [Image.frombuffer("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw), W * H * 3)]

def text_layer(lines, y0, size, step=1.12):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t[0], W - 120, size).size for t in lines)
    f = m.font(fs)
    y = y0
    for t, col in lines:
        m.outlined(d, (W / 2, y), t, f, col, anchor="mm")
        y += fs * step
    return lay

HOOK_TXT = text_layer([("APPLE SLOWED YOUR IPHONE DOWN", m.WHITE), ("AND NEVER TOLD YOU.", m.YEL)], 96, 84)
CTA_TXT = text_layer([("FOLLOW", m.YEL)], 215, 150)
CTA_TXT2 = text_layer([("New business story tomorrow", m.WHITE)], 335, 70)
# hook text blast: frame -> (dx, dy); text sits static until frame 30 (1.0 s)
BLAST = {30: (14, 4), 31: (-16, -5), 32: (10, 3), 33: (0, -120), 34: (0, -420), 35: (0, -1000)}

def hook_text(fr, i):
    if i >= 36:
        return fr                                         # fully gone by 1.2 s
    dx, dy = BLAST.get(i, (0, 0))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay.paste(HOOK_TXT, (dx, dy))
    fr.alpha_composite(lay)
    return fr

def captions(fr, t):
    g = next((g for g in GROUPS if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None)
    if not g:
        return
    d = ImageDraw.Draw(fr)
    txt = [w[0].upper() for w in g]
    cf = CAP_F
    while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50:
        cf = m.font(cf.size - 4)
    widths = [d.textlength(w + " ", font=cf) for w in txt]
    x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
    for w, wd, (_, a, b) in zip(txt, widths, g):
        m.outlined(d, (x, CAP_Y), w, cf, m.YEL if a - 0.05 <= t <= b + 0.05 else m.WHITE, anchor="lm")
        x += wd

def main():
    imgs = {n: load(n) for _, n in SHOTS if n != "hook"}
    hook = decode_hook()
    ow, oh = (540, 960) if PREVIEW else (W, H)
    out = ROOT / ("preview-540p.mp4" if PREVIEW else "iphone-slowdown.mp4")
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(ROOT / "clips/voice_norm.wav"), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad,atrim=0:{TOTAL_FR / FPS:.3f}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "23" if PREVIEW else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [TOTAL_FR / FPS]
    dump = {} if "--dump" in sys.argv else None
    for i in range(TOTAL_FR):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t + 1e-9)
        t0, name = SHOTS[k]
        if name == "hook":
            fr = hook[min(i, len(hook) - 1)].copy().convert("RGBA")
            fr = hook_text(fr, i)
        else:
            fr = imgs[name] if name in STATIC else push(imgs[name], (t - t0) / (starts[k + 1] - t0))
            fr = fr.convert("RGBA")
        if name == "img10" and CTA[0] <= t < CTA[1]:
            fr.alpha_composite(CTA_TXT); fr.alpha_composite(CTA_TXT2)
        captions(fr, t)
        fr = fr.convert("RGB")
        if dump is not None and i in (0, 29, 30, 31, 33, 34, 35, 36, 37, 38):
            fr.save(HERE / f"dump_{i:03d}.png")
        if PREVIEW:
            fr = fr.resize((ow, oh), Image.LANCZOS)
        wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait()
    print(out, TOTAL_FR / FPS, "s | splits:", round(SPLIT_TO, 2), round(SPLIT_A, 2))

main()
