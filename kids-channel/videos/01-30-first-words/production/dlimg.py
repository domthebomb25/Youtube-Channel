import json,sys,subprocess
names=json.load(open('image_index.json')); jobs=json.load(open('img_jobs.json'))
args=sys.argv[1:]
for i in range(0,len(args),2):
    idx,url=args[i],args[i+1]
    jobs[idx]=url.split('_')[-1].split('.')[0] if '/' in url else jobs.get(idx)
    subprocess.run(['curl','-sS','-o',f'frames/{names[int(idx)]}.png',url],check=True)
json.dump(jobs,open('img_jobs.json','w')); print("have",len(jobs),"jobs")
