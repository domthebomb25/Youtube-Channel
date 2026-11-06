import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav15/'     # BRAM-093..103 with clipped tail noise silenced (durations unchanged)
from build_section import build,wd
nums=list(range(93,104))
START=424.56             # Section 14 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
pics={93:'CF-079.jpg',94:'CF-081.jpg',95:'CF-082.jpg',96:'CF-083.jpg',97:'CF-080.jpg',98:'CF-084.jpg',99:'CF-085.jpg',100:'CF-086.jpg',101:'CF-087.jpg',102:'CF-088.jpg',103:'CF-089.jpg'}
beats=[]
for n in nums:
    e=st[n+1] if n+1 in st else end
    beats.append((pics[n],st[n],e))
f,log=build('15',beats,nums)
print(f)
for l in log: print(l)
