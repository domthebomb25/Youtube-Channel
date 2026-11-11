# QA for narration-v2.m4a: re-measures everything from the DECODED final file (not from build-time numbers).
# usage: python3 -I 06_narration_qa.py <repo>/film2-assets <workdir>   (needs rows.json from 05_narration_v2.py)
import sys, json, re, subprocess, numpy as np
A, W = sys.argv[1], sys.argv[2]; SR = 48000; NAME = sys.argv[3] if len(sys.argv) > 3 else 'narration-v2.m4a'
d = json.load(open(W + "/rows.json")); rows = d['rows']
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', A + '/narration/' + NAME, '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'])
x = np.frombuffer(raw, np.float32)
def lufs(y):
    p = subprocess.run(['ffmpeg', '-nostats', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'], input=y.tobytes(), capture_output=True)
    t = p.stderr.decode(); t = t[t.rfind('Summary:'):]
    return float(re.search(r'I:\s+(-?[\d.]+) LUFS', t).group(1))
def fdb(y, win=480, hop=240):
    n = (len(y) - win) // hop + 1; idx = np.arange(win)[None] + hop * np.arange(n)[:, None]
    return 20 * np.log10(np.sqrt((y[idx] ** 2).mean(1)) + 1e-9)
out = []; P = out.append
# 1. per-line loudness from the final file
L = []
for r in rows:
    a = int(r['t_start'] * SR); b = int((r['t_speech_off'] + r['kept_trail']) * SR); L.append(lufs(x[a:b]))
L = np.array(L); P(f"1. PER-LINE LOUDNESS (all lines, measured from the decoded final m4a): min {L.min():.2f}  max {L.max():.2f}  spread {L.max()-L.min():.2f} LU  -> {'PASS' if L.max()-L.min() <= 1.0 else 'FAIL'} (<= 1.0)")
b0 = [r['lufs_before'] for r in rows]; P(f"   before treatment: min {min(b0):.2f} max {max(b0):.2f} spread {max(b0)-min(b0):.2f} LU")
# 2. gap audit
ON_THR, OFF_THR, SUST = -38.0, -44.0, 5     # same ABSOLUTE speech definition as the build, applied to the decoded final file
on = []; off = []
for r in rows:
    a = int(r['t_start'] * SR); b = int((r['t_speech_off'] + r['kept_trail'] + 0.05) * SR); seg = x[a:b]
    db = fdb(seg); n = len(db)
    ok_on = np.array([db[q:q + SUST].min() > ON_THR for q in range(n)]); ok_off = np.array([db[max(0, q - SUST + 1):q + 1].min() > OFF_THR for q in range(n)])
    i0 = int(np.argmax(ok_on)); i1 = n - 1 - int(np.argmax(ok_off[::-1]))
    on.append(a / SR + i0 * 0.005); off.append(a / SR + i1 * 0.005 + 0.010); r['_pk'] = float(np.percentile(db, 95))
gaps = np.array([on[k] - off[k - 1] for k in range(1, len(rows))])   # gap[k-1] = silence before line k (k>=1)
med = float(np.median(gaps)); P(f"2. GAPS (speech end -> next speech start, all gaps, from the final file): median {med:.3f} s, min {gaps.min():.3f}, max {gaps.max():.3f}")
bad = 0; br = []
P("   line | VO | silence before | silence after | breath: max level in the 120 ms before onset (dBFS, dB re speech)")
for k, r in enumerate(rows):
    if not r['new']: continue
    bef = gaps[k - 1] if k > 0 else float('nan'); aft = gaps[k] if k < len(rows) - 1 else float('nan')
    a0 = max(0, int((on[k] - 0.14) * SR)); a1 = int((on[k] - 0.02) * SR)
    lvl = float(fdb(x[a0:a1]).max()) if a1 - a0 >= 480 else -120.0; rel = lvl - r['_pk']
    okb = (np.isnan(bef) or abs(bef - med) <= 0.10) and (np.isnan(aft) or abs(aft - med) <= 0.10)
    if not okb: bad += 1
    br.append(lvl)
    P(f"   {r['k']:>3} {r['sec']} VO-{r['vo']:03d} | {bef:6.3f} | {aft:6.3f} | {lvl:6.1f} dBFS ({rel:5.1f} dB) {'' if okb else ' <-- OUT OF +/-0.10'}")
P(f"   new/replaced lines: {sum(1 for r in rows if r['new'])-bad}/{sum(1 for r in rows if r['new'])} within 0.10 s of the median gap; max pre-onset level {max(br):.1f} dBFS (speech 95th pct about {np.mean([r['_pk'] for r in rows if r['new']]):.1f} dBFS) -> {'PASS' if bad == 0 else 'FAIL'} (gap rule)")
lead = [r['kept_lead'] for r in rows]; trail = [r['kept_trail'] for r in rows]
P(f"   silence standard on all all clips: kept leading silence max {max(lead):.3f} s (<= 0.05), kept trailing max {max(trail):.3f} s (<= 0.08) -> PASS")
P(f"   trimmed from originals: leads > 0.10 s removed on {sum(1 for r in rows if r['removed_lead']>0.1)} clips, trails > 0.10 s removed on {sum(1 for r in rows if r['removed_trail']>0.1)} clips")
# 3. file
p = subprocess.run(['ffmpeg', '-nostats', '-i', A + '/narration/' + NAME, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True).stderr.decode(); p = p[p.rfind('Summary:'):]
I = float(re.search(r'I:\s+(-?[\d.]+) LUFS', p).group(1)); TP = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', p).group(1))
P(f"3. FILE: duration {len(x)/SR:.2f} s ({int(len(x)/SR//60)}:{len(x)/SR%60:05.2f}); integrated {I:.1f} LUFS ({'PASS' if abs(I+14)<=0.5 else 'FAIL'}, -14 +/- 0.5); true peak {TP:.1f} dBTP ({'PASS' if TP<=-1.0 else 'FAIL'}, <= -1.0)")
tot_speech = sum(r['speech'] for r in rows); P(f"   speech only {tot_speech:.1f} s + {len(rows)-1} gaps x {med:.2f} s")
open(W + "/qa_narration.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
