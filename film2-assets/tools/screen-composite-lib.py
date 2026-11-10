from PIL import Image, ImageDraw, ImageChops, ImageFilter
import numpy as np, sys
C="canon/film2-assets/section2/"
def load(n): return Image.open(C+f"{n}.png").convert("RGB")
def persp(dst,src):
    A=[];B=[]
    for (X,Y),(x,y) in zip(dst,src):
        A.append([X,Y,1,0,0,0,-x*X,-x*Y]); B.append(x); A.append([0,0,0,X,Y,1,-y*X,-y*Y]); B.append(y)
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()
def warp(img,dst,src,size=(1920,1080)):
    return img.transform(size,Image.PERSPECTIVE,persp(dst,src),Image.BICUBIC)
def polymask(poly,size=(1920,1080)):
    m=Image.new("L",size,0); ImageDraw.Draw(m).polygon(poly,fill=255); return m
def rimscan(a,x,y0,y1,thr=16):
    lum=a.mean(2); ys=[y for y in range(y0,y1) if lum[y,x]<thr]; g=[]
    for y in ys:
        if g and y-g[-1][1]<=2: g[-1][1]=y
        else: g.append([y,y])
    return g
