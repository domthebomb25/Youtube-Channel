"""Assemble the Costco hot dog video from stills + voiceover.

usage: python3 build.py [--only 1,2,3] [--jobs 4] [--no-concat] [--concat-only]
Outputs (in assembly/out/): shots/shotNNN.mp4, video.mp4 (1080p), preview-720p.mp4
"""
import argparse
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import draw  # noqa: E402
import overlays as ov  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).parent / "out"
FPS = 30
SW, SH = 3840, 2160  # working resolution for smooth zoom/pan


def shots():
    sl = json.load(open(ROOT / "clips/shotlist.json"))
    bounds = [round(s["t0"] * FPS) for s in sl] + [round(sl[-1]["t1"] * FPS)]
    for i, s in enumerate(sl):
        s["frames"] = bounds[i + 1] - bounds[i]
    sl[-1]["frames"] += round(ov.END_TAIL * FPS)
    return sl


def motion_expr(n, idx):
    m = ov.MOTION.get(n, ov.MOTION_CYCLE[idx % len(ov.MOTION_CYCLE)])
    p = "(on/duration)"
    if isinstance(m, dict):
        fx, fy = m["at"]
        z = f"({m['z0']}+({m['z1']}-{m['z0']})*(1-pow(1-{p},3)))"
        x = f"max(0,min(iw-iw/zoom,{fx}*iw-iw/zoom/2))"
        y = f"max(0,min(ih-ih/zoom,{fy}*ih-ih/zoom/2))"
        return z, x, y
    cx, cy = "(iw/2-iw/zoom/2)", "(ih/2-ih/zoom/2)"
    if m == "in":
        return f"(1+0.10*{p})", cx, cy
    if m == "out":
        return f"(1.10-0.10*{p})", cx, cy
    if m == "hold":
        return f"(1+0.04*{p})", cx, cy
    if m == "right":
        return "1.10", f"(iw-iw/zoom)*{p}", cy
    if m == "left":
        return "1.10", f"(iw-iw/zoom)*(1-{p})", cy
    if m == "up":
        return "1.10", cx, f"(ih-ih/zoom)*(1-{p})"
    raise ValueError(m)


def build_still(n):
    src = ov.REUSE.get(n, n)
    img = Image.open(ROOT / f"images/img{src}.png").convert("RGBA").resize((SW, SH), Image.LANCZOS)
    for spec in ov.SIGNS.get(src, []):
        draw.paint_sign(img, spec)
    path = OUT / "stills" / f"s{n:03d}.png"
    img.convert("RGB").save(path, compress_level=1)
    return path


ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", str(FPS * 2)]


def render_graphic(n, frames):
    dur = frames / FPS
    out = OUT / "shots" / f"shot{n:03d}.mp4"
    proc = subprocess.Popen(
        ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{draw.W}x{draw.H}",
         "-r", str(FPS), "-i", "-", *ENC, str(out)], stdin=subprocess.PIPE)
    fn = draw.GRAPHIC_FN[n]
    for i in range(frames):
        proc.stdin.write(fn(i / FPS, dur).convert("RGB").tobytes())
    proc.stdin.close()
    proc.wait()
    return out


def render_still(n, idx, frames):
    still = build_still(n)
    out = OUT / "shots" / f"shot{n:03d}.mp4"
    z, x, y = motion_expr(n, idx)
    fc = f"[0]zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s=1920x1080:fps={FPS},setsar=1[bg]"
    args = ["ffmpeg", "-loglevel", "error", "-y", "-i", str(still)]
    if n in ov.LABELS:
        lab = OUT / "labels" / f"l{n:03d}.png"
        draw.label_layer(ov.LABELS[n]).save(lab)
        args += ["-loop", "1", "-framerate", str(FPS), "-i", str(lab)]
        fc += ";[1]format=rgba,fade=in:st=0.15:d=0.2:alpha=1[lab];[bg][lab]overlay=0:0:shortest=1[v]"
    else:
        fc += ";[bg]null[v]"
    args += ["-filter_complex", fc, "-map", "[v]", "-frames:v", str(frames), *ENC, str(out)]
    subprocess.run(args, check=True)
    return out


def render(job):
    n, idx, frames = job
    if n in ov.GRAPHICS:
        return render_graphic(n, frames)
    return render_still(n, idx, frames)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--no-concat", action="store_true")
    ap.add_argument("--concat-only", action="store_true")
    a = ap.parse_args()
    for d in ["stills", "labels", "shots"]:
        (OUT / d).mkdir(parents=True, exist_ok=True)
    sl = shots()
    only = {int(x) for x in a.only.split(",")} if a.only else None
    jobs = [] if a.concat_only else [(s["n"], i, s["frames"]) for i, s in enumerate(sl) if not only or s["n"] in only]
    with ProcessPoolExecutor(a.jobs) as ex:
        for out in ex.map(render, jobs):
            print("done", out.name, flush=True)
    if a.no_concat or only:
        return
    lst = OUT / "concat.txt"
    lst.write_text("".join(f"file 'shots/shot{s['n']:03d}.mp4'\n" for s in sl))
    total = sum(s["frames"] for s in sl) / FPS
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-i", str(ROOT / "clips/voiceover.mp3"), "-filter_complex", "[1:a]apad[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT / "video.mp4")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(OUT / "video.mp4"), "-vf", "scale=1280:720",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", str(OUT / "preview-720p.mp4")], check=True)
    print("total", round(total, 2), "s")


if __name__ == "__main__":
    main()
