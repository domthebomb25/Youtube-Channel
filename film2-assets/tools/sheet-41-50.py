import sys
from PIL import Image, ImageDraw, ImageFont
# usage: python3 -I sheet-41-50.py <repo>/film2-assets <outprefix>
A=sys.argv[1]; R=A+"/section2/"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
shots=[
 (41,"VO-053","3.4s","41.png","“You’re not doing anything special today. You’re just talking to them.”","EDITED: chat column is now the genuine shot-36 chat (icon column + colored bars), warped to the monitor angle. Local composite, 0 credits."),
 (42,"VO-054","5.9s","42.png","“Telling them you can’t believe it. Thanking them. Reading names as the gifts fly in.”","Approved as-is."),
 (43,"VO-055","4.4s","43.png","“And the whole time, on the screen next to your chat, the counter is climbing.”","Approved as-is."),
 (44,"VO-056–057","6.6s","44.png","“Now the gifts and the money start pouring in — faster than you can even keep up. And tonight is not even here yet.”","NEW VO ASSIGNMENT: VO-057 now plays here (45 is cut). Image unchanged."),
 (46,"VO-058–059","7.1s","46.png","“Your phone won’t stop ringing. Friends, family and even people you haven’t heard from in years are reaching out.”","NEW VO ASSIGNMENT: now starts at VO-058 (45 is cut). Image unchanged."),
 (47,"VO-060","3.9s","47.png","“There is so much happening that you don’t even know what to do.”","EDITED: burst removed; his stream preview (same overwhelmed face) + established chat streaking past, overloaded. Viewer icons 3 and 4 repainted from clean icons in the same column (local, 0 credits)."),
 (48,"VO-061–062","4.9s","48.png","“And you can’t stop watching the number climb. You tell yourself to stop checking.”","Approved as-is."),
 (49,"VO-063–064","3.5s","49.png","“You check again five minutes later. Eight hundred thousand.”","Approved as-is."),
 (50,"VO-065","1.7s","50.png","“Nine hundred thousand.”","Approved as-is. ASSEMBLY STATE (counter flipped to 900,000 on 49)."),
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
d.text((M,50),"FILM #2 · #1 STREAMER OVERNIGHT · Storyboard v4 · Section 2 · Shots 41–50",font=f(B,56),fill="white")
d.text((M,140),"Status: 41 and 47 edited locally · shot 45 is CUT (omitted; no renumbering) · 44 carries VO-056–057, 46 carries VO-058–059",font=f(Rg,34),fill=(230,200,60))
d.text((M,200),"1920×1080 · edits are regional (rest of each master unchanged) · 42, 43, 48, 49, 50 approved as-is",font=f(Rg,30),fill=(160,160,160))
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
