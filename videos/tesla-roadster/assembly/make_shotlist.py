import sys
from shots import SHOTS, END, HOOK
def ts(t):
    t=t+HOOK; return f"{int(t//60)}:{t%60:04.1f}"
rows=[]
n=len(SHOTS)
for i,(t,vo,img,txt) in enumerate(SHOTS):
    e=SHOTS[i+1][0] if i+1<n else END
    rows.append((i+1,f"{ts(t)}-{ts(e)}",f"{e-t:.1f}s",vo,img,txt))
# markdown
md=["# Tesla Roadster — shot list (DRAFT for approval)","",
"Video time = narration time + 2.6 s (hook file plays first). 16:9, stickman style, 100 generated images + 1 free hook freeze-frame.",
"On-screen text is drawn by the renderer, never by the image model. No logos, badges or readable text inside images.","",
"| # | Video time | Len | Narration | Image idea | On-screen text |","|---|---|---|---|---|---|"]
for r in rows: md.append("| "+" | ".join(str(x).replace("|","/") for x in r)+" |")
open("../SHOTLIST.md","w",encoding="utf-8").write("\n".join(md)+"\n")
# pdf
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from xml.sax.saxutils import escape
out=sys.argv[1]
b="Helvetica"
P=ParagraphStyle("P",fontName=b,fontSize=7.6,leading=9.2)
H=ParagraphStyle("H",fontName=b+"-Bold",fontSize=7.8,leading=9.5,textColor=colors.white)
T=ParagraphStyle("T",fontName=b+"-Bold",fontSize=15,leading=18)
S=ParagraphStyle("S",fontName=b,fontSize=8.5,leading=11,textColor=colors.HexColor("#444444"))
data=[[Paragraph(h,H) for h in ("#","Video time","Len","Narration","Image idea","On-screen text")]]
for r in rows: data.append([Paragraph(escape(str(x)),P) for x in r])
tbl=Table(data,colWidths=[0.3*inch,1.05*inch,0.4*inch,2.35*inch,3.9*inch,1.9*inch],repeatRows=1)
st=[("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1a3c8f")),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("GRID",(0,0),(-1,-1),0.25,colors.HexColor("#bbbbbb")),("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2)]
for i in range(2,len(data),2): st.append(("BACKGROUND",(0,i),(-1,i),colors.HexColor("#f3f6ff")))
tbl.setStyle(TableStyle(st))
def foot(c,d):
    c.setFont(b,7); c.setFillColor(colors.grey)
    c.drawString(0.5*inch,0.3*inch,"Tesla Roadster shot list - draft"); c.drawRightString(landscape(letter)[0]-0.5*inch,0.3*inch,f"Page {d.page}")
doc=SimpleDocTemplate(out,pagesize=landscape(letter),leftMargin=0.5*inch,rightMargin=0.5*inch,topMargin=0.5*inch,bottomMargin=0.55*inch,title="Tesla Roadster shot list")
doc.build([Paragraph("Tesla Roadster - shot list (draft for approval)",T),
  Paragraph("Video time = narration time + 2.6 s (your hook plays first). 16:9, stickman style. 100 generated images + the free hook freeze-frame (shot 1). On-screen text is drawn by the renderer, not the image model.",S),Spacer(1,6),tbl],onFirstPage=foot,onLaterPages=foot)
