import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav13/'
from build_section import build,wd
nums=[78,79,80,81,82,83,84]
START=151.28+27.33+28.91+34.32+31.76+27.60+27.92+29.68      # Section 12 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
beats=[('CF-067.jpg',st[78],st[79]),
       ('CF-067B.jpg',st[79],st[80]),
       ('CF-068F.jpg',st[80],st[81]),     # 068B ride folded in
       ('CF-069F.jpg',st[81],st[82]),     # 069B ride folded in
       ('CF-070.jpg',st[82],st[83]),
       ('CF-071.jpg',st[83],st[84]),      # 071B ride folded in
       ('CF-072F.jpg',st[84],end)]        # THIRD-PARTY ESTIMATE label composited (072B ride folded in)
f,log=build('13',beats,nums)
print(f)
for l in log: print(l)
