import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
from build_section import build,wd
nums=[19,20,21,22,23,24]
off=sum(wd(n) for n in range(1,19))
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(off,4),'length',round(end,4),'ends',round(off+end,4))
CUT17=1.98   # word "and" starts 1.98 s into BRAM-019 (pocketsphinx alignment)
CUT21=5.40   # sheet-marked point inside BRAM-024 (beat 27, ZOOM)
beats=[('CF-017.jpg',st[19],st[19]+CUT17),
       ('CF-017B.jpg',st[19]+CUT17,st[20]),
       ('CF-018.jpg',st[20],st[21]),
       ('CF-019.jpg',st[21],st[22]),
       ('CF-020.jpg',st[22],st[23]),
       ('CF-020B.jpg',st[23],st[24]),
       ('CF-021.jpg',st[24],st[24]+CUT21),
       ('CF-021B.jpg',st[24]+CUT21,end)]
f,log=build('04',beats,nums)
print(f)
for l in log: print(l)
