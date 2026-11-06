import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav12/'
from build_section import build,wd
nums=[71,72,73,74,75,76,77]
START=151.28+27.33+28.91+34.32+31.76+27.60+27.92      # Section 11 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
beats=[('CF-060F.jpg',st[71],st[72]),     # $1,000 base stack
       ('CF-061F.jpg',st[72],st[73]),     # COMPANY / YOU split stacks (061B ride folded in)
       ('CF-062F.jpg',st[73],st[74]),     # one SALE check, night store (062B ride folded in)
       ('CF-063F.jpg',st[74],st[75]),     # SALE + PROFIT checks (063B ride folded in)
       ('CF-064F.jpg',st[75],st[76]),     # paid LAST tag
       ('CF-065F.jpg',st[76],st[77]),     # MY CUT stack
       ('CF-065B.jpg',st[77],end)]        # alone in the dark restaurant
f,log=build('12',beats,nums)
print(f)
for l in log: print(l)
