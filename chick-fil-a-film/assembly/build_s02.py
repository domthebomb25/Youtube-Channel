import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/449e7c41-1593-568a-a48e-42113e5e2ca2/scratchpad')
from build_section import build,wd,SC
nums=[7,8,9,10,11]
pics=['CF-007B.jpg','CF-008.jpg','CF-009.jpg','CF-009B.jpg','CF-010.jpg']
c=0.0;beats=[];starts=[]
for n,p in zip(nums,pics):
    d=wd(n);beats.append([p,c,c+d]);starts.append(c);c+=d
# CF-008 tighten: push starts 3.0s into BRAM-008, eases into the CF-008B close frame by the end of the file
FPS=30
f0=round(starts[1]*FPS);f1=round(starts[2]*FPS);N=f1-f0
p0=round(3.0*FPS)                      # frame index inside the beat where the push begins
ZF=2688/1230.0                          # close frame width 1230 px of 2688
GZ=0.02                                 # gentle push before the tighten
e=f"(0.5-0.5*cos(3.14159265*(on-{p0})/{N-1-p0}))"
zexpr=f"if(lt(on,{p0}),1+{GZ}*on/{p0},{1+GZ}+({ZF}-{1+GZ})*{e})"
cx=f"if(lt(on,{p0}),1344,1344+(1500-1344)*{e})"
cy=f"if(lt(on,{p0}),760,760+(690-760)*{e})"
xe=f"({cx})*{SC}-iw/zoom/2"
ye=f"({cy})*{SC}-ih/zoom/2"
beats[1].append({'custom':(zexpr,xe,ye)})
beats=[tuple(b) for b in beats]
print('section length',round(c,4),'CF-008 beat frames',N,'push begins at beat frame',p0)
f,log=build('02',beats,nums)
for l in log: print(l)
