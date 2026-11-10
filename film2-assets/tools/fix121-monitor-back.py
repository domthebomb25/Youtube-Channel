# Section 6 fix: shot 121 monitor panel -> plain dark monitor back (local edit, 0 credits).
# usage: python3 -I fix121-monitor-back.py <repo>/film2-assets   (reads discarded/121-original.png, writes section6/121.png)
# Fill = the panel's own measured colours: clean bottom strip colour (flat dark slate) blended up toward the
# clean top-strip colour per column (window glare), smooth only; edges feathered into the untouched original.
import sys, numpy as np
from PIL import Image, ImageFilter
A=sys.argv[1]
src=np.asarray(Image.open(A+"/discarded/121-original.png").convert("RGB")).astype(np.float64)
H,W,_=src.shape
X0,Y0,X1,Y1=1380,330,W,699
box=np.zeros((H,W),bool); box[Y0:Y1,X0:X1]=True
box[Y1:709,X0:1692]=True            # thin remnant under the preview, left of the stand
B=src[715:790,1400:1680].reshape(-1,3).mean(0)             # clean bottom plastic colour
T=src[300:325,:,:].mean(0)                                  # clean top strip per column
k=np.exp(-0.5*(np.arange(-75,76)/25.0)**2); k/=k.sum()
Tp=np.pad(T,((75,75),(0,0)),mode='edge')
T=np.stack([np.convolve(Tp[:,c],k,mode='valid') for c in range(3)],1)
yy,xx=np.mgrid[0:H,0:W]
w=np.clip(1-(yy-310)/330.0,0,1)**2.2
fill=B[None,None,:]+(T[None,:,:]-B[None,None,:])*w[...,None]
fill[:, :1400]=fill[:,1400:1401]   # stable at the left edge
# feathered mask: full inside the box, ramps to 0 over ~10 px outside
d=Image.fromarray((box*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))
m=np.maximum(np.asarray(d).astype(float)/255.0*2.0,0); m=np.clip(m,0,1); m[box]=1.0
out=src*(1-m[...,None])+fill*m[...,None]
Image.fromarray(np.clip(out+0.5,0,255).astype(np.uint8)).save(A+"/section6/121.png")
