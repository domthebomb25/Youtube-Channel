"""3-second viral hook: shot1 (0-0.5s) low-angle shock, shot2 (0.5-1.5s) Roadster fly-over, shot3 (1.5-3.0s) snap-zoom face,
with slanted Anton text ("FLY?" 3x, blue glow, shaking "?"), camera shake, chromatic aberration on the slam, rocket SFX.

usage: python3 viral_hook.py CLIP1 CLIP2 CLIP3 SFX OUT.mp4
"""
import math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR = 1080, 1920, 24, 3.0
N = int(DUR * FPS)
ANTON = "/home/user/Youtube-Channel/videos/costco-hot-dog/assembly/fonts/Anton.ttf"
BLUE = (40, 150, 255)
# (start, end, clip index, offset into clip)
SHOTS = [(0.0, 0.5, 0, 0.0), (0.5, 1.5, 1, 0.2), (1.5, 3.0, 2, 0.0)]
SLAM1, SLAM2 = 1.50, 1.72       # small line, then FLY?
TXT_Y = 1440                    # below the mouth, over the chest; inside the Shorts safe zone


def frames(path, t0, t1):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-t", str(t1 - t0), "-i", path, "-vf",
                          f"fps={FPS},scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    n = len(raw) // (W * H * 3)
    return [Image.frombuffer("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]


def shake(im, amp, t):
    dx, dy = amp * math.sin(t * 95), amp * math.cos(t * 83)
    return im.transform((W, H), Image.AFFINE, (1, 0, dx, 0, 1, dy), Image.BILINEAR)


def zoom(im, z):
    cw, ch = W / z, H / z
    return im.transform((W, H), Image.EXTENT, ((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2), Image.BICUBIC)


def text_layer(txt, size, fill, stroke, center, rot_shear=0.22, shadow=True):
    """One word/line as an RGBA layer, slanted for speed."""
    f = ImageFont.truetype(ANTON, size)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if shadow:
        d.text((center[0] + 8, center[1] + 12), txt, font=f, fill=(0, 0, 0, 170), anchor="mm", stroke_width=stroke)
        lay = lay.filter(ImageFilter.GaussianBlur(5)); d = ImageDraw.Draw(lay)
    d.text(center, txt, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    cx, cy = center
    return lay.transform((W, H), Image.AFFINE, (1, rot_shear, -rot_shear * cy, 0, 1, 0), Image.BICUBIC)


def glow(txt, size, center, strength):
    f = ImageFont.truetype(ANTON, size)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((center[0], center[1] + 20), txt, font=f, fill=BLUE + (255,), anchor="mm", stroke_width=34)
    lay = lay.filter(ImageFilter.GaussianBlur(26))
    a = np.array(lay).astype(np.float32); a[..., 3] *= strength
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def chroma(layer, off):
    """Red/blue channel split on an RGBA layer."""
    a = np.array(layer)
    out = a.copy()
    out[..., 0] = np.roll(a[..., 0], off, axis=1)
    out[..., 2] = np.roll(a[..., 2], -off, axis=1)
    out[..., 3] = np.maximum(np.maximum(np.roll(a[..., 3], off, axis=1), np.roll(a[..., 3], -off, axis=1)), a[..., 3])
    return Image.fromarray(out)


def ease_out(p): return 1 - (1 - min(max(p, 0), 1)) ** 3


def main():
    c1, c2, c3, sfx, out = sys.argv[1:6]
    clips = [c1, c2, c3]
    src = []
    for s, e, k, off in SHOTS:
        src.append(frames(clips[k], off, off + (e - s) + 0.1))
    first = src[0][0]
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", sfx, "-t", str(DUR),
                           "-af", f"atrim=0:{DUR},afade=t=out:st={DUR - 0.15}:d=0.15", "-c:v", "libx264", "-preset", "slow",
                           "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)
    base1 = (W // 2, TXT_Y - 175)
    base2 = (W // 2, TXT_Y + 95)
    for i in range(N):
        t = i / FPS
        k = max(j for j, s in enumerate(SHOTS) if SHOTS[j][0] <= t)
        s, e, _, _ = SHOTS[k]
        idx = min(int(round((t - s) * FPS)), len(src[k]) - 1)
        fr = src[k][idx]
        if k == 1:
            fr = shake(fr, 14 * (1 - (t - s) / (e - s) * 0.4), t)
        if k == 2:
            p = (t - s) / (e - s)
            fr = zoom(fr, 1.0 + 0.32 * (1 - ease_out(p * 4)) + 0.05 * p)       # snap zoom: punch in, settle
            fr = shake(fr, 20 * max(0, 1 - (t - s) / 0.5), t)
        if abs(t - 1.5) < 1 / FPS:                                                # impact flash on the cut to shot 3
            fr = Image.blend(fr, Image.new("RGB", (W, H), (255, 255, 255)), 0.65)
        # loop: last frames melt back to the opening frame
        if t > DUR - 0.17:
            fr = Image.blend(fr, first, (t - (DUR - 0.17)) / 0.17)
        fr = fr.convert("RGBA")
        # --- kinetic text ---
        if t >= SLAM1:
            p1 = ease_out((t - SLAM1) / 0.12)
            sz1 = int(88 * (1.8 - 0.8 * p1))
            lay = text_layer("THE TESLA ROADSTER CAN", sz1, (255, 255, 255, 255), 7, (base1[0], base1[1]))
            if t - SLAM1 < 0.3:
                lay = chroma(lay, int(10 * (1 - (t - SLAM1) / 0.3)))
            fr.alpha_composite(lay)
        if t >= SLAM2:
            q = t - SLAM2
            p2 = ease_out(q / 0.14)
            sz = int(330 * (2.6 - 1.6 * p2))                      # slams down from huge to 3x
            sz = min(sz, 330)
            jit = 22 * max(0, 1 - q / 0.5)
            cx = base2[0] + jit * math.sin(q * 160) - 40
            cy = base2[1] + jit * math.cos(q * 130)
            gl = glow("FLY", sz, (cx, cy), 1.0 + 0.0 * math.sin(t * 18))
            fr.alpha_composite(gl)
            fly = text_layer("FLY", sz, (255, 255, 255, 255), 16, (cx, cy))
            qm_sz = int(sz * 0.62)
            qx = cx + sz * 0.88 + 5 * math.sin(t * 90)           # the small "?" vibrates
            qy = cy - sz * 0.18 + 5 * math.cos(t * 110)
            qm = text_layer("?", qm_sz, (255, 255, 255, 255), 11, (qx, qy))
            both = Image.alpha_composite(fly, qm)
            if q < 0.35:
                both = chroma(both, int(14 * (1 - q / 0.35)))
            fr.alpha_composite(both)
        wr.stdin.write(fr.convert("RGB").tobytes())
    wr.stdin.close(); wr.wait()
    print(out)


if __name__ == "__main__":
    main()
