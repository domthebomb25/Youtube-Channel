"""Synthesized rocket whoosh + rumble for the hook's silent tail (about 2.5-4.0 s). No samples, no licensing."""
import sys, numpy as np, wave
SR = 48000
dur = 4.0
n = int(SR * dur)
t = np.arange(n) / SR
rng = np.random.default_rng(7)
start, peak, end = 2.45, 3.25, 4.0
env = np.zeros(n)
rise = (t >= start) & (t < peak); fall = (t >= peak) & (t <= end)
env[rise] = ((t[rise] - start) / (peak - start)) ** 1.8
env[fall] = np.cos((t[fall] - peak) / (end - peak) * np.pi / 2) ** 1.6
# whoosh: white noise through a low-pass whose cutoff sweeps upward, then back down
x = rng.standard_normal(n)
cut = np.interp(t, [start, peak, end], [0.015, 0.45, 0.10])
y = np.zeros(n); prev = 0.0
for i in range(n):
    prev += cut[i] * (x[i] - prev); y[i] = prev
y = y / (np.max(np.abs(y)) + 1e-9)
# rumble: low sine + very low-passed noise
rum = np.sin(2 * np.pi * (48 + 22 * env) * t) * 0.7
lp = np.zeros(n); p2 = 0.0; z = rng.standard_normal(n)
for i in range(n):
    p2 += 0.01 * (z[i] - p2); lp[i] = p2
lp = lp / (np.max(np.abs(lp)) + 1e-9)
sig = (0.75 * y + 0.55 * (rum * 0.6 + lp * 0.8)) * env
sig = sig / (np.max(np.abs(sig)) + 1e-9) * 0.30   # about -10 dBFS peak, well under the speech peak
st = np.stack([sig, np.roll(sig, 40)], axis=1)     # tiny delay on one side for width
pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", sys.argv[1])
