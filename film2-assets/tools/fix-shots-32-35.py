# Shots 32-35 monitor fix (LOCAL composite, 0 credits): shot 28's dashboard screen perspective-warped onto the dead monitor.
# usage: python3 -I fix-shots-32-35.py <repo>/film2-assets   (reads discarded/{32..35}-original.png and section2/28.png)
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
A=sys.argv[1]
def homography(src,dst):
    M=[]
    for (x,y),(u,v) in zip(src,dst):
        M.append([x,y,1,0,0,0,-u*x,-u*y]); M.append([0,0,0,x,y,1,-v*x,-v*y])
    h=np.linalg.solve(np.array(M,float),np.array(dst,float).reshape(-1))
    return np.append(h,1).reshape(3,3)
# ---- source: shot 28's screen (inner rim quad TL,TR,BR,BL), face occluder at the left patched with the screen's own dark margin
s28=Image.open(A+"/section2/28.png").convert("RGB"); a=np.asarray(s28).copy()
a[330:745,440:500]=a[330:745,500:504].mean(1,keepdims=True)
S28=[(469,141),(1813,46),(1813,830),(1469+0,820)]; S28[3]=(469,820)
src_img=Image.fromarray(a)
# ---- destination monitor screens (inner-rim quads TL,TR,BR,BL, full-frame px; TR/BR extrapolated off-frame, see notes)
DST={32:[(1400,300),(2305,51),(2305,638),(1405,643)],
     33:[(1498,258),(2430,-52),(2430,562),(1512,600)],
     34:[(1478,302),(2257,210),(2257,670),(1486,647)]}
def vis_poly(q): return q
def composite(base,quad,inset=4):
    H=homography(quad,S28)            # dst -> src
    coef=tuple(H.flatten()[:8]/H[2,2])
    warped=src_img.transform(base.size,Image.PERSPECTIVE,coef,Image.BICUBIC)
    # mask: dst quad (supersampled), eroded by `inset` px so the monitor's rim line stays untouched, softly feathered
    m=Image.new("L",(base.width*2,base.height*2),0)
    ImageDraw.Draw(m).polygon([(x*2,y*2) for x,y in quad],fill=255)
    m=m.resize(base.size,Image.LANCZOS).filter(ImageFilter.MinFilter(inset*2+1)).filter(ImageFilter.GaussianBlur(1.2))
    mm=np.asarray(m).astype(float)/255.0
    w=np.asarray(warped).astype(float)
    # morning light: slightly lower the screen's glow, add a faint window reflection toward the upper-left corner
    w=w*0.92
    yy,xx=np.mgrid[0:base.height,0:base.width]
    x0,y0=quad[0]; refl=np.clip(1-((xx-x0)/900.0+(yy-y0)/400.0),0,1)**2*0.10
    w=w*(1-refl[...,None])+np.array([235,240,255])[None,None,:]*refl[...,None]
    b=np.asarray(base).astype(float)
    out=b*(1-mm[...,None])+w*mm[...,None]
    return Image.fromarray(np.clip(out+0.5,0,255).astype(np.uint8))
res={}
for n in (32,33,34):
    base=Image.open(A+f"/discarded/{n}-original.png").convert("RGB")
    res[n]=composite(base,DST[n]); res[n].save(A+f"/section2/{n}.png")
# shot 35 = shot 34's assembly-state file: identical composite on its own original so the ONLY difference to 34 stays the LIVE light
base35=Image.open(A+"/discarded/35-original.png").convert("RGB")
composite(base35,DST[34]).save(A+"/section2/35.png")
