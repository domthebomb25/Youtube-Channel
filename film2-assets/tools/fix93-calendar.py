# Shot 93 local edit (0 credits): move Ninja's two red X marks to TWO CONSECUTIVE squares (same row, side by side).
# Steps: (1) mask the two original X's (red pixels), fill from the surrounding cell colour (grid lines untouched),
# (2) paste the same X sprite (cut from the original X) onto two adjacent squares. Everything else byte-identical.
# usage: python3 -I fix93-calendar.py <repo>/film2-assets
import sys, numpy as np
from PIL import Image, ImageFilter
A=sys.argv[1]
src=Image.open(A+"/discarded/93-original.png").convert("RGB")
a=np.asarray(src).astype(np.int32)
R,G,B=a[...,0],a[...,1],a[...,2]
red=(R-(G+B)//2)
# search window = calendar area only
win=np.zeros(R.shape,bool); win[100:560,1230:1710]=True
core=(red>60)&win
m=Image.fromarray((core*255).astype(np.uint8))
mask=np.asarray(m.filter(ImageFilter.MaxFilter(9)))>0     # dilate ~4px to cover antialiasing
ring=np.asarray(m.filter(ImageFilter.MaxFilter(41)))>0
ring=ring & ~(np.asarray(m.filter(ImageFilter.MaxFilter(21)))>0)
out=a.copy()
ys,xs=np.nonzero(core)
groups=[xs<1480, xs>=1480]
sprites=[]
for g in groups:
    y0,y1,x0,x1=ys[g].min()-6,ys[g].max()+7,xs[g].min()-6,xs[g].max()+7
    sprites.append((x0,y0,x1,y1))
    # fill every masked pixel by linear interpolation along its row between the nearest clean pixels left/right
    # (inside the same square: the horizontal margin to the grid lines is larger than the mask)
    for y in range(y0,y1):
        row=mask[y,x0:x1]
        x=0
        while x<len(row):
            if row[x]:
                xa=x
                while x<len(row) and row[x]: x+=1
                xb=x-1
                L=a[y,x0+xa-3:x0+xa-1].mean(0); Rr=a[y,x0+xb+2:x0+xb+4].mean(0)
                n=xb-xa+1
                for i in range(n):
                    t=(i+1)/(n+1)
                    out[y,x0+xa+i]=np.round(L*(1-t)+Rr*t)
            else: x+=1
# sprite = the upper-right X (x>=1480): colour + alpha from original pixels
sx0,sy0,sx1,sy1=sprites[1]
spr=a[sy0:sy1,sx0:sx1]; alpha=np.clip((spr[...,0]-(spr[...,1]+spr[...,2])//2)/150.0,0,1)
alpha[alpha<0.05]=0
h,w=alpha.shape
cx,cy=(sx0+sx1)//2,(sy0+sy1)//2
# target centres: row 3, columns 3 and 4 (two side-by-side squares)
targets=[(1405,357),(1473,353)]
for tx,ty in targets:
    x0,y0=tx-w//2,ty-h//2
    reg=out[y0:y0+h,x0:x0+w].astype(float)
    out[y0:y0+h,x0:x0+w]=(reg*(1-alpha[...,None])+spr*alpha[...,None]).round().astype(np.int32)
Image.fromarray(out.astype(np.uint8)).save(A+"/section5/93.png")
print("sprite",sprites,"targets",targets)
