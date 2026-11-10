# usage: python3 -I section4-states.py <repo>/film2-assets   (builds section4/85-state.png locally, 0 credits)
import sys, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np
A=sys.argv[1]
base=Image.open(A+"/section4/85.png").convert("RGB")
asset=Image.open(A+"/assets/stream-screen-asset-640x360.png").convert("RGB")
def persp(dst,src):
    M=[];B=[]
    for (X,Y),(x,y) in zip(dst,src):
        M.append([X,Y,1,0,0,0,-x*X,-x*Y]); B.append(x); M.append([0,0,0,X,Y,1,-y*X,-y*Y]); B.append(y)
    return np.linalg.solve(np.array(M,float),np.array(B,float)).tolist()
W,H=base.size
# 1) room lights up: warm radial glow centred on the monitor
cx,cy=1095,715
yy,xx=np.mgrid[0:H,0:W]
d=np.sqrt((xx-cx)**2+(yy-cy)**2)/1100.0
g=np.clip(1-d,0,1)**1.4
a=np.asarray(base).astype(float)
warm=np.array([255,214,120],float)
a=a*(1+0.9*g[...,None])+warm*(0.38*g[...,None])
im=Image.fromarray(np.clip(a,0,255).astype("uint8"))
# 2) light burst rays from the monitor
ray=Image.new("RGBA",(W,H),(0,0,0,0)); rd=ImageDraw.Draw(ray)
for k in range(16):
    ang=math.radians(k*22.5+6); L=1500
    p=[(cx,cy),(cx+L*math.cos(ang-0.05),cy+L*math.sin(ang-0.05)),(cx+L*math.cos(ang+0.05),cy+L*math.sin(ang+0.05))]
    rd.polygon(p,fill=(255,230,150,46))
im=Image.alpha_composite(im.convert("RGBA"),ray.filter(ImageFilter.GaussianBlur(6))).convert("RGB")
# 3) monitor comes alive: genuine stream-screen asset onto the screen quad
dst=[(1034,659),(1169,652),(1153,768),(1018,775)]
src=[(0,0),(640,0),(640,360),(0,360)]
w=asset.transform((W,H),Image.PERSPECTIVE,persp(dst,src),Image.BICUBIC)
m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon(dst,fill=255)
im=Image.composite(w,im,m)
# 4) crowd of white viewer icons flooding in (head + shoulders), back to front, never over the streamer/desk
random.seed(85)
d=ImageDraw.Draw(im)
def icon(x,y,s):
    ol=max(2,int(s*0.06)); col=(250,250,252)
    d.ellipse([x-s*0.30,y-s*0.55,x+s*0.30,y+s*0.05],fill=col,outline=(30,40,70),width=ol)
    d.pieslice([x-s*0.55,y-s*0.02,x+s*0.55,y+s*1.1],180,360,fill=col,outline=(30,40,70),width=ol)
pts=[]
for row,(ys,s) in enumerate([(420,70),(500,86),(590,104),(700,128),(830,156),(980,190),(1090,225)]):
    n=int(W/(s*0.78))+2
    for i in range(n):
        x=i*s*0.78+random.uniform(-s*0.2,s*0.2)-s*0.2+(s*0.39 if row%2 else 0)
        y=ys+random.uniform(-12,12)
        # keep the streamer, chair, desk and monitor clear
        if 790<x<1270 and 560<y<1060: continue
        pts.append((y,x,s))
for y,x,s in sorted(pts): icon(x,y,s)
im.save(A+"/section4/85-state.png")
