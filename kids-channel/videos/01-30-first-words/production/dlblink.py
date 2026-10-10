"""python3 dlblink.py idx url ...   idx = line*10 + (0 closed | 1 half)"""
import sys, os, json, re, subprocess
os.makedirs('blinks', exist_ok=True)
log = json.load(open('blink_jobs.json')) if os.path.exists('blink_jobs.json') else {}
a = sys.argv[1:]
for i in range(0, len(a), 2):
    idx, url = int(a[i]), a[i+1]
    name = f"blinks/b-{idx//10:03d}-{'closed' if idx%10==0 else 'half'}.png"
    subprocess.run(['curl', '-sS', '-o', name, url], check=True)
    log[str(idx)] = re.search(r'_([0-9a-f-]{36})\.', url).group(1)
json.dump(log, open('blink_jobs.json', 'w'), indent=0); print(len(log), "blink images")
