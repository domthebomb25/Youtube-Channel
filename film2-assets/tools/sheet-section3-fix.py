import sys
from PIL import Image, ImageDraw, ImageFont
# usage: python3 -I sheet-section3-fix.py <repo>/film2-assets  (Section 3 fix-round sheets)
A=sys.argv[1]; R=A+"/section3/"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
def wrap(d,t,font,w):
    out=[];cur=""
    for word in t.split():
        x=(cur+" "+word).strip()
        if d.textlength(x,font=font)<=w: cur=x
        else: out.append(cur);cur=word
    out.append(cur);return out
def sheet(shots,title,status,out):
    rows=[shots[i:i+3] for i in range(0,len(shots),3)]
    RH=IH+400; H=300+len(rows)*RH+40
    im=Image.new("RGB",(W,H),(14,14,16));d=ImageDraw.Draw(im)
    d.text((M,50),title,font=f(B,54),fill="white")
    d.text((M,140),status,font=f(Rg,34),fill=(230,200,60))
    d.text((M,200),"Ludwig = GREEN sweatshirt · Ninja = BLUE sweatshirt (character color lock) · 1920×1080 masters",font=f(Rg,30),fill=(160,160,160))
    for r,row in enumerate(rows):
        for c,(label,vo,dur,fn,line,note) in enumerate(row):
            x=M+c*(CW+G); y=290+r*RH
            im.paste(Image.open(R+fn).convert("RGB").resize((CW,IH),Image.LANCZOS),(x,y))
            d.text((x,y+IH+14),f"{label} · {vo} · {dur}",font=f(B,34),fill=(250,210,40))
            yy=y+IH+66
            for l in wrap(d,line,f(B,28),CW): d.text((x,yy),l,font=f(B,28),fill="white"); yy+=38
            yy+=6
            for l in wrap(d,note,f(Rg,25),CW): d.text((x,yy),l,font=f(Rg,25),fill=(150,150,155)); yy+=33
    im.save(out+".png"); im.save(out+".pdf","PDF",resolution=100)
S1=[
 ("SHOT 59","VO-076–078","8.1s","59.png","“Every single name on that counter pays about six dollars a month. Six dollars sounds like nothing. It is the price of a coffee.”","NEW (1.00). Lead at his desk, unimpressed; hero gold coin with $6 tag + coffee cup; stream screen. Tag text retouched locally (model garbled it)."),
 ("SHOT 63","VO-086–088","7.1s","63.png","“In one month. And he had fewer subscribers than you are about to have. That is just the subscribers.”","MODEL EDIT (1.00): calendar removed; bars, icons, arrow, faces unchanged. No text."),
 ("SHOT 65","VO-091","5.3s","65.png","“One streamer showed his real numbers for one month. His name is Ludwig.”","LOCAL recolor (0.00): Ludwig's sweatshirt now GREEN. Label untouched."),
 ("SHOT 69","VO-095","11.6s","69.png","“One platform, called Mixer, reportedly paid the streamer named Ninja … between twenty and thirty million dollars. Just to stream on their site instead of Twitch.”","NEW (1.00): fills the full frame. Ninja in BLUE sweatshirt, no gold tie. Text: MIXER, NINJA."),
 ("SHOT 69 · STATE","VO-095 payoff","(free)","69-state.png","“…between twenty and thirty million dollars.”","FREE STATE rebuilt from the new 69 (local, 0.00): $20,000,000 – $30,000,000 on a banner under the contract. The new composition has no empty band, so the text is smaller than before."),
 ("SHOT 70","VO-096–097","4.1s","70.png","“Just to stream on their site instead of Twitch. So add it up.”","MODEL EDIT (1.00): walking figure replaced by Ninja (BLUE sweatshirt, no gold tie). Doors, labels, lighting unchanged."),
]
S2=[
 ("SHOT 71","VO-098","3.6s","71.png","“Millions from the subscribers climbing on your screen.”","Row 1 lit (viewers), rows 2–3 dark. Was 71 (unchanged file). “Every viewer pays.”"),
 ("SHOT 72","VO-099","3.6s","72.png","“Hundreds of thousands from the brands lining up behind them.”","Rows 1–2 lit (was 71-state2). “Every company pays more.”"),
 ("SHOT 73","VO-100","3.4s","73.png","“Tens of millions from the platforms fighting over you.”","All three rows lit (was 71-state3). “Even the platforms take their cut.”"),
 ("SHOT 74","VO-101–103","8.8s","74.png","“That is truth number one. At number one, the money does not come from one place. It comes from everywhere — all at the same time.”","Money from everywhere. Renumbered from 72 (image unchanged)."),
 ("SHOT 75","VO-104","2.8s","75.png","“Now let's uncover the hidden truth number 2.”","Bridge back to the room. Renumbered from 73 (image unchanged)."),
]
sheet(S1,"FILM #2 · Storyboard v4 · Section 3 FIX ROUND · Changed shots 59, 63, 65, 69, 70 + 69-state","Fix round: 59, 69 new · 63, 70 model edits · 65 local recolor · 69-state rebuilt · 4.00 credits",A+"/storyboards/section3-fix-v4-changed-shots")
sheet(S2,"FILM #2 · Storyboard v4 · Section 3 · Shots 71–75 (old 71 split into three)","Cumulative row highlight across 71–73 · old 72/73 renumbered to 74/75 · local file work, 0 credits",A+"/storyboards/section3-fix-v4-shots-71-75")
