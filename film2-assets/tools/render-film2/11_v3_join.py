# Narration v3 join: trim ONLY dead silence (< -50 dBFS, 10 ms RMS) at each passage's two edges, concatenate as performed (no gaps added,
# no gain, no leveling, no fades). Timeline of every line/word from the forced alignment, shifted by each passage's trim offset.
import sys, os, json, subprocess, wave, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v3_passages import PASSAGES
A, ALIGN, W = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(W, exist_ok=True)
SR = 48000; DEAD = -50.0; PRE = int(0.010 * SR)
al = json.load(open(ALIGN))
def dec(p): return np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-']), np.float32).copy()
def fdb(x, win=480, hop=240):
    n = (len(x) - win) // hop + 1; i = np.arange(win)[None] + hop * np.arange(n)[:, None]; return 20 * np.log10(np.sqrt((x[i] ** 2).mean(1)) + 1e-9)
chunks = []; lines = []; passages = []; pos = 0
for pid, p1, p2, txt in PASSAGES:
    x = dec(f"{A}/narration-v3/takes/{pid}.mp3"); db = fdb(x)
    live = np.where(db > DEAD)[0]; a = max(0, live[0] * 240 - PRE); b = min(len(x), live[-1] * 240 + 480 + PRE)
    seg = x[a:b]; off = pos / SR - a / SR          # joined_time = take_time + off
    lead_trim = a / SR; tail_trim = (len(x) - b) / SR
    passages.append(dict(pid=pid, start=pos / SR, end=(pos + len(seg)) / SR, lead_trimmed=lead_trim, tail_trimmed=tail_trim, lead_kept=(live[0] * 240 - a) / SR, tail_kept=(b - (live[-1] * 240 + 480)) / SR))
    for li in al[pid]["lines"]:
        lines.append(dict(pid=pid, text=li["text"], start=li["start"] + off, end=li["end"] + off, words=[(w, s + off, e + off) for w, s, e in li["words"]]))
    chunks.append(seg); pos += len(seg)
nar = np.concatenate(chunks)
with wave.open(W + "/narration-v3-raw.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(nar, -1, 1) * 32767).astype('<i2').tobytes())
assert len(lines) == 153, len(lines)
json.dump(dict(total=len(nar) / SR, passages=passages, lines=lines), open(W + "/v3_timeline.json", "w"), indent=1)
gaps = [lines[k + 1]["start"] - lines[k]["end"] for k in range(152)]
pj = [passages[k + 1]["start"] for k in range(len(passages) - 1)]
print(f"joined narration {len(nar)/SR:.3f} s, {len(PASSAGES)} passages, 153 lines | dead-silence trimmed: leads max {max(p['lead_trimmed'] for p in passages):.3f} s, tails max {max(p['tail_trimmed'] for p in passages):.3f} s | kept lead/tail max {max(p['lead_kept'] for p in passages):.3f}/{max(p['tail_kept'] for p in passages):.3f} s")
print("line-to-line pauses as performed (aligned word times): min %.2f  median %.2f  max %.2f s" % (min(gaps), float(np.median(gaps)), max(gaps)))
