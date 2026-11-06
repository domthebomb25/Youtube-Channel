import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav16/'     # BRAM-104..109 with clipped tail noise silenced (durations unchanged)
from build_section import build,wd
nums=list(range(104,110))
START=454.08             # Section 15 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
beats=[('CF-090.jpg',st[104],st[106]),    # holds through BRAM-104 + 105
       ('CF-092.jpg',st[106],st[107]),
       ('CF-019.jpg',st[107],st[108]),    # 019R reuse of the CF-019 picture
       ('CF-091.jpg',st[108],end)]        # holds through BRAM-108 + 109
f,log=build('16',beats,nums)
print(f)
for l in log: print(l)
