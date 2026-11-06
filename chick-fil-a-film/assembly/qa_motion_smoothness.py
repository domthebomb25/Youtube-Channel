"""Frame-by-frame smoothness check for every moved shot: tracks features between consecutive decoded frames,
fits scale + translation per step, and reports speed and the second difference (jerk). Any jitter -> FAIL."""
import json, subprocess, sys, numpy as np, cv2
ROOT = '/home/user/Youtube-Channel/chick-fil-a-film'
sys.path.insert(0, ROOT + '/assembly')
from build_v2_motion import MOVES
def frames(path, f0, n):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'select=between(n\\,{f0}\\,{f0+n-1}),format=gray', '-vsync', '0', '-f', 'rawvideo', '-'], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8); return a.reshape(-1, 1080, 1920)
rows = []
for (sec, beat), (kind, prm) in sorted(MOVES.items()):
    log = json.load(open(f'{ROOT}/sections-v2/SECTION-{sec:02d}-v2-log.json'))[beat - 1]
    F = frames(f'{ROOT}/sections-v2/SECTION-{sec:02d}-v2.mp4', log['frame_start'], log['frames'])
    pts0 = cv2.goodFeaturesToTrack(F[len(F)//2], 600, 0.01, 12)
    S, TX, TY = [], [], []
    for i in range(len(F) - 1):
        a, b = F[i], F[i + 1]
        p0 = cv2.goodFeaturesToTrack(a, 600, 0.01, 12)
        p1, st, _ = cv2.calcOpticalFlowPyrLK(a, b, p0, None, winSize=(41, 41), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.001))
        ok = st.ravel() == 1
        M, _ = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.LMEDS)
        s = np.hypot(M[0, 0], M[1, 0]); S.append(s - 1); TX.append(M[0, 2] + (1 - s) * 960 * 0); TY.append(M[1, 2])
    S, TX, TY = map(np.array, (S, TX, TY))
    # smooth reference (what a perfectly smooth sine-eased move would look like) via a wide moving average; residual = jitter
    def jitter(x, k=9):
        ref = np.convolve(np.pad(x, k // 2, mode='edge'), np.ones(k) / k, mode='valid'); return np.abs(x - ref).max()
    rows.append((sec, beat, kind, len(F), jitter(S), jitter(TX), jitter(TY), np.abs(S).max(), np.abs(TX).max(), np.abs(TY).max()))
    print(f"S{sec:02d}.{beat} {kind:4s} frames={len(F):3d}  jitter: scale {rows[-1][4]:.5f} tx {rows[-1][5]:.3f}px ty {rows[-1][6]:.3f}px | peak speed/frame: scale {rows[-1][7]:.5f} tx {rows[-1][8]:.3f}px ty {rows[-1][9]:.3f}px", flush=True)
