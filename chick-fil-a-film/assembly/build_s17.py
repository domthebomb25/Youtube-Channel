import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav17/'     # BRAM-110..116, clipped tail noise silenced where found (durations unchanged)
from build_section import build,wd
nums=list(range(110,117))
START=486.32             # Section 16 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
HOLD={'z_start':1.04,'z_step':0.0}   # CF-091 continues still from Section 16's last frame (091B crop retired by the no-crop rule)
beats=[('CF-091.jpg',st[110],st[111],HOLD),
       ('CF-022.jpg',st[111],st[112]),     # 023R reuse beat uses the CF-022 picture
       ('CF-095.jpg',st[112],st[113]),
       ('CF-093.jpg',st[113],st[115]),      # holds through BRAM-113 + 114 (093B crop folded in)
       ('CF-041.jpg',st[115],st[116]),      # 041R
       ('CF-094.jpg',st[116],end)]
f,log=build('17',beats,nums)
print(f)
for l in log: print(l)
