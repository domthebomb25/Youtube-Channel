# Film #2 render, step 3: BUILD the assembly-state frames that have no file in the repo (shot 9 counter flips, shot 10 alert flip).
# Local edit only: number/banner area repainted in the screen colour, new text composed from the ORIGINAL glyphs (shot 9 / shot 10 own pixels;
# the "5" comes from shot 17's counter, same condensed bold counter style). Everything outside the edited area is byte-identical.
# usage: python3 -I 02_states.py <repo>/film2-assets
import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
A=sys.argv[1]; OUT=A+"/render/states/"
def blur(a,r): return np.asarray(Image.fromarray(np.clip(a*255,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(float)/255
def dilate(mask,r):   # square dilation by an integral image (PIL's big MaxFilter crashes on this box)
    m=mask.astype(np.int32); H,W=m.shape
    ii=np.zeros((H+1,W+1),np.int64); ii[1:,1:]=m.cumsum(0).cumsum(1)
    y0=np.clip(np.arange(H)-r,0,H); y1=np.clip(np.arange(H)+r+1,0,H); x0=np.clip(np.arange(W)-r,0,W); x1=np.clip(np.arange(W)+r+1,0,W)
    s=ii[y1][:,x1]-ii[y0][:,x1]-ii[y1][:,x0]+ii[y0][:,x0]
    return s>0
def fit_bg(im,mask,ring,deg=2):
    H,W,_=im.shape; yy,xx=np.mgrid[0:H,0:W]
    def F(x,y):
        x=(x-W/2)/W; y=(y-H/2)/H
        return np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],-1)
    sel=ring&~mask; Fs=F(xx[sel].astype(float),yy[sel].astype(float)); Fa=F(xx.astype(float),yy.astype(float))
    out=np.zeros_like(im)
    for c in range(3):
        coef,*_=np.linalg.lstsq(Fs,im[...,c][sel],rcond=None); out[...,c]=Fa@coef
    return out
def inpaint(im,mask,usable=None):
    valid=((~mask) if usable is None else (usable&~mask)).astype(float); out=im.copy(); done=~mask
    for sg in (8,16,32,64,128):
        w=blur(valid,sg); sel=(~done)&(w>0.04)
        for c in range(3):
            e=blur(im[...,c]/255.0*valid,sg)/np.maximum(w,1e-9)*255.0
            out[...,c][sel]=e[sel]
        done=done|sel
    # smooth only inside the hole
    sm=np.stack([blur(out[...,c]/255.0,5)*255.0 for c in range(3)],-1)
    out[mask]=sm[mask]
    return out
def alpha_from(im,bg):  # white-on-bg alpha incl. glow, using the green channel
    g=im[...,1]; b=bg[...,1]; return np.clip((g-b)/(255-b+1e-6),0,1)
def soft(a,t=0.05): return np.clip((a-t)/(1-t),0,1)
# =====================================================================  SHOT 9  (counter 10,000 -> 50,000 -> 100,000)
im9=np.asarray(Image.open(A+"/section1/9.png").convert("RGB")).astype(float); H,W,_=im9.shape
core=(im9.min(2)>225); reg=np.zeros((H,W),bool); reg[360:560,1400:1880]=True
glyph_cols=[(1446,1488),(1501,1564),(1575,1596),(1603,1669),(1678,1748),(1757,1830)]   # 1 0 , 0 0 0 (measured)
M=np.zeros((H,W),bool); M[372:592,1385:1896]=True; M[346:372,1670:1896]=True                  # the number box (glyph cores 1446-1830 x 360-532 + their glow)
bg9=inpaint(im9,M)
A0=soft(alpha_from(im9,bg9))*reg                                   # alpha of the original "10,000" (cores + glow) in the number box
A0[~dilate(M,2)]=0
def shift(a,dx,dy):
    return np.asarray(Image.fromarray((a*255).astype(np.uint8)).transform((a.shape[1],a.shape[0]),Image.AFFINE,(1,0,-dx,0,1,-dy),Image.BICUBIC)).astype(float)/255
def build9(kind):
    N=np.zeros((H,W))
    if kind=="100000":
        cut1=1494; cut2=1570                   # cut lines in the gaps: after "1" and after first "0"
        L=A0.copy(); L[:,cut2:]=0                                  # "10"
        P=np.zeros_like(A0); P[:,cut1:cut2]=A0[:,cut1:cut2]        # a copy of the first "0" (+gap)
        Rr=A0.copy(); Rr[:,:cut2]=0                                # ", 0 0 0"
        adv=cut2-cut1
        N=np.maximum.reduce([L,shift(P,adv,-6),shift(Rr,adv,-7)])
        N=shift(N,-adv/2,+adv*0.09/2)                              # recentre on the original number's centre
    else:  # 50,000: swap the "1" for a "5" taken from shot 17
        s17=np.asarray(Image.open(A+"/section1/17.png").convert("RGB")).astype(float)
        r17=np.zeros(s17.shape[:2],bool); r17[300:720,1300:1920]=True
        c17=(s17.min(2)>225)&r17; cols=c17.any(0); runs=[];s=None
        for x,v in enumerate(cols):
            if v and s is None: s=x
            if (not v) and s is not None: runs.append((s,x-1)); s=None
        # glyph order 9 5 0 , 0 0 0 -> second run is the "5"
        a5,b5=runs[1]
        ys=np.where(c17[:,a5:b5+1].any(1))[0]; y0,y1=ys.min(),ys.max()
        bgp=np.median(s17[330:380,1420:1470].reshape(-1,3),0)
        g=s17[...,1]; al=np.clip((g-bgp[1])/(255-bgp[1]),0,1)
        pad=22
        hard=np.zeros(al.shape); hard[y0-3:y1+4,a5-3:b5+4]=al[y0-3:y1+4,a5-3:b5+4]; hard=(hard>0.55)*hard
        hard=hard[y0-pad:y1+pad+1,a5-pad:b5+pad+1]
        patch=np.maximum(hard,blur(hard,6)*0.55)
        # keep only this glyph: zero the columns outside the core extent +glow so neighbours don't leak
        h5=y1-y0+1; target=121.0; sc=target/h5
        pim=Image.fromarray((patch*255).astype(np.uint8)); pim=pim.resize((int(patch.shape[1]*sc),int(patch.shape[0]*sc)),Image.LANCZOS)
        pim=pim.rotate(-2,resample=Image.BICUBIC,expand=True)
        p5=np.asarray(pim).astype(float)/255; w5=(b5-a5+1)*sc
        # place: left core edge at x=1446, core bottom at y~516
        px=int(1446-pad*sc); py=int(516-(h5*sc)-pad*sc+ (0))
        canvas=np.zeros_like(A0); hh,ww=p5.shape
        canvas[py:py+hh,px:px+ww]=np.maximum(canvas[py:py+hh,px:px+ww],p5[:min(hh,H-py),:min(ww,W-px)])
        cut=1494; Rr=A0.copy(); Rr[:,:cut]=0
        newleft=1446+w5; delta=(newleft+13)-1501
        N=np.maximum(canvas,shift(Rr,delta,-delta*0.09))
        N=shift(N,-delta/2,+delta*0.09/2)
    return N
def apply9(N,name):
    a=np.clip(N,0,1)
    comp=bg9*(1-a[...,None])+255*a[...,None]
    m=blur(M.astype(float),2.5); m[M]=1
    out=im9*(1-m[...,None])+comp*m[...,None]
    Image.fromarray(np.clip(out+0.5,0,255).astype(np.uint8)).save(OUT+name)
apply9(build9("50000"),"09-50000.png"); apply9(build9("100000"),"09-100000.png")
print("shot 9 states written")
# =====================================================================  SHOT 10  (banner "100 GIFTED SUBS" -> "1,000 GIFTED SUBS")
im10=np.asarray(Image.open(A+"/section1/10.png").convert("RGB")).astype(float)
box=np.zeros((H,W),bool); box[280:466,1572:1892]=True
core10=(im10.min(2)>225)&box
redish=((im10[...,0]>190)&(im10[...,1]<150)&(im10[...,2]<140))
M10=dilate(core10,25)&(redish|dilate(core10,4)); M10[:,1872:]=False
deep=((im10[...,0]>200)&(im10[...,1]<85)&(im10[...,2]<85))&(np.arange(W)[None,:]>1566)&(np.arange(W)[None,:]<1895)&(np.arange(H)[:,None]>262)&(np.arange(H)[:,None]<480)
bg10=fit_bg(im10,M10,deep)           # smooth quadratic surface through the banner's deep-red pixels (ignores halos/highlights)
A10=soft(alpha_from(im10,bg10))*dilate(core10,7)*M10
def rot(a,ang,center):
    return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).rotate(ang,resample=Image.BICUBIC,center=center)).astype(float)/255
cx,cy=1735.0,375.0
TH=9.6                                  # banner tilt (deg CCW), measured from the levelled text (see lev preview)
AL=rot(A10,-TH,(cx,cy)); CL=rot(core10.astype(float),-TH,(cx,cy))>0.5
rowp=CL.sum(1); rows=np.where(rowp>2)[0]
gaps=np.diff(rows); k=int(np.argmax(gaps)); l1=(int(rows[0]),int(rows[k])); l2=(int(rows[k+1]),int(rows[-1]))
print("text line rows (levelled):",l1,l2)
def shear(a,k,yc):   # x' = x + k*(y-yc)  (k>0 : top moves right)  -> use to remove / re-apply the italic slant
    return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).transform((a.shape[1],a.shape[0]),Image.AFFINE,(1,-k,k*yc,0,1,0),Image.BICUBIC)).astype(float)/255
yc=(l1[0]+l1[1])/2.0
bestk=None
for kk in np.arange(0.0,0.45,0.02):
    sc=shear(CL.astype(float),kk,yc)[l1[0]:l1[1]+1].sum(0); v=(sc**2).sum()
    if bestk is None or v>bestk[0]: bestk=(v,kk)
KS=bestk[1]; print("italic shear k:",round(KS,2))
def runs_of(mask1d):
    out=[];s_=None
    for x,v in enumerate(mask1d):
        if v and s_ is None: s_=x
        if (not v) and s_ is not None: out.append((s_,x-1)); s_=None
    if s_ is not None: out.append((s_,len(mask1d)-1))
    return out
ALd=shear(AL,KS,yc); CLd=shear(CL.astype(float),KS,yc)>0.5
cols1=runs_of(CLd[l1[0]:l1[1]+1].any(0))
print("line-1 glyph runs (deslanted):",cols1)
# ---- compose "1,000 GIFTED" (line 1) + untouched "SUBS" (line 2) in the levelled/deslanted space, then restore tilt and slant
x1=1570; cA=1602; cZ1=1635; cZ2=1669; cSp=1681; xE=1872
def band(a,x0,x1_,rr): 
    o=np.zeros_like(a); o[rr[0]-8:rr[1]+9,x0:x1_]=a[rr[0]-8:rr[1]+9,x0:x1_]; return o
pieces=[("A",band(ALd,x1,cA,l1),cA-x1)]
# comma, drawn at 4x then reduced: round head + short tail, stroke ~ the digit stroke
base=l1[1]; hgt=l1[1]-l1[0]; cw=18
SS=4; cim=Image.new("L",(cw*SS,(hgt+30)*SS),0); d=ImageDraw.Draw(cim)
bx=cw*SS//2; by=(base-l1[0]+8)*SS     # baseline in patch coords
r=6.4*SS
d.ellipse([bx-r,by-2*r-0.0*SS,bx+r,by-0.0*SS],fill=255)
d.polygon([(bx+r*0.95,by-r*1.2),(bx+r*0.95,by+1*SS),(bx-r*1.3,by+14*SS),(bx-r*0.2,by+14*SS),(bx-r*0.6,by-1*SS)],fill=255)
cim=cim.resize((cw,hgt+30),Image.LANCZOS)
comma=np.zeros_like(ALd); comma[l1[0]-8:l1[0]-8+hgt+30,0:cw]=np.asarray(cim).astype(float)/255
comma=np.maximum(comma,blur(comma,1.2)*0.5)
pieces.append(("comma",comma,cw))
Z1=band(ALd,cA,cZ1,l1); Z2=band(ALd,cZ1,cZ2,l1)
pieces+= [("Z1",Z1,cZ1-cA),("Z2",Z2,cZ2-cZ1),("Z1b",Z1,cZ1-cA)]
pieces.append(("rest",band(ALd,cZ2,xE,l1),xE-cZ2))
# lay the pieces edge to edge on a canvas, left edge at x1
N1=np.zeros_like(ALd); x=x1-60; srcx={"A":x1,"comma":0,"Z1":cA,"Z2":cZ1,"Z1b":cA,"rest":cZ2}
for name,arr,w in pieces:
    sx=srcx[name]; seg=arr[:,sx:sx+w]
    N1[:,x:x+w]=np.maximum(N1[:,x:x+w],seg); x+=w
newlen=x-(x1-60); oldlen=xE-x1
# horizontal extent of the visible text (old / new) to centre + fit
def extent(a): 
    cols=np.where((a[l1[0]:l1[1]+1]>0.5).any(0))[0]; return cols.min(),cols.max()
o0,o1=extent(band(ALd,x1,xE,l1)); n0,n1=extent(N1)
oldw=o1-o0+1; neww=n1-n0+1; ocx=(o0+o1)/2.0
sfit=min(1.0,(oldw+22)/neww); print("line 1 width old/new",oldw,neww,"-> scale",round(sfit,3))
ncx=(n0+n1)/2.0; yc1=(l1[0]+l1[1])/2.0
Hh,Ww=ALd.shape
def affine_scale_shift(a,s,cx_src,cy,cx_dst):
    # dst(x,y) = src((x-cx_dst)/s+cx_src, (y-cy)/s+cy)
    return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).transform((Ww,Hh),Image.AFFINE,(1/s,0,cx_src-cx_dst/s,0,1/s,cy-cy/s),Image.BICUBIC)).astype(float)/255
N1s=affine_scale_shift(N1,sfit,ncx,yc1,ocx)
L2=band(ALd,x1,xE,l2)
FL=np.maximum(N1s,L2)
FL=shear(FL,-KS,yc)               # restore the italic slant
FL=rot(FL,+TH,(cx,cy))            # restore the banner tilt
a10=np.clip(FL,0,1)
comp10=bg10*(1-a10[...,None])+255*a10[...,None]
m10=blur(M10.astype(float),2.5); m10[M10]=1
out10=im10*(1-m10[...,None])+comp10*m10[...,None]
Image.fromarray(np.clip(out10+0.5,0,255).astype(np.uint8)).save(OUT+"10-1000.png")
print("shot 10 state written")
