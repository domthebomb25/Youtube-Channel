import numpy as np, math, cv2
from PIL import Image, ImageDraw, ImageFilter
N=121; FPS=30
fr=[Image.open(f"h6/f{i+1:03d}.png").convert("RGB") for i in range(N)]
W,H=fr[0].size
A=[np.asarray(f).astype(np.float32) for f in fr]
# ---- geometry (measured at t=0, full-res px) ----
CAN=(165,555,198,620)            # top-right window can (bbox)
WIN=(52,543,220,793)             # window interior (clip for the in-window fall)
BIN=(113,823,305,960)            # bin recess
U=(215,590,336,935)              # region where the original can fell outside the glass
T_ON, T_END = 1.93, 2.27         # fake fall start / original can handed back
# interior colour of the empty slot (sampled above the top row of cans)
interior=np.asarray(fr[0]).astype(np.float32)[535:548,140:200].reshape(-1,3).mean(0)

def feather_mask(box, r=7):
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).rectangle(box,fill=255)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(r))).astype(np.float32)[...,None]/255.0

MU=feather_mask(U)
plate_top=A[int(round(2.50*FPS))]   # no can, slot glowing
plate_bin=A[int(round(1.80*FPS))]   # empty bin
yy=np.arange(H)[:,None,None]
blend_y=np.clip((yy-700)/12.0,0,1)   # y<700: 2.5 s plate (slot glow); y>=700: 1.8 s plate (no head edge, empty bin)
plate=plate_top*(1-blend_y)+plate_bin*blend_y

# can sprite from t=0 with a rounded mask
sx0,sy0,sx1,sy1=CAN
spr=fr[0].crop((sx0-1,sy0-1,sx1+2,sy1+1)).convert("RGBA")
mk=Image.new("L",spr.size,0); ImageDraw.Draw(mk).rounded_rectangle((2,2,spr.width-3,spr.height-3),radius=9,fill=255)
spr.putalpha(mk.filter(ImageFilter.GaussianBlur(0.8)))

def paste_clipped(img, sprite, cx, cy, clip):
    s=Image.new("RGBA",(W,H),(0,0,0,0)); s.alpha_composite(sprite,(int(cx-sprite.width/2),int(cy-sprite.height/2)))
    c=Image.new("L",(W,H),0); ImageDraw.Draw(c).rectangle(clip,fill=255)
    a=np.minimum(np.asarray(s.getchannel("A")),np.asarray(c))
    s.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(s)

def sprite_pos(t):
    """returns (phase, cx, cy, angle) for the fake can."""
    d=t-T_ON
    if d<0: return None
    ay=12000.0
    top_cy=(CAN[1]+CAN[3])/2
    if d<0.17:                                   # falls inside the window, behind the glass
        return ("win", (CAN[0]+CAN[2])/2+ d*50, top_cy+0.5*ay*d*d, 8*d/0.17)
    if d<0.27: return None                       # hidden inside the machine body
    e=d-0.27                                     # drops into the bin from the top
    return ("bin", 271, 760+1320*e+0.5*9000*e*e, 40+80*e)

BINR=(113,823,305,965)
def can_mask(a):
    R,G,B=a[...,0],a[...,1],a[...,2]
    x0,y0,x1,y1=BINR
    reg=np.zeros(R.shape,bool); reg[y0:y1,x0:x1]=True
    white=(np.minimum(np.minimum(R,G),B)>195).astype(np.uint8)
    n,lab,st,_=cv2.connectedComponentsWithStats(white,connectivity=8)
    bigw=np.zeros(R.shape,bool)
    for k in range(1,n):
        if st[k,cv2.CC_STAT_AREA]>2500: bigw|=(lab==k)      # head / shirt
    head=cv2.dilate(bigw.astype(np.uint8),np.ones((13,13),np.uint8))>0
    smallw=(white>0)&~bigw                                    # the can's own white band
    body=(B>150)&(R<130)
    red=(R>170)&(G<85)&(B<100)&((R-G)>110)
    mx=np.maximum(np.maximum(R,G),B); mn=np.minimum(np.minimum(R,G),B); mean=(R+G+B)/3
    gray=((mx-mn)<48)&(mean>62)&(mean<215)                 # crumpled metal bits of the old can
    c=(body|red|smallw|gray)&reg&~head
    c=cv2.morphologyEx(c.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    c=cv2.dilate(c,np.ones((11,11),np.uint8))>0
    return c&~head&reg, head
cents=[]
for i in range(int(2.33*FPS),int(2.50*FPS)+1):
    cm0,_=can_mask(A[i])
    if cm0.sum()>250:
        ys0,xs0=np.nonzero(cm0); cents.append((xs0.mean(),ys0.mean()))
REST=(float(np.median([c[0] for c in cents])),float(np.median([c[1] for c in cents]))) if cents else (240.0,925.0)
print("rest centre",REST)
out=[]
for i in range(N):
    t=i/FPS
    a=A[i].copy()
    if 1.90<=t<T_END:
        a=a*(1-MU)+plate*MU
    img=Image.fromarray(a.clip(0,255).astype(np.uint8)).convert("RGBA")
    if t>=T_ON:                                   # the spot the can fell from stays empty
        g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).rectangle((CAN[0]-2,CAN[1]-3,CAN[2]+2,CAN[3]-3),fill=tuple(int(v) for v in interior)+(255,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(0.6)))
    p=sprite_pos(t) if t<T_END else None
    if p:
        ph,cx,cy,ang=p
        sp=spr.rotate(-ang,expand=True,resample=Image.BICUBIC)
        paste_clipped(img,sp,cx,cy, WIN if ph=="win" else (BIN[0],BIN[1],BIN[2],BIN[3]))
    if 2.27<=t<=2.93:                                  # replace the crumpled landed can with a clean one until he lifts it
        cm,hd=can_mask(A[i])
        if cm.sum()>250:
            ys,xs=np.nonzero(cm)
            cx,cy=xs.mean(),ys.mean()
            if t>=2.33: cx,cy=REST                           # keep the clean can steady while it rests
            base=np.asarray(img.convert("RGB")).astype(np.uint8).copy()
            fill=cv2.inpaint(base,(cm*255).astype(np.uint8),6,cv2.INPAINT_TELEA)
            im2=Image.fromarray(fill).convert("RGBA")
            sp=spr.resize((int(spr.width*1.25),int(spr.height*1.25)),Image.LANCZOS).rotate(-105,expand=True,resample=Image.BICUBIC)
            paste_clipped(im2,sp,cx,cy,BINR)
            # head and hands stay in front of the can
            orig=Image.fromarray(A[i].clip(0,255).astype(np.uint8)).convert("RGBA")
            hm=Image.fromarray((hd*255).astype(np.uint8))
            im2.paste(orig,(0,0),hm)
            img=im2
    out.append(img.convert("RGB"))
import os
os.makedirs("h7",exist_ok=True)
for i,f in enumerate(out): f.save(f"h7/f{i+1:03d}.png")
print("done",len(out))
