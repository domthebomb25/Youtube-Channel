# Final QA on the rendered master: ffprobe, loudness, FULL LINEAR audio decode (no seeking), per-10 s L/R correlation + RMS, video frame check of every segment.
import sys, os, json, re, subprocess, numpy as np
A, W, F = sys.argv[1], sys.argv[2], sys.argv[3]; SR = 48000
def probe(f):
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", f]))
    return j
for f in (F, F.replace(".mp4", "-under25mb.mp4")):
    j = probe(f); v = [s for s in j["streams"] if s["codec_type"] == "video"][0]; a = [s for s in j["streams"] if s["codec_type"] == "audio"][0]
    print(f"{os.path.basename(f)}: {os.path.getsize(f)} bytes | duration {float(j['format']['duration']):.3f} s | video {v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']} frames {v.get('nb_frames')} | audio {a['codec_name']} {a['channels']}ch {a['sample_rate']} Hz {a.get('bit_rate')} b/s")
    # faststart: moov before mdat
    b = open(f, "rb").read(65536); print("   faststart (moov before mdat):", b.find(b"moov") != -1 and (b.find(b"mdat") == -1 or b.find(b"moov") < b.find(b"mdat")))
    p = subprocess.run(["ffmpeg", "-nostats", "-i", f, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr; p = p[p.rfind("Summary:"):]
    print("   loudness: integrated %s LUFS, true peak %s dBFS, LRA %s LU" % (re.search(r"I:\s+(-?[\d.]+)", p).group(1), re.search(r"Peak:\s+(-?[\d.]+)", p).group(1), re.search(r"LRA:\s+([\d.]+)", p).group(1)))
# ---- full linear decode of the master's audio
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", F, "-map", "0:a:0", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"])
x = np.frombuffer(raw, np.float32).reshape(-1, 2); n10 = len(x) // (10 * SR)
cor = []; rms = []
for k in range(n10 + 1):
    s = x[k * 10 * SR:(k + 1) * 10 * SR]
    if len(s) < SR: continue
    l, r = s[:, 0], s[:, 1]; c = float(np.corrcoef(l, r)[0, 1]) if l.std() > 1e-6 else float("nan")
    cor.append(c); rms.append(20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9))
cor = np.array(cor); rms = np.array(rms)
print(f"LINEAR decode: {len(x)/SR:.3f} s, {len(cor)} ten-second windows | L/R correlation min {np.nanmin(cor):.5f} max {np.nanmax(cor):.5f} | RMS dBFS min {rms.min():.1f} max {rms.max():.1f} (spread {rms.max()-rms.min():.1f} dB) | largest step between adjacent windows {np.abs(np.diff(rms)).max():.1f} dB | silent windows (<-60 dBFS): {int((rms < -60).sum())}")
print("RMS contour per 10 s:", " ".join(f"{v:.1f}" for v in rms))
# ---- video frame check: exact seek to 3 points inside each segment (25%, 50%, end-0.2 s), compare to the intended source image
from PIL import Image
tl = json.load(open(W + "/final_timeline.json")); segs = tl["segs"]
W0, H0 = 96, 54
def grab(t):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", F, "-frames:v", "1", "-vf", f"scale={W0}:{H0}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(out, np.uint8).reshape(H0, W0, 3).astype(np.float32)
sm = lambda p: np.asarray(Image.open(os.path.join(A, p)).convert("RGB").resize((W0, H0), Image.BILINEAR), np.float32)
def corr(a, b):
    a = a.ravel() - a.mean(); b = b.ravel() - b.mean(); return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
low = []; res = []
for i, (img, t0, t1, lab) in enumerate(segs):
    ref = sm(img); c = min(corr(grab(t), ref) for t in (t0 + 0.25 * (t1 - t0), t0 + 0.5 * (t1 - t0), t1 - 0.2))
    res.append((lab, img, c))
    if c < 0.96: low.append((lab, img, round(c, 4)))
print(f"video frame-check: {len(res)} segments (91 positions + {len(res)-91} in-shot state frames), 3 exact-seek samples each, compared to the intended source image; min corr {min(r[2] for r in res):.4f}; below 0.96: {low}")
# last frame
last = np.asarray(Image.open(subprocess.run(["ffmpeg", "-v", "error", "-sseof", "-0.2", "-i", F, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout and __import__("io").BytesIO(subprocess.run(["ffmpeg", "-v", "error", "-sseof", "-0.2", "-i", F, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout)).convert("RGB").resize((W0, H0), Image.BILINEAR), np.float32)
print("final frame vs shot 121: corr %.4f" % corr(last, sm("section6/121.png")))
json.dump(dict(seg_corr=res), open(W + "/frame_check.json", "w"))
