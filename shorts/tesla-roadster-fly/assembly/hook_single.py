"""Hook from ONE clip (the fly-over clip): slanted Anton text, FLY? in red (3x, red glow, shaking "?"), rocket SFX + bass hit on the slam.

usage: python3 hook_single.py CLIP SFX OUT.mp4
"""
import math, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image
import viral_hook as v

W, H, FPS, DUR = v.W, v.H, v.FPS, 3.0
RED = (235, 40, 35, 255)
v.BLUE = (255, 40, 30)           # glow colour used by viral_hook.glow()
SFX_TRIM = 0.35                  # the AI sound starts ~0.4 s in; the car is on screen from 0 s
SLAM1, SLAM2 = 1.15, 1.45        # small line, then FLY? (lands with the big flare)
TXT_Y = 1430                     # over his legs and the dust; face and the car stay clear


def main():
    clip, sfx, out = sys.argv[1:4]
    src = v.frames(clip, 0.0, DUR + 0.1)
    tmp = Path(tempfile.mkdtemp(dir=Path(out).parent))
    boom = tmp / "boom.wav"
    # synthetic sub boom for the slam (free): 110 -> 35 Hz sweep with a fast decay
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "aevalsrc='0.9*sin(2*PI*(35*t+75*(1-exp(-9*t))/9))*exp(-6*t)':d=0.6:s=48000", str(boom)], check=True)
    ms = int(SLAM2 * 1000)
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-ss", str(SFX_TRIM), "-i", sfx, "-i", str(boom), "-filter_complex",
                           f"[1:a]volume=1.0,afade=t=out:st={DUR - 0.3}:d=0.3[a1];[2:a]adelay={ms}|{ms},volume=1.2[a2];"
                           f"[a1][a2]amix=inputs=2:duration=first:normalize=0,atrim=0:{DUR}[a]",
                           "-map", "0:v", "-map", "[a]", "-t", str(DUR), "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)
    base1 = (W // 2, TXT_Y - 175)
    base2 = (W // 2, TXT_Y + 95)
    for i in range(int(DUR * FPS)):
        t = i / FPS
        fr = src[min(i, len(src) - 1)]
        if SLAM2 <= t < SLAM2 + 0.4:
            fr = v.shake(fr, 18 * (1 - (t - SLAM2) / 0.4), t)
        fr = fr.convert("RGBA")
        if t >= SLAM1:
            p1 = v.ease_out((t - SLAM1) / 0.12)
            lay = v.text_layer("THE TESLA ROADSTER CAN", int(88 * (1.8 - 0.8 * p1)), (255, 255, 255, 255), 7, base1)
            if t - SLAM1 < 0.3:
                lay = v.chroma(lay, int(10 * (1 - (t - SLAM1) / 0.3)))
            fr.alpha_composite(lay)
        if t >= SLAM2:
            q = t - SLAM2
            sz = min(int(330 * (2.6 - 1.6 * v.ease_out(q / 0.14))), 330)
            jit = 22 * max(0, 1 - q / 0.5)
            cx, cy = base2[0] + jit * math.sin(q * 160) - 40, base2[1] + jit * math.cos(q * 130)
            fr.alpha_composite(v.glow("FLY", sz, (cx, cy), 1.0))
            fly = v.text_layer("FLY", sz, RED, 16, (cx, cy))
            qm = v.text_layer("?", int(sz * 0.62), RED, 11,
                              (cx + sz * 0.88 + 5 * math.sin(t * 90), cy - sz * 0.18 + 5 * math.cos(t * 110)))
            both = Image.alpha_composite(fly, qm)
            if q < 0.35:
                both = v.chroma(both, int(14 * (1 - q / 0.35)))
            fr.alpha_composite(both)
        wr.stdin.write(fr.convert("RGB").tobytes())
    wr.stdin.close(); wr.wait()
    boom.unlink(); tmp.rmdir()
    print(out)


if __name__ == "__main__":
    main()
