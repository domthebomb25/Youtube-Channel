"""Word timings for the voiceover via pocketsphinx forced alignment -> word_timing.json.
Usage: python3 align.py /path/to/voiceover.mp3"""
import json, re, subprocess, sys
from pathlib import Path
from pocketsphinx import Decoder
HERE = Path(__file__).resolve().parent
raw = HERE / "n.raw"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", sys.argv[1],
                "-ar", "16000", "-ac", "1", "-f", "s16le", str(raw)], check=True)
TEXT = open(HERE / "script.txt").read()
words = re.sub(r"[^a-z' ]", " ", TEXT.lower().replace("-", " ")).split()
SUB = {"spacex": ["space", "x"], "byd": ["b", "y", "d"], "tesla's": ["tesla", "s"],
       "elon": ["e", "lawn"], "seaters": ["seat", "errs"]}
toks, owner = [], []
for i, w in enumerate(words):
    for t in SUB.get(w, [w]): toks.append(t); owner.append(i)
d = Decoder(samprate=16000, bestpath=False)
d.set_align_text(" ".join(toks))
pcm = raw.read_bytes()
d.start_utt(); d.process_raw(pcm, full_utt=True); d.end_utt()
d.set_alignment(); d.start_utt(); d.process_raw(pcm, full_utt=True); d.end_utt()
al = [w for w in d.get_alignment() if w.name not in ("<sil>", "<s>", "</s>")]
assert len(al) == len(toks), (len(al), len(toks))
out = []
for k, w in enumerate(al):
    i = owner[k]; a, b = w.start / 100, (w.start + w.duration) / 100
    if out and out[-1][3] == i: out[-1][2] = b
    else: out.append([words[i], a, b, i])
json.dump([o[:3] for o in out], open(HERE / "word_timing.json", "w"))
raw.unlink()
print(len(out), "words, last ends", out[-1][2])
