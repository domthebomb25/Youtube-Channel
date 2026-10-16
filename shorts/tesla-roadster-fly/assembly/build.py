"""Tesla Roadster Short: stickman hook (animated clip + big text) + the user's event recording (layout A: wide footage
centered over a dark blurred copy of itself).

usage: python3 build.py HOOK_CLIP RECORDING OUT.mp4 [--preview]
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, "/home/user/Youtube-Channel/videos/costco-hot-dog/shorts")
import make_short as m  # noqa: E402  (fonts + outlined text)

W, H, FPS = 1080, 1920, 30
HOOK_SEC = 2.2
TOP_Y = 800                       # clear sky between the flying car and his head; inside every app's safe area
CROP = "crop=1180:572:0:698"      # the footage strip inside the screen recording
RED = (235, 50, 40)


def hook_text(top_y=TOP_Y, last="FLY"):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f1 = m.fit("THE TESLA ROADSTER", W - 160, 100)
    f2 = m.font(170)
    m.outlined(d, (W / 2, top_y - 40), "THE TESLA ROADSTER", f1, m.WHITE)
    w1, w2 = d.textlength("CAN ", font=f2), d.textlength(last, font=f2)
    x = (W - w1 - w2) / 2
    m.outlined(d, (x, top_y + 90), "CAN ", f2, m.WHITE, anchor="lm")
    m.outlined(d, (x + w1, top_y + 90), last, f2, m.YEL, anchor="lm")
    return lay


def main():
    hook_clip, rec, out = sys.argv[1:4]
    preview = "--preview" in sys.argv
    opt = dict(a.lstrip("-").split("=") for a in sys.argv if a.startswith("--") and "=" in a)
    tmp = Path(out).with_suffix(".hook.mp4") if "--hook-only" not in sys.argv else Path(out)
    lay = hook_text(int(opt.get("texty", TOP_Y)), opt.get("last", "FLY"))
    hook_sec = float(opt.get("sec", HOOK_SEC))
    n = int(hook_sec * FPS)
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", hook_clip, "-t", str(hook_sec),
                          "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    frames = [Image.frombuffer("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw), W * H * 3)]
    wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                           "-t", str(hook_sec), "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(tmp)], stdin=subprocess.PIPE)
    for i in range(n):
        fr = frames[min(i, len(frames) - 1)].convert("RGBA")
        fr.alpha_composite(lay)
        wr.stdin.write(fr.convert("RGB").tobytes())
    wr.stdin.close(); wr.wait()
    if "--hook-only" in sys.argv:
        print(out); return

    fc = (f"[0:v]{CROP},split[a][b];[a]scale=-2:{H},crop={W}:{H},boxblur=30:5,eq=brightness=-0.15[bg];"
          f"[b]scale={W}:-2[fg];[bg][fg]overlay=0:(H-h)/2,fps={FPS},format=yuv420p[v];"
          f"[0:a]aresample=48000,aformat=channel_layouts=stereo[a]")
    main_seg = Path(out).with_suffix(".main.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", rec, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-c:a", "aac", "-b:a", "192k", str(main_seg)], check=True)
    vf = "scale=540:960," if preview else ""
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-i", str(main_seg), "-filter_complex",
                    f"[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a];[v]{vf}format=yuv420p[vo]", "-map", "[vo]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "22" if preview else "20", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)
    tmp.unlink(); main_seg.unlink()
    print(out)


if __name__ == "__main__":
    main()
