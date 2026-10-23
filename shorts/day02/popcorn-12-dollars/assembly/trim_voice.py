"""Rebuild clips/voiceover.mp3 from the raw voice: gaps 0.2 s through line 3, 0.4 s from line 4 onward. No regeneration."""
import subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent / "clips"
# sentence speech spans in the raw file (silencedetect, -35 dB)
S = [(0.0, 2.4278), (3.4964, 4.8997), (5.3150, 6.1821), (6.7911, 10.3776), (10.9901, 11.6809),
     (12.182, 13.9646), (14.7216, 17.1615), (17.9532, 20.7066), (21.3087, 23.8599), (24.5187, 26.64)]
GAP_EARLY, GAP_LATE, LATE_FROM = 0.2, 0.4, 3      # boundary index >= 3 is after line 3 (S4 -> S5 onward)
parts = []
for i, (a, b) in enumerate(S):
    lead = 0 if i == 0 else (GAP_EARLY if i - 1 < LATE_FROM else GAP_LATE) / 2
    tail = 0.05 if i == len(S) - 1 else (GAP_EARLY if i < LATE_FROM else GAP_LATE) / 2
    a2, b2 = a - lead, b + tail
    parts.append(f"[0:a]atrim={a2:.4f}:{b2:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={b2-a2-0.004:.4f}:d=0.004[p{i}]")
fc = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(len(S))) + f"concat=n={len(S)}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(R / "voiceover_raw.mp3"), "-filter_complex", fc, "-map", "[o]",
                "-c:a", "libmp3lame", "-q:a", "2", str(R / "voiceover.mp3")], check=True)
