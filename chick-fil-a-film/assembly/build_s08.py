import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav8/'
from build_section import build,wd
nums=[48,49,50,51,52,53,54]
START=151.28+27.33+28.91      # Section 07 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
C51=4.52    # breath inside BRAM-051 (user-given; "and" starts 4.48)
C54=3.05    # middle of the gap between "his" (ends 2.87) and "Here" (3.22) inside BRAM-054
beats=[('CF-036.jpg',st[48],st[49]),                  # CF-042 on the labeled Item 7 list, holds (no reframe)
       ('CF-043.jpg',st[49],st[50]),
       ('CF-043B.jpg',st[50],st[51]),
       ('CF-044.jpg',st[51],st[51]+C51),
       ('CF-044B.jpg',st[51]+C51,st[52]),             # NEW: rent envelope at the counter
       ('CF-045.jpg',st[52],st[53]),
       ('CF-045B.jpg',st[53],st[54]),
       ('CF-046.jpg',st[54],st[54]+C54),
       ('CF-046B.jpg',st[54]+C54,end)]                # NEW: company carries the sack
f,log=build('08',beats,nums)
print(f)
for l in log: print(l)
