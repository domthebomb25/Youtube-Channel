import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav6/'          # BRAM-001..037 untouched; BRAM-038 trimmed to 2.05 s (ends after "That is exactly the right question.")
from build_section import build,wd
nums=[33,34,35,36,37,38]
off=sum(wd(n) for n in range(1,33))
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(off,4),'length',round(end,4),'ends',round(off+end,4))
C34,C36,C37=2.48,2.17,2.50   # user-given splits (alignment: "and" 2.44, "It" 2.13, "but" 2.42)
beats=[('CF-029.jpg',st[33],st[34]),                 # CF-028 line on the photo board
       ('CF-NEW029.jpg',st[34],st[34]+C34),          # CF-029 line on the new check-handover image
       ('CF-029B-check.jpg',st[34]+C34,st[35]),
       ('CF-030.jpg',st[35],st[36]),                 # holds 6.0 s, gentle push only
       ('CF-031.jpg',st[36],st[36]+C36),
       ('CF-031B.jpg',st[36]+C36,st[37]),
       ('CF-033.jpg',st[37],st[37]+C37),             # CF-032 line on image file CF-033
       ('CF-032B.jpg',st[37]+C37,st[38]),
       ('CF-032.jpg',st[38],end)]                    # CF-033 line on image file CF-032
f,log=build('06',beats,nums)
print(f)
for l in log: print(l)
