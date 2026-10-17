"""Assemble the Tesla Roadster long-form: hook -> 101 Ken-Burns stills timed to the Benji voiceover.
usage: render.py OUT.mp4 WIDTH   (1920 = final, 640 = preview)"""
import sys, os, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
import shots
T = "/tmp/claude-0/-home-user-Youtube-Channel/2ee8fda5-8aff-57ca-9ae9-d4d984797fb0/scratchpad/tesla"
out, W = sys.argv[1], int(sys.argv[2]); H = W * 9 // 16
FPS = 30
def img(n):
    if n == 1: return "shot01/shot01.png"
    if n == 7: return "shot07_calendar.png"
    if n == 10: return "fix2/shot10_new.png"
    if n in (12, 3): return f"fix1/shot{n:02d}.png"
    if n in (13, 17): return f"fix3/shot{n}.png"
    if n == 71: return "fix3/shot17.png"
    if n == 4: return "fix2/shot04.png"
    if n in (21, 28): return f"fix4/shot{n}.png"
    if n in (30, 32, 33, 36, 37): return f"fix5/shot{n}.png"
    if n == 48: return "fix6/shot48.png"
    if n == 50: return "fix7/shot50.png"
    if n in (87, 88): return f"fix10/shot{n}.png"
    if n == 99: return "fix11/shot99.png"
    if n == 80: return "batch8/shot80.png"
    if 70 <= n <= 79: return f"batch7/real{n}.png"
    if n >= 90: return f"batch9/shot{n:03d}.png"
    for d in ("test1", "batch1", "batch2", "batch3", "batch4", "batch5", "batch6", "batch8"):
        p = f"{d}/shot{n:02d}.png"
        if os.path.exists(f"{T}/{p}"): return p
    raise SystemExit(f"no image for shot {n}")
S = shots.SHOTS
starts = [shots.HOOK] + [s[0] + shots.HOOK for s in S[1:]]
ends = starts[1:] + [shots.END + shots.HOOK]
work = f"{T}/render_{W}"; shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
def clip(i):
    n = i + 1; dur = ends[i] - starts[i]; fr = max(2, round(dur * FPS)); dur = fr / FPS
    z = f"min(1+0.04*on/{fr},1.04)" if i % 2 == 0 else f"max(1.04-0.04*on/{fr},1)"
    vf = (f"scale={7680}:-2:flags=lanczos,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d={fr}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p")
    p = f"{work}/c{n:03d}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{T}/{img(n)}","-vf",vf,"-frames:v",str(fr),
                    "-c:v","libx264","-crf","18" if W>=1920 else "16","-preset","medium","-tune","animation","-r",str(FPS),p],check=True)
    return p, fr
with ThreadPoolExecutor(max_workers=os.cpu_count()) as ex: res = list(ex.map(clip, range(len(S))))
hook = f"{work}/hook.mp4"
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{T}/hook_v9_youtube_1080p_rocket.mp4","-an","-vf",f"scale={W}:{H},fps={FPS},setsar=1,format=yuv420p",
                "-c:v","libx264","-crf","18" if W>=1920 else "16","-preset","medium","-tune","animation","-t","4.0",hook],check=True)
with open(f"{work}/list.txt","w") as f:
    f.write(f"file '{hook}'\n"); [f.write(f"file '{p}'\n") for p,_ in res]
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{work}/list.txt","-i",f"{T}/hook_v9_youtube_1080p_rocket.mp4","-i",f"{T}/voiceover.mp3",
  "-filter_complex","[1:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=4[h];[2:a]aresample=48000,aformat=channel_layouts=stereo,adelay=4000|4000[v];[h][v]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.95[a]",
  "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",out],check=True)
print("done", out)
