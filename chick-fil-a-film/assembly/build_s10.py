import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav10/'
from build_section import build,wd
nums=[60,61,62,63,64]
START=151.28+27.33+28.91+34.32+31.76      # Section 09 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
beats=[('CF-052.jpg',st[60],st[61]),             # $15 slice card, GEAR RENT tag
       ('CF-052B-edit.jpg',st[61],st[62]),      # same shot, SERVICES tag added (CF-052B.jpg is the retired seesaw)
       ('CF-053.jpg',st[62],st[64]),            # billboard bar holds through BRAM-062 + BRAM-063
       ('CF-054-edit.jpg',st[64],end)]          # bar full billboard width, "?" plate
f,log=build('10',beats,nums)
print(f)
for l in log: print(l)
