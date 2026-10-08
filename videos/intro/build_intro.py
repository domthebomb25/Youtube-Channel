"""Build the vertical channel intro (TikTok/Reels/Shorts) from Costco stills + narration.mp3.

usage: python3 build_intro.py   ->  intro-the-business-stick-hq.mp4
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
COSTCO = HERE.parent / "costco-hot-dog"
sys.path.insert(0, str(COSTCO / "shorts"))
import make_short as m  # noqa: E402

AUD = HERE / "narration.mp3"
NARR = 20.61
CARD_AT = 15.70                     # "This is The Business Stick HQ…" plays over the end card
TAIL = 1.5
STILLS = COSTCO / "assembly/out/stills"
# (start, still, motion) — cuts land on the narration's word timings
SHOTS = [(0.00, "s001", "in"), (4.50, "s174", "right"), (6.40, "s175", "in"), (8.25, "s026", "left"),
         (9.80, "s144", "in"), (11.20, "s147", "right"), (13.10, "mascot", "in")]


def mascot_frame():
    bg = Image.new("RGB", (3840, 2160), m.BLUE)
    p = Image.open(HERE.parent.parent / "channel/profile/raw/p3-nobrows.png").convert("RGB")
    p = p.resize((2160, 2160 * p.height // p.width))
    bg.paste(p, ((3840 - p.width) // 2, 0))
    out = HERE / "_mascot.png"; bg.save(out)
    return out


def src_video():
    mf = mascot_frame()
    parts = []
    for k, (t0, name, mo) in enumerate(SHOTS):
        t1 = SHOTS[k + 1][0] if k + 1 < len(SHOTS) else CARD_AT
        n = round((t1 - t0) * m.FPS)
        img = mf if name == "mascot" else STILLS / f"{name}.png"
        p = "(on/duration)"
        z, x, y = {"in": (f"(1+0.08*{p})", "(iw/2-iw/zoom/2)", "(ih/2-ih/zoom/2)"),
                   "right": ("1.08", f"(iw-iw/zoom)*{p}", "(ih/2-ih/zoom/2)"),
                   "left": ("1.08", f"(iw-iw/zoom)*(1-{p})", "(ih/2-ih/zoom/2)")}[mo]
        out = HERE / f"_s{k}.mp4"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(img), "-vf",
                        f"scale=3840:2160,zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=1920x1080:fps={m.FPS},setsar=1",
                        "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
                        str(out)], check=True)
        parts.append(out)
    lst = HERE / "_list.txt"; lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    src = HERE / "_src.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(AUD),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(src)],
                   check=True)
    for p in parts + [lst, mf]: p.unlink()
    return src


def main():
    m.SRC = src_video()
    wt = json.load(open(HERE / "word_timing.json"))
    m.words_for = lambda segs: ([(w, a, b) for w, a, b in wt if a < segs[0][1]], segs[0][1])
    m.END_SEC = round(NARR - CARD_AT + TAIL, 2)
    spec = {"name": "intro-the-business-stick-hq", "segments": [[0, CARD_AT]],
            "title": ["NEW HERE?", "HERE'S WHAT THIS", "CHANNEL IS ABOUT 👇"],
            "end": ["THE BUSINESS STICK HQ", "NEW STORY EVERY WEEK", "@TheBusinessStickHQ"]}
    (HERE / "_spec.json").write_text(json.dumps(spec))
    sys.argv = ["make_short.py", str(HERE / "_spec.json")]
    m.main()
    raw = HERE / f"{spec['name']}.mp4"; tmp = HERE / "_noaudio.mp4"; raw.rename(tmp)
    total = CARD_AT + m.END_SEC
    # full narration over the whole thing (the short builder only carries audio up to the card)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-i", str(AUD), "-map", "0:v", "-map", "1:a",
                    "-af", f"apad,atrim=0:{total:.2f},afade=t=out:st={total - 0.2:.2f}:d=0.2", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(raw)], check=True)
    for p in (tmp, HERE / "_spec.json", m.SRC): p.unlink()
    print(raw, round(total, 2), "s")


if __name__ == "__main__":
    main()
