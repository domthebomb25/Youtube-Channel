import sys,json,subprocess,random,math,time
from PIL import Image,ImageDraw,ImageFilter,ImageEnhance
sys.path.insert(0,'/home/user/Youtube-Channel/videos/costco-hot-dog/shorts')
import make_short as m
SC='/tmp/claude-0/-home-user-Youtube-Channel/106344fc-a6df-5727-8e9a-6202357a4618/scratchpad'
IM='/home/user/Youtube-Channel/videos/costco-hot-dog/images/'
W,H,FPS=1080,1920,30
BAND_H=607;BAND_Y=(H-BAND_H)//2
CAP_Y=1556
YEL,WHITE=m.YEL,m.WHITE
# ---------- timing
words=json.load(open('word_timing.json'))
AUD_LEN=28.76;GAPMAX=0.45
removed=[]
for k in range(1,len(words)):
    g=words[k][1]-words[k-1][2]
    if g>GAPMAX: removed.append((words[k-1][2]+GAPMAX/2,words[k][1]-GAPMAX/2))
def f(t):
    r=0.0
    for a,b in removed:
        if t>=b: r+=b-a
        elif t>a: r+=t-a
    return t-r
segs=[];cur=0.0
for a,b in removed: segs.append((cur,a));cur=b
segs.append((cur,AUD_LEN))
TOTAL=f(AUD_LEN);print('total',round(TOTAL,2))
# ---------- audio: compressed narration + quiet chickens
fc=''.join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{i}];" for i,(a,b) in enumerate(segs))
fc+=''.join(f"[s{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=0:a=1[n];[1:a]volume=0.16[c];[n][c]amix=inputs=2:duration=first:normalize=0,atrim=0:{TOTAL:.3f}[o]"
subprocess.run(['ffmpeg','-y','-v','error','-i','narr.mp3','-i','chickens_full.wav','-filter_complex',fc,'-map','[o]','final_audio.wav'],check=True)
# ---------- shots (orig start times)
def wstart(name,nth=0):
    c=[w for w in words if w[0]==name];return c[nth][1]
SHOTS=[ # (orig start, kind, image, motion)
 (0.0,'hook',None,None),
 (wstart("costco's"),'band','e132.png','in'),
 (wstart('since'),'band','img133.png','punch'),
 (wstart('it',0),'band','img139.png','shake_in'),
 (wstart('but'),'band','img134.png','pan_r'),
 (wstart('coming'),'band','img153.png','in_cart'),
 (wstart('when'),'band','e141.png','pan_in'),
 (wstart('costco',1),'band','e143_smile.png','in_mascot'),
 (wstart('in',1),'band','img144.png','out'),
 (wstart('it',2),'band','img146.png','pan_r'),
 (wstart('and',0),'band','img147.png','pan_r'),
 (wstart('so'),'loop',None,'pullout'),
]
starts=[f(s[0])-(0.06 if i else 0) for i,s in enumerate(SHOTS)]
starts[0]=0.0
ends=starts[1:]+[TOTAL]
for i,(s,e) in enumerate(zip(starts,ends)): print(i+1,round(s,2),round(e,2),round(e-s,2))
# ---------- text style (Tesla video)
def panel_layer(lines,top=250):
    sz=min(m.fit(l,810,92).size for l in lines);fnt=m.font(sz)
    lay=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(lay)
    mask=Image.new('L',(W,H),0);md=ImageDraw.Draw(mask)
    y=top;ys=[]
    for l in lines:
        tw=d.textlength(l,font=fnt);px,py=int(sz*0.42),int(sz*0.28);bh=int(sz*1.0+2*py)
        md.rounded_rectangle([(W-tw)/2-px,y,(W+tw)/2+px,y+bh],radius=int(sz*0.34),fill=255)
        ys.append((l,y+bh/2));y+=int(sz*1.04+py*0.9)
    box=Image.new('RGBA',(W,H),(20,35,45,0));box.putalpha(mask.point(lambda v:int(v*0.70)))
    lay.alpha_composite(box)
    for i,(l,yc) in enumerate(ys): m.outlined(d,(W/2,yc+sz*0.02),l,fnt,YEL if i==0 else WHITE)
    return lay
PH={ 'A':['COSTCO BUILT ITS OWN','CHICKEN FARM'],'B':['TO KEEP THE ROTISSERIE','CHICKEN AT $4.99'],
 'P1':['ROTISSERIE CHICKEN','$4.99 SINCE 2009'],'P2':['COSTCO LOSES','MILLIONS'],'P3':['THE PRICE KEEPS','PEOPLE COMING BACK'],
 'P4':['CHICKEN COSTS','GOT PRICIER'],'P5':['BUILT ITS OWN FARM','NEBRASKA 2016'],'P6':['IT RAISES ITS OWN','CHICKENS'],'P7':['THE PRICE STAYS','AT $4.99']}
LAY={k:panel_layer(v) for k,v in PH.items()}
phases=[(0.0,wstart('to'),'A'),(wstart('to'),wstart("costco's"),'B'),(wstart("costco's"),wstart('it',0),'P1'),(wstart('it',0),wstart('but'),'P2'),
 (wstart('but'),wstart('when'),'P3'),(wstart('when'),wstart('costco',1),'P4'),(wstart('costco',1),wstart('it',2),'P5'),(wstart('it',2),wstart('and',0),'P6'),
 (wstart('and',0),wstart('so'),'P7'),(wstart('so'),AUD_LEN+1,'A')]
phases=[(f(a),f(b),k) for a,b,k in phases]
# ---------- captions (2-token groups, spoken token in yellow)
toks=[];i=0
while i<len(words):
    n=words[i][0]
    if n=='four' and words[i+1][0]=='ninety': toks.append(('$4.99',words[i][1],words[i+2][2]));i+=3;continue
    if n=='two' and words[i+1][0]=='thousand': toks.append(('2009',words[i][1],words[i+2][2]));i+=3;continue
    if n=='twenty' and words[i+1][0]=='sixteen': toks.append(('2016',words[i][1],words[i+1][2]));i+=2;continue
    toks.append((n.upper(),words[i][1],words[i][2]));i+=1
toks=[(t,f(a),f(b)) for t,a,b in toks]
groups=[];cur=[]
for tk in toks:
    if cur and (len(cur)==2 or tk[1]-cur[-1][2]>0.30): groups.append(cur);cur=[]
    cur.append(tk)
if cur: groups.append(cur)
cf=m.font(72)
def cap_layer(texts,active,cy):
    lay=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(lay)
    sp=d.textlength(' ',font=cf);ws=[d.textlength(t,font=cf) for t in texts];tot=sum(ws)+sp*(len(ws)-1)
    px,py=30,20;bh=int(72*1.0+2*py)
    box=Image.new('RGBA',(W,H),(0,0,0,0));bd=ImageDraw.Draw(box)
    bd.rounded_rectangle([(W-tot)/2-px,cy-bh/2,(W+tot)/2+px,cy+bh/2],radius=24,fill=(30,30,32,200));lay.alpha_composite(box)
    x=(W-tot)/2
    for i,(t,wd) in enumerate(zip(texts,ws)):
        m.outlined(d,(x,cy+2),t,cf,YEL if i==active else WHITE,anchor='lm');x+=wd+sp
    return lay
capcache={}
def cap_for(t,full):
    for gi,g in enumerate(groups):
        nxt=groups[gi+1][0][1] if gi+1<len(groups) else TOTAL
        t0=g[0][1]-0.02;t1=min(g[-1][2]+0.22,nxt-0.02)
        if t0<=t<t1:
            act=-1
            for j,(tx,a,b) in enumerate(g):
                if a-0.02<=t<b+0.03: act=j
            key=(gi,act,full)
            if key not in capcache: capcache[key]=cap_layer([x[0] for x in g],act,1625 if full else CAP_Y)
            return capcache[key]
    return None
# ---------- imagery
def band_bg(img):
    s=max(W/img.width,H/img.height);b=img.resize((int(img.width*s)+1,int(img.height*s)+1),Image.LANCZOS)
    l=(b.width-W)//2;tp=(b.height-H)//2;b=b.crop((l,tp,l+W,tp+H)).filter(ImageFilter.GaussianBlur(45))
    return ImageEnhance.Brightness(b).enhance(0.55)
def band_frame(img,z,cx,cy):
    cw,ch=img.width/z,img.height/z;x=min(max(cx*img.width-cw/2,0),img.width-cw);y=min(max(cy*img.height-ch/2,0),img.height-ch)
    return img.resize((W,BAND_H),Image.LANCZOS) if z==1 and cx==.5 and cy==.5 else img.transform((W,BAND_H),Image.EXTENT,(x,y,x+cw,y+ch),Image.BICUBIC)
def motion(kind,p):
    e=p*p*(3-2*p)
    if kind=='in': return 1.0+0.18*e,.5,.5
    if kind=='out': return 1.2-0.2*e,.5,.5
    if kind=='punch': return (1.0+0.28*min(p/0.12,1)+0.06*p),.5,.5
    if kind=='shake_in': return 1.0+0.2*e,.5,.5
    if kind=='pan_r': return 1.28,0.38+0.24*e,.5
    if kind=='pan_in': return 1.0+0.22*e,0.35+0.3*e,.5
    if kind=='in_cart': return 1.0+0.22*e,0.4+0.08*e,.5
    if kind=='in_mascot': return 1.0+0.2*e,0.5+0.12*e,.5
    return 1.0,.5,.5
imgs={}
for s in SHOTS:
    if s[1]=='band':
        p=s[2];im=Image.open((SC+'/edits/' if p.startswith('e') else IM)+p).convert('RGB');imgs[p]=(im,band_bg(im))
hook_len=starts[1]
fc2=(f"[0:v]split[a][b];[a]trim=0:3.0,setpts=1.1*(PTS-STARTPTS)[a1];[b]trim=3.0:4.05,setpts={(hook_len-3.3)/1.05:.4f}*(PTS-STARTPTS)[b1];"
     f"[a1][b1]concat=n=2:v=1:a=0,scale={W}:{H}:flags=lanczos,fps={FPS}[o]")
raw=subprocess.run(['ffmpeg','-loglevel','error','-i',SC+'/payoff/hook3.mp4','-filter_complex',fc2,'-map','[o]','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True).stdout
hook=[Image.frombuffer('RGB',(W,H),raw[i:i+W*H*3]) for i in range(0,len(raw),W*H*3)]
print('hook frames',len(hook),'need',int(round(hook_len*FPS)))
first=hook[0].copy()
def zoomfull_img(im,z):
    if z<=1.0: return im.copy()
    w,h=int(W*z),int(H*z);b=im.resize((w,h),Image.LANCZOS);x=(w-W)//2;y=(h-H)//2
    return b.crop((x,y,x+W,y+H))
def zoomfull(im,z):
    base=im.resize((W,H),Image.LANCZOS)
    if z==1.0: return base
    w,h=int(W*z),int(H*z);b=im.resize((w,h),Image.LANCZOS);x=(w-W)//2;y=(h-H)//2
    return b.crop((x,y,x+W,y+H))
nfr=int(round(TOTAL*FPS))
wr=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','final_audio.wav','-map','0:v','-map','1:a',
    '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-profile:v','high','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest','costco-chicken-farm-short.mp4'],stdin=subprocess.PIPE)
random.seed(3);t0=time.time()
for n in range(nfr):
    t=n/FPS
    si=max(i for i,s in enumerate(starts) if t>=s-1e-6)
    kind=SHOTS[si][1];s0,s1=starts[si],ends[si];p=min(max((t-s0)/(s1-s0),0),1)
    if kind=='hook':
        k=min(n,len(hook)-1);frame=hook[k].copy()
    elif kind=='loop':
        p2=min(p*1.06,1.0);z=round(1.0+0.08*(1-p2),4);frame=zoomfull_img(first,z)   # reaches exactly 1.00 for the last ~0.15 s
        if n==nfr-1: frame=first.copy()
    else:
        im,bg=imgs[SHOTS[si][2]];z,cx,cy=motion(SHOTS[si][3],p)
        b=band_frame(im,z,cx,cy)
        dx=dy=0
        if SHOTS[si][3]=='shake_in' and (t-s0)<0.4: dx=random.randint(-9,9);dy=random.randint(-7,7)
        frame=bg.copy();frame.paste(b,(dx,BAND_Y+dy))
    img=frame.convert('RGBA')
    for a,b2,k in phases:
        if a-1e-6<=t<b2: img.alpha_composite(LAY[k]);break
    cl=cap_for(t,kind in ('hook','loop'))
    if cl is not None: img.alpha_composite(cl)
    wr.stdin.write(img.convert('RGB').tobytes())
    if n%150==0: print(n,'/',nfr,round(time.time()-t0),'s',flush=True)
wr.stdin.close();wr.wait();print('done')
