"""Compose a 1080x1920 extension frame.
generated 9:16 art  +  original 16:9 frame scaled to 1080x608 pasted at y=656..1263.
Seam handling (v2): translation + dense-flow registration of the generated art to the band, PER-COLUMN colour ramp at each
seam (full at the seam, ~0 at RAMP px away), and a 16 px cosine crossfade straddling each seam (8 px inside the band,
8 px outside, against the band's edge row continued outward). Band pixels deeper than 8 px from a seam are untouched."""
import cv2, numpy as np, sys
Y0,BH=656,608; Y1=Y0+BH; XF=8; RAMP=200; PROBE=6
def compose(gen_path, band_path, out_path):
    g=cv2.imread(gen_path); h0,w0=g.shape[:2]
    cw=round(h0*9/16); x0=(w0-cw)//2; g=g[:,x0:x0+cw]; g=cv2.resize(g,(1080,1920),interpolation=cv2.INTER_LANCZOS4)
    b=cv2.imread(band_path)
    gg=cv2.cvtColor(g,cv2.COLOR_BGR2GRAY); bg=cv2.cvtColor(b,cv2.COLOR_BGR2GRAY); m=12
    res=cv2.matchTemplate(gg[Y0-m:Y1+m],bg,cv2.TM_CCOEFF_NORMED); _,mx,_,loc=cv2.minMaxLoc(res); dy=loc[1]-m; dx=loc[0]
    g=cv2.warpAffine(g,np.float32([[1,0,-dx],[0,1,-dy]]),(1080,1920),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)
    gb=cv2.cvtColor(g[Y0:Y1],cv2.COLOR_BGR2GRAY)
    fl=cv2.calcOpticalFlowFarneback(bg,gb,None,0.5,6,25,6,7,1.5,0); fl=cv2.GaussianBlur(fl,(0,0),sigmaX=10,sigmaY=6)
    H=1920; flow=np.zeros((H,1080,2),np.float32); top=cv2.GaussianBlur(fl[:20].mean(0)[None],(0,0),sigmaX=8,sigmaY=0.01)[0]; bot=cv2.GaussianBlur(fl[-20:].mean(0)[None],(0,0),sigmaX=8,sigmaY=0.01)[0]
    for y in range(Y0): flow[y]=top*np.exp(-(Y0-y)/110)
    for y in range(Y1,H): flow[y]=bot*np.exp(-(y-Y1+1)/110)
    gy,gx=np.mgrid[0:H,0:1080].astype(np.float32)
    gw=cv2.remap(g,gx+flow[...,0],gy+flow[...,1],cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    bf=b.astype(np.float32)
    # per-column colour match at each seam (measured on the edge rows, light smoothing along x only)
    sm=lambda v:cv2.GaussianBlur(v[None],(0,0),sigmaX=6,sigmaY=0.01)[0]
    dtop=sm(bf[:PROBE].mean(0)-gw[Y0:Y0+PROBE].mean(0)); dbot=sm(bf[-PROBE:].mean(0)-gw[Y1-PROBE:Y1].mean(0))
    for y in range(0,Y0):   gw[y]+=dtop*(0.5*(1+np.cos(np.pi*min(1,(Y0-y)/RAMP))))
    for y in range(Y1,H):   gw[y]+=dbot*(0.5*(1+np.cos(np.pi*min(1,(y-Y1+1)/RAMP))))
    # also colour-match the generated art inside the crossfade zone so both sides of the blend agree
    out=gw.copy()
    # crossfade: reference = band edge row continued outward; weight of the reference rises 0->1 across 2*XF rows
    for k in range(2*XF):
        wref=0.5*(1-np.cos(np.pi*(k+0.5)/(2*XF)))      # 0 at the outer end -> 1 at the inner end
        y=Y0-XF+k
        ref=bf[0] if y<Y0 else bf[y-Y0]
        out[y]=(1-wref)*gw[y]+wref*ref
        y=Y1+XF-1-k
        ref=bf[-1] if y>=Y1 else bf[y-Y0]
        out[y]=(1-wref)*gw[y]+wref*ref
    out=np.clip(out,0,255).astype(np.uint8)
    out[Y0+XF:Y1-XF]=b[XF:BH-XF]          # band interior pixel-exact
    cv2.imwrite(out_path,out)
    diff=np.abs(out[Y0:Y1].astype(int)-b.astype(int)); inner=diff[XF:BH-XF].max()
    return dict(dx=int(dx),dy=int(dy),match=round(float(mx),3),inner_max_diff=int(inner),edge_max_diff=int(diff.max()))
if __name__=='__main__': print(compose(*sys.argv[1:4]))
