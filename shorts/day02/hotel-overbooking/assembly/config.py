# Hotel overbooking Short. One shot per script beat; cut ~0.05s before the first word of each beat.
NARR = 28.108  # voiceover length (s); trailing silence ~0.06s
HOOK_END = 3.51  # twin check-in hook is speed-matched to line 1 (cut just before "It is not a mistake")
SHOTS = [(0.00, "hook", None), (3.51, "img02", "in"), (5.98, "img03", "in"), (9.58, "img4a", "out"),
         (12.93, "img4b", "in"), (16.01, "img05", "out"), (17.84, "img06", "in"), (19.40, "img07", "in"),
         (22.50, "img08", "in"), (25.12, "img09", "hold"), (27.22, "img01", "static")]  # last shot = loop frame
HOOK_TEXT = (["YOUR ROOM", "SOLD TWICE?!"], 215, 330, 118)  # lines, y line 1, y line 2, start size
CTA = (25.35, 27.10, ["FOLLOW", "New business story tomorrow"])  # image 9 only, gone before the loop frame
CAP_Y_SHOT = {"img02": 1665}  # captions sit below the card so both SOLD stamps stay readable
