import sys,json,os
from PIL import Image, ImageDraw, ImageFont
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def wrap(d,text,font,maxw):
    out=[];cur=''
    for w in text.split(' '):
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: out.append(cur);cur=w
    out.append(cur);return out
def card(img_path,label,caption,out):
    W=1600;im=Image.open(img_path).convert('RGB');h=int(im.height*W/im.width);im=im.resize((W,h),Image.LANCZOS)
    probe=ImageDraw.Draw(Image.new('RGB',(10,10)))
    fl=ImageFont.truetype(FB,40);fc=ImageFont.truetype(F,44);fs=ImageFont.truetype(FB,30)
    lines=wrap(probe,caption,fc,W-80)
    H=70+h+60+len(lines)*58+40
    c=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(c)
    d.rectangle((0,0,W,64),fill=(235,235,235));d.text((24,12),label,font=fl,fill=(20,20,20))
    c.paste(im,(0,70))
    y=70+h+14
    d.text((24,y),'SAID WHILE THIS SHOT IS ON SCREEN:',font=fs,fill=(150,30,30));y+=48
    for ln in lines: d.text((40,y),ln,font=fc,fill=(0,0,0));y+=58
    c.save(out);return out
if __name__=='__main__':
    cells=json.load(open('cells_opts8.json'))
    os.makedirs('review',exist_ok=True)
    for c in cells[:2]:
        o=c['label'];card(f"opts8/CF-{c['img']}.png",f"{o}   (sheet 8 of 13)",c['caption'].strip('"'),f"review/{c['img']}.png");print(c['img'])
