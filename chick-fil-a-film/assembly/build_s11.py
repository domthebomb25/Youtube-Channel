import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav11/'
from build_section import build,wd
nums=[65,66,67,68,69,70]
START=151.28+27.33+28.91+34.32+31.76+27.60      # Section 10 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
beats=[('CF-055-edit.jpg',st[65],st[66]),     # $85 counter state
       ('CF-055B.jpg',st[66],st[67]),        # crew carrying crates
       ('CF-056.jpg',st[67],st[68]),         # busy kitchen (056B ride folded in)
       ('CF-057.jpg',st[68],st[69]),         # RENT envelope in front of the store (057B ride folded in)
       ('CF-058.jpg',st[69],st[70]),         # $3.25 billboard (058B ride folded in)
       ('CF-059F.jpg',st[70],end)]           # CUT 2 stack
f,log=build('11',beats,nums)
print(f)
for l in log: print(l)
