import cv2, numpy as np, sys
Y0,BH=656,608
def compose(gen_path, band_path, out_path, decay=220, probe=48):
    g=cv2.imread(gen_path); h0,w0=g.shape[:2]
    cw=round(h0*9/16); x0=(w0-cw)//2; g=g[:,x0:x0+cw]; g=cv2.resize(g,(1080,1920),interpolation=cv2.INTER_LANCZOS4)
    b=cv2.imread(band_path)
    # 1. global registration of generated canvas to the placed band (translation only, +-12 px)
    gg=cv2.cvtColor(g,cv2.COLOR_BGR2GRAY); bg=cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
    m=12; res=cv2.matchTemplate(gg[Y0-m:Y0+BH+m],bg[m:BH-m] if False else bg,cv2.TM_CCOEFF_NORMED)
    _,mx,_,loc=cv2.minMaxLoc(res); dy=loc[1]-m; dx=loc[0]
    M=np.float32([[1,0,-dx],[0,1,-dy]]); g=cv2.warpAffine(g,M,(1080,1920),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)
    # 2. dense flow orig -> generated within the band
    gb=g[Y0:Y0+BH]
    fl=cv2.calcOpticalFlowFarneback(cv2.cvtColor(b,cv2.COLOR_BGR2GRAY),cv2.cvtColor(gb,cv2.COLOR_BGR2GRAY),None,0.5,5,41,5,7,1.5,0)
    fl=cv2.GaussianBlur(fl,(0,0),25)
    # seam flow = flow at the edge rows, extended outward with decay
    H=1920; flow=np.zeros((H,1080,2),np.float32)
    top=fl[0:probe].mean(axis=0); bot=fl[BH-probe:BH].mean(axis=0)
    for y in range(0,Y0):
        w=np.exp(-(Y0-y)/decay); flow[y]=top*w
    for y in range(Y0+BH,H):
        w=np.exp(-(y-(Y0+BH-1))/decay); flow[y]=bot*w
    gy,gx=np.mgrid[0:H,0:1080].astype(np.float32)
    gw=cv2.remap(g,gx+flow[...,0],gy+flow[...,1],cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)
    # 3. low-frequency colour match at the seams
    gwb=gw[Y0:Y0+BH].astype(np.float32); bf=b.astype(np.float32)
    dtop=(bf[0:probe].mean(0)-gwb[0:probe].mean(0)); dbot=(bf[BH-probe:].mean(0)-gwb[BH-probe:].mean(0))
    dtop=cv2.GaussianBlur(dtop[None],(0,0),30)[0]; dbot=cv2.GaussianBlur(dbot[None],(0,0),30)[0]
    out=gw.astype(np.float32)
    for y in range(0,Y0): out[y]+=dtop*np.exp(-(Y0-y)/decay)
    for y in range(Y0+BH,H): out[y]+=dbot*np.exp(-(y-(Y0+BH-1))/decay)
    out=np.clip(out,0,255).astype(np.uint8)
    # 4. paste the pixel-exact original over the centre band
    out[Y0:Y0+BH]=b
    cv2.imwrite(out_path,out); return dx,dy,mx
if __name__=='__main__': print(compose(*sys.argv[1:4]))
