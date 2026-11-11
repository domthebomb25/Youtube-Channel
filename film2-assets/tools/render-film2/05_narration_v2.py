# Film #2 rebuild v2: 154-line narration with per-line silence trim + per-line loudness (NOT one loudnorm over the whole track).
# usage: python3 -I 05_narration_v2.py <repo>/film2-assets <workdir> [target_lufs_per_line]
import sys, os, re, json, subprocess, wave
import numpy as np
A = sys.argv[1]; W = sys.argv[2]; os.makedirs(W + "/clips", exist_ok=True)
TARGET = float(sys.argv[3]) if len(sys.argv) > 3 else -14.0
SR = 48000
LEAD, TRAIL, GAP = 0.04, 0.06, 0.30          # kept lead/trail around speech; uniform speech-to-speech gap

ORDER_TXT = """
S1: 1 2 4 5 6 7 8 9 10 11 12 13 14 15 16 19 201 23 24 202 203 204
S2: 30 31 32 33 34 35 36 205 206 207 208 209 210 211 212
S3: 74 75 76 77 78 79 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104
S4: 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131
S5: 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 167 168 169 170 171 161 162 163 164 165 166 172 173 174 175 176
S6: 177 178 179 180 181 182 183 184 185 186 188 189 190 191 192 193 195
"""
NEW44 = [2,11,12,13,15,16,201,202,203,204,30,205,206,207,208,209,210,211,212,74,75,76,79,82,95,102,106,125,137,147,148,149,150,151,154,167,176,177,183,184,185,186,188,190]
order = []; sect = []
for l in ORDER_TXT.strip().splitlines():
    s, ids = l.split(":");
    for i in ids.split(): order.append(int(i)); sect.append(s)
assert len(order) == 154 and len(set(order)) == 154, len(order)
assert len(NEW44) == 44 and set(NEW44) <= set(order)
for i in order: assert os.path.exists(f"{A}/voiceover/VO-{i:03d}.mp3"), i

def dec(path):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', path, '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'])
    return np.frombuffer(raw, dtype=np.float32).copy()

def frame_db(x, win=480, hop=240):   # 10 ms window, 5 ms hop
    n = (len(x) - win) // hop + 1
    if n < 1: return np.array([-120.0])
    idx = np.arange(win)[None, :] + hop * np.arange(n)[:, None]
    r = np.sqrt((x[idx] ** 2).mean(1) + 1e-12)
    return 20 * np.log10(r + 1e-9)

def lufs(x, extra=""):
    p = subprocess.run(['ffmpeg', '-nostats', '-i', 'pipe:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'] if False else
                       ['ffmpeg', '-nostats', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       input=x.astype(np.float32).tobytes(), capture_output=True)
    t = p.stderr.decode()
    t = t[t.rfind('Summary:'):]
    I = float(re.search(r'I:\s+(-?[\d.]+) LUFS', t).group(1)); TP = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', t).group(1))
    return I, TP

ON_THR, OFF_THR, SUST = -38.0, -44.0, 5     # ABSOLUTE thresholds (dBFS, 10 ms frames) applied AFTER per-line leveling; onset must be sustained 5 frames (~25 ms)
def edges(y):
    db = frame_db(y); n = len(db)
    ok_on = np.array([db[q:q + SUST].min() > ON_THR for q in range(n)]); ok_off = np.array([db[max(0, q - SUST + 1):q + 1].min() > OFF_THR for q in range(n)])
    on = int(np.argmax(ok_on)); off = n - 1 - int(np.argmax(ok_off[::-1]))
    return on * 240, off * 240 + 480
CEIL = 10 ** (float(sys.argv[4] if len(sys.argv) > 4 else -2.5) / 20)
def limit(y, ceil=CEIL, look=240):
    a = np.abs(y); g = np.minimum(1.0, ceil / np.maximum(a, 1e-9))
    pad = np.pad(g, (look, look), constant_values=1.0)
    w = np.lib.stride_tricks.sliding_window_view(pad, 2 * look + 1).min(1)[: len(y)]
    k = np.hanning(2 * look + 1); k /= k.sum()
    env = np.convolve(np.pad(w, (look, look), mode='edge'), k, mode='valid')[: len(y)]
    return y * np.minimum(env, g)
rows = []; clips = []; gains = []; after_I = []; gr_max = []
for k, i in enumerate(order):
    x = dec(f"{A}/voiceover/VO-{i:03d}.mp3")
    I0, TP0 = lufs(x)                                   # BEFORE: the take as recorded/approved (whole clip, gated)
    g = TARGET - I0
    def process(g):
        y = limit(x * (10 ** (g / 20))); s_on, s_off = edges(y)
        a = max(0, s_on - int(LEAD * SR)); b = min(len(y), s_off + int(TRAIL * SR))
        seg = y[a:b].copy(); ln = s_on - a; tn = b - s_off
        if ln > 0: seg[:ln] *= np.linspace(0, 1, ln)           # fade the whole kept lead in from zero (kills any breath/click ahead of the word)
        seg[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
        if tn > 0: seg[-tn:] *= np.linspace(1, 0, tn)          # fade the whole kept trail out
        return y, s_on, s_off, a, b, seg
    for _ in range(14):                                 # gain so the TRIMMED line (as it plays) lands on TARGET after peak limiting
        y, s_on, s_off, a, b, seg = process(g); I1, _tp = lufs(seg)
        if abs(I1 - TARGET) < 0.04: break
        g += TARGET - I1
    sg = x * (10 ** (g / 20)); ratio = np.abs(y) / np.maximum(np.abs(sg), 1e-9); gr = float(20 * np.log10(ratio[np.abs(sg) > 1e-3].min() + 1e-9))
    rows.append(dict(k=k + 1, sec=sect[k], vo=i, orig_dur=len(x) / SR, lead_orig=s_on / SR, trail_orig=(len(y) - s_off) / SR,
                     kept_lead=(s_on - a) / SR, kept_trail=(b - s_off) / SR, removed_lead=a / SR, removed_trail=(len(y) - b) / SR,
                     speech=(s_off - s_on) / SR, lufs_before=I0, tp_before=TP0, new=(i in NEW44)))
    clips.append(seg.astype(np.float32)); gains.append(g); after_I.append(I1); gr_max.append(gr)
before = np.array([r['lufs_before'] for r in rows])
print(f"BEFORE per-line loudness: min {before.min():.2f} max {before.max():.2f} spread {before.max()-before.min():.2f} LU  (median {np.median(before):.2f})")
clips_final = clips
out = []; pos = 0.0
for n, (r, y, g, I, gr) in enumerate(zip(rows, clips_final, gains, after_I, gr_max)):
    r['lufs_after'] = float(I); r['limiter_gr_max_db'] = gr
    r['gain_db'] = float(g); r['peak_after'] = float(20 * np.log10(np.abs(y).max() + 1e-9))
    if n:  # pad so speech-end -> next speech-start is exactly GAP seconds
        padn = int(round((GAP - rows[n - 1]['kept_trail'] - r['kept_lead']) * SR)); out.append(np.zeros(padn, np.float32)); pos += padn / SR
    r['t_start'] = pos; r['t_speech_on'] = pos + r['kept_lead']; r['t_speech_off'] = pos + r['kept_lead'] + r['speech']
    out.append(y); pos += len(y) / SR
nar = np.concatenate(out)
aft = np.array(after_I); print(f"AFTER per-line loudness: min {aft.min():.2f} max {aft.max():.2f} spread {aft.max()-aft.min():.2f} LU; limiter makeup mean {np.mean([r['gain_db']-(TARGET-r['lufs_before']) for r in rows]):.2f} dB")
I, TP = lufs(nar); print(f"WHOLE TRACK: {len(nar)/SR:.2f} s  integrated {I:.2f} LUFS  true-peak {TP:.2f} dBTP")
# master: ONE uniform gain (not per-segment) to land on -14.0; per-line spread is unchanged by a linear gain
G = -14.0 - I
if abs(G) > 0.02: nar = nar * (10 ** (G / 20)); I, TP = lufs(nar); print(f"after uniform trim {G:+.2f} dB: {I:.2f} LUFS, {TP:.2f} dBTP")
assert TP <= -1.0, TP
np.save(W + "/narration_final.npy", nar.astype(np.float32))
with wave.open(W + "/narration-v2.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(nar, -1, 1) * 32767).astype('<i2').tobytes())
for r in rows: r['uniform_trim_db'] = float(G)
json.dump(dict(total=len(nar) / SR, integrated=I, true_peak=TP, rows=rows), open(W + "/rows.json", "w"), indent=1)
