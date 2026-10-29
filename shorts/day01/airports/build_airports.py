"""Airports Short renderer. usage: python3 build_airports.py [--preview]
Reads assembly/config.py + assembly/word_timing.json; clips/hook.mp4, clips/voiceover.mp3, images/*.png.
Like shorts/day01/build_short.py, but the hook clip is trimmed (not stretched), the hook text shakes and blasts off at ~1.2s,
captions are word-for-word with the locked script, and the VO is normalised to -14 LUFS."""
import importlib.util, json, math, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "videos/costco-hot-dog/shorts"))
import make_short as m  # noqa: E402

spec = importlib.util.spec_from_file_location("cfg", HERE / "assembly/config.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

W, H, FPS = 1080, 1920, 30
CAP_DEFAULT = 1330
NARR, SHOTS = C.NARR, C.SHOTS


def load(name):
    im = Image.open(HERE / f"images/{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def view(img, motion, p):
    z = 1.0 + (0.03 * p if motion == "hold" else 0.0)      # gentle ~3% push-in on story stills; hook + loop frame static
    cw, ch = W / z, H / z
    x, y = (W - cw) / 2, (H - ch) / 2
    return img.transform((W, H), Image.EXTENT, (x, y, x + cw, y + ch), Image.BICUBIC)


def left_layer(lines, x0, y0, size):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fs = min(m.fit(t, W - x0 - 90, size).size for t in lines)
    f = m.font(fs)
    y = y0
    for i, t in enumerate(lines):
        m.outlined(d, (x0, y), t, f, m.YEL if i == 0 else m.WHITE, anchor="lm")
        y += fs * 1.08
    return lay


def center_layer(lines, sizes, ys, cols):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for t, s, y, c in zip(lines, sizes, ys, cols):
        f = m.fit(t, W - 160, s)
        m.outlined(d, (W / 2, y), t, f, c, anchor="mm")
    return lay


def shifted(lay, dx, dy):
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(lay, (int(dx), int(dy)), lay)
    return out


def caption_words():
    """Spoken (aligned) words -> the locked script's caption words ($6 BILLION, $4.3 BILLION), no punctuation."""
    ws = [list(w) for w in json.load(open(HERE / "assembly/word_timing.json"))]
    out, i = [], 0
    while i < len(ws):
        for seq, rep in C.MERGE:
            n = len(seq)
            if tuple(w[0] for w in ws[i:i + n]) == seq:
                a, b = ws[i][1], ws[i + n - 1][2]
                nb = n - 2                             # spoken number words ("four point three") collapse into one caption word
                num_end = ws[i + nb - 1][2]
                out.append((rep[0], a, num_end))
                out.append((rep[1], ws[i + nb][1], b))  # BILLION stays up through the spoken "dollars"
                i += n
                break
        else:
            out.append((ws[i][0].upper(), ws[i][1], ws[i][2]))
            i += 1
    return out


def loudnorm_wav(src, dst):
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af",
                           "loudnorm=I=-14:LRA=11:TP=-1.5:print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    j = json.loads(meas[meas.rindex("{"):])
    af = (f"loudnorm=I=-14:LRA=11:TP=-1.5:measured_I={j['input_i']}:measured_LRA={j['input_lra']}:"
          f"measured_TP={j['input_tp']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-af", af, "-ar", "48000", "-ac", "1", str(dst)], check=True)


def main():
    preview = "--preview" in sys.argv
    toks = caption_words()
    gs = m.groups(toks)
    imgs = {n: load(n) for _, n, _ in SHOTS if n != "hook"}
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-t", str(C.HOOK_SEC), "-i", str(HERE / "clips/hook.mp4"), "-vf",
                          f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    hook = [Image.frombuffer("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw), W * H * 3)]
    hook_text = left_layer(C.HOOK_TEXT, C.HOOK_TEXT_X, C.HOOK_TEXT_Y, 100)
    f0, f1, l1, l2 = C.FOLLOW
    follow = center_layer([l1, l2], [76, 46], [1450, 1522], [m.YEL, m.WHITE])
    cap_f = m.font(92)
    nfr = int(round(NARR * FPS))
    ow, oh = (540, 960) if preview else (W, H)
    out = HERE / ("preview-540p.mp4" if preview else "airports-1080p.mp4")
    norm = HERE / "clips/vo_norm.wav"
    loudnorm_wav(HERE / "clips/voiceover.mp3", norm)
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-i", str(norm), "-map", "0:v", "-map", "1:a",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "23" if preview else "17", "-pix_fmt", "yuv420p",
                           "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{NARR:.4f}",
                           "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    starts = [s[0] for s in SHOTS] + [NARR]
    for i in range(nfr):
        t = i / FPS
        k = max(j for j in range(len(SHOTS)) if SHOTS[j][0] <= t)
        t0, name, mo = SHOTS[k]
        fr = (hook[min(i, len(hook) - 1)].copy() if name == "hook"
              else view(imgs[name], mo, (t - t0) / (starts[k + 1] - t0)))
        fr = fr.convert("RGBA")
        if name == "hook":                                  # hook text: shake ~1.10s, blast off the top, gone by 1.20s
            if i < C.SHAKE_FRAMES[0]:
                fr.alpha_composite(hook_text)
            elif i in C.SHAKE_FRAMES:
                s = 1 if i == C.SHAKE_FRAMES[0] else -1
                fr.alpha_composite(shifted(hook_text, 16 * s, -10 * s))
            elif i == C.BLAST_FRAME:
                fr.alpha_composite(shifted(hook_text, 0, -820))
        if f0 <= t < f1:
            fr.alpha_composite(follow)
        g = next((g for g in gs if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None)
        if g:
            d = ImageDraw.Draw(fr)
            txt = [w[0] for w in g]
            cf = cap_f
            while sum(d.textlength(w + " ", font=cf) for w in txt) > W - 100 and cf.size > 50:
                cf = m.font(cf.size - 4)
            widths = [d.textlength(w + " ", font=cf) for w in txt]
            x = (W - sum(widths) + d.textlength(" ", font=cf)) / 2
            cy = C.CAP_Y.get(name, CAP_DEFAULT)
            for w, wd, (_, a, b) in zip(txt, widths, g):
                m.outlined(d, (x, cy), w, cf, m.YEL if a - 0.05 <= t <= b + 0.05 else m.WHITE, anchor="lm")
                x += wd
        fr = fr.convert("RGB")
        if preview:
            fr = fr.resize((ow, oh), Image.BILINEAR)
        wr.stdin.write(fr.tobytes())
    wr.stdin.close()
    wr.wait()
    print(out, round(NARR, 3), "s")


main()
