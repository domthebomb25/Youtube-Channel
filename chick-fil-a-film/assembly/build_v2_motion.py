"""Motion pass v2: rebuild every section from the source stills with restrained movement.
Timings/pictures come from sections/SECTION-NN-log.json; audio is stream-copied from the locked SECTION-NN-FINAL.mp4.
Moves are rendered per frame with float (sub-pixel) affine sampling from a 2x canvas - no zoompan integer stepping."""
import json, os, subprocess, sys, shutil, numpy as np, cv2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEC, OUT = f'{ROOT}/sections', f'{ROOT}/sections-v2'
IMG = f'{ROOT}/images/'
WORK = os.environ.get('V2WORK', '/tmp/v2work')
OVERRIDE = {'CF-008.jpg': f'{ROOT}/review/CF-008-v5-lines-down.png',
            'CF-044B.jpg': f'{ROOT}/review/CF-044B-v7-clean-red-and-wall.png'}
FPS, OW, OH = 30, 1920, 1080
CW, CH = OW * 2, OH * 2            # 2x canvas
# (section, beat): (kind, params)  -- every entry must be justified in MOVES.md
MOVES = {
 (1, 8):  ('push', dict(zend=1.05, target=(0.52, 0.58))),
 (3, 7):  ('push', dict(zend=1.05, target=(0.78, 0.55))),
 (4, 7):  ('pan',  dict(z=1.07, direction='right')),
 (9, 1):  ('pan',  dict(z=1.07, direction='down')),
 (10, 3): ('push', dict(zend=1.05, target=(0.45, 0.38))),
 (12, 7): ('push', dict(zend=1.05, target=(0.72, 0.45))),
 (16, 1): ('pan',  dict(z=1.07, direction='up')),
 (17, 6): ('push', dict(zend=1.05, target=(0.55, 0.40))),
}
def ease(t): return 0.5 - 0.5 * np.cos(np.pi * t)          # sine in-out: zero speed at both ends
def load_canvas(p):
    im = cv2.imread(OVERRIDE.get(p, IMG + p), cv2.IMREAD_COLOR)
    return cv2.resize(im, (CW, CH), interpolation=cv2.INTER_LANCZOS4)
def render(canvas, z, cx, cy):
    w, h = CW / z, CH / z
    cx = min(max(cx, w / 2), CW - w / 2); cy = min(max(cy, h / 2), CH - h / 2)
    tlx, tly = cx - w / 2, cy - h / 2
    s = 1.0 / (OW / w)                                       # canvas px per output px
    M = np.array([[s, 0, tlx + 0.5 * s - 0.5], [0, s, tly + 0.5 * s - 0.5]], np.float64)
    return cv2.warpAffine(canvas, M, (OW, OH), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
def path(kind, prm, n):
    C = np.array([CW / 2, CH / 2])
    for i in range(n):
        e = ease(i / max(n - 1, 1))
        if kind == 'push':
            z = 1 + (prm['zend'] - 1) * e
            f = np.array(prm['target']) * [CW, CH]
            wend, hend = CW / prm['zend'], CH / prm['zend']
            cend = C + 0.6 * (f - C)
            cend = np.array([min(max(cend[0], wend / 2), CW - wend / 2), min(max(cend[1], hend / 2), CH - hend / 2)])
            c = C + e * (cend - C)
        else:
            z = prm['z']; w, h = CW / z, CH / z
            lo = np.array([w / 2, h / 2]); hi = np.array([CW - w / 2, CH - h / 2])
            a, b = C.copy(), C.copy()
            d = prm['direction']
            if d == 'right': a[0], b[0] = lo[0], hi[0]
            if d == 'left':  a[0], b[0] = hi[0], lo[0]
            if d == 'down':  a[1], b[1] = lo[1], hi[1]
            if d == 'up':    a[1], b[1] = hi[1], lo[1]
            c = a + e * (b - a)
        yield z, c[0], c[1]
def enc_cmd(out):
    return ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{OW}x{OH}', '-r', str(FPS), '-i', '-',
            '-vf', 'format=yuv420p', '-c:v', 'libx264', '-crf', '15', '-preset', 'medium', '-r', str(FPS), out]
def build(sec):
    log = json.load(open(f'{SEC}/SECTION-{sec:02d}-log.json'))
    wd = f'{WORK}/s{sec:02d}'; os.makedirs(wd, exist_ok=True)
    clips, outlog = [], []
    for b in log:
        n, pic = b['frames'], b['picture']
        o = f'{wd}/c{b["beat"]:02d}.mp4'
        canvas = load_canvas(pic)
        mv = MOVES.get((sec, b['beat']))
        p = subprocess.Popen(enc_cmd(o), stdin=subprocess.PIPE)
        if mv is None:
            fr = render(canvas, 1.0, CW / 2, CH / 2).tobytes()
            for _ in range(n): p.stdin.write(fr)
        else:
            for z, cx, cy in path(mv[0], mv[1], n): p.stdin.write(render(canvas, z, cx, cy).tobytes())
        p.stdin.close(); assert p.wait() == 0
        clips.append(o)
        outlog.append({'beat': b['beat'], 'picture': pic, 'frame_start': b['frame_start'], 'frames': n,
                       'move': 'still' if mv is None else f'{mv[0]} {mv[1]}'})
    open(f'{wd}/list.txt', 'w').write(''.join(f"file '{c}'\n" for c in clips))
    final = f'{OUT}/SECTION-{sec:02d}-v2.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-i', f'{SEC}/SECTION-{sec:02d}-FINAL.mp4',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-movflags', '+faststart', final], check=True)
    json.dump(outlog, open(f'{OUT}/SECTION-{sec:02d}-v2-log.json', 'w'), indent=1)
    return final
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for s in [int(a) for a in sys.argv[1:]] or range(1, 19): print(build(s), flush=True)
