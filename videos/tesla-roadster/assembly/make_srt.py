"""English captions for the Tesla Roadster video: SCRIPT.md text timed by word_timing.json (+ hook offset)."""
import difflib, json, re
from pathlib import Path
HOOK = 4.0
HERE = Path(__file__).resolve().parent
MAX_CHARS, MAX_SEC = 84, 6.0
def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower().replace("’", "'"))
def fmt(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
vo = re.findall(r'\*\*VO:\*\* "(.*)"', (HERE.parent / "SCRIPT.md").read_text())[1:]  # [0] is the hook file line
sw = " ".join(vo).split()
tw = json.load(open(HERE / "word_timing.json"))
times = [None] * len(sw)
sm = difflib.SequenceMatcher(None, [norm(w) for w in sw], [norm(w[0]) for w in tw], autojunk=False)
for a, b, n in sm.get_matching_blocks():
    for k in range(n): times[a + k] = (tw[b + k][1] + HOOK, tw[b + k][2] + HOOK)
for i, t in enumerate(times):
    if t is None:
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), HOOK)
        nxt = next((times[j][0] for j in range(i + 1, len(sw)) if times[j]), prev)
        times[i] = (prev, max(prev, nxt))
cues, cur = [], []
for i, w in enumerate(sw):
    cur.append(i); txt = " ".join(sw[j] for j in cur)
    nxt_len = len(txt) + 1 + len(sw[i + 1]) if i + 1 < len(sw) else 0
    if re.search(r"[.?!…]\"?$", w) or nxt_len > MAX_CHARS or times[i][1] - times[cur[0]][0] > MAX_SEC or i == len(sw) - 1:
        cues.append(cur); cur = []
out = ["1\n00:00:00,300 --> 00:00:02,900\nTesla's new car can fly.\n"]  # the hook file's own line
for k, c in enumerate(cues):
    t0 = times[c[0]][0]
    t1 = min(times[c[-1]][1] + 0.3, times[cues[k + 1][0]][0] if k + 1 < len(cues) else 1e9)
    words = [sw[j] for j in c]; line = " ".join(words)
    if len(line) > 42:
        best = min(range(1, len(words)), key=lambda m: abs(len(" ".join(words[:m])) - len(" ".join(words[m:]))))
        line = " ".join(words[:best]) + "\n" + " ".join(words[best:])
    out.append(f"{k + 2}\n{fmt(t0)} --> {fmt(t1)}\n{line}\n")
dst = HERE / "tesla-roadster-english.srt"; dst.write_text("\n".join(out))
print(dst, len(cues) + 1, "cues; matched", sum(n for *_, n in sm.get_matching_blocks()), "/", len(sw))
