import json,sys,os,re
from PIL import Image, ImageDraw, ImageFont
n=int(sys.argv[1]);flags=sys.argv[2:]
cells=json.load(open('data/cells_v2.json'));total=13
def _range(n):
    if n<=7: return (n-1)*10,n*10
    if n==8: return 70,78
    a=78+(n-9)*10;return a,a+10
byid={c['id']:c for c in cells};sel=[byid[i] for i in ['023R', '095', '093', '093B', '041R', '094', '095B', '096', '097']]
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fl=ImageFont.truetype(FB,26);fc=ImageFont.truetype(F,27);ft=ImageFont.truetype(FB,40);fs=ImageFont.truetype(F,22)
CW,CH=840,473;MARGIN=40;GUT=40;CAPH=190;LABH=44;ROWH=LABH+CH+CAPH+26
W=MARGIN*2+CW*2+GUT
def wrap(d,text,font,maxw):
    out=[];cur=''
    for w in text.split(' '):
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: out.append(cur);cur=w
    out.append(cur);return out
probe=ImageDraw.Draw(Image.new('RGB',(10,10)))
flag_lines=[]
for f in flags: flag_lines+=wrap(probe,'FLAG · '+f,fs,W-2*MARGIN)
rows=-(-len(sel)//2)
H=100+rows*ROWH+(40+len(flag_lines)*30 if flag_lines else 0)+30
page=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(page)
d.text((MARGIN,28),f"Chick-fil-A Film · Storyboard v2 · Sheet {n:02d} of {total} · CF-{sel[0]['id']} to CF-{sel[-1]['id']}",font=ft,fill=(20,20,20))
for i,c in enumerate(sel):
    x=MARGIN+(i%2)*(CW+GUT);y=100+(i//2)*ROWH;sid=c['id']
    if c['kind']=='GEN':
        iid=c.get('img',sid);img=Image.open(f'images/CF-{iid}.jpg')
        lab=c['label'] if 'label' in c else (f"CF-{sid} · GEN" if iid==sid else (f"CF-{sid} line · NEW image (option A)" if iid=='NEW029' else f"CF-{sid} line · image CF-{iid}"))
        zl=c['zoom'] if 'zoom' in c else [k['id'] for k in c['crops']]
        if zl: lab+=" · zoom: "+", ".join('CF-'+z for z in zl)
    else:
        e=f'shots/CF-{sid}-edit.png';img=Image.open(e if os.path.exists(e) else f"shots/CF-{c['base']}.png")
        ovt=c['overlay'];lab=f"CF-{sid} · EDIT STATE (base CF-{c['base']})"
        if c['crops']: lab+=" · zoom: "+", ".join('CF-'+k['id'] for k in c['crops'])
    img=img.convert('RGB').resize((CW,CH),Image.LANCZOS)
    d.rectangle((x-2,y-2,x+CW+2,y+LABH+CH+CAPH),outline=(190,190,190))
    d.rectangle((x,y,x+CW,y+LABH-4),fill=(235,235,235))
    lf=fl
    while d.textlength(lab,font=lf)>CW-16: lf=ImageFont.truetype(FB,lf.size-2)
    d.text((x+10,y+7),lab,font=lf,fill=(150,30,30) if c['kind']=='EDIT' else (20,20,20))
    page.paste(img,(x,y+LABH))
    ty=y+LABH+CH+10
    for ln in wrap(d,c['caption'],fc,CW-20)[:4]: d.text((x+10,ty),ln,font=fc,fill=(0,0,0));ty+=32
    if c['kind']=='EDIT' and c['overlay']:
        for ln in wrap(d,'OVERLAY (edit): '+c['overlay'],fs,CW-20)[:2]: d.text((x+10,ty),ln,font=fs,fill=(150,30,30));ty+=26
fy=100+rows*ROWH+10
for ln in flag_lines: d.text((MARGIN,fy),ln,font=fs,fill=(160,30,30));fy+=30
os.makedirs('sheets_new',exist_ok=True)
page.save(f'sheets_new/storyboard-v2-sheet-{n:02d}.png');page.save(f'sheets_new/storyboard-v2-sheet-{n:02d}.pdf',resolution=150)
print(page.size,[c['id'] for c in sel])
