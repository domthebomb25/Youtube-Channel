import subprocess,wave,sys,os,json
S='/tmp/claude-0/-home-user-Youtube-Channel/449e7c41-1593-568a-a48e-42113e5e2ca2/scratchpad'
IM=S+'/film/chick-fil-a-film/images/'
WAVD=S+'/bram/wav/'
FPS=30;SC=3;W0,H0=2688,1520
def wd(n):
    w=wave.open(WAVD+f'BRAM-{n:03d}.wav');return w.getnframes()/w.getframerate()
def build(name,beats,audio_files,push=0.04,hold_under=1.0,hold_pics=()):
    # beats: (picture file, start_s, end_s)
    out_dir=f'{S}/sections/work{name}';os.makedirs(out_dir,exist_ok=True)
    total=beats[-1][2]
    cuts=[round(b[1]*FPS) for b in beats]+[round(total*FPS)]
    clips=[];log=[]
    for i,b in enumerate(beats):
        img,s,e=b[0],b[1],b[2];opts=b[3] if len(b)>3 else None
        N=cuts[i+1]-cuts[i]
        dur=e-s
        z0,z1=1.0,(1.0 if (dur<hold_under or img in hold_pics) else 1.0+push)
        z=f"({z0}+({z1}-{z0})*on/{max(N-1,1)})"
        if opts and 'z_start' in opts: z=f"({opts['z_start']}+{opts['z_step']}*on)"; z1=opts['z_start']+opts['z_step']*(N-1)
        xe,ye="iw/2-iw/zoom/2","ih/2-ih/zoom/2"
        if opts and 'custom' in opts: z,xe,ye=opts['custom']; z1=9.99
        zp=f"zoompan=z='{z}':x='{xe}':y='{ye}':d={N}:s=1920x1080:fps={FPS}"
        o=f'{out_dir}/c{i:02d}.mp4'
        subprocess.run(['ffmpeg','-v','error','-y','-i',IM+img,'-vf',f"scale={W0*SC}:{H0*SC}:flags=lanczos,{zp},format=yuv420p",'-frames:v',str(N),'-c:v','libx264','-crf','15','-preset','medium','-r',str(FPS),o],check=True)
        clips.append(o);log.append({'beat':i+1,'picture':img,'start_exact':round(s,4),'frame_start':cuts[i],'cut_time_s':round(cuts[i]/FPS,4),'frames':N,'move':'hold' if z1==1.0 else f'push-in 1.00->{z1:.2f}'})
    open(out_dir+'/list.txt','w').write(''.join(f"file '{c}'\n" for c in clips))
    open(out_dir+'/alist.txt','w').write(''.join(f"file '{WAVD}BRAM-{n:03d}.wav'\n" for n in audio_files))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',out_dir+'/alist.txt','-c','copy',out_dir+'/audio.wav'],check=True)
    final=f'{S}/sections/SECTION-{name}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',out_dir+'/list.txt','-i',out_dir+'/audio.wav','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',final],check=True)
    json.dump(log,open(f'{S}/sections/SECTION-{name}-log.json','w'),indent=1)
    return final,log
if __name__=='__main__':
    d={n:wd(n) for n in range(1,7)}
    st={};c=0.0
    for n in range(1,7): st[n]=c;c+=d[n]
    end=c
    PUSH=0.04;F0=396;F1=round(st[6]*30)
    def cont(f): return {'z_start':1+PUSH*(f-F0)/(F1-F0),'z_step':PUSH/(F1-F0)}
    beats=[('CF-001.jpg',st[1],st[2]),
           ('CF-002.jpg',st[2],st[2]+1.45),
           ('CF-003.jpg',st[2]+1.45,st[3]),
           ('CF-004.jpg',st[3],st[4]),
           ('CF-005.jpg',st[4],st[5],cont(396)),
           ('CF-006-owner.jpg',st[5],st[5]+6.11,cont(468)),
           ('CF-006-edit.jpg',st[5]+6.11,st[6],cont(651)),
           ('CF-007.jpg',st[6],end)]
    f,log=build('01',beats,[1,2,3,4,5,6],hold_pics=('CF-003.jpg',))
    print(f,round(end,4))
    for l in log: print(l)
