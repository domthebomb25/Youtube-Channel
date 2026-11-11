# Film #2 render, step 4: ONE ffmpeg run with the CONCAT FILTER (full decode + a single encode). Never stream-copy concat.
# usage: python3 -I 03_render.py <repo>/film2-assets <workdir> <out.mp4>
import sys, os, json, subprocess, re
A=sys.argv[1]; W=sys.argv[2]; OUT=sys.argv[3]
T=json.load(open(W+"/timeline.json")); FPS=30
ts={int(k):v for k,v in T["ts"].items()}
# trigger points INSIDE a line, measured from the audio (pause analysis, see QA-REPORT): seconds from the start of the line
CUE69=7.85   # VO-095: the 0.38 s pause (7.47-7.85) before "between twenty and thirty million dollars" ends here -> 69-state
CUE85=8.01   # VO-124: the energy dip between "room" and "explodes" (8.01) -> 85-state at "explodes in seconds"
def F(t): return int(t*FPS+0.5)
segs=[]   # (image, t0, t1, label)
for s in T["shots"]:
    n=s["shot"]; img=A+"/"+s["img"]; t0,t1=s["t0"],s["t1"]
    if n==9:
        segs+=[(img,t0,ts[12],"9 base 10,000 (VO-011)"),(A+"/render/states/09-50000.png",ts[12],ts[13],"9 -> 50,000 (VO-012)"),(A+"/render/states/09-100000.png",ts[13],t1,"9 -> 100,000 (VO-013)")]
    elif n==10:
        segs+=[(img,t0,ts[15],"10 base 100 GIFTED SUBS (VO-014)"),(A+"/render/states/10-1000.png",ts[15],t1,"10 -> 1,000 GIFTED SUBS (VO-015)")]
    elif n==69:
        c=ts[95]+CUE69; segs+=[(img,t0,c,"69 base"),(A+"/section3/69-state.png",c,t1,"69-state ($20,000,000 - $30,000,000)")]
    elif n==85:
        c=ts[124]+CUE85; segs+=[(img,t0,c,"85 base"),(A+"/section4/85-state.png",c,t1,"85-state (crowd flood)")]
    else: segs.append((img,t0,t1,f"{n}"))
# frame accounting: boundaries rounded once, so nothing drifts
fr=[]; 
for img,t0,t1,lab in segs:
    nf=F(t1)-F(t0); assert nf>=1,(lab,t0,t1); fr.append(nf)
total_frames=sum(fr); assert total_frames==F(T["total"]),(total_frames,F(T["total"]))
print("segments:",len(segs),"| frames:",total_frames,"=",round(total_frames/FPS,3),"s | narration:",T["total"],"s")
for img,t0,t1,lab in segs: assert os.path.exists(img),img
# True-peak target of the loudnorm filter: -1.5 dBTP. The AAC encode adds ~0.3 dB of inter-sample overshoot, so a -1.0 target measured -0.7 dBTP on the
# encoded file (v1 attempt); -1.5 leaves the headroom so the FINAL FILE measures <= -1.0 dBTP.
TPT='-1.5'
# ---- audio loudness: pass 1 measure, pass 2 apply (linear) -> I=-14 LUFS, TP<=-1, LRA 11
nar=W+"/narration.wav"
p=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",nar,"-af","pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=%s:LRA=11:print_format=json"%TPT+"","-f","null","-"],capture_output=True,text=True)
j=json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}",p.stderr,re.S).group(0)); print("loudnorm pass 1:",j)
af=("pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=%s:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true:print_format=summary,aresample=48000"
    %(TPT,j["input_i"],j["input_tp"],j["input_lra"],j["input_thresh"],j["target_offset"]))
# ---- filter graph: one input per segment (single frame, looped in the graph), then concat
lines=[]; ins=[]
for k,((img,t0,t1,lab),nf) in enumerate(zip(segs,fr)):
    ins+=["-framerate",str(FPS),"-i",img]
    lines.append(f"[{k}:v]scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p,setsar=1,"
                 f"loop=loop={nf-1}:size=1:start=0,setpts=N/({FPS}*TB),trim=end_frame={nf},setpts=PTS-STARTPTS[v{k}]")
lines.append("".join(f"[v{k}]" for k in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=0[vout]")
lines.append(f"[{len(segs)}:a]{af}[aout]")
open(W+"/filter.txt","w").write(";\n".join(lines))
cmd=["ffmpeg","-y","-hide_banner","-nostats","-loglevel","info"]+ins+["-i",nar,"-filter_complex_script",W+"/filter.txt",
     "-map","[vout]","-map","[aout]","-r",str(FPS),"-fps_mode","cfr",
     "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-color_range","tv",
     "-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-movflags","+faststart",OUT]
open(W+"/ffmpeg_cmd.txt","w").write(" ".join(cmd))
r=subprocess.run(cmd,capture_output=True,text=True)
open(W+"/render.log","w").write(r.stderr)
print("ffmpeg exit",r.returncode); print(r.stderr[-1500:])
json.dump(dict(segments=[dict(label=l,t0=a,t1=b,frames=n) for (i,a,b,l),n in zip(segs,fr)],cue69=CUE69,cue85=CUE85,loudnorm_pass1=j),open(W+"/segments.json","w"),indent=1)
