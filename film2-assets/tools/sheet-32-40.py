import sys
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1]; R=S+"/repo/film2-assets/section2/"; F=S+"/edit/final"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
shots=[
 (32,"VO-041","3.0s",R+"32.png","“You keep asking yourself if this is even real.”","Hand on cheek, “is this real?”. LIVE off. Unchanged."),
 (33,"VO-042–043","4.8s",F+"33.png","“Your phone won’t stop ringing. It can’t keep up with all the notifications you are getting.”","FIX ROUND: LIVE box now unlit, matches shot 32 (no red, no glow). Phone, bubbles, room unchanged."),
 (34,"VO-044–045","3.0s",R+"34.png","“You take a moment to gather yourself. You press the button.”","Deep breath, hand on the button, LIVE still OFF. Base for 35. Unchanged."),
 (35,"VO-046","1.7s",R+"35.png","“The red light turns on.”","ASSEMBLY STATE of 34: LIVE light flipped bright red, free local recolor. Unchanged."),
 (36,"VO-047","4.5s",F+"36.png","“And the room is already full — before you even say a single word.”","FIX ROUND: shocked open mouth added; face in the stream preview now the same shocked face. Chat column unchanged."),
 (37,"VO-048","2.9s",R+"37.png","“Yesterday, this room was empty.”","YESTERDAY: stream view with eye icon + 2, EMPTY chat column, dull-red LIVE. Unchanged."),
 (38,"VO-049–050","5.4s",F+"38.png","“You close your eyes, take a deep breath and start the only way you know how.”","FIX ROUND: monitor now shows his stream preview — exact closed-eyes calm-smile face + chat column (landscape removed)."),
 (39,"VO-051","5.4s",F+"39.png","“You open your mouth with a big smile and say the same thing you have for every stream before this.”","FIX ROUND: monitor now shows his stream preview — exact beaming open-mouth face + chat column. Base for 40."),
 (40,"VO-052","2.3s",F+"40.png","“Hello everyone, welcome to my stream!”","ASSEMBLY STATE of 39, REBUILT from the fixed 39: ×2 push-in, crop (500,180)–(1460,720). No on-screen text."),
]
def wrap(d,t,font,w):
    out=[];cur=""
    for word in t.split():
        x=(cur+" "+word).strip()
        if d.textlength(x,font=font)<=w: cur=x
        else: out.append(cur);cur=word
    out.append(cur);return out
rows=[shots[i:i+3] for i in range(0,len(shots),3)]
RH=IH+340; H=300+len(rows)*RH+40
im=Image.new("RGB",(W,H),(14,14,16));d=ImageDraw.Draw(im)
d.text((M,50),"FILM #2 · #1 STREAMER OVERNIGHT · Storyboard v4 · Section 2 · Shots 32–40",font=f(B,56),fill="white")
d.text((M,140),"Status: fix round applied to 33, 36, 38, 39 · 40 rebuilt from new 39 · shot 31 is CUT (omitted; VO-040 plays over shot 30)",font=f(Rg,34),fill=(230,200,60))
d.text((M,200),"1920×1080 · FIX ROUND = edited region only, everything else identical to the previous master · shots 32, 34, 35, 37 unchanged",font=f(Rg,30),fill=(160,160,160))
for r,row in enumerate(rows):
    for c,(n,vo,dur,p,line,note) in enumerate(row):
        x=M+c*(CW+G); y=290+r*RH
        t=Image.open(p).convert("RGB").resize((CW,IH),Image.LANCZOS); im.paste(t,(x,y))
        d.text((x,y+IH+14),f"SHOT {n} · {vo} · {dur}",font=f(B,34),fill=(250,210,40))
        yy=y+IH+66
        for l in wrap(d,line,f(B,30),CW): d.text((x,yy),l,font=f(B,30),fill="white"); yy+=40
        yy+=6
        for l in wrap(d,note,f(Rg,25),CW): d.text((x,yy),l,font=f(Rg,25),fill=(150,150,155)); yy+=33
im.save(sys.argv[2]+".png"); im.save(sys.argv[2]+".pdf","PDF",resolution=100)
