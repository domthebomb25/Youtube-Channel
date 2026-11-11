# Forced alignment of each v3 passage take (pocketsphinx) -> word times -> per-line start/end. No audio is modified here.
import sys, os, re, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v3_passages import PASSAGES
import pocketsphinx
from pocketsphinx import Decoder
A = sys.argv[1]; OUT = sys.argv[2]
mp = pocketsphinx.get_model_path(); DICT = {}
for l in open(os.path.join(mp, "en-us", "cmudict-en-us.dict"), encoding="latin-1"):
    w = l.split()[0]; DICT[re.sub(r"\(\d+\)$", "", w)] = 1
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
def norm(line):
    t = line.replace("#1", " number one ").replace("number 2", "number two").replace("$6", " six dollars ")
    t = t.replace("2018", " twenty eighteen ").replace("2021", " twenty twenty one ").replace("2025", " twenty twenty five ")
    t = re.sub(r"[—…\-]", " ", t); t = re.sub(r"[^A-Za-z' ]", " ", t)
    return [w for w in t.lower().split() if w]
OOV = {"cenat": "S IH N AA T", "subathon": "S AH B AH TH AA N", "fortnite": "F AO R T N AY T", "kai": "K AY", "ludwig": "L AH D W IH G", "twitch": "T W IH CH", "tv": "T IY V IY", "mixer": "M IH K S ER", "ninja's": "N IH N JH AH Z", "ninja": "N IH N JH AH"}
res = {}
for pid, p1, p2, lines in PASSAGES:
    wl = [norm(l) for l in lines]; words = [w for ws in wl for w in ws]
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", f"{A}/narration-v3/takes/{pid}.mp3", "-ar", "16000", "-ac", "1", "-f", "s16le", "-"])
    d = Decoder(loglevel="FATAL")
    for w in set(words):
        if w not in DICT:
            if w not in OOV: raise SystemExit(f"OOV word needs a pronunciation: {w}")
            d.add_word(w, OOV[w], False)
    d.set_align_text(" ".join(words)); d.start_utt(); d.process_raw(raw, False, True); d.end_utt()
    seg = [(re.sub(r"\(\d+\)$", "", s.word), s.start_frame / 100, s.end_frame / 100) for s in d.seg() if not s.word.startswith("<") and not s.word.startswith("[") and not s.word.startswith("+")]
    ok = [s[0] for s in seg] == words
    if not ok: print(pid, "WORD MISMATCH", len(seg), len(words)); 
    k = 0; per = []
    for ws, ln in zip(wl, lines):
        sl = seg[k:k + len(ws)]; k += len(ws)
        per.append(dict(text=ln, start=sl[0][1], end=sl[-1][2], words=[(w, round(a, 2), round(b, 2)) for w, a, b in sl]))
    res[pid] = dict(first=p1, last=p2, aligned_ok=ok, lines=per)
    print(pid, "ok" if ok else "MISMATCH", [(round(x['start'], 2), round(x['end'], 2)) for x in per])
json.dump(res, open(OUT, "w"), indent=1)
