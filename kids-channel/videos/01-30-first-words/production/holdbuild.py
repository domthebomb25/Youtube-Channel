"""Builds the 3.4 s 'wait' hold for a teach line: the clip's last frame, held, with 2 blinks.
Only the eye area from the closed / half-closed edits is pasted in, after aligning the edit to the frame,
so nothing else in the picture changes.  python3 holdbuild.py 000 [002 ...]"""
import cv2, numpy as np, sys, os
os.makedirs('holdclips', exist_ok=True)

def align(src, ref):
    s = cv2.resize(src, (ref.shape[1], ref.shape[0]))
    g1 = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY).astype(np.float32); g2 = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY).astype(np.float32)
    W = np.eye(2, 3, dtype=np.float32)
    try:
        _, W = cv2.findTransformECC(g1, g2, W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
    except cv2.error:
        pass
    return cv2.warpAffine(s, W, (ref.shape[1], ref.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)

def eye_mask(ref, closed):
    h, w = ref.shape[:2]
    d = cv2.absdiff(ref, closed).max(axis=2).astype(np.float32)
    d = cv2.GaussianBlur(d, (0, 0), 3)
    roi = np.zeros_like(d); roi[int(h*0.05):int(h*0.6), int(w*0.25):int(w*0.75)] = 1   # face area only
    d *= roi
    m = (d > max(18, d.max() * 0.35)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = sorted(range(1, n), key=lambda i: -st[i, cv2.CC_STAT_AREA])[:2]          # the two eyes
    mask = np.zeros((h, w), np.float32)
    for i in keep:
        x, y, bw, bh = st[i, :4]
        cv2.ellipse(mask, (int(x + bw/2), int(y + bh/2)), (int(bw*0.75) + 6, int(bh*0.85) + 6), 0, 0, 360, 1, -1)
    return cv2.GaussianBlur(mask, (0, 0), 6)[..., None], keep

for n in sys.argv[1:]:
    ref = cv2.imread(f'holds/hold-{n}.png')
    c = align(cv2.imread(f'blinks/b-{n}-closed.png'), ref)
    hf = align(cv2.imread(f'blinks/b-{n}-half.png'), ref)
    m, keep = eye_mask(ref, c)
    C = (ref * (1 - m) + c * m).astype(np.uint8); H = (ref * (1 - m) + hf * m).astype(np.uint8)
    cv2.imwrite(f'holdclips/eyes-{n}-closed.png', C); cv2.imwrite(f'holdclips/eyes-{n}-half.png', H)
    seq = [ref] * 102
    for start in (27, 72):
        for k, f in enumerate([H, H, C, C, C, H, H]): seq[start + k] = f
    vw = cv2.VideoWriter(f'holdclips/tmp-{n}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (ref.shape[1], ref.shape[0]))
    for f in seq: vw.write(f)
    vw.release()
    os.system(f"ffmpeg -v error -y -i holdclips/tmp-{n}.mp4 -vf scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30,format=yuv420p -c:v libx264 -crf 18 holdclips/hold-{n}.mp4 && rm holdclips/tmp-{n}.mp4")
    print(n, "eye blobs", len(keep))
