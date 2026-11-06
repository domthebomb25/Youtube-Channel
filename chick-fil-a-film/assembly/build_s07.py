import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav7/'     # BRAM-038 = the part after 2.05 s (Section 06 ends there); BRAM-039..047 untouched
from build_section import build,wd
nums=[38,39,40,41,42,43,44,45,46,47]
START=151.28+27.33       # Section 06 end (audio)
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'length',round(end,4),'ends',round(START+end,4))
HOLD={'z_start':1.04,'z_step':0.0}   # CF-032 picture continues from Section 06's last frame (it ended at 104%)
beats=[('CF-032.jpg',st[38],st[39],HOLD),     # rest of "That is exactly the right question..." sentence, no crop
       ('CF-036.jpg',st[39],st[41]),          # CF-035 list with TOTAL holds across BRAM-039 + BRAM-040 (CF-034 truck retired)
       ('CF-036B.jpg',st[41],st[42]),         # CF-035B fenced empty lot
       ('CF-036A.jpg',st[42],st[43]),         # CF-036 dashed outline
       ('CF-040.jpg',st[43],st[44]),          # CF-037 deed signing
       ('CF-038B.jpg',st[44],st[45]),         # CF-038 car + empty lot
       ('CF-035B.jpg',st[45],st[46]),         # CF-039 crane
       ('CF-039B.jpg',st[46],st[47]),         # CF-040 finished, sunset
       ('CF-041.jpg',st[47],end)]             # CF-041 finished building
f,log=build('07',beats,nums)
print(f)
for l in log: print(l)
