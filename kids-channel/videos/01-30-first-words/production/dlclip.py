import sys,subprocess,json,os
# usage: dlclip.py <dir> <jobsfile> idx url [idx url...]
d,jf=sys.argv[1],sys.argv[2]; a=sys.argv[3:]
jobs=json.load(open(jf)) if os.path.exists(jf) else {}
for i in range(0,len(a),2):
    idx,url=a[i],a[i+1]; jobs[idx]=url.split('_')[-1].split('.')[0]
    subprocess.run(['curl','-sS','-o',f'{d}/{d}-{int(idx):03d}.mp4',url],check=True)
json.dump(jobs,open(jf,'w')); print(len(jobs),"clips logged")
