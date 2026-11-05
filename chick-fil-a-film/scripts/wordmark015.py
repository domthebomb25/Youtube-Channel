import numpy as np
from PIL import Image, ImageDraw, ImageFont
wm=Image.open('wordmark_alpha_clean.png').convert('L')
def coeffs(src,dst):
    A=[];B=[]
    for (x,y),(u,v) in zip(src,dst):
        A.append([x,y,1,0,0,0,-u*x,-u*y]);A.append([0,0,0,x,y,1,-v*x,-v*y]);B+=[u,v]
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()
def lerp(q,u,v):
    tl,tr,br,bl=[np.array(p,float) for p in q];top=tl+(tr-tl)*u;bot=bl+(br-bl)*u;return tuple(top+(bot-top)*v)
def place(base,quad,opacity=1.0,fill=0.84):
    tl,tr,br,bl=[np.array(p,float) for p in quad]
    pw=(np.linalg.norm(tr-tl)+np.linalg.norm(br-bl))/2;ph=(np.linalg.norm(bl-tl)+np.linalg.norm(br-tr))/2
    wpx=pw*fill;hpx=wpx*wm.height/wm.width
    if hpx>ph*0.8: hpx=ph*0.8;wpx=hpx*wm.width/wm.height
    u0=(1-wpx/pw)/2;u1=1-u0;v0=(1-hpx/ph)/2;v1=1-v0
    dst=[lerp(quad,u0,v0),lerp(quad,u1,v0),lerp(quad,u1,v1),lerp(quad,u0,v1)]
    W,H=wm.size
    c=coeffs(dst,[(0,0),(W,0),(W,H),(0,H)])
    layer=wm.transform(base.size,Image.PERSPECTIVE,c,Image.BICUBIC)
    if opacity<1: layer=layer.point(lambda p:int(p*opacity))
    return Image.composite(Image.new('RGB',base.size,(255,255,255)),base,layer)
base=Image.open('shots_orig/CF-015.png').convert('RGB')
quads=[
 ([(1168,531),(1590,531),(1590,672),(1168,672)],1.0),
 ([(1790,585),(2030,610),(2035,718),(1792,698)],0.97),
 ([(2178,650),(2340,668),(2345,758),(2182,742)],0.95),
 ([(2427,707),(2540,720),(2543,785),(2430,772)],0.93),
 ([(252,688),(398,665),(400,755),(255,770)],0.97),
 ([(85,738),(192,720),(195,790),(88,802)],0.93),
]
out=base
for q,o in quads: out=place(out,q,o)
out.save('CF-015-signed-noX.png')
# re-apply 2X
import sys;sys.path.insert(0,'.')
from overlay import put_text
out=put_text(out,[(1165,238),(1590,238),(1590,375),(1165,375)],'2X',(0.2,0.12,0.8,0.88),(40,40,40,255))
out.save('shots/CF-015.png')
