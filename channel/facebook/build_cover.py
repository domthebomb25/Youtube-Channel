import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W, _ = im.shape
ys, xs = np.mgrid[0:H, 0:W]
X, Y = xs / W, ys / H
# Background mask: bright, low-saturation-ish pixels far from dark lines
lum = im.mean(2)
bgmask = lum > 120
# exclude yellow tie / blue text (saturated, darker)
sat = im.max(2) - im.min(2)
bgmask &= ~((sat > 90) & (lum < 200))
# Fit smooth 2D polynomial background per channel
def feats(X, Y):
    return np.stack([np.ones_like(X), X, Y, X*X, X*Y, Y*Y, X**3, X*X*Y, X*Y*Y, Y**3], -1)
F = feats(X, Y)
idx = np.where(bgmask.ravel())[0][::7]
A = F.reshape(-1, F.shape[-1])[idx]
bg = np.zeros_like(im)
for c in range(3):
    coef, *_ = np.linalg.lstsq(A, im[..., c].ravel()[idx], rcond=None)
    bg[..., c] = F @ coef
bg = np.clip(bg, 0, 255)
# left side is pure white in the original (figure area); keep it white
# foreground alpha from difference to background
diff = np.abs(im - bg).max(2)
alpha_full = np.clip((diff - 10) / 40, 0, 1)

def piece(x0, y0, x1, y1, scale, fill_white=False):
    rgb = Image.fromarray(im[y0:y1, x0:x1].astype(np.uint8))
    a = alpha_full[y0:y1, x0:x1].copy()
    if fill_white:
        # figure: fill interior (white face/shirt) so background doesn't show through
        from scipy import ndimage
        solid = a > 0.5
        filled = ndimage.binary_fill_holes(solid)
        # bottom edge is open (body runs off-canvas): close it before filling
        closed = solid.copy(); closed[-1, :] = True
        filled |= ndimage.binary_fill_holes(closed) & ~np.zeros_like(solid)
        a = np.maximum(a, ndimage.gaussian_filter(filled.astype(np.float32), 1))
    A = Image.fromarray((a * 255).astype(np.uint8))
    w, h = int((x1 - x0) * scale), int((y1 - y0) * scale)
    rgb = rgb.resize((w, h), Image.LANCZOS); A = A.resize((w, h), Image.LANCZOS)
    rgb.putalpha(A); return rgb

canvas = Image.fromarray(bg.astype(np.uint8)).convert('RGBA')
# Figure: anchored to bottom, head inside the desktop safe band (y 150-774)
fig = piece(95, 80, 750, 924, 0.84, fill_white=True)
canvas.alpha_composite(fig, (150, 924 - fig.height))
# Headline + "In 30 Seconds"
txt = piece(790, 90, 1560, 725, 0.74)
tx, ty = 830, 182
canvas.alpha_composite(txt, (tx, ty))
row_y = ty + txt.height + 22
# handle (left) and icons (right) on one row under the headline
handle = piece(785, 868, 1052, 912, 0.95)
icons = piece(1095, 745, 1510, 862, 0.55)
canvas.alpha_composite(icons, (tx + txt.width - icons.width, row_y))
canvas.alpha_composite(handle, (tx + 4, row_y + (icons.height - handle.height) // 2))
print('text bottom row ends at y =', row_y + icons.height)
canvas.convert('RGB').save(out, quality=95)
