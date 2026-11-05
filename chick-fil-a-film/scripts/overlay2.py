import numpy as np
from PIL import Image, ImageDraw, ImageFont
from overlay import coeffs, lerp_quad
def put_text_fs(base,quad,text,uv,color,size_px,align='center',fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
    u0,v0,u1,v1=uv
    dst=[lerp_quad(quad,u0,v0),lerp_quad(quad,u1,v0),lerp_quad(quad,u1,v1),lerp_quad(quad,u0,v1)]
    w=int(max(np.hypot(*(np.array(dst[1])-dst[0])),np.hypot(*(np.array(dst[2])-dst[3]))))
    h=int(max(np.hypot(*(np.array(dst[3])-dst[0])),np.hypot(*(np.array(dst[2])-dst[1]))))
    S=3;W,H=w*S,h*S
    tile=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(tile)
    f=ImageFont.truetype(fontpath,int(size_px*S));bb=d.textbbox((0,0),text,font=f)
    tw,th=bb[2]-bb[0],bb[3]-bb[1]
    if tw>W*0.98: print('WARNING text wider than box',text,tw/W)
    x={'center':(W-tw)/2,'left':0.02*W,'right':W-tw-0.02*W}[align]
    d.text((x-bb[0],(H-th)/2-bb[1]),text,font=f,fill=color)
    c=coeffs(dst,[(0,0),(W,0),(W,H),(0,H)])
    warped=tile.transform(base.size,Image.PERSPECTIVE,c,Image.BICUBIC)
    return Image.alpha_composite(base.convert('RGBA'),warped).convert('RGB')
