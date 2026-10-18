"""Rain v2: dense splash noise-bursts (no tonal pings) + random-walk intensity.
Usage: rain_audio2.py OUT SECONDS [SEED]"""
import os, subprocess, sys
import numpy as np
from scipy.signal import oaconvolve, lfilter

out_path, secs = sys.argv[1], float(sys.argv[2])
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
SR = 44100
CH = 10 * SR
rng = np.random.default_rng(seed)
DENSITY = float(os.environ.get('DENSITY', 1.0))   # drop count scale
TILT = float(os.environ.get('TILT', 0.0))         # <0 darker/softer, >0 brighter
DROPS = float(os.environ.get('DROPS', 1.0))       # big sill/roof drop level
CANOPY = float(os.environ.get('CANOPY', 0.0))     # soft drips falling from branches
WIND = float(os.environ.get('WIND', 0.0))         # wind swells through the pines

def burst_kernel(f, octaves, tau_ms, rng):
    """short noise burst, band-limited around f, exponentially decaying"""
    L = int(SR * tau_ms * 6 / 1000)
    t = np.arange(L) / SR
    x = rng.standard_normal(L) * np.exp(-t / (tau_ms / 1000))
    X = np.fft.rfft(x, 4096)
    fr = np.fft.rfftfreq(4096, 1 / SR)
    g = np.exp(-0.5 * ((np.log2(np.maximum(fr, 1) / f)) / (octaves / 2)) ** 2)
    k = np.fft.irfft(X * g, 4096)[:L]
    return k / (np.sqrt(np.sum(k ** 2)) + 1e-9)

# kernel bank: (kernel, events/sec, weight)
bank = []
for f in np.geomspace(350, 9000, 22):
    for _ in range(2):                                   # two random kernels per band so no two drops sound identical
        tau = float(np.clip(5.0 * (1000 / f) ** 0.5, 0.8, 9.0))
        k = burst_kernel(f * rng.uniform(0.85, 1.15), rng.uniform(0.9, 1.6), tau * rng.uniform(0.7, 1.4), rng)
        rate = DENSITY * 190.0 * (f / 2000) ** -0.15
        w = (f / 2000) ** (0.3 + TILT)
        bank.append((k, rate, w))
# bigger, slower drops on the sill / roof / leaves
for f, tau, rate, w in [(1400, 14, 9, 2.0), (900, 25, 4, 2.2), (2500, 9, 12, 1.6), (220, 40, 1.2, 1.4), (160, 55, 0.5, 1.6)]:
    bank.append((burst_kernel(f, 1.2, tau, rng), rate * DROPS, w))

# soft drips falling from pine branches onto needles, ground and roof (round, low, never sharp)
for f, tau, rate, w in [(650, 22, 5.0, 1.6), (480, 30, 3.0, 1.7), (1100, 14, 6.0, 1.2), (320, 45, 1.5, 1.5)]:
    if CANOPY > 0:
        bank.append((burst_kernel(f, 1.4, tau, rng), rate * CANOPY, w))

LMAX = max(len(k) for k, _, _ in bank)

def smooth_walk(n, tc_s, rng_):
    """slowly wandering gain around 1.0 (random, not periodic)"""
    a = np.exp(-1 / (tc_s * SR))
    x = lfilter([1 - a], [1, -a], rng_.standard_normal(n))
    return x

class Chan:
    def __init__(s, seed_):
        s.r = np.random.default_rng(seed_)
        s.tail = np.zeros(LMAX)
        s.zi_g1 = np.zeros(1); s.zi_g2 = np.zeros(1)
        s.zi_lo = np.zeros(2)
        s.zi_w = [np.zeros(1) for _ in range(5)]
    def chunk(s, n):
        y = np.zeros(n + LMAX)
        for k, rate, w in bank:
            cnt = s.r.poisson(rate * n / SR)
            if not cnt:
                continue
            pos = s.r.integers(0, n, cnt)
            amp = s.r.lognormal(0, 0.9, cnt) * s.r.choice([-1, 1], cnt) * w
            tr = np.zeros(n)
            np.add.at(tr, pos, amp)
            c = oaconvolve(tr, k)
            y[:len(c)] += c[:n + LMAX]
        y[:LMAX] += s.tail
        s.tail = y[n:n + LMAX].copy()
        y = y[:n]
        # random-walk loudness: ~+-2.5 dB wander over tens of seconds, plus gentle gusts
        a1 = np.exp(-1 / (45 * SR)); a2 = np.exp(-1 / (9 * SR))
        g1, s.zi_g1 = lfilter([1 - a1], [1, -a1], s.r.standard_normal(n) * 6.0, zi=s.zi_g1)
        g2, s.zi_g2 = lfilter([1 - a2], [1, -a2], s.r.standard_normal(n) * 3.0, zi=s.zi_g2)
        gain = np.exp(0.16 * np.clip(g1, -3, 3) + 0.07 * np.clip(g2, -3, 3))
        y = y * gain
        if WIND > 0:
            a_lp = np.exp(-2 * np.pi * 650 / SR)
            w = s.r.standard_normal(n)
            w, s.zi_w[0] = lfilter([1 - a_lp], [1, -a_lp], w, zi=s.zi_w[0])
            w, s.zi_w[1] = lfilter([1 - a_lp], [1, -a_lp], w, zi=s.zi_w[1])
            a_g = np.exp(-1 / (14 * SR))
            g, s.zi_w[2] = lfilter([1 - a_g], [1, -a_g], s.r.standard_normal(n) * 6.0, zi=s.zi_w[2])
            a_g2 = np.exp(-1 / (3.5 * SR))
            g2, s.zi_w[3] = lfilter([1 - a_g2], [1, -a_g2], s.r.standard_normal(n) * 3.0, zi=s.zi_w[3])
            gust = np.clip(0.35 + 0.55 * g + 0.25 * g2, 0.05, 1.6) ** 2     # swells come and go, never constant
            w = w / (np.sqrt(np.mean(w ** 2)) + 1e-9)
            y = y + w * gust * np.sqrt(np.mean(y ** 2)) * 0.55 * WIND
        return y

chans = [Chan(seed * 10 + 1), Chan(seed * 10 + 2)]

# calibrate loudness on a throwaway run
cal = [Chan(999), Chan(998)]
c0 = np.stack([c.chunk(15 * SR) for c in cal], axis=1)
gain0 = 0.065 / np.sqrt(np.mean(c0 ** 2))

af = "highpass=f=60,lowpass=f=12000"
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", af]
cmd += ["-c:a", "pcm_s16le"] if out_path.endswith(".wav") else ["-c:a", "aac", "-b:a", "192k"]
cmd += [out_path]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
total = int(secs * SR)
done = 0
while done < total:
    n = min(CH, total - done)
    y = np.stack([c.chunk(n) for c in chans], axis=1) * gain0
    proc.stdin.write((0.5 * np.tanh(y / 0.5)).astype(np.float32).tobytes())
    done += n
proc.stdin.close()
proc.wait()
