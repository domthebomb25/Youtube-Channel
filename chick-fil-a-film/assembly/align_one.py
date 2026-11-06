import json,re,subprocess,sys
from pocketsphinx import Decoder
wav,text,out=sys.argv[1],sys.argv[2],sys.argv[3]
raw=out+'.raw'
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',wav,'-ar','16000','-ac','1','-f','s16le',raw],check=True)
words=re.sub(r"[^a-z' ]"," ",text.lower()).split()
SUB={'fil':['fill'],'a':['a']}
toks=[];owner=[]
for i,w in enumerate(words):
    for t in SUB.get(w,[w]): toks.append(t);owner.append(i)
d=Decoder(samprate=16000,bestpath=False)
d.set_align_text(' '.join(toks))
pcm=open(raw,'rb').read()
d.start_utt();d.process_raw(pcm,full_utt=True);d.end_utt()
d.set_alignment();d.start_utt();d.process_raw(pcm,full_utt=True);d.end_utt()
al=[w for w in d.get_alignment() if w.name not in ('<sil>','<s>','</s>')]
print(len(al),len(toks))
res=[]
for k,w in enumerate(al):
    res.append((toks[k],w.start/100,(w.start+w.duration)/100))
for r in res: print(f"{r[1]:6.2f} {r[2]:6.2f} {r[0]}")
