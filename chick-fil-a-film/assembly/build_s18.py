import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
import build_section as bs
bs.WAVD='/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad/wav18/'     # BRAM-117..121,123 (BRAM-122 duplicate plays nowhere); clipped tail noise silenced where found
from build_section import build,wd
nums=[117,118,119,120,121,123]
START=510.32             # Section 17 end
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(START,4),'narration length',round(end,4),'narration ends',round(START+end,4),'video ends',round(START+end+1.2,4))
C120=7.30    # gap between "small." (ends 7.14) and "It is cheap" (7.40) inside BRAM-120
C123=1.55    # start of "to run one" inside BRAM-123 (CF-100 -> CF-101 closer; cut at a word boundary)
beats=[('CF-095.jpg',st[117],st[118]),          # CF-095B zoom crop dropped: CF-095 holds
       ('CF-096.jpg',st[118],st[119]),
       ('CF-097.jpg',st[119],st[120]),
       ('CF-098.jpg',st[120],st[120]+C120),     # $10,000 tag; 098B zoom dropped
       ('CF-099.jpg',st[120]+C120,st[123]),     # display case holds through BRAM-120 tail + BRAM-121 (099B ride folded)
       ('CF-100.jpg',st[123],st[123]+C123),
       ('CF-101.jpg',st[123]+C123,end)]         # sunrise closer takes the final line's tail
TAIL=1.2     # final breath: CF-101 holds 1.2 s past the last spoken word, silent audio, then cut (no fade, no end card)
beats[-1]=(beats[-1][0],beats[-1][1],end+TAIL)
f,log=build('18',beats,nums+[999])
print(f)
for l in log: print(l)
