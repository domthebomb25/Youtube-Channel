import sys
from PIL import Image, ImageDraw, ImageFont
# usage: python3 -I sheet-section3.py <repo>/film2-assets   (writes both Section 3 sheets into storyboards/)
A=sys.argv[1]; R=A+"/section3/"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
S=[
 (58,"VO-074–075","6.0s","58.png","“Truth number one is about the money. And the money starts with the counter you could not stop watching.”","ROOM shot. COUNTER screen: 900,000 + one blurred line. LIVE bright."),
 (59,"VO-076–078","8.1s","59.png","“Every single name on that counter pays about six dollars a month. Six dollars sounds like nothing. It is the price of a coffee.”","One name pill, one $6 coin, coffee cup beside it. Dark background."),
 (60,"VO-079–081","6.9s","60.png","“But tonight, you are crossing one million of them. One million people. Six dollars each.”","Scale: sea of viewer icons, coin stacks. Text: 1,000,000 and $6."),
 (61,"VO-082–083","8.6s","61.png","“Now — the website takes its cut first. About half of every subscription goes to the platform before it ever reaches you.”","Coin split in half; website window's hand takes one half. No text."),
 (62,"VO-084–085","8.8s","62.png","“And still. The last time a streamer made a run like yours, they grossed … about three and a half million dollars.”","Precedent streamer (plain hoodie, no gold tie). Text: $3,500,000."),
 (63,"VO-086–088","7.1s","63.png","“In one month. And he had fewer subscribers than you are about to have. That is just the subscribers.”","Calendar; his bar SHORTER (plain icon), lead's bar TALLER + arrow (gold-tie icon). No text."),
 (64,"VO-089–090","7.5s","64.png","“You haven't even realized what else is in store for you. Because once a crowd that size exists, the companies come next.”","ROOM shot. LIVE bright. Door side: viewer crowd, suits + briefcases + office building. No text. NOTE: room framing/angle slightly differs from shot 9 (door added)."),
 (65,"VO-091","5.3s","65.png","“One streamer showed his real numbers for one month. His name is Ludwig.”","Plain streamer (no gold tie), ledger blurred. Text: LUDWIG."),
 (66,"VO-092","8.9s","66.png","“His viewers and his streaming sites paid him over three hundred thousand dollars — but the brands paid him eight hundred thousand dollars.”","Two bars, right taller. Text: $300,000+ and $800,000."),
 (67,"VO-093","4.9s","67.png","“The companies that want to stand next to your crowd pay more than the crowd does.”","Balance scale: company pan sinks lower. No text."),
 (68,"VO-094","5.6s","68.png","“And then there are the platforms themselves — the websites fighting to be the place you stream.”","Three storefronts, spotlights toward him at the #1 chair. No names, no text."),
 (69,"VO-095","11.6s","69.png","“One platform, called Mixer, reportedly paid the streamer named Ninja … between twenty and thirty million dollars. Just to stream on their site instead of Twitch.”","APPROVED OVER-CAP (payoff withheld). Text: MIXER, NINJA. FREE STATE 69-state.png: same image + $20,000,000 – $30,000,000, lands at the payoff. 0 credits."),
 (70,"VO-096–097","4.1s","70.png","“Just to stream on their site instead of Twitch. So add it up.”","MIXER doorway lit, he walks through; TWITCH doorway dim behind. Text: MIXER, TWITCH."),
 (71,"VO-098–100","10.5s","71.png","“Millions from the subscribers … Hundreds of thousands from the brands … Tens of millions from the platforms fighting over you.”","APPROVED EXCEPTION. 71 = row 1 lit. FREE STATES: 71-state2.png (rows 1–2 lit), 71-state3.png (all 3 lit). Local, 0 credits. No text."),
 (72,"VO-101–103","8.8s","72.png","“That is truth number one. At number one, the money does not come from one place. It comes from everywhere — all at the same time.”","ROOM shot. LIVE bright. Coins converge from window, door, monitor, above. No text."),
 (73,"VO-104","2.8s","73.png","“Now let's uncover the hidden truth number 2.”","BRIDGE: echoes 58. COUNTER 900,000 + TWO blurred lines. LIVE bright."),
]
def wrap(d,t,font,w):
    out=[];cur=""
    for word in t.split():
        x=(cur+" "+word).strip()
        if d.textlength(x,font=font)<=w: cur=x
        else: out.append(cur);cur=word
    out.append(cur);return out
def sheet(shots,rng,status,out):
    rows=[shots[i:i+3] for i in range(0,len(shots),3)]
    RH=IH+400; H=300+len(rows)*RH+40
    im=Image.new("RGB",(W,H),(14,14,16));d=ImageDraw.Draw(im)
    d.text((M,50),f"FILM #2 · #1 STREAMER OVERNIGHT · Storyboard v4 · Section 3 · Shots {rng}",font=f(B,56),fill="white")
    d.text((M,140),status,font=f(Rg,34),fill=(230,200,60))
    d.text((M,200),"1920×1080 masters · gpt_image_2_5 16:9 2k medium · 1.00 each · one generation per shot, no re-rolls",font=f(Rg,30),fill=(160,160,160))
    for r,row in enumerate(rows):
        for c,(n,vo,dur,fn,line,note) in enumerate(row):
            x=M+c*(CW+G); y=290+r*RH
            im.paste(Image.open(R+fn).convert("RGB").resize((CW,IH),Image.LANCZOS),(x,y))
            d.text((x,y+IH+14),f"SHOT {n} · {vo} · {dur}",font=f(B,34),fill=(250,210,40))
            yy=y+IH+66
            for l in wrap(d,line,f(B,28),CW): d.text((x,yy),l,font=f(B,28),fill="white"); yy+=38
            yy+=6
            for l in wrap(d,note,f(Rg,25),CW): d.text((x,yy),l,font=f(Rg,25),fill=(150,150,155)); yy+=33
    im.save(out+".png"); im.save(out+".pdf","PDF",resolution=100)
sheet(S[:10],"58–67","Section 3 (Truth 1: The Money) · batch 1 of 2 · all 10 generated, passed self-check",A+"/storyboards/section3-storyboard-v4-shots-58-67")
sheet(S[10:],"68–73","Section 3 · batch 2 of 2 · free states: 69-state, 71-state2, 71-state3 (local)",A+"/storyboards/section3-storyboard-v4-shots-68-73")
