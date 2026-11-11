# Film #2 render, step 1+2: timeline from assembly/MANIFEST.txt + narration track (exact per-line durations).
# usage: python3 -I 01_timeline_audio.py <repo>/film2-assets <workdir>
import sys, os, re, json, subprocess, importlib.util, wave
import numpy as np
A=sys.argv[1]; W=sys.argv[2]; os.makedirs(W,exist_ok=True); os.environ["F2"]=A
spec=importlib.util.spec_from_file_location("d",A+"/tools/fullfilm-data.py"); d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
SR=48000
# ---- manifest rows (source of truth for shot order, image, VO files, durations)
rows=[]
for l in open(A+"/assembly/MANIFEST.txt",encoding="utf-8"):
    m=re.match(r'^\[S(\d)\]\s+(\d+) \| (\S+)\s+\| (.*?)\s+\| +([\d.]+) \|',l)
    if m: rows.append(dict(sec=int(m.group(1)),shot=int(m.group(2)),zimg=m.group(3),vo=m.group(4).strip(),mdur=float(m.group(5))))
assert len(rows)==117, len(rows)
# ---- played VO lines in order (VO-194 retired)
LINES=[i for i in range(1,196) if i not in d.RETIRED]; assert len(LINES)==194
ts={}; t=0.0; cum=0
for i in LINES:
    n=round(d.DUR[i]*SR); ts[i]=cum; cum+=n
TOTAL_SAMPLES=cum
# ---- narration: decode every mp3, resample 48k mono, trim/pad to EXACTLY the timing-report duration, no gaps
chunks=[]; report=[]
for i in LINES:
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',A+f'/voiceover/VO-{i:03d}.mp3','-ar',str(SR),'-ac','1','-f','f32le','-'])
    x=np.frombuffer(raw,dtype=np.float32); n=round(d.DUR[i]*SR)
    if len(x)>=n: y=x[:n]; act='trim'
    else: y=np.concatenate([x,np.zeros(n-len(x),np.float32)]); act='pad'
    report.append((i,len(x)/SR,n/SR,act)); chunks.append(y)
nar=np.concatenate(chunks); assert len(nar)==TOTAL_SAMPLES
with wave.open(W+"/narration.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(nar,-1,1)*32767).astype('<i2').tobytes())
np.save(W+"/narration.npy",nar)
pads=[r for r in report if r[3]=='pad']; trims=[r for r in report if r[3]=='trim']
print(f"narration: {len(LINES)} lines, {TOTAL_SAMPLES/SR:.3f} s ; padded {len(pads)} lines (max pad {max((r[2]-r[1]) for r in pads):.3f}s), trimmed {len(trims)} lines (max trim {max(((r[1]-r[2]) for r in trims),default=0):.3f}s)")
# ---- shot boundaries (seconds) from line starts
def start(i): return ts[i]/SR
def end(i): return (ts[i]+round(d.DUR[i]*SR))/SR
shots=[]
for r in rows:
    n=r['shot']; a,b=d.MAPVO[n]
    a2=a; b2=b
    while b2 in d.RETIRED: b2-=1
    s0=start(a2); s1=end(b2)
    if n==53: s1=start(69)+4.80
    if n==54: s0=start(69)+4.80
    shots.append(dict(shot=n,sec=r['sec'],img=d.img(n),vo=r['vo'],t0=s0,t1=s1,mdur=r['mdur']))
# continuity checks
for k in range(len(shots)-1):
    assert abs(shots[k]['t1']-shots[k+1]['t0'])<1e-6,(shots[k]['shot'],shots[k]['t1'],shots[k+1]['t0'])
assert shots[0]['t0']==0 and abs(shots[-1]['t1']-TOTAL_SAMPLES/SR)<1e-6
bad=[(s['shot'],round(s['t1']-s['t0'],3),s['mdur']) for s in shots if abs((s['t1']-s['t0'])-s['mdur'])>0.0051]
print("shots:",len(shots),"| shots whose duration differs from the manifest by >0.005 s:",bad)
cues={"69":start(95),"85":start(124),"11":start(11),"12":start(12),"13":start(13),"14":start(14),"15":start(15)}
json.dump(dict(total=TOTAL_SAMPLES/SR,shots=shots,ts={str(k):v/SR for k,v in ts.items()},cues=cues,pad_report=[(r[0],round(r[1],3),r[2],r[3]) for r in report]),open(W+"/timeline.json","w"),indent=1)
print("total narration seconds:",TOTAL_SAMPLES/SR)
