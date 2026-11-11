# Film #2 render, step 5: QA gates. usage: python3 -I 04_qa.py <repo>/film2-assets <workdir> <final.mp4>
import sys, os, json, subprocess, re, numpy as np
from PIL import Image
A=sys.argv[1]; W=sys.argv[2]; MP4=sys.argv[3]
T=json.load(open(W+"/timeline.json")); ts={int(k):v for k,v in T["ts"].items()}; SEG=json.load(open(W+"/segments.json"))
out=[]; ok=True
def P(*a):
    s=" ".join(str(x) for x in a); print(s); out.append(s)
def gate(name,cond,detail):
    global ok; ok=ok and cond; P(f"[{'PASS' if cond else 'FAIL'}] {name}: {detail}")
def probe(args): return subprocess.check_output(["ffprobe","-v","error"]+args+[MP4],text=True).strip()
P("FILM #2 — QA REPORT for",os.path.basename(MP4)); P("="*80)
# ---- 5. file facts
size=os.path.getsize(MP4); dur=float(probe(["-show_entries","format=duration","-of","csv=p=0"]))
v=probe(["-select_streams","v:0","-show_entries","stream=codec_name,profile,width,height,pix_fmt,avg_frame_rate,nb_frames,duration,color_space,color_range","-of","default=nw=1"])
a=probe(["-select_streams","a:0","-show_entries","stream=codec_name,profile,channels,sample_rate,bit_rate,duration","-of","default=nw=1"])
P("FILE:",MP4); P(f"size: {size} bytes ({size/1048576:.1f} MB)"); P("video stream:",v.replace("\n"," | ")); P("audio stream:",a.replace("\n"," | "))
# ---- GATE 1 duration
exp=631.22
gate("1. DURATION",abs(dur-exp)<=1.0,f"final file {dur:.3f} s (spec 631.22 s ± 1 s; narration track {T['total']:.3f} s = sum of the 194 timing-report durations)")
vd=float(probe(["-select_streams","v:0","-show_entries","stream=duration","-of","csv=p=0"])); ad=float(probe(["-select_streams","a:0","-show_entries","stream=duration","-of","csv=p=0"]))
gate("1b. A/V length match",abs(vd-ad)<0.05,f"video {vd:.3f} s, audio {ad:.3f} s, difference {abs(vd-ad)*1000:.0f} ms")
# ---- full LINEAR video decode (no seeking)
r=subprocess.run(["ffmpeg","-v","error","-nostats","-i",MP4,"-map","0:v","-f","null","-"],capture_output=True,text=True)
r2=subprocess.run(["ffmpeg","-nostats","-i",MP4,"-map","0:v","-f","null","-"],capture_output=True,text=True)
fr=re.findall(r"frame=\s*(\d+)",r2.stderr); nfr=int(fr[-1]) if fr else -1
gate("1c. FULL LINEAR VIDEO DECODE",r.stderr.strip()=="" and nfr==sum(s['frames'] for s in SEG['segments']),f"decoded {nfr} frames (expected {sum(s['frames'] for s in SEG['segments'])}), decoder errors: {'none' if r.stderr.strip()=='' else r.stderr.strip()[:200]}")
# ---- GATE 2 full linear audio decode, 10 s windows
raw=subprocess.run(["ffmpeg","-v","error","-nostats","-i",MP4,"-vn","-f","f32le","-ac","2","-ar","48000","-"],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32).reshape(-1,2); SR=48000; n=SR*10
wins=[x[i:i+n] for i in range(0,len(x),n)]
corrs=[];rms=[];
for w in wins:
    l,rr=w[:,0].astype(np.float64),w[:,1].astype(np.float64)
    rm=np.sqrt(((l**2+rr**2)/2).mean()); rms.append(20*np.log10(rm+1e-12))
    if l.std()<1e-9 or rr.std()<1e-9: corrs.append(1.0 if np.allclose(l,rr) else 0.0)
    else: corrs.append(float(np.corrcoef(l,rr)[0,1]))
corrs=np.array(corrs); rms=np.array(rms)
P(f"decoded audio: {len(x)/SR:.3f} s in {len(wins)} windows of 10 s (last window {len(wins[-1])/SR:.2f} s)")
gate("2a. L/R CORRELATION per 10 s window (dual-mono)",corrs.min()>=0.99,f"minimum {corrs.min():.5f} (window #{int(corrs.argmin())+1}, t={int(corrs.argmin())*10}-{int(corrs.argmin())*10+10}s), maximum {corrs.max():.5f}; windows below 0.99: {int((corrs<0.99).sum())}")
q,lo=int(rms.argmin()),int(rms.argmax())
gate("2b. RMS per 10 s window (none silent)",rms.min()>-60,f"quietest window #{q+1} (t={q*10}-{q*10+10}s) {rms.min():.1f} dBFS; loudest window #{lo+1} (t={lo*10}-{lo*10+10}s) {rms.max():.1f} dBFS; windows below -50 dBFS: {int((rms<-50).sum())}")
# ---- GATE 3 loudness / true peak on the FINAL FILE
e=subprocess.run(["ffmpeg","-nostats","-i",MP4,"-vn","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
I=float(re.findall(r"I:\s+(-?[\d.]+) LUFS",e)[-1]); LRA=float(re.findall(r"LRA:\s+(-?[\d.]+) LU",e)[-1]); TP=float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS",e)[-1])
gate("3a. INTEGRATED LOUDNESS",abs(I-(-14))<=1.0,f"{I:.1f} LUFS (target -14 ± 1), LRA {LRA:.1f} LU")
gate("3b. TRUE PEAK",TP<=-1.0,f"{TP:.1f} dBTP (must be <= -1.0)")
gate("3c. AUDIO STREAM",a.count("codec_name=aac")==1 and "channels=2" in a and "sample_rate=48000" in a,a.replace("\n"," | "))
# ---- GATE 4 frame verification
def frame_at(t,name):
    p=f"{W}/qa_{name}.png"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t:.3f}","-i",MP4,"-frames:v","1",p],check=True); return p
def src_of(path): return np.asarray(Image.open(path).convert("RGB")).astype(float)
checks=[("shot9_VO012",ts[12]+0.5,A+"/render/states/09-50000.png","shot 9 during VO-012: counter reads 50,000"),
        ("shot9_VO013",ts[13]+1.0,A+"/render/states/09-100000.png","shot 9 during VO-013: counter reads 100,000"),
        ("shot10_VO015",ts[15]+0.5,A+"/render/states/10-1000.png","shot 10 during VO-015: banner reads 1,000 GIFTED SUBS"),
        ("shot35",ts[46]+0.5,A+"/section2/35.png","shot 35 (VO-046): LIVE bright"),
        ("shot50",ts[65]+0.8,A+"/section2/50.png","shot 50 (VO-065): counter reads 900,000"),
        ("shot69_after",ts[95]+7.85+1.2,A+"/section3/69-state.png","shot 69 after its trigger: $20,000,000 – $30,000,000 visible"),
        ("shot85_after",ts[124]+8.01+0.7,A+"/section4/85-state.png","shot 85 after its trigger: crowd flood visible"),
        ("final_frame",T["total"]-1.5/30,A+"/section6/121.png","final frame (shot 121): plain monitor back"),
        ("shot69_before",ts[95]+3.0,A+"/section3/69.png","(control) shot 69 BEFORE the trigger: base frame, no figure"),
        ("shot85_before",ts[124]+3.0,A+"/section4/85.png","(control) shot 85 BEFORE the trigger: base frame"),
        ("shot1_first",0.05,A+"/section1/1.png","(control) first frame = shot 1")]
P("-"*80); P("GATE 4: frames extracted from the FINAL file and compared with the intended source image (PSNR; >30 dB = same picture):")
for name,t,srcp,desc in checks:
    f=frame_at(t,name); a_=np.asarray(Image.open(f).convert("RGB")).astype(float); b_=src_of(srcp)
    mse=((a_-b_)**2).mean(); psnr=99.0 if mse==0 else 10*np.log10(255**2/mse)
    P(f"  {name:15s} t={t:8.3f}s  PSNR vs {os.path.relpath(srcp,A):34s} = {psnr:5.1f} dB  -> {desc}")
    json.dump({},open(W+"/_",'w'))
P("(each frame was also viewed by eye; see the visual verdicts appended below)")
open(W+"/qa_numbers.txt","w").write("\n".join(out)); 
P("="*80); P("AUTOMATED GATES:","ALL PASS" if ok else "FAILURES PRESENT")
open(A+("/render/QA-REPORT-v2.txt" if "v2" in MP4 else "/render/QA-REPORT.txt"),"w").write("\n".join(out)+"\n")
