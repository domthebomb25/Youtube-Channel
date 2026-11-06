import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav14/'     # BRAM-085..092 with clipped tail noise silenced (durations unchanged)
from build_section import build,wd
nums=[85,86,87,88,89,90,91,92]
START=394.16             # Section 13 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
beats=[('CF-073F.jpg',st[85],st[87]),    # holds through BRAM-085 + 086 (mid-line zoom superseded)
       ('CF-074F.jpg',st[87],st[90]),    # holds through BRAM-087, 088, 089
       ('CF-075F.jpg',st[90],st[91]),
       ('CF-076.jpg',st[91],st[92]),     # 076B ride folded in
       ('CF-077.jpg',st[92],end)]        # 077B ride folded in
f,log=build('14',beats,nums)
print(f)
for l in log: print(l)
