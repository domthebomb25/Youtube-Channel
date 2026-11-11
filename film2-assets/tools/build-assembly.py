# Assembly handoff bundle: one zip per section + MANIFEST.txt (only files already in the repo; no generation).
import sys, os, zipfile, importlib.util
A=sys.argv[1]; os.environ["F2"]=A
spec=importlib.util.spec_from_file_location("d",A+"/tools/fullfilm-data.py"); d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
SEC={1:(1,20,1,27),2:(21,57,28,73),3:(58,75,74,104),4:(76,88,105,129),5:(89,111,130,176),6:(112,121,177,195)}
TITLE={1:"THE HOOK / INTRO",2:"THE MORNING AFTER",3:"TRUTH 1: THE MONEY",4:"TRUTH 2: THE POWER",5:"TRUTH 3: THE CATCH",6:"THE PAYOFF"}
def dur(n):
    a,b=d.MAPVO[n]; s=d.vsum(a,b)
    if n==53: s=4.8
    if n==54: s=round(d.DUR[69]-4.8+d.vsum(70,71),2)
    return s
def vofiles(n):
    a,b=d.MAPVO[n]; return [f"VO-{i:03d}.mp3" for i in range(a,b+1)]
def zname(n):
    if n==27: return "masters/027-REUSE-of-001.png"
    if n==57: return "masters/057-REUSE-of-054.png"
    return f"masters/{n:03d}.png"
STATE={ # shot -> (state description, trigger, file in zip or None)
 9:("Counter flips 10,000 -> 50,000 (VO-012), then 100,000 (VO-013). Text swap at assembly, NO separate file in the repo.","VO-012 'Fifty thousand.' ; VO-013 'One hundred thousand'",None),
 10:("Alert flips 100 GIFTED SUBS -> 1,000 GIFTED SUBS. Text swap at assembly, NO separate file in the repo.","VO-015 'Then a thousand.'",None),
 18:("Shot 18 IS the assembly state of shot 17 (own file): tighter crop, counter 999,999.","plays on VO-024; shot 17 (950,000) plays on VO-023",None),
 35:("Shot 35 IS the assembly state of shot 34 (own file): LIVE light flipped bright.","plays on VO-046 'The red light turns on.'",None),
 40:("Shot 40 IS the assembly state of shot 39 (own file): x2 push-in.","plays on VO-052 'Hello everyone, welcome to my stream!'",None),
 50:("Shot 50 IS the assembly state of shot 49 (own file): counter flipped to 900,000.","plays on VO-065 'Nine hundred thousand.'",None),
 54:("Shot 54 IS the push-in state of shot 53 (own file). Split VO-069 between 53 and 54 at the comma after 'on your screen,'.","VO-069 2nd half 'there is one small line...' through VO-071",None),
 69:("69-state.png: '$20,000,000 - $30,000,000' banner added under the contract.","payoff clause of VO-095: 'between twenty and thirty million dollars.' (final words of the 11.65 s line)","states/069-state.png"),
 85:("85-state.png: room floods with the crowd, monitor alive, light rays.","VO-124 at 'and his room explodes in seconds.' (end of the 9.87 s line)","states/085-state.png"),
}
STSRC={69:"section3/69-state.png",85:"section4/85-state.png"}
lines=["FILM #2 — \"POV: You Became the #1 Streamer Overnight.\" — ASSEMBLY MANIFEST",
"All 117 shots in playing order (shots 7, 31, 45, 55 are CUT and do not exist; no renumbering). Masters 1920x1080 PNG. Voice = Bram ("+d.TOTAL+" s total, voiceover/timing-report.md).",
"Durations = sum of the VO files each shot carries (repo timing report). Shot 53/54 split VO-069 (9.64 s): 53 = first half (4.8 s), 54 = second half + VO-070 + VO-071 (about 9.0 s).",
"Zip layout: masters/NNN.png (shot order) · voiceover/VO-NNN.mp3 · states/ (separate state files, sections 3 and 4 only) · SECTION-MANIFEST.txt.",
"Reused images: shot 27 = shot 1 (masters/027-REUSE-of-001.png in the section 2 zip; the original is in the section 1 zip). Shot 57 = shot 54 (masters/057-REUSE-of-054.png).",
"NEW takes: VO-178 ('You went to sleep as nobody.', 2.12 s), VO-179 ('And you woke up as the biggest show on Earth.', 3.47 s), VO-195 ('Staying at #1 is just as hard.', 2.77 s). VO-193 is the ORIGINAL take (untouched). Old takes are NOT in any zip.",
"VO-194 ('Staying there?') is RETIRED: not carried by any shot, not counted in the total, and NOT in any zip (the file stays in voiceover/ as VO-194-UNUSED-staying-there.mp3). Shot 121 = VO-193 + VO-195 only. Every other VO file (001..195 minus 194) is carried exactly once.",""]
hdr="{:>4} | {:<30} | {:<22} | {:>7} | {}"
lines.append(hdr.format("Shot","Image (path inside the zip)","VO files carried","Dur (s)","Assembly state / trigger"))
lines.append("-"*140)
tot=0
per={s:[] for s in SEC}
for n in d.SHOTS:
    s=next(k for k,(a,b,_,_) in SEC.items() if a<=n<=b)
    a,b=d.MAPVO[n]
    vf=f"VO-{a:03d}" if a==b else f"VO-{a:03d}..{b:03d}"
    if n==121: vf="VO-193 + VO-195"
    if n==53: vf="VO-069 (1st half)"
    if n==54: vf="VO-069 (2nd half)..071"
    z=f"section{s}-assembly.zip:{zname(n)}"
    st=""
    if n in STATE:
        st=STATE[n][0]+" TRIGGER: "+STATE[n][1]
        if STATE[n][2]: z2=STATE[n][2]; st+=f"  FILE: {z2}"
    dd=dur(n); tot+=dd
    row=hdr.format(n,f"{zname(n)}",vf,f"{dd:.2f}",st)
    per[s].append(row); lines.append(f"[S{s}] "+row)
lines+=["",f"Sum of shot durations (timing-report rounded values): {tot:.2f} s ; exact VO total "+d.TOTAL+" s (difference is per-file rounding only).",""]
os.makedirs(A+"/assembly",exist_ok=True)
open(A+"/assembly/MANIFEST.txt","w",encoding="utf-8").write("\n".join(lines))
ONLY=[int(x) for x in sys.argv[2:]] or list(SEC)
for s,(a,b,v0,v1) in SEC.items():
    if s not in ONLY: continue
    zp=A+f"/assembly/section{s}-assembly.zip"
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for n in d.SHOTS:
            if a<=n<=b: z.write(A+"/"+d.img(n),zname(n))
        for i in range(v0,v1+1):
            if i in d.RETIRED: continue
            z.write(A+f"/voiceover/VO-{i:03d}.mp3",f"voiceover/VO-{i:03d}.mp3")
        for n,src in STSRC.items():
            if a<=n<=b: z.write(A+"/"+src,STATE[n][2])
        sm=[f"SECTION {s}: {TITLE[s]} — shots {a}-{b}, VO-{v0:03d}..VO-{v1:03d}","(see ../MANIFEST.txt for the whole film)",""]+per[s]
        sm+=[""]+[f"STATE n{n}: {STATE[n][0]} TRIGGER: {STATE[n][1]}" for n in STATE if a<=n<=b]
        z.writestr("SECTION-MANIFEST.txt","\n".join(sm))
    print(os.path.basename(zp),os.path.getsize(zp),"bytes",round(os.path.getsize(zp)/1048576,1),"MB")
