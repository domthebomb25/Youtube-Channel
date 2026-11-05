import numpy as np
from PIL import Image, ImageDraw, ImageFont
def coeffs(src,dst):
    A=[];B=[]
    for (x,y),(u,v) in zip(src,dst):
        A.append([x,y,1,0,0,0,-u*x,-u*y]);A.append([0,0,0,x,y,1,-v*x,-v*y]);B+= [u,v]
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()
def lerp_quad(q,u,v):
    tl,tr,br,bl=[np.array(p,float) for p in q]
    top=tl+(tr-tl)*u;bot=bl+(br-bl)*u
    return tuple(top+(bot-top)*v)
def put_text(base,quad,text,uv,color,fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',scale=4):
    u0,v0,u1,v1=uv
    dst=[lerp_quad(quad,u0,v0),lerp_quad(quad,u1,v0),lerp_quad(quad,u1,v1),lerp_quad(quad,u0,v1)]
    w=int(max(np.hypot(*(np.array(dst[1])-dst[0])),np.hypot(*(np.array(dst[2])-dst[3]))))*scale//scale
    h=int(max(np.hypot(*(np.array(dst[3])-dst[0])),np.hypot(*(np.array(dst[2])-dst[1]))))
    W,H=w*2,h*2
    tile=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(tile)
    size=H
    while True:
        f=ImageFont.truetype(fontpath,size);bb=d.textbbox((0,0),text,font=f)
        if (bb[2]-bb[0])<=W*0.98 and (bb[3]-bb[1])<=H*0.98: break
        size-=4
    d.text(((W-(bb[2]-bb[0]))/2-bb[0],(H-(bb[3]-bb[1]))/2-bb[1]),text,font=f,fill=color)
    src=[(0,0),(W,0),(W,H),(0,H)]
    c=coeffs(dst,src)  # maps output(x,y)->tile coords
    big=base.convert('RGBA')
    warped=tile.transform(big.size,Image.PERSPECTIVE,c,Image.BICUBIC)
    return Image.alpha_composite(big,warped).convert('RGB')
