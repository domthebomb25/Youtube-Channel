import cv2,numpy as np,os
C={79:(1793,554,1.0),80:(1794,576,1.05),81:(1792,597,.97),82:(1793,614,.84),83:(1785,628,.89),84:(1776,641,.91),85:(1766,652,.94),86:(1750,665,1.05),
87:(1731,672,1.1),88:(1704,685,1.2),89:(1672,693,1.32),90:(1647,709,1.44),91:(1600,712,1.52),92:(1535,708,2.26),93:(1462,697,2.39),
94:(1348,687,2.6),95:(1181,672,3.2),96:(973,620,4.2),97:(563,525,4.8)}
os.makedirs('out',exist_ok=True)
for n in range(1,98):
    im=cv2.imread(f'f{n:03d}.png')
    if n in C:
        cx,cy,s=C[n]; hw=int(16*s); up=int(14*s); dn=int(26*s)
        x0,x1,y0,y1=max(0,cx-hw),min(1920,cx+hw),max(0,cy-up),min(1080,cy+dn)
        g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        m=np.zeros(g.shape,np.uint8)
        sub=g[y0:y1,x0:x1]
        m[y0:y1,x0:x1]=((sub<115)|(sub>235)*0).astype(np.uint8)
        # also the white glyph: fill holes by closing
        k=max(3,int(3*s)|1)
        m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k)))
        # fill the white glyph inside the dark wedge: fill holes of the mask
        ff=m.copy(); h_,w_=ff.shape; mk=np.zeros((h_+2,w_+2),np.uint8)
        cnts,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c)>3*s*s: cv2.drawContours(m,[cv2.convexHull(c)],-1,1,-1)
        m=cv2.dilate(m,np.ones((max(3,int(1.5*s)|1),)*2,np.uint8))
        r=max(3,int(2*s))
        im=cv2.inpaint(im,m*255,r,cv2.INPAINT_TELEA)
    cv2.imwrite(f'out/f{n:03d}.png',im)
