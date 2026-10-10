import cv2, numpy as np, subprocess, sys
ref, src, out = sys.argv[1:4]
def frames(p):
    c = cv2.VideoCapture(p); r = []
    while True:
        ok, f = c.read()
        if not ok: break
        r.append(f.copy())
    return r
def stats(fs):
    l = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.float32) for f in fs[::5]])
    return l.mean((0, 1, 2), dtype=np.float64), l.std((0, 1, 2), dtype=np.float64)
R = frames(ref); S = frames(src); rm, rs = stats(R); sm, ss = stats(S)
h, w = S[0].shape[:2]; fps = cv2.VideoCapture(src).get(cv2.CAP_PROP_FPS)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-i", src,
                      "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "copy", out], stdin=subprocess.PIPE)
for f in S:
    lab = (cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.float32) - sm) / ss * rs + rm
    p.stdin.write(cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).tobytes())
p.stdin.close(); p.wait()
print("ref", rm.round(1), "src", sm.round(1), "new", stats(frames(out))[0].round(1))
