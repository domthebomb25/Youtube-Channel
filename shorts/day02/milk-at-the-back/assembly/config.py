NARR = 25.63
END_SEC = 0.0   # voice already ends clean; no trailing silence
# cuts on narration word starts (word_timing.json); hook clip speed-matched to FIRST_CUT
SHOTS = [(0.0, "hook", None), (2.38, "img2", "in"), (4.65, "img3", "in"), (7.50, "img4a", "in"), (10.70, "img4b", "out"),
         (13.64, "img5", "in"), (15.42, "img6", "in"), (17.15, "img7", "out"), (20.10, "img8", "in"),
         (22.65, "img9", "hold"), (24.51, "img1", "still")]
# on-screen text pops (t0, t1, [lines], first-line color, y, size). CTA only on image 9; loop frame stays clean.
TEXT = [(22.65, 24.51, ["FOLLOW FOR TOMORROW'S STORY", "New business story tomorrow"], YEL, 1500, 50)]
# hook: game banner above the objective marker; shake then blast up
HOOK_LINES = []   # hook text removed; the banner alone sits above the objective marker
HOOK_BANNER = ("NEW QUEST:", "GET THE MILK")
HOOK_BANNER_POS = (545, 205, 295)   # banner centre x (over the marker), top y, bottom y
HOOK_SHAKE, HOOK_BLAST, HOOK_GONE = 1.00, 1.07, 1.20
BURST = (1.66, 2.38, (0.52, 0.41))   # starburst rays on the trophy-pose frames: t0, t1, jug centre
