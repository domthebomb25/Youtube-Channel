"""Build English captions (.srt) for the full video: SCRIPT.md text timed by clips/word_timing.json."""
import difflib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_CHARS, MAX_SEC = 84, 6.0  # two lines of ~42


def script_words():
    text = ROOT.joinpath("SCRIPT.md").read_text().split("## Sources")[0]
    paras = [p.strip() for p in text.split("\n\n")]
    body = [p for p in paras if p and not p.startswith(("#", "**", "*[", "---"))]
    return " ".join(body).split()


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower().replace("’", "'"))


def fmt(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    sw = script_words()
    tw = json.load(open(ROOT / "clips/word_timing.json"))
    times = [None] * len(sw)
    sm = difflib.SequenceMatcher(None, [norm(w) for w in sw], [norm(w[0]) for w in tw], autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            times[a + k] = (tw[b + k][1], tw[b + k][2])
    # fill unmatched words by interpolating between neighbours
    for i, t in enumerate(times):
        if t is None:
            prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
            nxt = next((times[j][0] for j in range(i + 1, len(sw)) if times[j]), prev)
            times[i] = (prev, max(prev, nxt))
    cues, cur = [], []
    for i, w in enumerate(sw):
        cur.append(i)
        txt = " ".join(sw[j] for j in cur)
        end_sent = re.search(r"[.?!…]\"?$", w)
        nxt_len = len(txt) + 1 + len(sw[i + 1]) if i + 1 < len(sw) else 0
        if end_sent or nxt_len > MAX_CHARS or times[i][1] - times[cur[0]][0] > MAX_SEC or i == len(sw) - 1:
            cues.append(cur)
            cur = []
    out = []
    for k, c in enumerate(cues):
        t0 = times[c[0]][0]
        t1 = min(times[c[-1]][1] + 0.3, cues[k + 1] and times[cues[k + 1][0]][0] if k + 1 < len(cues) else 1e9)
        words = [sw[j] for j in c]
        line = " ".join(words)
        if len(line) > 42:  # split into two balanced lines
            best = min(range(1, len(words)), key=lambda m: abs(len(" ".join(words[:m])) - len(" ".join(words[m:]))))
            line = " ".join(words[:best]) + "\n" + " ".join(words[best:])
        out.append(f"{k + 1}\n{fmt(t0)} --> {fmt(t1)}\n{line}\n")
    dst = Path(__file__).parent / "costco-hot-dog-english.srt"
    dst.write_text("\n".join(out))
    print(dst, len(cues), "cues; matched", sum(n for *_, n in sm.get_matching_blocks()), "/", len(sw), "script words")


if __name__ == "__main__":
    main()
