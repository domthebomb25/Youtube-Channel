# Shared data for the full-film storyboard + assembly manifest (reads only files already in the repo).
import re, os, json
A=os.environ.get("F2","/home/user/Youtube-Channel/film2-assets")
# --- locked script (line N = VO-N) and timing report
L=[l.strip() for l in open(A+"/voiceover/script-locked.txt",encoding="utf-8")]
SP=[l for l in L if l and not re.match(r'^SECTION|^TRUTH|^[A-Z0-9 —:\-\.\(\)#]+$',l) or l=="But."]
V={i:l for i,l in enumerate(SP,1)}
assert len(V)==195
DUR={}
for l in open(A+"/voiceover/timing-report.md",encoding="utf-8"):
    m=re.match(r'\| VO-(\d+) \|.*\| ([\d.]+) \|',l)
    if m: DUR[int(m.group(1))]=float(m.group(2))
assert len(DUR)==195
import re as _re
TOTAL=_re.search(r"\*\*([\d.]+) s",open(A+"/voiceover/timing-report.md",encoding="utf-8").read()).group(1)
RETIRED={194}   # VO-194 "Staying there?" is retired: it never plays and is never counted
def _r(a,b): return [i for i in range(a,b+1) if i not in RETIRED]
def quote(a,b=None):
    b=b or a; return "“"+" ".join(V[i] for i in _r(a,b))+"”"
def vsum(a,b=None):
    b=b or a; return round(sum(DUR[i] for i in _r(a,b)),2)
def vlabel(a,b=None):
    b=b or a
    if any(i in RETIRED for i in range(a,b+1)): return " + ".join(f"VO-{i:03d}" for i in _r(a,b))
    return f"VO-{a:03d}" if b==a else f"VO-{a:03d}–{b:03d}"
# --- map durations (as written in each section's own map / sheet), for the cross-check
MAPDUR={}
S1={1:2.9,2:4.6,3:4.0,4:2.9,5:3.5,6:3.1,8:6.8,9:6.4,10:4.3,11:4.7,12:4.6,13:3.9,14:3.1,15:3.4,16:4.9,17:5.4,18:3.8,19:4.7,20:3.6}
S2={21:4.49,22:3.47,23:5.59,24:5.15,25:5.41,26:3.00,27:2.77,28:3.55,29:4.28,30:5.9,32:3.0,33:4.8,34:3.0,35:1.7,36:4.5,37:2.9,38:5.4,39:5.4,40:2.3,41:3.4,42:5.9,43:4.4,44:6.6,46:7.1,47:3.9,48:4.9,49:3.5,50:1.7,51:6.0,52:5.6,53:4.8,54:9.0,56:3.4,57:2.4}
MAPDUR.update(S1); MAPDUR.update(S2)
MAPVO={}   # (a,b) the map's own VO range per shot
for n,(a,b) in {1:(1,1),2:(2,3),3:(4,4),4:(5,5),5:(6,6),6:(7,8),8:(9,10),9:(11,13),10:(14,15),11:(16,16),12:(17,18),13:(19,19),14:(20,20),15:(21,21),16:(22,22),17:(23,23),18:(24,24),19:(25,26),20:(27,27)}.items(): MAPVO[n]=(a,b)
S2VO={21:(28,29),22:(30,30),23:(31,32),24:(33,33),25:(34,34),26:(35,35),27:(36,36),28:(37,37),29:(38,38),30:(39,40),32:(41,41),33:(42,43),34:(44,45),35:(46,46),36:(47,47),37:(48,48),38:(49,50),39:(51,51),40:(52,52),41:(53,53),42:(54,54),43:(55,55),44:(56,57),46:(58,59),47:(60,60),48:(61,62),49:(63,64),50:(65,65),51:(66,67),52:(68,68),53:(69,69),54:(69,71),56:(72,72),57:(73,73)}
MAPVO.update(S2VO)
NOTE={}
# Section 1 notes (from the approved Section 1 sheets)
NOTE.update({1:"Locked thumbnail (thumbC). The #1 chair, crown and spotlight appear only here.",
2:"Yesterday: dim evening, plain chair, eye icon and 2. LIVE sign dull red.",
3:"Yesterday: defeated and weary at the mic. Stream view with eye icon and 2, empty chat column.",
4:"Morning: phone buzzing on a complete tabletop that runs back to the monitor base and LIVE light.",
5:"Morning: sitting down into the #1 chair.",
6:"Close shot: hand on the button, LIVE light glowing.",
8:"Seated in the #1 chair, overwhelmed, blurred chat. Desk setup matched to shot 9.",
9:"BASE image: counter 10,000. Assembly flips: 50,000 (VO-012), then 100,000 (VO-013). The standard desk setup.",
10:"BASE image: 100 GIFTED SUBS. Assembly flip: 1,000 GIFTED SUBS (VO-015). Desk setup matched to shot 9.",
11:"Morning: wall of phones and screens, each showing his face only. Amazed, center foreground.",
12:"Desk standard. Generic brand email, only text on screen: We want YOU.",
13:"Close shot: phone held up, only readable text: you did it!! Grinning face at the edge.",
14:"New location: living room, evening. Asleep on the couch, dream bubble shows him live to a crowd. No text.",
15:"Three icons, each with a red prohibition sign: generic boss silhouette, folded uniform, wall clock. No text.",
16:"Desk standard. Relaxed at the mic; globe ringed by viewer faces behind.",
17:"NIGHT room, moon in the window. Subscriber counter: person icon and 950,000.",
18:"ASSEMBLY STATE of shot 17 (numbered shot, own file): tighter crop on the monitor and his wide eyes, counter flipped to 999,999.",
19:"Mood shift: room dim and dark, he is uneasy. Exactly three glowing question marks.",
20:"The darkest shot: chair barely visible, lit mainly by the red LIVE glow. He glances sideways, uneasy. No crown."})
# Section 2 notes from the section-2 sheet builders (last string field of each shot row)
for f in ("sheet-21-30.py","sheet-32-40.py","sheet-41-50.py","sheet-50-57.py"):
    for line in open(A+"/tools/"+f,encoding="utf-8"):
        m=re.match(r'^\s*\((\d+),.*,"((?:[^"\\]|\\.)*)"\),?\s*$',line)
        if m and 21<=int(m.group(1))<=57: NOTE[int(m.group(1))]=m.group(2)
NOTE[30]="RE-ROLLED (2nd). Screen only; digits ~75% of width, smeared beyond reading. Carries VO-039-040 (shot 31 is CUT); slow push at assembly. 5.9 s"
NOTE[27]="REUSED Section 1 shot 1 (thumbC frame, no edit, no cost)."
NOTE[44]="VO-057 plays here (shot 45 is CUT). Image unchanged."
NOTE[46]="Starts at VO-058 (shot 45 is CUT). Image unchanged."
NOTE[53]="APPROVED AS-IS: first half of VO-069 (to \"on your screen,\")."
NOTE[54]="ASSEMBLY STATE (push-in of 53). Carries VO-069 2nd half, VO-070 and VO-071 (shot 55 is CUT)."
NOTE[57]="REUSED shot 54 exactly (same image). No separate 57 file."
NOTE[35]="ASSEMBLY STATE of shot 34 (numbered shot, own file): LIVE light flipped bright red."
NOTE[40]="ASSEMBLY STATE of shot 39 (numbered shot, own file): x2 push-in, crop (500,180)-(1460,720). No on-screen text."
NOTE[50]="ASSEMBLY STATE of shot 49 (numbered shot, own file): counter flipped to 900,000."
# Sections 3-6 straight from their map files
for sec,fn in ((3,"SECTION3-MAP.txt"),(4,"SECTION4-MAP.txt"),(5,"SECTION5-MAP.txt"),(6,"SECTION6-MAP.txt")):
    inmap=False
    for line in open(A+"/docs/"+fn,encoding="utf-8"):
        if line.startswith("---- MAP"): inmap=True; continue
        if line.startswith("---- ORIGINAL"): inmap=False
        if not inmap: continue
        m=re.match(r'^(\d+)\s+VO-(\d+)(?:(?:[–-]|\s*\+\s*VO-)(\d+))?\s+([\d.]+)s\s+(.*)$',line.rstrip())
        if m:
            n=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a)
            MAPVO[n]=(a,b); MAPDUR[n]=float(m.group(4))
            t=re.sub(r'^\[[A-Z ]+\]\s*','',m.group(5)); NOTE[n]=t
NOTE[69]="APPROVED OVER-CAP (11.6 s). Full-frame: MIXER building, contract + money, Ninja (BLUE sweatshirt). Free assembly state follows."
NOTE[85]="BASE: tiny plain streamer alone in a small dim room, one viewer icon on the dark monitor, lead's pointing silhouette entering from the left. Free assembly state follows."
NOTE[88]="Closing bridge: calm evening outside his door; building figure + company suit + star figure wait, one knocks gently. Ends at VO-129 (VO-130-131 open Section 5)."
NOTE[93]="Ninja (BLUE hoodie, no tie) at his peak setup; wall calendar with two CONSECUTIVE days X'd. FIX ROUND: local edit. Text: NINJA label."
NOTE[101]="Five faded ghost gift boxes + one solid bright box; a plain viewer holds up a gold coin. ACCEPTED as-is after the fix round."
NOTE[121]="FINAL FRAME (VO-193 + VO-195 only; VO-194 retired). Morning light, him at the desk, hands on keyboard, LIVE bright; monitor seen from behind (plain back, FIX ROUND local edit)."
NOTE[112]="Callback: the locked room DIM at morning, the plain SMALL chair, him just woken, small in frame. Line changed (VO-178 now 'went to sleep'). Text: none."
NOTE[71]="Cumulative rows: row 1 lit (viewers); rows 2-3 dark. No text."
NOTE[72]="Cumulative rows: rows 1-2 lit (viewers + briefcases); row 3 dark. No text. (file = old 71-state2)"
NOTE[73]="Cumulative rows: all three rows lit (+ platform buildings). No text. (file = old 71-state3)"
NOTE[32]="Hand on cheek, 'is this real?'. LIVE off. FINAL REVIEW FIX: monitor now shows shot 28's dashboard screen (blurred, unreadable number), local composite 0.00."
NOTE[33]="Phone ringing, chat bubbles. LIVE off. FINAL REVIEW FIX: monitor now shows shot 28's dashboard screen (blurred), local composite 0.00."
NOTE[34]="Deep breath, hand on the button, LIVE still OFF. FINAL REVIEW FIX: monitor now shows shot 28's dashboard screen (blurred), local composite 0.00. Base for 35."
NOTE[35]="ASSEMBLY STATE of shot 34 (own file): LIVE light flipped bright red; same fixed dashboard screen as 34."
SHOTS=sorted(MAPVO)
CUTS=[7,31,45,55]
def img(n):
    if n==27: return "section1/1.png"
    if n==57: return "section2/54.png"
    s=1 if n<=20 else 2 if n<=57 else 3 if n<=75 else 4 if n<=88 else 5 if n<=111 else 6
    return f"section{s}/{n}.png"
STATE_SHOTS={18:17,35:34,40:39,50:49,54:53}
