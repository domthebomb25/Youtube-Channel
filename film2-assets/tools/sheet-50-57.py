import sys
from PIL import Image, ImageDraw, ImageFont
# usage: python3 -I sheet-50-57.py <repo>/film2-assets <outprefix>
A=sys.argv[1]; R=A+"/section2/"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
shots=[
 (50,"VO-065","1.7s","50.png","“Nine hundred thousand.”","Unchanged. ASSEMBLY STATE (counter flipped to 900,000 on 49)."),
 (51,"VO-066–067","6.0s","51.png","“Your heart keeps pounding as the number continues to rise. You can’t believe this is actually happening.”","NOT EDITED: the chat column cannot be added without moving or shrinking the counter (see report). Current master shown."),
 (52,"VO-068","5.6s","52.png","“You are just someone sitting in a small room, watching his whole life change on a screen.”","EDITED: blank glow replaced by the established stream screen from shot 41 (his preview + genuine chat column), perspective-matched. Local, 0 credits."),
 (53,"VO-069 (1st half)","4.8s","53.png","“Under all these new hundreds of thousands of subscribers on your screen,”","NOT EDITED: same reason as 51 (chat column vs. the full-screen counter). Current master shown."),
 (54,"VO-069 (2nd half)–071","9.0s","54.png","“…there is one small line containing the first hidden truth. You don’t read it. It is the last thing on your mind at this current time.”","Push-in state of 53 (unchanged master). NOW CARRIES VO-070–071 (shot 55 is cut)."),
 (56,"VO-072","3.4s","56.png","“You are too busy becoming the biggest streamer in the world.”","EDITED: landscape removed; stream screen with his own beaming head (copied from this shot) on the dark preview + genuine chat column. Local, 0 credits."),
 (57,"VO-073","2.4s","57.png","“Let’s jump in to the first hidden truth.”","EDITED: sunset removed; shot 53’s counter design (person icon, 900,000, the one unreadable blurred line), perspective-matched and darkened for the dusk room. Local, 0 credits."),
]
def wrap(d,t,font,w):
    out=[];cur=""
    for word in t.split():
        x=(cur+" "+word).strip()
        if d.textlength(x,font=font)<=w: cur=x
        else: out.append(cur);cur=word
    out.append(cur);return out
rows=[shots[i:i+3] for i in range(0,len(shots),3)]
RH=IH+380; H=300+len(rows)*RH+40
im=Image.new("RGB",(W,H),(14,14,16));d=ImageDraw.Draw(im)
d.text((M,50),"FILM #2 · #1 STREAMER OVERNIGHT · Storyboard v4 · Section 2 · Shots 50–57",font=f(B,56),fill="white")
d.text((M,140),"Status: 52, 56, 57 edited · 51, 53 NOT edited · 55 CUT (omitted) · 54 carries VO-069 (2nd half)–071",font=f(Rg,34),fill=(230,200,60))
d.text((M,200),"1920×1080 · edits are monitor-screen only (rest of each master unchanged) · 0 credits",font=f(Rg,30),fill=(160,160,160))
for r,row in enumerate(rows):
    for c,(n,vo,dur,fn,line,note) in enumerate(row):
        x=M+c*(CW+G); y=290+r*RH
        t=Image.open(R+fn).convert("RGB").resize((CW,IH),Image.LANCZOS); im.paste(t,(x,y))
        d.text((x,y+IH+14),f"SHOT {n} · {vo} · {dur}",font=f(B,34),fill=(250,210,40))
        yy=y+IH+66
        for l in wrap(d,line,f(B,30),CW): d.text((x,yy),l,font=f(B,30),fill="white"); yy+=40
        yy+=6
        for l in wrap(d,note,f(Rg,25),CW): d.text((x,yy),l,font=f(Rg,25),fill=(150,150,155)); yy+=33
im.save(sys.argv[2]+".png"); im.save(sys.argv[2]+".pdf","PDF",resolution=100)
