"""Build a vertical 1080x1920 part from the 16:9 compilation (same look as the Costco parts).

usage: python3 make_part.py <part.json> <compilation.mp4> <word_timing.json> [--preview]
part.json: {"name", "segments": [[t0, t1], ...], "title": [3 lines], "end": [3 lines], "badge": "PART 1 OF 4"}
Frames that hold a vertical Short (already captioned) are cropped to fill 1080x1920; title, bridge and outro
frames are 16:9, so they use the Costco layout (blurred background, picture centred, burned-in captions).
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "costco-hot-dog/shorts"))
import make_short as ms

W, H, FPS = ms.W, ms.H, ms.FPS
# source-time ranges where the frame is a vertical Short (608x1080 window centred in the 1920x1080 frame)
VERT = [(7.4, 14.9), (16.5, 60.5), (67.6, 101.2), (105.9, 121.8), (125.0, 156.2), (162.1, 211.8),
        (220.1, 249.4), (256.9, 291.6)]
X0, X1 = 656, 1264


def is_vert(t): return any(a <= t < b for a, b in VERT)


def main():
    spec = json.load(open(sys.argv[1])); src = sys.argv[2]; wt = json.load(open(sys.argv[3]))
    prev = "--preview" in sys.argv
    outdir = Path(sys.argv[1]).resolve().parent
    segs = spec["segments"]
    total = sum(b - a for a, b in segs)
    words, off = [], 0.0
    for t0, t1 in segs:
        words += [(w.strip(".,?!"), a - t0 + off, min(b, t1) - t0 + off) for w, a, b in wt if t0 <= a < t1]
        off += t1 - t0
    gs = ms.groups(ms.tidy([(w.lower(), a, b) for w, a, b in words]))
    top = ms.static_layers(spec["title"])
    endimg = np.asarray(ms.end_card(spec["end"]))
    badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ms.outlined(ImageDraw.Draw(badge), (W / 2, 1690), spec["badge"], ms.font(50), ms.YEL)
    cap_f = ms.font(92)
    flt = "+".join(f"between(t,{a},{b})" for a, b in segs)
    # concat the segments (video + audio) into one temp file
    seg = outdir / f"_{spec['name']}-src.mkv"
    parts = []
    for i, (a, b) in enumerate(segs):
        p = outdir / f"_{spec['name']}_s{i}.mov"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-i", src, "-t", f"{b - a:.3f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-r", str(FPS),
                        "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(p)], check=True)
        parts.append(p)
    lst = outdir / f"_{spec['name']}_list.txt"; lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(seg)], check=True)
    # source time for each output frame
    def src_t(t):
        for a, b in segs:
            if t < b - a: return a + t
            t -= b - a
        return segs[-1][1]
    nfr = int(round(total * FPS)); nend = int(ms.END_SEC * FPS)
    out = outdir / f"{spec['name']}{'-preview' if prev else ''}.mp4"
    rd = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(seg), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(seg), "-map", "0:v", "-map", "1:a",
                           "-af", f"apad=pad_dur={ms.END_SEC},afade=t=out:st={total - 0.15:.2f}:d=0.15",
                           "-c:v", "libx264", "-preset", "veryfast" if prev else "medium", "-crf", "26" if prev else "23",
                           "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "160k",
                           "-movflags", "+faststart", "-shortest", str(out)], stdin=subprocess.PIPE)
    fsz = 1920 * 1080 * 3
    for i in range(nfr):
        buf = rd.stdout.read(fsz)
        if len(buf) < fsz: break
        fr = Image.frombuffer("RGB", (1920, 1080), buf)
        t = i / FPS
        if is_vert(src_t(t)):
            bg = fr.crop((X0, 0, X1, 1080)).resize((W, H), Image.LANCZOS).convert("RGBA")
            bg.alpha_composite(badge)
        else:
            bg = fr.resize((int(1920 * H / 1080), H), Image.BILINEAR)
            x0 = (bg.width - W) // 2
            bg = bg.crop((x0, 0, x0 + W, H)).resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
            bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.45).convert("RGBA")
            bg.paste(fr.resize((W, 608), Image.LANCZOS), (0, ms.VID_Y))
            d = ImageDraw.Draw(bg); d.rectangle((0, ms.VID_Y - 4, W, ms.VID_Y + 611), outline=ms.INK, width=6)
            bg.alpha_composite(top)
            g = next((g for g in gs if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None)
            if g:
                txt = [w[0].upper() for w in g]; cf = cap_f
                while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50: cf = ms.font(cf.size - 4)
                widths = [d.textlength(w + " ", font=cf) for w in txt]
                x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
                for w, wd, (_, a, b) in zip(txt, widths, g):
                    ms.outlined(d, (x, ms.CAP_Y), w, cf, ms.YEL if a - 0.05 <= t <= b + 0.05 else ms.WHITE, anchor="lm")
                    x += wd
        wr.stdin.write(bg.convert("RGB").tobytes())
    rd.stdout.close(); rd.wait()
    for _ in range(nend): wr.stdin.write(endimg.tobytes())
    wr.stdin.close(); wr.wait()
    for p in parts + [seg, lst]: p.unlink()
    print(out, round(total + ms.END_SEC, 1), "s")


if __name__ == "__main__":
    main()
