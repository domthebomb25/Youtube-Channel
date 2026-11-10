import sys
from PIL import Image, ImageDraw, ImageFont
# usage: python3 -I sheet-section4.py <repo>/film2-assets   (writes the three Section 4 sheets into storyboards/)
A=sys.argv[1]; R=A+"/section4/"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
W=2640; M=60; G=40; CW=(W-2*M-2*G)//3; IH=CW*9//16
S=[
 (76,"VO-105–106","4.1s","76.png","“Truth number two is not about money. It is about power.”","Locked room, morning. Coin stacks shoved to the desk edge; he stands tall in front of the #1 chair. STREAM screen, his confident face. LIVE bright. No text."),
 (77,"VO-107–109","9.7s","77.png","“Yesterday, you wrote to people — and nobody wrote back. You asked brands to notice you. Nothing. You asked the platforms for a chance. Silence.”","YESTERDAY: dim evening, small plain chair + desk. Three gray bubbles toward person / brand-tag / building icons, all unanswered. LIVE unlit. No text."),
 (78,"VO-110–111","6.3s","78.png","“Today, everybody answers in minutes. The platforms are not just paying you. They are calling you.”","TODAY: #1 chair, morning. Phone lit with blurred incoming replies; ringing-phone symbols. STREAM screen, LIVE bright. FLAG: ringing icons are phone symbols, not platform buildings."),
 (79,"VO-112–114","8.9s","79.png","“Each one wants you standing on their side. And they are not calling because of how you play. They are calling because of the crowd standing behind you.”","Three generic platform buildings lean in; huge viewer-icon crowd behind him (biggest element). Gold tie, calm. No text, no logos."),
 (80,"VO-115–116","7.2s","80.png","“Because that is what you own now. A crowd that companies cannot build for themselves — so they have to come to you.”","His door: line of suits with briefcases, hats in hand; he stands relaxed, crowd icons visible inside. No text."),
 (81,"VO-117–118","4.9s","81.png","“The famous names you used to watch? They are asking to come on YOUR stream now.”","Three generic star stickmen (sunglasses, sparkles) ask to come on; he is surprised. STREAM screen, LIVE bright. NOTE: one star wears a blue shirt. No text."),
 (82,"VO-119–120","7.9s","82.png","“Not because you are famous like them. Because your room is where the people are — and being seen in your room is worth money to them.”","Room glowing gold, packed with viewer icons; stars outside door/window looking in. [LOCAL FIX] monitor = locked STREAM screen asset (model's eye-icon screen replaced). No text."),
 (83,"VO-121–122","7.9s","83.png","“And your crowd is not just an audience anymore. It is a store, a TV channel, and a billboard — all in one place.”","One crowd, three forms: storefront, TV, billboard around him. Blank signs. No text."),
 (84,"VO-123","2.3s","84.png","“You point at a product, and it sells out.”","Empty shelf, ONE blank box, his gold-tie sleeve points from frame left. Text: SOLD OUT (tag only)."),
 (85,"VO-124","9.9s","85.png","“You point at a tiny streamer nobody knows — a kid in a small room, talking to nobody, just like you were yesterday — and his room explodes in seconds.”","BASE: tiny plain streamer (no tie), one viewer icon on dark monitor, lead's pointing silhouette + glow from left. FREE STATE 85-state.png (sheet 3) lands at “explodes”. No text."),
 (86,"VO-125–126","5.1s","86.png","“You can make somebody else's whole business in one night. With one sentence.”","[FIX ROUND, model edit 1.00] Night street: the store is lit and open, small crowd inside. He stands frame left, HAPPY, hands on hips, gold tie; speech bubble removed. Blank sign. No text."),
 (87,"VO-127–128","5.9s","87.png","“Yesterday, you needed the world. Today, the world needs you.”","Mirror halves: LEFT dim, small, reaching up to a huge globe; RIGHT bright, tall, globe small by the #1 chair. No text."),
 (88,"VO-129","2.7s","88.png","“And it knocks on your door — politely.”","Closing bridge: calm evening, building figure + company suit + star figure wait, one knocks gently, hats in hand; warm light under the door. No text. [VO-130–131 now OPEN Section 5.]"),
 ("85·STATE","VO-124 (payoff)","9.9s","85-state.png","“…and his room explodes in seconds.”  (free state of shot 85)","FREE STATE, built locally, 0 credits: crowd icons flooding in, light burst, monitor alive with the STREAM screen. [FIX ROUND] his face repainted HAPPY (raised brows, big open smile), face only."),
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
    RH=IH+470; H=300+len(rows)*RH+40
    im=Image.new("RGB",(W,H),(14,14,16));d=ImageDraw.Draw(im)
    d.text((M,50),f"FILM #2 · #1 STREAMER OVERNIGHT · Storyboard v4 · Section 4 · Shots {rng}",font=f(B,56),fill="white")
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
P=A+"/storyboards/section4-storyboard-v4-"
sheet(S[0:6],"76–81","Section 4 (Truth 2: The Power) · sheet 1 of 3 · generated; 82 locally fixed; 78 flagged",P+"shots-76-81")
sheet(S[6:12],"82–87","Section 4 · sheet 2 of 3 · 82 monitor replaced locally · 86 edited (fix round, 1.00)",P+"shots-82-87")
sheet([S[12],S[13]],"88","Section 4 · sheet 3 of 3 · 88 = VO-129 only (2.7s) · 85-state face fixed (local, 0.00)",P+"shots-88-and-85-state")

# individual tiles (fix-round review): 85 base, 85-state, 86, 88
def tile(n,out):
    t=[x for x in S if str(x[0])==n][0]; (nn,vo,dur,fn,line,note)=t
    TW=1700; IH2=TW*9//16; im=Image.new("RGB",(TW+120,IH2+330),(14,14,16)); d=ImageDraw.Draw(im)
    im.paste(Image.open(R+fn).convert("RGB").resize((TW,IH2),Image.LANCZOS),(60,40))
    y=IH2+60; d.text((60,y),f"SHOT {nn} · {vo} · {dur}",font=f(B,44),fill=(250,210,40)); y+=70
    for l in wrap(d,line,f(B,36),TW): d.text((60,y),l,font=f(B,36),fill="white"); y+=48
    for l in wrap(d,note,f(Rg,28),TW): d.text((60,y),l,font=f(Rg,28),fill=(150,150,155)); y+=38
    im.crop((0,0,im.width,y+30)).save(out)
for n,nm in [("85","85-base"),("85·STATE","85-state"),("86","86"),("88","88")]:
    tile(n,A+"/storyboards/section4-fix-tile-"+nm+".png")
