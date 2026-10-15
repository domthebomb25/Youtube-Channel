import cv2, numpy as np, sys, math, os
from scipy import ndimage as ndi
sys.path.insert(0, 'tools')
import tagfix2 as T

FPS = 24
A = 52.0          # max feature shift in px
PERIOD = 0.72
T0, RAMP, TAPER0, TEND = 0.10, 0.25, 1.75, 2.35

def shake_env(t):
    if t < T0 or t >= TEND: return 0.0
    if t < T0 + RAMP: return 0.5 - 0.5 * math.cos(math.pi * (t - T0) / RAMP)
    if t < TAPER0: return 1.0
    return 0.5 + 0.5 * math.cos(math.pi * (t - TAPER0) / (TEND - TAPER0))

def head_shake(im, dx, ang):
    # returns (frame with face features shifted, head interior mask)
    white = (im.min(axis=2) > 236)
    lab, n = ndi.label(white)
    sizes = ndi.sum(white, lab, range(1, n + 1))
    k = int(np.argmax(sizes)) + 1
    comp = lab == k
    M = ndi.binary_fill_holes(comp)
    Min = cv2.erode(M.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(bool)
    ys, xs = np.where(M)
    cx, cy = xs.mean(), ys.mean()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    alpha = np.clip((215.0 - gray) / 130.0, 0, 1) * Min
    # remove the features from the head by inpainting only inside the head
    F = ((alpha > 0.03) & Min).astype(np.uint8)
    F = cv2.dilate(F, np.ones((7, 7), np.uint8))
    y0, y1, x0, x1 = max(0, ys.min() - 5), ys.max() + 5, max(0, xs.min() - 5), xs.max() + 5
    crop = im[y0:y1, x0:x1].copy()
    # fill features with the local head color: use nearest white-ish neighbors via inpaint on a head-only canvas
    canvas = crop.copy()
    canvas[~Min[y0:y1, x0:x1]] = (255, 255, 255)
    ip = cv2.inpaint(canvas, (F[y0:y1, x0:x1] * 255).astype(np.uint8), 6, cv2.INPAINT_TELEA)
    base = im.copy()
    m_ = Min[y0:y1, x0:x1]
    base[y0:y1, x0:x1][m_] = ip[m_]
    feat = (alpha * 255).astype(np.float32)
    Mtx = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
    Mtx[0, 2] += dx
    f2 = cv2.warpAffine(feat, Mtx, (im.shape[1], im.shape[0]), flags=cv2.INTER_LINEAR) / 255.0
    f2 = f2 * Min
    out = base.astype(np.float32) * (1 - f2[..., None])
    return np.clip(out, 0, 255).astype(np.uint8), M


HEAD_K = 0.18    # head translation as a fraction of the face-feature shift
HEAD_ANG = 3.2   # head tilt (deg) about the neck, same direction as the face turn

def head_move(orig, shaken, M, hdx, hang, hdy=0.0):
    """Move the whole head (outline + face) in sync with the face shake. orig = frame before the shake."""
    H = cv2.dilate(M.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (59, 59))).astype(bool)
    ys, xs = np.where(M)
    cx, cy = xs.mean(), ys.mean()
    R = (ys.max() - ys.min()) / 2.0
    h, w = orig.shape[:2]
    y0, y1, x0, x1 = max(0, ys.min() - 60), min(h, ys.max() + 60), max(0, xs.min() - 60), min(w, xs.max() + 60)
    mask_ip = cv2.dilate(H[y0:y1, x0:x1].astype(np.uint8) * 255, np.ones((13, 13), np.uint8))
    # protect the envelope: treat it as unknown while inpainting (so red does not smear), then paste it back on top
    envi = T.find_env(orig)
    prot = np.zeros((h, w), np.uint8)
    if envi is not None:
        lab_full, idx = envi[6], envi[5]
        prot = cv2.dilate((lab_full == idx).astype(np.uint8), np.ones((11, 11), np.uint8))
        mask_ip = np.maximum(mask_ip, cv2.dilate(prot[y0:y1, x0:x1], np.ones((9, 9), np.uint8)) * 255)
    bg = orig.copy()
    bg[y0:y1, x0:x1] = cv2.inpaint(orig[y0:y1, x0:x1], mask_ip, 9, cv2.INPAINT_TELEA)
    alpha = cv2.GaussianBlur(H.astype(np.float32), (0, 0), 1.2)
    Mt = cv2.getRotationMatrix2D((cx, cy + R), hang, 1.0)
    Mt[0, 2] += hdx
    Mt[1, 2] += hdy
    spr = cv2.warpAffine(shaken, Mt, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    al = cv2.warpAffine(alpha, Mt, (w, h), flags=cv2.INTER_LINEAR)
    out = bg.astype(np.float32) * (1 - al[..., None]) + spr.astype(np.float32) * al[..., None]
    out = np.clip(out, 0, 255).astype(np.uint8)
    out[prot.astype(bool)] = orig[prot.astype(bool)]
    return out

BAD = {85: [84, 86], 89: [88], 90: [88, 91]}   # tag detection fails -> union of neighbours' tag masks (shifted)

def main(src_dir, out_dir, n_frames=97):
    os.makedirs(out_dir, exist_ok=True)
    for n in range(1, n_frames + 1):
        im = cv2.imread(f'{src_dir}/{n:03d}.png')
        t = (n - 1) / FPS
        out, env, hull = T.fix_tag(im)
        if n in BAD and env is not None:
            acc = np.zeros(im.shape[:2], np.uint8)
            for k in BAD[n]:
                imk = cv2.imread(f'{src_dir}/{k:03d}.png')
                _, ek, hk = T.fix_tag(imk)
                if ek is None or hk is None:
                    continue
                dx = int(round((env[1] + env[2]) / 2 - (ek[1] + ek[2]) / 2))
                dy = int(round((env[3] + env[4]) / 2 - (ek[3] + ek[4]) / 2))
                M = np.float32([[1, 0, dx], [0, 1, dy]])
                acc |= cv2.warpAffine(hk.astype(np.uint8), M, (im.shape[1], im.shape[0]))
            acc = cv2.dilate(acc, np.ones((9, 9), np.uint8)).astype(bool)
            out = im.copy()
            out[acc] = T.REF.astype(np.uint8)
        im = out
        e = shake_env(t)
        if e > 0:
            s = math.sin(2 * math.pi * (t - T0) / PERIOD)
            fdx, fang = -A * e * s, 5.0 * e * s
            shaken, M = head_shake(im, fdx, fang)
            im = head_move(im, shaken, M, HEAD_K * fdx, HEAD_ANG * e * s)
        cv2.imwrite(f'{out_dir}/{n:03d}.png', im)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
