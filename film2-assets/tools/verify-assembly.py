# Verify every assembly zip against assembly/MANIFEST.txt and against the current repo files.
import sys, re, zipfile, os, importlib.util
A=sys.argv[1]; os.environ["F2"]=A
spec=importlib.util.spec_from_file_location("d",A+"/tools/fullfilm-data.py"); d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
rows={s:[] for s in range(1,7)}
for l in open(A+"/assembly/MANIFEST.txt",encoding="utf-8"):
    m=re.match(r'^\[S(\d)\]\s+(\d+) \| (\S+)\s+\| (.*?)\s+\| ',l)
    if m: rows[int(m.group(1))].append((int(m.group(2)),m.group(3),m.group(4).strip()))
SEC={1:(1,27),2:(28,73),3:(74,104),4:(105,129),5:(130,176),6:(177,195)}
tot_img=0; tot_vo=0; ok=True
for s in range(1,7):
    z=zipfile.ZipFile(A+f"/assembly/section{s}-assembly.zip"); names=z.namelist()
    masters=[n for n in names if n.startswith("masters/")]; vos=[n for n in names if n.startswith("voiceover/")]; sts=[n for n in names if n.startswith("states/")]
    exp_img=[r[1] for r in rows[s]]
    # expected VO files from the manifest rows
    exp_vo=set()
    for n,img,vf in rows[s]:
        a,b=d.MAPVO[n]
        for i in range(a,b+1):
            if i not in d.RETIRED: exp_vo.add(f"voiceover/VO-{i:03d}.mp3")
    problems=[]
    if sorted(masters)!=sorted(exp_img): problems.append(f"masters differ: zip {len(masters)} vs manifest {len(exp_img)}; missing {sorted(set(exp_img)-set(masters))} extra {sorted(set(masters)-set(exp_img))}")
    if set(vos)!=exp_vo: problems.append(f"VO differ: zip {len(vos)} vs manifest {len(exp_vo)}; missing {sorted(exp_vo-set(vos))} extra {sorted(set(vos)-exp_vo)}")
    bad=[n for n in names if re.search(r"OLD|UNUSED|194",n)]
    if bad: problems.append(f"forbidden names {bad}")
    if z.testzip(): problems.append("corrupt zip")
    # byte-for-byte against the current repo files
    for n in d.SHOTS:
        a,b,_,_=None,None,None,None
    for n,img,vf in rows[s]:
        if z.read(img)!=open(A+"/"+d.img(n),"rb").read(): problems.append(f"master {img} != repo file {d.img(n)}")
    for v in vos:
        if z.read(v)!=open(A+"/"+v,"rb").read(): problems.append(f"{v} != repo file")
    for st in sts:
        src={"states/069-state.png":"section3/69-state.png","states/085-state.png":"section4/85-state.png"}[st]
        if z.read(st)!=open(A+"/"+src,"rb").read(): problems.append(f"{st} != {src}")
    print(f"S{s}: {len(masters)} masters (manifest {len(exp_img)}), {len(vos)} VO (manifest {len(exp_vo)}), state files {sts or 'none'}, {os.path.getsize(A+f'/assembly/section{s}-assembly.zip')/1048576:.1f} MB ->", "OK" if not problems else "PROBLEMS")
    for p in problems: print("   ",p); ok=False
    tot_img+=len(masters); tot_vo+=len(vos)
print("whole film:",tot_img,"masters,",tot_vo,"VO files,","ALL OK" if ok and tot_img==117 and tot_vo==194 else "CHECK FAILED")
