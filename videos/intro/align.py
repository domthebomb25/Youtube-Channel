"""Word timings for narration.mp3 via pocketsphinx forced alignment -> word_timing.json."""
import json, re
from pocketsphinx import Decoder
TEXT = open("script.txt").read()
words = re.sub(r"[^a-z' ]", " ", TEXT.lower()).split()
SUB = {"costco": ["cost", "co"], "hq": ["h", "q"]}
toks, owner = [], []
for i, w in enumerate(words):
    for t in SUB.get(w, [w]): toks.append(t); owner.append(i)
d = Decoder(samprate=16000, bestpath=False)
d.set_align_text(" ".join(toks))
d.start_utt(); d.process_raw(open("n.raw", "rb").read(), full_utt=True); d.end_utt()
d.set_alignment(); d.start_utt(); d.process_raw(open("n.raw", "rb").read(), full_utt=True); d.end_utt()
al = [w for w in d.get_alignment() if w.name not in ("<sil>", "<s>", "</s>")]
assert len(al) == len(toks), (len(al), len(toks))
out = []
for k, w in enumerate(al):
    i = owner[k]; a, b = w.start / 100, (w.start + w.duration) / 100
    if out and out[-1][3] == i: out[-1][2] = b
    else: out.append([words[i], a, b, i])
out = [o[:3] for o in out]
json.dump(out, open("word_timing.json", "w"))
print(len(out), len(words)); print(out[:6], out[-3:])
