import sys, cv2, numpy as np
src, dst, r0, r1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
img = cv2.imread(src); H, W = img.shape[:2]
# barrier mask: allow flood only in rows r0+7 .. r1 (the beige strip)
barrier = np.ones((H+2, W+2), np.uint8)
barrier[r0+7+1:r1+1+1, 1:W+1] = 0
fm = np.zeros((H, W), np.uint8)
seeds=[(x,y) for x in range(20, W-20, 40) for y in (r0+30, r0+80, r0+140, r1-60, r1-20)]
for x,y in seeds:
    b, g, r = [int(v) for v in img[y, x]]
    if r > 200 and 10 <= r - b <= 45 and r - g <= 25:   # beige, not white
        m = barrier.copy()
        cv2.floodFill(img.copy(), m, (x, y), (0,0,0), (10,10,10), (10,10,10), 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
        fm |= ((m[1:-1, 1:-1] == 255) & (barrier[1:-1, 1:-1] == 0)).astype(np.uint8)
# far-edge dark line rows: remove only where cabinet red sits directly above the line and beige strip directly below
lm = np.zeros((H, W), np.uint8)
for x in range(W):
    col = np.nonzero(fm[r0:r1+1, x])[0]
    if len(col) == 0: continue
    t = r0 + int(col[0])
    ab = img[t-10, x]
    if ab[2] > 120 and ab[1] < 90:   # red cabinet above, beige strip below -> the dark edge line goes too
        lm[t-9:t, x] = 1
mask = (fm | lm)
# also remove light antialias fringe next to outlines (but never dark outline pixels)
lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
d = cv2.dilate(mask, np.ones((5,5), np.uint8))
fringe = (d == 1) & (mask == 0) & (lum > 90)
rows = np.zeros((H, W), bool); rows[r0-1:r1, :] = True
mask = ((mask == 1) | fringe) & rows
# reference cabinet colour per column from rows just above the edge line, flattened horizontally
ref = np.zeros((W, 3), np.float32); ok = np.zeros(W, bool)
for x in range(W):
    px = img[r0-14:r0-5, x].astype(int)
    red = px[(px[:,2] > 120) & (px[:,1] < 90)]
    if len(red): ref[x] = np.median(red, axis=0); ok[x] = True
idx = np.arange(W); ref = np.stack([np.interp(idx, idx[ok], ref[ok, c]) for c in range(3)], 1)
k = 121
ref = np.stack([np.convolve(np.pad(ref[:, c], k//2, mode='edge'), np.ones(k)/k, mode='valid') for c in range(3)], 1)
if len(sys.argv) > 5 and sys.argv[5] == 'flat':
    ref[:] = np.median(ref[60:380], axis=0)
out = img.copy()
ys, xs = np.nonzero(mask)
out[ys, xs] = ref[xs].astype(np.uint8)
if len(sys.argv) > 6 and sys.argv[5] == 'tile':
    bx0, bx1, ct = int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
    block = img[ct:r0-3, bx0:bx1].copy(); bh, bw = block.shape[:2]
    out[ys, xs] = block[(ys - ct) % bh, (xs - bx0) % bw]
# soften the filled area edge slightly
cv2.imwrite(dst, out, [cv2.IMWRITE_JPEG_QUALITY, 95] if dst.endswith('.jpg') else [])
print(dst, 'masked px', int(mask.sum()))
