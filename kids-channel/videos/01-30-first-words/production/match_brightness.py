"""Makes one clip's lighting match another's, area by area (background, face, hair...).
Both clips start from the same picture with a locked camera, so their median frames line up. Three steps, each fitted on
the median frames: a smooth lighting map (ratio of the blurred medians), a per-colour tone curve (fixes darks vs
brights inside an area), then a second smooth map for what is left. Audio is copied untouched."""
import cv2, numpy as np, subprocess, sys
ref, src, out = sys.argv[1:4]
def frames(p):                        # decoded by ffmpeg with exact colour rounding (default rounding loses ~2 brightness on the way back)
    w, h = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", p]).decode().split(","))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-sws_flags", "accurate_rnd+full_chroma_int+bitexact", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    return list(np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3))
R, S = frames(ref), frames(src)
med = lambda fs: np.median(np.stack(fs[::3]).astype(np.float32), axis=0)
blur = lambda a, s: cv2.GaussianBlur(a, (0, 0), s)
mr, ms = med(R), med(S)
g1 = blur(mr, 30) / np.maximum(blur(ms, 30), 1)
def curve(x, y):                      # per-colour lookup: average target value for each input value
    lut = np.zeros((3, 256), np.float32)
    for c in range(3):
        xi = np.clip(x[..., c], 0, 255).astype(np.int32).ravel(); yi = y[..., c].ravel()
        s = np.bincount(xi, yi, 256); n = np.bincount(xi, None, 256); k = n > 50
        lut[c] = np.interp(np.arange(256), np.nonzero(k)[0], s[k] / n[k])
    return lut
apply_curve = lambda a, lut: np.stack([np.interp(a[..., c], np.arange(256), lut[c]) for c in range(3)], -1).astype(np.float32)
m1 = np.clip(ms * g1, 0, 255); lut = curve(m1, mr); m2 = apply_curve(m1, lut)
g2 = blur(mr, 20) / np.maximum(blur(m2, 20), 1)
fix = lambda f: np.clip(apply_curve(np.clip(f * g1, 0, 255), lut) * g2, 0, 255).astype(np.uint8)
h, w = S[0].shape[:2]; fps = cv2.VideoCapture(src).get(cv2.CAP_PROP_FPS)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-i", src,
                      "-map", "0:v", "-map", "1:a", "-sws_flags", "accurate_rnd+full_chroma_int+bitexact", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "copy", out], stdin=subprocess.PIPE)
for f in S: p.stdin.write(fix(f.astype(np.float32)).tobytes())
p.stdin.close(); p.wait()
