# Film #2 FINAL: 91 storyboard positions x 153 narration lines -> master 1080p + 720p under-25MB, ffmpeg concat FILTER (full decode, one encode).
# usage: python3 -I 08_assemble_final.py <repo>/film2-assets <workdir>
import sys, os, json, subprocess, re
A, W = sys.argv[1], sys.argv[2]; FPS = 30; TAIL = 0.5
rows = json.load(open(W + "/rows.json"))['rows']; R = {r['vo']: r for r in rows}
order_expected = [r['vo'] for r in rows]
def sf(n):
    for d in ("section1","section2","section3","section4","section5","section6"):
        p = f"{A}/{d}/{n}.png"
        if os.path.exists(p): return p
    raise SystemExit(f"missing shot {n}")
F = A + "/section2-final/"
CHAIR = A + "/section2-v2/chair-empty.png"
# (position order) (image, [VO ids])  -- verbatim from the final storyboard
P = [(sf(1),[1]),(sf(2),[2]),(sf(3),[4]),(sf(4),[5]),(sf(5),[6]),(sf(6),[7,8]),(sf(8),[9,10]),(sf(9),[11,12,13]),(sf(10),[14,15]),(sf(11),[16]),(sf(13),[19]),(sf(52),[201]),(sf(17),[23]),(sf(18),[24]),(sf(19),[202,203]),(sf(20),[204]),
 (sf(22),[30]),(sf(23),[31,32]),(sf(24),[33]),(sf(25),[34]),(sf(26),[35]),(sf(1),[36]),(CHAIR,[205,206]),(F+"ninja-blue-hoodie.png",[207]),(F+"ludwig-monitorback-fix2.png",[208]),(F+"kai-red-hoodie-v2.png",[209]),(sf(56),[210]),(sf(26),[211,212]),
 (sf(59),[74]),(sf(59),[76,77,78]),(sf(60),[79]),(sf(61),[82,83]),(sf(62),[84,85,86]),(sf(63),[87,88]),(sf(64),[89,90]),(sf(65),[91]),(sf(66),[92]),(sf(67),[93]),(sf(68),[94]),(sf(69),[95]),(sf(70),[96,97]),(sf(71),[98]),(sf(72),[99]),(sf(73),[100]),(sf(74),[101,102,103]),
 (sf(76),[104,106]),(sf(77),[107,108,109]),(sf(78),[110,111]),(sf(79),[112,113,114]),(sf(80),[115,116]),(sf(81),[117,118]),(sf(82),[119,120]),(sf(83),[121,122]),(sf(84),[123]),(sf(85),[124]),(sf(86),[125,126]),(sf(87),[127,128]),(sf(88),[129]),(sf(89),[130,131]),
 (sf(90),[132,133]),(sf(91),[134]),(sf(92),[135,136]),(sf(93),[137]),(sf(94),[138,139]),(sf(95),[140,141]),(sf(96),[142]),(sf(97),[143,144]),(sf(98),[145,146]),(sf(99),[147,148,149]),(sf(100),[150,151]),(sf(101),[152,153]),(sf(102),[154,155]),(sf(103),[156,157,158]),(sf(104),[159,160]),(sf(106),[167]),(sf(107),[168,169]),(sf(108),[170,171]),(sf(104),[161,162,163]),(sf(105),[164,165,166]),(sf(109),[172]),(sf(110),[173,174]),(sf(111),[175,176]),
 (sf(112),[177,178]),(sf(113),[179]),(sf(114),[180,181]),(sf(115),[182,183]),(sf(87),[184,185,186]),(sf(118),[188,189]),(sf(119),[190]),(sf(120),[191,192]),(sf(121),[193,195])]
assert len(P) == 91, len(P)
flat = [v for _, ids in P for v in ids]; assert flat == order_expected, "storyboard VO order != narration order"
# cut times: midpoint of the 0.30 s gap between shots (lands on a line boundary)
cuts = [0.0]
for k in range(1, 91):
    a = R[P[k-1][1][-1]]; b = R[P[k][1][0]]; cuts.append((a['t_speech_off'] + b['t_speech_on']) / 2)
end = R[P[-1][1][-1]]['t_speech_off'] + R[P[-1][1][-1]]['kept_trail'] + TAIL
cuts.append(end)
# in-shot state flips: (position index 0-based) -> [(time, image)]
def line_start_cut(vo):  # cut inside a shot, between two of its lines
    k = flat.index(vo); a = R[flat[k-1]]; b = R[vo]; return (a['t_speech_off'] + b['t_speech_on']) / 2
S = A + "/render/states/"
flips = {
 7:  [(line_start_cut(12), S + "09-50000.png"), (line_start_cut(13), S + "09-100000.png")],   # position 8 (shot 9)
 8:  [(line_start_cut(15), S + "10-1000.png")],                                                  # position 9 (shot 10)
 54: [(R[124]['t_start'] + (8.01 - R[124]['removed_lead']), A + "/section4/85-state.png")],       # position 55 (shot 85): pop on "explodes"
 39: [(R[95]['t_start'] + (4.80 - R[95]['removed_lead']), A + "/section3/69-state.png")],         # position 40 (shot 69): money figure on "between twenty..."
}
segs = []   # (image, start_s, end_s, label)
for k, (img, ids) in enumerate(P):
    t0, t1 = cuts[k], cuts[k+1]; pts = [(t0, img)] + sorted(flips.get(k, []))
    for j, (ts, im) in enumerate(pts):
        te = pts[j+1][0] if j+1 < len(pts) else t1
        segs.append((im, ts, te, f"pos{k+1}" + ("" if j == 0 else f"-state{j}")))
fr = lambda t: int(round(t * FPS))
bounds = [fr(s[1]) for s in segs] + [fr(segs[-1][2])]
frames = [bounds[i+1] - bounds[i] for i in range(len(segs))]
assert min(frames) > 0 and sum(frames) == bounds[-1]
tot = bounds[-1] / FPS
# --- inputs + filter graph
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
for im, *_ in segs: cmd += ["-loop", "1", "-framerate", str(FPS), "-i", im]
cmd += ["-i", W + "/narration-153.wav"]
n = len(segs); ai = n
fg = []
for i in range(n):
    fg.append(f"[{i}:v]trim=end_frame={frames[i]},setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,setsar=1,fps={FPS},format=yuv420p[v{i}]")
fg.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]")
fg.append("[vc]split=2[vm][vs]; [vs]scale=1280:720:flags=lanczos,format=yuv420p[v720]")
# two-pass loudnorm in LINEAR mode (measured on the exact audio that gets encoded) = a pure gain trim, no dynamic processing
if "--dry" in sys.argv: LN = "I=-14:TP=-1.5:LRA=11"
else:
    m = subprocess.run(["ffmpeg", "-nostats", "-i", W + "/narration-153.wav", "-af", f"pan=stereo|c0=c0|c1=c0,apad=whole_dur={tot:.4f},loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(m[m.rfind("{"):m.rfind("}")+1])
    LN = f"I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
    print("loudnorm pass 1:", {k: j[k] for k in ("input_i", "input_tp", "input_lra", "target_offset")})
fg.append(f"[{ai}:a]pan=stereo|c0=c0|c1=c0,apad=whole_dur={tot:.4f},loudnorm={LN},aresample=48000,asplit=2[am][as]")
open(W + "/filter.txt", "w").write(";\n".join(fg))
json.dump(dict(total=tot, frames=frames, segs=[(s[0].replace(A+'/',''), round(s[1],3), round(s[2],3), s[3]) for s in segs]), open(W + "/final_timeline.json", "w"), indent=1)
print(f"{len(segs)} segments (91 positions + {len(segs)-91} state flips); {sum(frames)} frames = {tot:.3f} s")
x264 = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
out1 = A + "/render/film2-streamer-REBUILD-v2.mp4"; out2 = A + "/render/film2-streamer-REBUILD-v2-under25mb.mp4"
VB = os.environ.get("VB720", "170k")
cmd += ["-filter_complex_script", W + "/filter.txt",
        "-map", "[vm]", "-map", "[am]"] + x264 + ["-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out1,
        "-map", "[v720]", "-map", "[as]"] + x264 + ["-preset", "slow", "-b:v", VB, "-maxrate", str(int(VB[:-1]) * 1.6) + "k", "-bufsize", str(int(VB[:-1]) * 4) + "k", "-c:a", "aac", "-b:a", "96k", "-ar", "48000", "-movflags", "+faststart", out2]
if "--dry" in sys.argv: print(" ".join(cmd[:8]), "...", len(cmd), "args"); sys.exit()
print("running ffmpeg ..."); subprocess.run(cmd, check=True)
print(out1, os.path.getsize(out1)); print(out2, os.path.getsize(out2))
