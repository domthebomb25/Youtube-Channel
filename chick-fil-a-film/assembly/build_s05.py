import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Youtube-Channel/25ce4138-4e12-575d-bc53-467d57007634/scratchpad')
from build_section import build,wd
nums=[25,26,27,28,29,30,31,32]
off=sum(wd(n) for n in range(1,25))
st={};c=0.0
for n in nums: st[n]=c;c+=wd(n)
end=c
print('section start',round(off,4),'length',round(end,4),'ends',round(off+end,4))
C29,C30,C31=4.23,3.41,3.60   # user-given internal splits (alignment: "and" 4.22, "Chick-fil-A" 3.39, "They" 3.72)
beats=[('CF-022.jpg',st[25],st[26]),
       ('CF-022B.jpg',st[26],st[27]),
       ('CF-023.jpg',st[27],st[28]),
       ('CF-023B.jpg',st[28],st[29]),
       ('CF-024.jpg',st[29],st[29]+C29),
       ('CF-024B.jpg',st[29]+C29,st[30]),
       ('CF-025.jpg',st[30],st[30]+C30),
       ('CF-025B.jpg',st[30]+C30,st[31]),
       ('CF-026.jpg',st[31],st[31]+C31),
       ('CF-026B.jpg',st[31]+C31,st[32]),
       ('CF-028.jpg',st[32],end)]   # CF-027's line plays on the FRYERS image (cells_v2: cell 027 img=028)
f,log=build('05',beats,nums)
print(f)
for l in log: print(l)
