"""Turn a 3620 s raw rain file into a 3600 s file whose end flows into its start (equal-power crossfade)."""
import sys, wave
import numpy as np
src, dst = sys.argv[1], sys.argv[2]
SR = 44100
w = wave.open(src)
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2)
N, F = 3600 * SR, 10 * SR
out = x[:N].astype(np.float32)
tail = x[N:N + F].astype(np.float32)
th = np.linspace(0, np.pi / 2, F, dtype=np.float32)[:, None]
out[:F] = out[:F] * np.sin(th) + tail * np.cos(th)
o = wave.open(dst, "wb"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR)
o.writeframes(np.clip(out, -32768, 32767).astype(np.int16).tobytes()); o.close()
