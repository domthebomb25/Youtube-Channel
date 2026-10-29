# Airports Short (Compilation #4 posting) - cut map from the render paste. Times in seconds on the VO timeline.
NARR = 30.4327          # airports-vo.mp3 length; video ends as the voice ends (trailing silence ~0)
HOOK_SEC = 2.895        # hook clip (take 2) trimmed at its tail to the line-1 slot, natural speed
SHOTS = [(0.0, "hook", "static"),
         (2.895, "s2", "hold"), (5.207, "s3", "hold"), (8.944, "s4", "hold"),
         (11.21, "s5", "hold"),            # line 4 split at the dash pause ("leave -" | "and shops")
         (13.507, "s6", "hold"),
         (15.99, "s7", "hold"),            # line 5 split at the dash pause ("longer -" | "and every")
         (18.217, "s8", "hold"),
         (22.69, "s9", "hold"),            # line 6 split at the dash pause ("there -" | "more than")
         (26.096, "s10", "hold"),
         (29.80, "loop", "static")]        # loop frame = img1_final.png, clean, closes as the voice ends
HOOK_TEXT = ["THE AIRPORT TRAPPED", "YOU INSIDE A MALL", "— ON PURPOSE."]   # line 1 of the script, left-aligned clear of the speech bubble
HOOK_TEXT_X, HOOK_TEXT_Y = 70, 270
SHAKE_FRAMES, BLAST_FRAME = (33, 34), 35      # shake ~1.10s (2 frames), blast up at 1.17s, gone from frame 36 (1.20s)
CAP_Y = {"s3": 1560, "s9": 1560}               # captions moved down off the in-image money tags
FOLLOW = (26.096, 29.80, "FOLLOW", "New business story tomorrow")
# spoken words -> caption words (script shows digits; spoken form is spelled out)
MERGE = [(("six", "billion", "dollars"), ["$6", "BILLION"]),
         (("four", "point", "three", "billion", "dollars"), ["$4.3", "BILLION"])]
