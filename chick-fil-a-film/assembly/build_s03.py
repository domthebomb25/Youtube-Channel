import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
from build_section import build,wd
nums=[12,13,14,15,16,17,18]
pics=['CF-011.jpg','CF-011B.jpg','CF-012.jpg','CF-013.jpg','CF-014.jpg','CF-015.jpg','CF-016.jpg']
# start offset = decoded sum of BRAM-001..011
off=sum(wd(n) for n in range(1,12))
print('section start',round(off,4))
c=0.0;beats=[]
for n,p in zip(nums,pics):
    d=wd(n);beats.append((p,c,c+d));c+=d
print('section length',round(c,4),'ends at',round(off+c,4))
f,log=build('03',beats,nums)
print(f)
for l in log: print(l)
