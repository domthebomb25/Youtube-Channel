import sys, json, re
from PIL import Image, ImageDraw, ImageFont
# usage: python3 -I sheet-section5.py <repo>/film2-assets  (writes the four Section 5 sheets into storyboards/)
A=sys.argv[1]; R=A+"/section5/"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Rg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
# verbatim script text from voiceover/script-locked.txt (line N = VO-N, speech lines only)
L=[l.strip() for l in open(A+"/voiceover/script-locked.txt",encoding="utf-8")]
sp=[l for l in L if l and not re.match(r'^SECTION|^TRUTH|^[A-Z0-9 —:\-\.\(\)#]+$',l) or l=="But."]
V={i:l for i,l in enumerate(sp,1)}
def line(a,b=None):
    b=b or a; return "“"+" ".join(V[i] for i in range(a,b+1))+"”"
S=[
 (89,"VO-130–131","3.5s",line(130,131),"BRIDGE. The locked room at dusk; the door from 88 now closed. He stands alone, serious, before the #1 chair. Monitor off, LIVE box UNLIT. Text: none (#1 on chair = locked prop)."),
 (90,"VO-132–133","9.0s",line(132,133),"Long staircase climbing to the glowing #1 throne far above; he stands small at a halfway marker (blank flag), looking up. Text: none (#1 on throne)."),
 (91,"VO-134","4.1s",line(134),"At the top: he grips the crown with both hands against blowing wind, tie flying, straining to hold on. Text: none."),
 (92,"VO-135–136","6.0s",line(135,136),"The #1 chair slides away across a tilting floor as he reaches for it. No desk/monitor in frame. Text: none (#1 on chair)."),
 (93,"VO-137","9.2s",line(137),"Ninja at his peak setup: plain stickman, BLUE hoodie, no tie, two monitors seen from behind, wall calendar with two days X'd (no numbers). Text: NINJA (label) only."),
 (94,"VO-138–139","7.3s",line(138,139),"Ninja (BLUE hoodie) staring at the COUNTER screen: 40,000 with a red down arrow; two torn calendar pages on the floor. Text: 40,000 only. Nit: right eyebrow tight to the head outline."),
 (95,"VO-140–141","7.8s",line(140,141),"Three calendar pages in a row (middle and right mid-flip); under each, the same vignette: he streams at his desk, LIVE BRIGHT (today, tomorrow, next day). Monitors from behind. No dates."),
 (96,"VO-142","2.4s",line(142),"Him beside the bright LIVE sign at the left edge; at the right edge a cliff drops into black nothing. Text: LIVE (sign) only."),
 (97,"VO-143–144","5.4s",line(143,144),"A sea of plain streamers (gray hoodies, no ties) at small desks, each pressing a red button, every eye on the #1 chair glowing at the top. Text: none (#1 on chair)."),
 (98,"VO-145–146","7.9s",line(145,146),"The #1 chair in shadow-light: a crown passes from one black silhouette's hands to another's; more challenger silhouettes approach from the dark. No faces. Text: none (#1 on chair)."),
 (99,"VO-147–149","8.3s",line(147,149),"His room: monitor on the COUNTER screen 1,000,000; the crowd around the desk and floor is made of gift boxes with bows. He looks uneasy. LIVE bright. Text: 1,000,000 (+ locked #1 / LIVE props)."),
 (100,"VO-150–151","5.4s",line(150,151),"One gift box wearing a BLANK expiration tag, sitting on a one-month calendar grid (blank squares, no dates). Text: none."),
 (101,"VO-152–153","6.9s",line(152,153),"The same gift box faded to a pale dashed ghost; beside it an empty, softly lit viewer seat in a row of dark empty seats. Text: none."),
 (102,"VO-154–155","7.6s",line(154,155),"The record holder: generic plain stickman (gray hoodie, NO tie, NO label) at his desk, arms up, confetti, COUNTER screen 1,000,000. Text: 1,000,000 only."),
 (103,"VO-156–158","7.2s",line(156,158),"The same man weeks later: slumped, shocked, calendar pages scattered on the floor, room quiet and empty, COUNTER screen 40,000. Text: 40,000 only."),
 (104,"VO-159–162","7.5s",line(159,162),"A giant calendar page looms over him; one day circled in red: the 30. He is small beneath it, gold tie. Text: 30 only."),
 (105,"VO-163–166","5.9s",line(163,166),"He is LIVE again, determined, gold tie; behind him a calendar grid with EVERY square checked, no gaps. LIVE bright. Note: the grid has 24 squares (4×6), not 30. Text: none (LIVE sign only)."),
 (106,"VO-167","6.0s",line(167),"Plain generic stickman (gray hoodie, no tie, no name colors) at a marathon setup: headphones, mic, cans, snacks, blanket; wall of 30 blank day squares (5×6). Text: KAI CENAT (plain label) only."),
 (107,"VO-168–169","7.3s",line(168,169),"His room around the clock: bed beside the streaming desk; sun on one half of the window, moon on the other; he sleeps on camera (tripod camera with red dot, mic, headphones). Text: none."),
 (108,"VO-170–171","9.0s",line(170,171),"A crown resting on a full calendar grid, every square checked; he stands guard with a spear, tired. Note: the grid has 20 squares (4×5), not 30. Text: none."),
 (109,"VO-172","4.4s",line(172),"Callback to 90 from the top: he stands at the #1 throne and the road keeps climbing past it, out of frame. Text: none (#1 on throne)."),
 (110,"VO-173–174","6.3s",line(173,174),"On his desk: an open envelope, a bill with a crown printed on it and a red due-date stamp (tiny calendar icon, nothing readable), coffee mug. Text: none."),
 (111,"VO-175–176","6.3s",line(175,176),"Closing: from far below, a swarm of black challenger silhouettes climbs the stairs toward his glowing throne; he stands at the top holding the crown. Text: none (#1 on throne)."),
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
    d.text((M,50),f"FILM #2 · #1 STREAMER OVERNIGHT · Storyboard v4 · Section 5 · Shots {rng}",font=f(B,56),fill="white")
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
    P=A+"/storyboards/section5-storyboard-v4-"
    T="Section 5 (Truth 3: The Catch)"
    sheet(S[0:6],"89–94",T+" · sheet 1 of 4 · all generated, all passed self-check",P+"shots-89-94")
    sheet(S[6:12],"95–100",T+" · sheet 2 of 4 · all generated, all passed self-check",P+"shots-95-100")
    sheet(S[12:18],"101–106",T+" · sheet 3 of 4 · 105 grid has 24 squares (flag)",P+"shots-101-106")
    sheet(S[18:23],"107–111",T+" · sheet 4 of 4 · 108 grid has 20 squares (flag)",P+"shots-107-111")
