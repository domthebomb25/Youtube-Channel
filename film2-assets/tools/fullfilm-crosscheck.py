import importlib.util,sys
spec=importlib.util.spec_from_file_location('d','/home/user/Youtube-Channel/film2-assets/tools/fullfilm-data.py'); d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
print("== VO continuity")
prev=0; tot=0
for n in d.SHOTS:
    a,b=d.MAPVO[n]
    ok = (a==prev+1) or (n==54 and a==69 and prev==69)
    if not ok: print("  gap/overlap at shot",n,"range",a,b,"prev end",prev)
    prev=b
print("  last VO covered:",prev)
print("== duration: timing-report sum vs map/sheet duration (flag diff >= 0.15 s)")
tr={}
for n in d.SHOTS:
    a,b=d.MAPVO[n]
    s=d.vsum(a,b)
    if n==53: s=4.8   # first half of VO-069 (map value; VO-069 total 9.64)
    if n==54: s=round(d.DUR[69]-4.8+d.vsum(70,71),2)
    tr[n]=s
    m=d.MAPDUR.get(n)
    diff=None if m is None else round(s-m,2)
    if m is None or abs(diff)>=0.15: print(f"  shot {n}: timing-report {s} s, map {m}  diff {diff}")
print("  total shot durations (timing report):",round(sum(tr.values()),2),"s;  VO total",d.TOTAL)
for n in (112,): print("  shot",n,tr[n])
