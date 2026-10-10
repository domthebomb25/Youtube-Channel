"""Works out when every line starts in FINAL-30-first-words.mp4 (same rules as assemble.py)
and writes the YouTube chapters + an .srt caption file."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); os.chdir(HERE)
T = json.load(open(f"{ROOT}/timeline.json")); TEXT = {l["id"]: l["text"] for l in json.load(open(f"{ROOT}/voice-lines.json"))}
dur = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
seg = lambda n: dur(f"build/seg/{n:03d}.mp4")
t = 0.0; starts = []; speech = []      # (line, start, speech length)
for n, e in enumerate(T):
    if not os.path.exists(f"build/seg/{n:03d}.mp4"): continue
    d = seg(n)
    if os.path.exists(f"build/seg/{n:03d}x.mp4"): t -= 0.4          # crossfaded into the hold before it
    if e[0] == "line":
        i = e[1]; starts.append((i, t))
        if i == 99: sp = dur("talk/talk-099a.mp4") + dur("talk/talk-099b.mp4")
        elif e[2] == "VO": sp = dur(f"{ROOT}/voice-lines/line-{i:03d}.mp3"); t0 = t + 0.3
        else: sp = dur(f"talk/talk-{i:03d}.mp4")
        speech.append((i, t + (0.3 if e[2] == "VO" else 0), sp))
        if T[n + 1][2] == "WAIT" if n + 1 < len(T) else False: pass
    elif e[2] == "SONG placeholder":
        starts.append(("song", t))
    t += d
fmt = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
S = dict((k, v) for k, v in starts if k != "song")
CH = [(0, "Hello song"), (S[0], "Hi, friends!"), (S[4], "Mama, dada & baby"), (S[16], "Ball, car & book"), (S[26], "Bubbles & block"),
      (S[32], "Wiggle break!"), (S[33], "Farm animals: dog, cat, cow, duck"), (S[46], "Fish"), (S[49], "Food: milk, apple, banana, cookie"),
      (S[65], "Clap break!"), (S[66], "More, up, go, all done"), (S[78], "Hug, shoe, hat, bath"), (S[90], "Moon & night-night"),
      (S[96], "Super-fast review"), (S[99], "Goodbye song")]
CH[-1] = (S[99] + dur("talk/talk-099a.mp4") + dur("talk/talk-099b.mp4"), "Goodbye song")
open("../CHAPTERS.txt", "w").write("\n".join(f"{fmt(s)} {name}" for s, name in CH) + "\n")
def ts(s): return f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
srt = []
lyrics = {"hello": "♪ Hello, hello, hello to you! Hello, hello, I'm happy to see you! Wave hello, wave hello — let's play and learn, here we go! ♪",
          "bye": "♪ Goodbye, goodbye, it's time to go! Goodbye, goodbye, I love you so! Wave bye-bye, wave bye-bye — see you soon, my friend, bye-bye! ♪"}
srt.append((0.2, 26.0, lyrics["hello"]))
for i, s, sp in speech: srt.append((s, s + sp, TEXT[i]))
srt.append((CH[-1][0] + 0.2, CH[-1][0] + 25.5, lyrics["bye"]))
open("../CAPTIONS-30-first-words.srt", "w").write("\n".join(f"{k + 1}\n{ts(a)} --> {ts(b)}\n{txt}\n" for k, (a, b, txt) in enumerate(srt)))
print(open("../CHAPTERS.txt").read())
