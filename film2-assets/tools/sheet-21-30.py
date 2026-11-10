import sys, textwrap
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1]
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
shots=[
 (21,"VO-028–029","shot21.png","“Before we get into those 3 hidden truths — let’s pause for a second.”","APPROVED as-is (WebP copy supplied by you). 4.49 s"),
 (22,"VO-030","shot22.png","“And understand what actually just happened to you last night.”","APPROVED as-is (WebP copy supplied by you). 3.47 s"),
 (23,"VO-031–032","shot23.png","“There are more than six million people who have pressed that same button you pressed. Six million.”","RE-ROLLED. ACCEPTED as delivered — FINAL. 5.59 s"),
 (24,"VO-033","shot24.png","“Most of them stream to an empty room — the same empty room you streamed to yesterday.”","RE-ROLLED. ACCEPTED as delivered — FINAL. 5.15 s"),
 (25,"VO-034","shot25.png","“Out of all six million, only about eighty thousand become an official partner.”","RE-ROLLED. ACCEPTED as delivered — FINAL. 5.41 s"),
 (26,"VO-035","shot26.png","“And above all of them, there is one chair.”","RE-ROLLED. ACCEPTED as delivered — FINAL. 3.00 s"),
 (27,"VO-036","shot27.png","“This morning, that chair became yours.”","REUSED — Section 1 shot 1 (thumbC frame, no edit, no cost). Re-roll discarded. 2.77 s"),
 (28,"VO-037","shot28.png","“You open your dashboard in shock — you can’t believe what you see.”","RE-ROLLED (2nd). Counter ~70% of screen width, digits motion-blurred, none identifiable; graph on right quarter climbing off top; LIVE off. 3.55 s"),
 (29,"VO-038","shot29.png","“Yesterday, that screen had almost nothing to say.”","APPROVED as-is (WebP copy supplied by you). Eye icon + “2”, dull red LIVE. 4.28 s"),
 (30,"VO-039","shot30.png","“This morning, the number will not sit still.”","RE-ROLLED (2nd). Screen only; digits ~75% of width, smeared beyond reading; icon far left, graph at right edge exiting top. Assembly 31 (VO-040) rebuilt as push-in on this. 3.55 s"),
]
def wrap(d,t,font,w):
    out=[];cur=""
    for word in t.split():
        x=(cur+" "+word).strip()
        if d.textlength(x,font=font)<=w: cur=x
        else: out.append(cur);cur=word
    out.append(cur);return out
rows=[shots[i:i+3] for i in range(0,len(shots),3)]
RH=IH+330
H=300+len(rows)*RH+60
im=Image.new("RGB",(W,H),(14,14,16));d=ImageDraw.Draw(im)
d.text((M,50),"FILM #2 · #1 STREAMER OVERNIGHT · Storyboard v4 · Shots 21–30",font=f(B,56),fill="white")
d.text((M,140),"Status: Section 2 batch 21–30 · FINAL decisions applied · 27 reused from Section 1 shot 1 · 28 and 30 re-rolled again (2.00 credits)",font=f(R,34),fill=(230,200,60))
d.text((M,200),"Script lines and durations verbatim from your VO list.  Shot 31 (VO-040 assembly push-in on 30) rebuilt.",font=f(R,30),fill=(160,160,160))
y0=290
for r,row in enumerate(rows):
    for c,(n,vo,fn,line,note) in enumerate(row):
        x=M+c*(CW+G); y=y0+r*RH
        if fn:
            t=Image.open(f"{S}/out/{fn}").resize((CW,IH),Image.LANCZOS); im.paste(t,(x,y))
        else:
            d.rectangle([x,y,x+CW,y+IH],fill=(40,40,46),outline=(90,90,100),width=3)
            d.text((x+30,y+IH//2-20),"APPROVED — re-attach image",font=f(B,36),fill=(150,150,160))
        d.text((x,y+IH+14),f"SHOT {n} · {vo}",font=f(B,34),fill=(250,210,40))
        yy=y+IH+66
        for l in wrap(d,line,f(B,30),CW): d.text((x,yy),l,font=f(B,30),fill="white"); yy+=40
        yy+=6
        for l in wrap(d,note,f(R,25),CW): d.text((x,yy),l,font=f(R,25),fill=(150,150,155)); yy+=33
im.save(sys.argv[2],"PDF",resolution=100)
im.save(sys.argv[2].replace(".pdf",".png"))
