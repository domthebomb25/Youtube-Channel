import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav9/'
from build_section import build,wd
nums=[55,56,57,58,59]
START=151.28+27.33+28.91+34.32      # Section 08 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
beats=[('CF-047.jpg',st[55],st[56]),            # holds all of BRAM-055 (047B zoom superseded)
       ('CF-048.jpg',st[56],st[57]),            # holds through the 048B line
       ('CF-049.jpg',st[57],st[58]),            # holds through the 049B line
       ('CF-050-edit.jpg',st[58],st[59]),       # torn-slice edit state, "15% - $15" on the slice
       ('CF-051-edit.jpg',st[59],end)]          # $85 bill, holds the full file (mid-line zoom superseded)
f,log=build('09',beats,nums)
print(f)
for l in log: print(l)
