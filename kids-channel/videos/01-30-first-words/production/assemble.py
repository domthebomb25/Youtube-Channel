"""Assembles the full video 1 from the clips in production/, in timeline.json order.

Rules (from the approved 30-second preview):
- TALK lines play the lip-sync clip with its own audio (never trimmed early).
- A teach line ("Can you say ___?") is followed by a 3.4 s hold of its last frame with 2 blinks,
  the WORD card on screen, then a 0.4 s crossfade into the praise line.
- The praise line gets confetti and a praise card ("Great job!" etc.).
- VO lines play the toy / animal motion clip with the narration on top.
- Hello / goodbye songs open and close the video; a quiet music bed runs under the lessons.
python3 assemble.py            -> FINAL video
python3 assemble.py 0 40      -> only timeline items 0..40 (quick check)
"""
import json, os, subprocess, sys, math, random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
os.chdir(HERE)
FONT = "/tmp/claude-0/-home-user-Youtube-Channel/8211810b-d0d1-5b42-8ba5-c41ae1e24771/scratchpad/fonts/package/files/fredoka-latin-700-normal.woff"
W, H = 1280, 720
V = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30,format=yuv420p"
A = "aresample=44100,aformat=channel_layouts=stereo"
ENC = ["-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]
os.makedirs("build/seg", exist_ok=True); os.makedirs("build/cards", exist_ok=True)

timeline = json.load(open(f"{ROOT}/timeline.json"))
TEXT = {l["id"]: l["text"] for l in json.load(open(f"{ROOT}/voice-lines.json"))}

def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))

# ---------- cards and confetti ----------
WORD = {0: None, 2: "HI", 5: "MAMA", 8: "DADA", 11: "BABY", 14: "BYE-BYE", 18: "BALL", 21: "CAR", 24: "BOOK",
        27: "BUBBLES", 30: "BLOCK", 35: "DOG", 38: "CAT", 41: "COW", 44: "DUCK", 47: "FISH", 51: "MILK", 54: "APPLE",
        57: "BANANA", 60: "COOKIE", 63: "EAT", 67: "MORE", 70: "UP", 73: "GO", 76: "ALL DONE", 79: "HUG", 82: "SHOE",
        85: "HAT", 88: "BATH", 91: "MOON", 94: "NIGHT-NIGHT"}
COLORS = [(230, 50, 50), (255, 140, 0), (46, 170, 90), (60, 140, 230), (150, 90, 210), (236, 72, 153)]

def text_card(path, text, size, pos, fill):
    if os.path.exists(path): return path
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    while d.textlength(text, font=f) > W * 0.5 and size > 60:   # keep long words inside their corner
        size -= 6; f = ImageFont.truetype(FONT, size)
    x, y = pos
    d.text((x + 6, y + 8), text, font=f, anchor="mm", fill=(40, 60, 90, 255), stroke_width=14, stroke_fill=(40, 60, 90, 255))
    d.text((x, y), text, font=f, anchor="mm", fill=fill + (255,), stroke_width=14, stroke_fill=(255, 255, 255, 255))
    im.save(path); return path

def word_card(i):
    w = WORD[i]
    return text_card(f"build/cards/word-{i:03d}.png", w, 150, (W * 0.27, H * 0.82), COLORS[i % len(COLORS)])

def praise_card(i):
    t = TEXT[i]
    for key, label in (("Great job", "Great job!"), ("Good job", "Good job!"), ("You did it", "You did it!"),
                       ("smart", "So smart!"), ("Pop", "Pop, pop!"), ("Yum", "Yum!"), ("Yay", "Yay!")):
        if key in t: break
    else:
        label = "Great job!"
    return text_card(f"build/cards/praise-{i:03d}.png", label, 110, (W * 0.734, H * 0.874), (255, 214, 64))

def confetti():
    if os.path.exists("build/confetti/c044.png"): return
    os.makedirs("build/confetti", exist_ok=True); random.seed(3)
    cols = [(230, 50, 50), (255, 170, 0), (255, 214, 64), (46, 170, 90), (60, 140, 230), (150, 90, 210)]
    pieces = [(random.uniform(0, W), random.uniform(-H, 0), random.uniform(120, 260), random.choice(cols), random.uniform(8, 18)) for _ in range(160)]
    for fr in range(45):
        t = fr / 30; im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for x, y, v, c, s in pieces:
            yy = y + v * t * 3; xx = x + 20 * math.sin(yy / 40)
            if 0 < yy < H: d.rectangle((xx, yy, xx + s, yy + s * 0.6), fill=c + (255,))
        im.save(f"build/confetti/c{fr:03d}.png")

# ---------- segment builders ----------
def talk_file(i):
    return f"talk/talk-{i:03d}.mp4"

def seg_talk(i, out):
    if i == 99:   # goodbye bridge line was made as two clips
        ff("-i", "talk/talk-099a.mp4", "-i", "talk/talk-099b.mp4", "-filter_complex",
           f"[0:v]{V}[a];[1:v]{V}[b];[0:a]{A}[x];[1:a]{A}[y];[a][x][b][y]concat=n=2:v=1:a=1[v][au]",
           "-map", "[v]", "-map", "[au]", *ENC, out)
    else:
        ff("-i", talk_file(i), "-vf", V, "-af", A, *ENC, out)

def seg_teach(i, out):
    """teach clip + 3.4 s blinking hold, word card on from 0.3 s"""
    hold = f"holdclips/hold-{i:03d}.mp4"
    if WORD[i]:
        ff("-i", talk_file(i), "-i", hold, "-f", "lavfi", "-t", "3.4", "-i", "anullsrc=r=44100:cl=stereo",
           "-loop", "1", "-i", word_card(i), "-filter_complex",
           f"[0:v]{V}[a0];[1:v]{V}[a1];[a0][a1]concat=n=2:v=1:a=0[b];[3:v]format=rgba[w];"
           f"[b][w]overlay=0:0:enable='gte(t,0.3)':shortest=1[v];[0:a]{A}[x0];[2:a]{A}[x1];[x0][x1]concat=n=2:v=0:a=1[au]",
           "-map", "[v]", "-map", "[au]", *ENC, out)
    else:
        ff("-i", talk_file(i), "-i", hold, "-f", "lavfi", "-t", "3.4", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex",
           f"[0:v]{V}[a0];[1:v]{V}[a1];[a0][a1]concat=n=2:v=1:a=0[v];[0:a]{A}[x0];[2:a]{A}[x1];[x0][x1]concat=n=2:v=0:a=1[au]",
           "-map", "[v]", "-map", "[au]", *ENC, out)

def seg_praise(i, out):
    confetti()
    ff("-i", talk_file(i), "-framerate", "30", "-i", "build/confetti/c%03d.png", "-loop", "1", "-i", praise_card(i),
       "-filter_complex",
       f"[0:v]{V}[b];[1:v]format=rgba,setpts=PTS+0.9/TB[c];[2:v]format=rgba[g];[b][c]overlay=0:0:eof_action=pass[bc];"
       f"[bc][g]overlay=0:0:enable='gte(t,1.0)':shortest=1[v]",
       "-map", "[v]", "-map", "0:a", "-af", A, *ENC, out)

def seg_vo(i, out):
    vo = f"{ROOT}/voice-lines/line-{i:03d}.mp3"
    if i == 97:   # super-fast review: five pictures, one per word
        pics = ["../preview-30s/frame-ball.png", "frames/O_dog.png", "frames/O_milk.png", "frames/O_up.png", "frames/O_moon.png"]
        d = dur(vo) + 0.6; each = d / 5
        ins = []; fc = ""
        for k, p in enumerate(pics):
            ins += ["-loop", "1", "-t", f"{each:.3f}", "-i", p]
            fc += f"[{k}:v]{V},zoompan=z='1+0.0015*on':d=1:s=1280x720:fps=30[p{k}];"
        fc += "".join(f"[p{k}]" for k in range(5)) + "concat=n=5:v=1:a=0[v];"
        fc += f"[5:a]adelay=300|300,apad,atrim=0:{d:.3f},{A}[au]"
        ff(*ins, "-i", vo, "-filter_complex", fc, "-map", "[v]", "-map", "[au]", *ENC, out)
        return
    clip = f"obj/obj-{i:03d}.mp4"
    d = min(dur(clip), max(3.5, dur(vo) + 1.4))
    ff("-i", clip, "-i", vo, "-filter_complex",
       f"[0:v]{V},trim=0:{d:.3f},setpts=PTS-STARTPTS[v];[1:a]adelay=300|300,apad,atrim=0:{d:.3f},{A}[au]",
       "-map", "[v]", "-map", "[au]", *ENC, out)

def seg_show(clip, secs, out):
    ff("-i", clip, "-f", "lavfi", "-t", str(secs), "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex",
       f"[0:v]{V},trim=0:{secs},setpts=PTS-STARTPTS[v]", "-map", "[v]", "-map", "1:a", *ENC, out)

def seg_song(song, clips, out, length=None, fade=2.0):
    d = length or dur(song)
    fc = "".join(f"[{k}:v]{V}[c{k}];" for k in range(len(clips)))
    fc += "".join(f"[c{k}]" for k in range(len(clips))) + f"concat=n={len(clips)}:v=1:a=0,trim=0:{d:.3f},setpts=PTS-STARTPTS," \
          f"fade=t=out:st={d - 0.6:.3f}:d=0.6[v];[{len(clips)}:a]atrim=0:{d:.3f},afade=t=out:st={d - fade:.3f}:d={fade},{A}[au]"
    ins = []
    for c in clips: ins += ["-i", c]
    # loop the dance clips if the song is longer than the clips
    total = sum(dur(c) for c in clips)
    if total < d:
        ins = []
        for c in clips: ins += ["-stream_loop", "2", "-i", c]
    ff(*ins, "-i", song, "-filter_complex", fc, "-map", "[v]", "-map", "[au]", *ENC, out)

def seg_sung(clips, out, fade=0.6):
    """songs Miss Poppy sings (lip-synced clips keep their own audio so the mouth stays in sync)"""
    # each clip is trimmed to the length of its piece of the song so the song never pauses at the join
    d = sum(t for _, t in clips)
    ins = []
    for c, _ in clips: ins += ["-i", c]
    fc = "".join(f"[{k}:v]{V},trim=0:{t},setpts=PTS-STARTPTS[v{k}];[{k}:a]atrim=0:{t},asetpts=PTS-STARTPTS,{A}[a{k}];"
                 for k, (_, t) in enumerate(clips))
    fc += "".join(f"[v{k}][a{k}]" for k in range(len(clips))) + f"concat=n={len(clips)}:v=1:a=1[cv][ca];"
    fc += f"[cv]fade=t=out:st={d - 0.6:.3f}:d=0.6[v];[ca]afade=t=out:st={d - fade:.3f}:d={fade}[au]"
    ff(*ins, "-filter_complex", fc, "-map", "[v]", "-map", "[au]", *ENC, out)

def xfade(a, b, out):
    off = dur(a) - 0.4
    ff("-i", a, "-i", b, "-filter_complex",
       f"[0:v][1:v]xfade=transition=fade:duration=0.4:offset={off:.3f}[v];[0:a][1:a]acrossfade=d=0.4[au]",
       "-map", "[v]", "-map", "[au]", *ENC, out)

# ---------- walk the timeline ----------
lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, len(timeline) - 1)
segs = []; n = 0; prev_line = None; songs_seen = 0
k = lo
while k <= hi:
    e = timeline[k]
    out = f"build/seg/{n:03d}.mp4"
    if e[0] == "line":
        i = e[1]
        is_teach = k + 1 < len(timeline) and timeline[k + 1][0] == "sil" and timeline[k + 1][2] == "WAIT"
        is_praise = prev_line in WORD and WORD.get(prev_line) and k >= 2 and timeline[k - 1][2] == "WAIT"
        if e[2] == "VO": seg_vo(i, out)
        elif is_teach: seg_teach(i, out)
        elif is_praise: seg_praise(i, out)
        else: seg_talk(i, out)
        if is_praise and segs and segs[-1][1] == "teach":   # 0.4 s crossfade hold -> praise
            xo = f"build/seg/{n:03d}x.mp4"; xfade(segs[-1][0], out, xo); segs[-1] = (xo, "merged")
        else:
            segs.append((out, "teach" if is_teach else "x"))
        prev_line = i
    else:
        kind = e[2]
        if kind == "SONG placeholder":
            if k == 0: seg_sung([("songs/hello-1.mp4", 13.55), ("songs/hello-2.mp4", 13.17)], out)
            else: seg_sung([("songs/bye-1.mp4", 13.05), ("songs/bye-2-bright.mp4", 12.95)], out, fade=1.5)
            segs.append((out, "song"))
        elif kind.startswith("SHOW"):
            seg_show("extra/extra-205.mp4" if prev_line == 32 else "extra/extra-206.mp4", 3.0, out)
            segs.append((out, "x"))
        # WAIT is built into the teach segment; cheers ride on the praise clip
    n += 1; k += 1
    print(f"{k}/{hi + 1}", end="\r", flush=True)

# body (everything between the songs) gets the quiet music bed
body = [s for s, t in segs if t != "song"]
open("build/body.txt", "w").write("".join(f"file 'seg/{os.path.basename(s)}'\n" for s in body))
ff("-f", "concat", "-safe", "0", "-i", "build/body.txt", "-c", "copy", "build/body_raw.mp4")
bd = dur("build/body_raw.mp4")
ff("-i", "build/body_raw.mp4", "-stream_loop", "-1", "-i", "music/bed.wav", "-filter_complex",
   f"[1:a]{A},volume=0.07,atrim=0:{bd:.3f},afade=t=in:d=2,afade=t=out:st={bd - 3:.3f}:d=3[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[au]",
   "-map", "0:v", "-map", "[au]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "build/body.mp4")
parts = [s for s, t in segs if t == "song"]
order = ([parts[0]] if parts and segs[0][1] == "song" else []) + ["build/body.mp4"] + \
        ([parts[-1]] if parts and segs[-1][1] == "song" else [])
open("build/all.txt", "w").write("".join(f"file '{os.path.relpath(p, 'build')}'\n" for p in order))
name = "FINAL-30-first-words.mp4" if (lo, hi) == (0, len(timeline) - 1) else f"build/check-{lo}-{hi}.mp4"
ff("-f", "concat", "-safe", "0", "-i", "build/all.txt", "-af", "loudnorm=I=-16:TP=-1.5", "-c:v", "libx264", "-crf", "20",
   "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", name)
print("\n", name, round(dur(name), 1), "s")
