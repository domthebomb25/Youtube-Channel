"""Build the 8 new Compilation #1 clips (1920x1080, 30 fps) from the full-body mascot still + Benji voiceovers.

usage: python3 compilations/comp1/build_comp1.py     (from the repo root)
Intro/outro cut to a new camera move every ~3 s on the same still; bridges are one slow zoom each.
Tail = voiceover length + 0.25 s. No fade, no end card, no music.
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
IMG = ASSETS / "mascot-full-16x9.png"
FPS, TAIL = 30, 0.25

# (zoom_start, zoom_end, cx, cy): camera moves on the still, cx/cy = view centre as a fraction of the frame
WIDE_IN = (1.00, 1.10, 0.50, 0.50)
FACE = (1.80, 1.95, 0.50, 0.27)
TIE = (1.45, 1.35, 0.50, 0.42)
WIDE_OUT = (1.14, 1.00, 0.50, 0.50)
MID = (1.25, 1.35, 0.50, 0.46)

CLIPS = {  # name: (audio, [camera moves])
    "comp1-intro": ("a0.mp3", [WIDE_IN, FACE, TIE, MID, WIDE_OUT]),
    "comp1-bridge-1": ("a1.mp3", [WIDE_IN]),
    "comp1-bridge-2": ("a2.mp3", [WIDE_IN]),
    "comp1-bridge-3": ("a3.mp3", [WIDE_IN]),
    "comp1-bridge-4": ("a4.mp3", [WIDE_IN]),
    "comp1-bridge-5": ("a5.mp3", [WIDE_IN]),
    "comp1-bridge-6": ("a6.mp3", [WIDE_IN]),
    "comp1-outro": ("a7.mp3", [WIDE_IN, FACE, TIE, WIDE_OUT]),
}


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]))


def run(*a):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *map(str, a)], check=True)


def segment(move, n, out):
    zs, ze, cx, cy = move
    z = f"{zs}+({ze}-{zs})*on/{n}"
    run("-i", IMG, "-vf",
        f"scale=3840:2160:flags=lanczos,zoompan=z='{z}':x='iw*{cx}-iw/zoom/2':y='ih*{cy}-ih/zoom/2':d={n}:s=1920x1080:fps={FPS},setsar=1",
        "-frames:v", n, "-c:v", "libx264", "-preset", "veryfast", "-crf", 16, "-pix_fmt", "yuv420p", out)


def build(name, audio, moves):
    a = ASSETS / audio
    total = dur(a) + TAIL
    frames = round(total * FPS)
    per = frames // len(moves)
    parts = []
    for k, mv in enumerate(moves):
        n = per if k < len(moves) - 1 else frames - per * (len(moves) - 1)
        p = HERE / f"_{name}_{k}.mp4"
        segment(mv, n, p)
        parts.append(p)
    lst = HERE / f"_{name}.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    run("-f", "concat", "-safe", 0, "-i", lst, "-i", a, "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
        "-preset", "slow", "-crf", 18, "-pix_fmt", "yuv420p", "-r", FPS, "-c:a", "aac", "-b:a", "192k",
        "-af", "apad", "-t", f"{total:.3f}", HERE / f"{name}.mp4")
    for p in parts + [lst]:
        p.unlink()


if __name__ == "__main__":
    for name, (audio, moves) in CLIPS.items():
        build(name, audio, moves)
        print(name, round(dur(HERE / f"{name}.mp4"), 2))
