import sys, json, re
from PIL import Image, ImageDraw, ImageFont
# usage: python3 -I sheet-section6.py <repo>/film2-assets  (writes the four Section 6 sheets into storyboards/)
A=sys.argv[1]; R=A+"/section6/"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
# verbatim script text from voiceover/script-locked.txt (line N = VO-N, speech lines only)
L=[l.strip() for l in open(A+"/voiceover/script-locked.txt",encoding="utf-8")]
sp=[l for l in L if l and not re.match(r'^SECTION|^TRUTH|^[A-Z0-9 —:\-\.\(\)#]+$',l) or l=="But."]
V={i:l for i,l in enumerate(sp,1)}
def line(a,b=None):
    b=b or a; return "“"+" ".join(V[i] for i in range(a,b+1))+"”"
S=[
 (112,"VO-177–178","7.6s",line(177,178),"Callback to yesterday: the locked room DIM at morning, the plain SMALL chair (not the #1 chair), him just woken, small in frame, looking at the little chair. Text: none."),
 (113,"VO-179","3.7s",line(179),"Night: him ASLEEP in the giant #1 chair, crown slipped on his head, room dark except monitor glow; STREAM screen with his exact sleeping face as preview. LIVE bright. Text: none (#1 / LIVE props only)."),
 (114,"VO-180–181","3.4s",line(180,181),"Gold coins piling up on the desk, spilling toward the #1 chair where he sits watching them land. No monitor in frame. Text: none."),
 (115,"VO-182–183","7.4s",line(182,183),"Him centered in the #1 chair; plain suited company stickmen and platform spotlights lean IN with packages and envelopes, a crowd behind. Everyone paying to be close. Text: none."),
 (116,"VO-184–185","3.5s",line(184,185),"He stands tall holding the CROWN HIGH in both hands, warm golden one-night glow, no wind, no strain. Text: none."),
 (117,"VO-186–187","6.6s",line(186,187),"Reprise of 108: the crown resting on top of a full one-month calendar grid (blank, 30 squares); him small beside it, looking at it. Text: none."),
 (118,"VO-188–189","4.9s",line(188,189),"Giant calendar page with the paper BILL pinned to it (crown, red stamp, nothing readable); below, the crowd of plain viewer stickmen faces him, deciding. He stands before them. Text: none."),
 (119,"VO-190","4.0s",line(190),"A plain challenger stickman (NO tie, hungry) grips the arm of the #1 chair and pulls; the business stickman turns toward him, startled. Text: none (#1 on chair = prop)."),
 (120,"VO-191–192","7.1s",line(191,192),"The endless sea of plain streamers at little desks to the horizon, every face turned toward the glowing #1 chair at the top. Text: none (#1 on chair)."),
 (121,"VO-193–195","5.4s",line(193,195),"FINAL FRAME. Morning light, the locked room, him AT THE DESK in the #1 chair, hands on keyboard, LIVE bright; monitor seen from behind (plain back, fix round). Text: none (LIVE prop only)."),
]
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
def wrap(d,t,font,w):
    out=[];cur=""
    for word in t.split():
        x=(cur+" "+word).strip()
        if d.textlength(x,font=font)<=w: cur=x
        else: out.append(cur);cur=word
    out.append(cur);return out
def sheet(shots,rng,status,out):
    rows=[shots[i:i+3] for i in range(0,len(shots),3)]
    RH=IH+520; H=300+len(rows)*RH+40
    im=Image.new("RGB",(W,H),(14,14,16));d=ImageDraw.Draw(im)
    d.text((M,50),f"FILM #2 · #1 STREAMER OVERNIGHT · Storyboard v4 · Section 6 · Shots {rng}",font=f(B,56),fill="white")
    d.text((M,140),status,font=f(Rg,34),fill=(230,200,60))
    d.text((M,200),"1920×1080 masters · gpt_image_2_5 16:9 2k medium · 1.00 each · one generation per shot, no re-rolls",font=f(Rg,30),fill=(160,160,160))
    for r,row in enumerate(rows):
        for c,(n,vo,dur,ln,note) in enumerate(row):
            x=M+c*(CW+G); y=290+r*RH
            im.paste(Image.open(R+f"{n}.png").convert("RGB").resize((CW,IH),Image.LANCZOS),(x,y))
            d.text((x,y+IH+14),f"SHOT {n} · {vo} · {dur}",font=f(B,34),fill=(250,210,40))
            yy=y+IH+66
            for l in wrap(d,ln,f(B,28),CW): d.text((x,yy),l,font=f(B,28),fill="white"); yy+=38
            yy+=6
            for l in wrap(d,note,f(Rg,25),CW): d.text((x,yy),l,font=f(Rg,25),fill=(150,150,155)); yy+=33
    im.save(out+".png"); im.save(out+".pdf","PDF",resolution=100)
if __name__=="__main__":
    P=A+"/storyboards/section6-storyboard-v4-"
    T="Section 6 (The Payoff)"
    sheet(S[0:6],"112–117",T+" · sheet 1 of 2 · all generated, awaiting review",P+"shots-112-117")
    sheet(S[6:10],"118–121",T+" · sheet 2 of 2 · FINAL SHOTS OF THE FILM · 121 monitor back fixed (local, 0.00) · awaiting review",P+"shots-118-121")
