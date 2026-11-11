# Full-film v4 storyboard: all 117 shots in playing order + free assembly-state tiles, 6 tiles per sheet.
# usage: python3 -I sheet-fullfilm.py <repo>/film2-assets   (writes storyboards/full-film/*.png)
import sys, os, importlib.util
from decimal import Decimal, ROUND_HALF_DOWN
def r1(x): return str(Decimal(str(x)).quantize(Decimal("0.1"),rounding=ROUND_HALF_DOWN))
from PIL import Image, ImageDraw, ImageFont
A=sys.argv[1]; os.environ["F2"]=A
spec=importlib.util.spec_from_file_location("d",A+"/tools/fullfilm-data.py"); d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
def dur(n):
    a,b=d.MAPVO[n]; s=d.vsum(a,b)
    if n==53: s=4.8
    if n==54: s=round(d.DUR[69]-4.8+d.vsum(70,71),2)
    return s
def q(n):
    a,b=d.MAPVO[n]
    if n==53: return "“Under all these new hundreds of thousands of subscribers on your screen,”"
    if n==54: return "“there is one small line containing the first hidden truth. "+" ".join(d.V[i] for i in (70,71))+"”"
    return d.quote(a,b)
def vo(n):
    a,b=d.MAPVO[n]
    if n==53: return "VO-069 (1st half)"
    if n==54: return "VO-069 (2nd half)–071"
    return d.vlabel(a,b)
def trim(t,n=215):
    t=" ".join(t.split())
    if len(t)<=n: return t
    c=t[:n]; i=max(c.rfind(". "),c.rfind("; "),c.rfind(", "))
    return (c[:i] if i>120 else c[:c.rfind(" ")])+" …"
tiles=[]
for n in d.SHOTS:
    st=d.STATE_SHOTS.get(n)
    head=f"SHOT {n} · "+("ASSEMBLY STATE of "+str(st)+" · " if st else "")+f"{vo(n)} · {r1(dur(n))}s"
    if n==27: note=d.NOTE[n]+" (file: section1/1.png)"
    elif n==57: note=d.NOTE[n]+" (file: section2/54.png)"
    else: note=d.NOTE[n]
    tiles.append(dict(img=d.img(n),head=head,quote=q(n),note=trim(note),badge=None,state=bool(st)))
    if n==9:
        for t,vn,lab in (("50,000",12,"VO-012"),("100,000",13,"VO-013")):
            tiles.append(dict(img="section1/9.png",head=f"ASSEMBLY STATE · SHOT 9 · counter → {t} · {lab} · {r1(d.DUR[vn])}s",quote=d.quote(vn),
              note=f"Free state of shot 9: the counter flips 10,000 → {t} at {lab}. No separate file exists in the repo (done at assembly); tile shows the base image.",
              badge=f"BASE IMAGE · counter → {t} at assembly",state=True))
    if n==10:
        tiles.append(dict(img="section1/10.png",head=f"ASSEMBLY STATE · SHOT 10 · alert → 1,000 GIFTED SUBS · VO-015 · {r1(d.DUR[15])}s",quote=d.quote(15),
          note="Free state of shot 10: the alert flips 100 → 1,000 GIFTED SUBS at VO-015 (“Then a thousand.”). No separate file exists in the repo (done at assembly); tile shows the base image.",
          badge="BASE IMAGE · alert → 1,000 GIFTED SUBS at assembly",state=True))
    if n==69:
        tiles.append(dict(img="section3/69-state.png",head=f"ASSEMBLY STATE · SHOT 69 · $20,000,000 – $30,000,000 · within VO-095 ({r1(d.DUR[95])}s)",quote=d.quote(95),
          note="Free state (local, 0.00): the “$20,000,000 – $30,000,000” banner lands on the payoff clause “between twenty and thirty million dollars.”",badge=None,state=True))
    if n==85:
        tiles.append(dict(img="section4/85-state.png",head=f"ASSEMBLY STATE · SHOT 85 · room floods with the crowd · within VO-124 ({r1(d.DUR[124])}s)",quote=d.quote(124),
          note="Free state (local, 0.00): warm glow, light-burst rays, crowd icons flood the room, monitor alive. Lands at “explodes in seconds.”",badge=None,state=True))
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
def wrap(dr,t,font,w):
    out=[];cur=""
    for word in t.split():
        x=(cur+" "+word).strip()
        if dr.textlength(x,font=font)<=w: cur=x
        else: out.append(cur);cur=word
    out.append(cur);return out
os.makedirs(A+"/storyboards/full-film",exist_ok=True)
N=(len(tiles)+5)//6
first_last=[]
for si in range(N):
    chunk=tiles[si*6:(si+1)*6]
    nums=[int(t["head"].split()[1]) if t["head"].startswith("SHOT") else int(t["head"].split("SHOT ")[1].split()[0]) for t in chunk]
    rng=f"{nums[0]}–{nums[-1]}" if nums[0]!=nums[-1] else f"{nums[0]}"
    RH=IH+560; rows=[chunk[i:i+3] for i in range(0,len(chunk),3)]
    H=300+len(rows)*RH+40
    im=Image.new("RGB",(W,H),(14,14,16)); dr=ImageDraw.Draw(im)
    dr.text((M,50),f"FILM #2 · #1 STREAMER OVERNIGHT · Full-Film Storyboard v4 · Sheet {si+1} of {N} · Shots {rng}",font=f(B,52),fill="white")
    dr.text((M,135),"FINAL REVIEW BOARD · all 117 shots generated, in playing order (shots 7, 31, 45, 55 are CUT) · awaiting final review before assembly",font=f(Rg,32),fill=(230,200,60))
    dr.text((M,195),"Final masters 1920×1080 · voice timings from the repo timing report (VO total "+d.TOTAL+" s) · ASSEMBLY STATE tiles play inside their shot",font=f(Rg,28),fill=(160,160,160))
    for r,row in enumerate(rows):
        for c,t in enumerate(row):
            x=M+c*(CW+G); y=290+r*RH
            tile=Image.open(A+"/"+t["img"]).convert("RGB").resize((CW,IH),Image.LANCZOS)
            im.paste(tile,(x,y))
            if t["badge"]:
                ov=Image.new("RGBA",(CW,52),(0,0,0,200)); im.paste(ov,(x,y+IH-52),ov)
                dr.text((x+12,y+IH-42),t["badge"],font=f(B,22),fill=(250,210,40))
            if t["state"]: dr.rectangle([x,y,x+CW-1,y+IH-1],outline=(250,210,40),width=5)
            dr.text((x,y+IH+14),"",font=f(B,34))
            yy=y+IH+14
            for l in wrap(dr,t["head"],f(B,32),CW): dr.text((x,yy),l,font=f(B,32),fill=(250,210,40)); yy+=42
            yy+=4
            for l in wrap(dr,t["quote"],f(B,27),CW): dr.text((x,yy),l,font=f(B,27),fill="white"); yy+=36
            yy+=6
            for l in wrap(dr,t["note"],f(Rg,24),CW): dr.text((x,yy),l,font=f(Rg,24),fill=(150,150,155)); yy+=31
    out=A+f"/storyboards/full-film/fullfilm-storyboard-v4-sheet-{si+1:02d}-of-{N}.png"
    im.save(out); first_last.append((si+1,rng,len(chunk)))
print(N,"sheets;",len(tiles),"tiles")
for x in first_last: print(x)
