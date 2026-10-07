"""Build a vertical 1080x1920 Short from segments of the final video.

usage: python3 make_short.py <clip.json>
clip.json: {"name", "segments": [[t0, t1], ...], "title": [line1, line2], "end": [line1, line2]}
Times refer to the final video / clips/voiceover.mp3 timeline.
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "final/costco-hot-dog-final-1080p-10mbps.mp4"
FONT = str(ROOT / "assembly/fonts/LuckiestGuy.ttf")
MASCOT = ROOT.parent.parent / "channel/profile/raw/p3-nobrows.png"
W, H, FPS = 1080, 1920, 30
VID_Y = 620                      # top of the 16:9 picture (1080x608)
CAP_Y = 1330                     # caption centre; stays above the bottom 20% UI zone
WHITE, YEL, INK, BLUE = (255, 255, 255), (255, 214, 0), (15, 15, 15), (7, 77, 172)
END_SEC = 2.0


def font(s): return ImageFont.truetype(FONT, s)


def outlined(d, xy, text, f, fill, anchor="mm"):
    d.text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=max(4, f.size // 9), stroke_fill=INK)


def fit(text, maxw, start):
    s = start
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    while s > 20:
        b = probe.textbbox((0, 0), text, font=font(s), stroke_width=s // 9)
        if b[2] - b[0] <= maxw: return font(s)
        s -= 2
    return font(s)


def words_for(segs):
    W_ = json.load(open(ROOT / "clips/word_timing.json"))
    out, off = [], 0.0
    for t0, t1 in segs:
        for w, a, b in W_:
            if t0 <= a < t1:
                out.append((re.sub(r"\(\d+\)$", "", w), a - t0 + off, min(b, t1) - t0 + off))
        off += t1 - t0
    return out, off


MERGE = [(("nineteen", "eighty", "three"), "1983"), (("nineteen", "eighty", "five"), "1985"),
         (("two", "thousand", "nine"), "2009"), (("twenty", "thirteen"), "2013"), (("twenty", "nineteen"), "2019"),
         (("twenty", "twenty", "five"), "2025"), (("twenty", "twenty", "six"), "2026"), (("s",), "2000s")]


def tidy(words):
    out, i = [], 0
    while i < len(words):
        for seq, rep in MERGE:
            n = len(seq)
            if tuple(w[0] for w in words[i:i + n]) == seq:
                out.append((rep, words[i][1], words[i + n - 1][2])); i += n; break
        else:
            out.append(words[i]); i += 1
    return out


def groups(words, maxn=3):
    gs, cur = [], []
    for i, w in enumerate(words):
        if cur and (len(cur) >= maxn or w[1] - cur[-1][2] > 0.35):
            gs.append(cur); cur = []
        cur.append(w)
    if cur: gs.append(cur)
    return gs


def cut(segs, out):
    parts = []
    for i, (a, b) in enumerate(segs):
        p = out.parent / f"{out.stem}_seg{i}.mp4"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-i", str(SRC), "-t", f"{b - a:.3f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-r", str(FPS),
                        "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(p.with_suffix(".mov"))], check=True)
        parts.append(p.with_suffix(".mov"))
    lst = out.parent / f"{out.stem}_list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out)], check=True)
    for p in parts: p.unlink()
    lst.unlink()


EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"


def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI_FONT, 109)
    im = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((int(im.width * size / im.height), size), Image.LANCZOS)


def static_layers(title):
    top = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(top)
    if len(title) == 2:
        f1 = fit(title[0], W - 120, 110); f2 = fit(title[1], W - 120, 110)
        outlined(d, (W / 2, 330), title[0], f1, WHITE)
        outlined(d, (W / 2, 330 + f1.size * 1.05), title[1], f2, YEL)
        return top
    # 3+ lines; a trailing emoji (non-ASCII last char) is drawn in colour
    colours = [WHITE, YEL, WHITE, YEL]
    lines = []
    for t in title:
        emo = t[-1] if ord(t[-1]) > 0x2000 else None
        lines.append((t[:-1].rstrip() if emo else t, emo))
    fs = min(fit(t + (" XX" if e else ""), W - 100, 96).size for t, e in lines)
    f = font(fs)
    y = 590 - (len(lines) - 1) * fs * 1.05 - fs * 0.55
    for i, (t, e) in enumerate(lines):
        tw = d.textlength(t, font=f); ew = int(fs * 1.1) if e else 0
        x = (W - tw - (ew + 16 if e else 0)) / 2
        outlined(d, (x, y), t, f, colours[i], anchor="lm")
        if e:
            em = emoji_img(e, int(fs * 1.05))
            top.alpha_composite(em, (int(x + tw + 16), int(y - em.height / 2)))
        y += fs * 1.05
    return top


def end_card(lines):
    img = Image.new("RGB", (W, H), BLUE)
    glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse((90, 380, 990, 1280), fill=120)
    img = Image.composite(Image.new("RGB", (W, H), (40, 115, 215)), img, glow.filter(ImageFilter.GaussianBlur(140)))
    src = np.array(Image.open(MASCOT).convert("RGB")).astype(float)
    a = np.clip((np.sqrt(((src - np.array(BLUE)) ** 2).sum(2)) - 45) / 40, 0, 1)
    fade = np.ones(src.shape[0]); fade[-140:] = np.linspace(1, 0, 140); a *= fade[:, None]
    m = Image.fromarray(np.dstack([src, a * 255]).astype(np.uint8), "RGBA").crop((90, 40, 934, 1024))
    m = m.resize((620, int(620 * m.height / m.width)), Image.LANCZOS)
    img = img.convert("RGBA"); img.alpha_composite(m, ((W - m.width) // 2, 640))
    d = ImageDraw.Draw(img)
    outlined(d, (W / 2, 330), lines[0], fit(lines[0], W - 120, 120), WHITE)
    outlined(d, (W / 2, 470), lines[1], fit(lines[1], W - 160, 100), YEL)
    if len(lines) > 2:
        outlined(d, (W / 2, 575), lines[2], fit(lines[2], W - 200, 70), WHITE)
    return img.convert("RGB")


def main():
    spec = json.load(open(sys.argv[1]))
    outdir = Path(sys.argv[1]).resolve().parent
    seg = outdir / f"_{spec['name']}-src.mp4"
    cut(spec["segments"], seg)
    words, total = words_for(spec["segments"])
    gs = groups(tidy(words))
    top = static_layers(spec["title"])
    endimg = np.asarray(end_card(spec["end"]))
    cap_f = font(92)
    nfr = int(round(total * FPS)); nend = int(END_SEC * FPS)
    out = outdir / f"{spec['name']}.mp4"
    rd = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(seg), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(seg), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad=pad_dur={END_SEC},afade=t=out:st={total - 0.15:.2f}:d=0.15",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)],
                          stdin=subprocess.PIPE)
    fsz = 1920 * 1080 * 3
    for i in range(nfr):
        buf = rd.stdout.read(fsz)
        if len(buf) < fsz: break
        fr = Image.frombuffer("RGB", (1920, 1080), buf)
        bg = fr.resize((int(1920 * H / 1080), H), Image.BILINEAR)
        x0 = (bg.width - W) // 2
        bg = bg.crop((x0, 0, x0 + W, H)).resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
        bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.45).convert("RGBA")
        pic = fr.resize((W, 608), Image.LANCZOS)
        bg.paste(pic, (0, VID_Y))
        ImageDraw.Draw(bg).rectangle((0, VID_Y - 4, W, VID_Y + 611), outline=INK, width=6)
        bg.alpha_composite(top)
        t = i / FPS
        g = next((g for g in gs if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None)
        if g:
            d = ImageDraw.Draw(bg)
            txt = [w[0].upper() for w in g]
            cf = cap_f
            while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50:
                cf = font(cf.size - 4)
            widths = [d.textlength(w + " ", font=cf) for w in txt]
            x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
            for w, wd, (_, a, b) in zip(txt, widths, g):
                outlined(d, (x, CAP_Y), w, cf, YEL if a - 0.05 <= t <= b + 0.05 else WHITE, anchor="lm")
                x += wd
        wr.stdin.write(bg.convert("RGB").tobytes())
    rd.stdout.close(); rd.wait()
    for _ in range(nend): wr.stdin.write(endimg.tobytes())
    wr.stdin.close(); wr.wait()
    seg.unlink()
    print(out, round(total + END_SEC, 1), "s")


if __name__ == "__main__":
    main()
