"""Find ONE winding route over the open (blue) floor of the arrow-free maze still and overlay
same-direction yellow arrows along it. Usage: draw_path.py clean.png out.png"""
import heapq, math, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt, binary_opening
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB"); W, H = im.size
a = np.asarray(im).astype(int)
blue = (abs(a[..., 0] - 4) < 40) & (abs(a[..., 1] - 82) < 40) & (abs(a[..., 2] - 201) < 40)
blue[:420] = False                     # top third (and sky) is not floor
blue = binary_opening(blue, iterations=3)
dist = distance_transform_edt(blue)
K = 4
dg = dist[::K, ::K]; ok = dg > 10 / K * 1.0
cost = np.where(ok, 1.0 + 60.0 / (dg + 1), np.inf)
def snap(p):
    x, y = p[0] // K, p[1] // K
    ys, xs = np.nonzero(ok); i = np.argmin((xs - x) ** 2 + (ys - y) ** 2); return int(xs[i]), int(ys[i])
def astar(s, t):
    h = lambda p: math.dist(p, t)
    pq = [(h(s), 0, s)]; g = {s: 0}; prev = {}
    while pq:
        _, gc, u = heapq.heappop(pq)
        if u == t: break
        if gc > g[u]: continue
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx and not dy: continue
                v = (u[0] + dx, u[1] + dy)
                if not (0 <= v[0] < ok.shape[1] and 0 <= v[1] < ok.shape[0]) or not np.isfinite(cost[v[1], v[0]]): continue
                ng = gc + cost[v[1], v[0]] * math.hypot(dx, dy)
                if ng < g.get(v, 1e18): g[v] = ng; prev[v] = u; heapq.heappush(pq, (ng + h(v), ng, v))
    p = [t]
    while p[-1] != s: p.append(prev[p[-1]])
    return p[::-1]
VIA = [(20, 1300), (330, 1030), (400, 905), (490, 600)]  # bottom-left entry, up the centre corridor, beside mascot, out the top
nodes = [snap(p) for p in VIA]
route = []
for s, t in zip(nodes, nodes[1:]): route += astar(s, t)[:-1]
route.append(nodes[-1])
pts = np.array([(x * K + K / 2, y * K + K / 2) for x, y in route], float)
for _ in range(25):                        # smooth
    pts[1:-1] = (pts[:-2] + 2 * pts[1:-1] + pts[2:]) / 4
cum = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
def at(s):
    i = min(np.searchsorted(cum, s), len(cum) - 1); i = max(i, 1)
    f = (s - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-6); p = pts[i - 1] + (pts[i] - pts[i - 1]) * f
    j = min(i + 3, len(pts) - 1); k = max(i - 4, 0); v = pts[j] - pts[k]
    return p, math.atan2(v[1], v[0])
SS, SQ = 2, 0.7
big = im.resize((W * SS, H * SS), Image.LANCZOS); d = ImageDraw.Draw(big)
L, HW, SH = 78, 30, 10
shape = [(-L / 2, -SH), (L / 8, -SH), (L / 8, -HW), (L / 2, 0), (L / 8, HW), (L / 8, SH), (-L / 2, SH)]
s = 50
while s < cum[-1] - 45:
    (x, y), ang = at(s)
    q = [((x + px * math.cos(ang) - py * math.sin(ang)) * SS, (y + (px * math.sin(ang) + py * math.cos(ang)) * SQ) * SS) for px, py in shape]
    d.polygon(q, fill=(255, 205, 0)); d.line(q + [q[0]], fill=(0, 0, 0), width=4 * SS)
    s += 105
big.resize((W, H), Image.LANCZOS).save(out)
