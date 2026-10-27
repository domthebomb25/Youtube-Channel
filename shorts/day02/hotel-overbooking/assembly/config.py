# Hotel overbooking Short. One shot per script beat; cut ~0.05s before the first word of each beat.
# Times follow the voice after the gap trims in lines 1-3 (line 3 now ends at 8.93s).
NARR = 27.488  # voiceover length (s); trailing silence ~0.05s
HOOK_END = 3.22  # twin check-in hook is speed-matched to line 1 (cut just before "It is not a mistake")
SHOTS = [(0.00, "hook", None), (3.22, "img02", "in"), (5.36, "img03", "in"), (8.96, "img4a", "out"),
         (12.31, "img4b", "in"), (15.39, "img05", "out"), (17.22, "img06", "in"), (18.78, "img07", "in"),
         (21.88, "img08", "in"), (24.50, "img09", "hold"), (26.60, "img01", "static")]  # last shot = loop frame
HOOK_TEXT = (["YOUR ROOM", "SOLD TWICE?!"], 215, 330, 118)  # lines, y line 1, y line 2, start size
CTA = (24.73, 26.48, ["FOLLOW", "New business story tomorrow"])  # image 9 only, gone before the loop frame
CAP_Y_SHOT = {"img02": 1665}  # captions sit below the card so both SOLD stamps stay readable
