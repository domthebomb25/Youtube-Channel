# YOUTUBE SHORTS 10/10 TEMPLATE (user's template — use for EVERY Short; it overrides older format notes)

## VIDEO SPECS (NON-NEGOTIABLE)
- Total length: 31-34 seconds, 100-110 words, 160 wpm
- 10 images total: 1 animated hook + 9 static
- 3.2 sec per image
- Vertical 9:16
- STICKMAN style (user decision Oct 14 2026: keep the channel's stickman theme; this replaces Pixar 3D everywhere below). Reference: the stickman anchor / mascot in the playbook image recipe

## STRUCTURE (3 PARTS)

### PART 1 — PAYOFF HOOK [0-1.5s] ANIMATED
- Line: tell the ending first. Format: "[Company] [did X shocking thing]".
- Example: "Blockbuster could have bought Netflix for $50M"
- Must include a number + the payoff.
- PROMPT TEMPLATE: Stickman cartoon [character] [action] [emotion], [key object with text], [background], dramatic close up, cinematic lighting, vertical 9:16 --animate

### PART 2 — BUILD [1.5-28s] 8 IMAGES
- Image 2 [3-6s]: Context fact + number
- Image 3 [6-9s]: How the business model works + number
- Image 4 [9-13s]: OPEN LOOP — line: "But that's not the dumbest part" or "That's when it gets worse"
- Image 5 [13-17s]: WTF fact (pattern interrupt) + number
- Image 6 [17-21s]: Villain + stakes ($ per day lost)
- Image 7 [21-25s]: Attempted fix / startup / solution
- Image 8 [25-28s]: Consequence / lawsuit / ban (verifiable only)
- Each PROMPT TEMPLATE: Stickman cartoon [subject], [action], [key text/number on object], [background], studio lighting, vertical 9:16

### PART 3 — LOOP ENDING [28-33s] 1 IMAGE
- Line: must be word-for-word the same as the Hook line (first 1.5 s line) so the Short loops.
- Example: first line = "Blockbuster could have bought Netflix for $50M" -> last line = "So yeah, Blockbuster could have bought Netflix for $50M"
- PROMPT: same scene as the hook, zoomed out, loops back.

---
## How Claude applies this template (interpretations; user may correct)
1. **Style (updated Oct 14): STAY STICKMAN.** The user wants to keep the stickman theme, so ignore the Pixar wording in this file and use the playbook's stickman image recipe. (Older note, superseded: Pixar 3D.) Day 0 and Day 01 Shorts stay stickman. Because there is no 3D style reference yet, the first image of the first Short made this way becomes the style reference for the rest (plain background, "art style only").
2. **Image count:** 10 images per Short (1 animated hook + 9 static), not 12. Image 10 = the loop-ending image (hook scene zoomed out).
3. **Length vs words:** the 31-34 s length is the hard spec. Benji reads about 185 wpm, so aim for roughly 98-108 words and check the real voiceover length (`ffprobe`) lands at 31-34 s; trim or add words if not.
4. **Timing:** each image is held about 3.2 s; cut on the first word of each beat from `word_timing.json`. The hook line is spoken first; the animated hook clip covers the first shot (stretched to the first cut).
5. **Hook animation:** `--animate` is generic shorthand. Use Higgsfield Kling `kling3_0`, std, sound off, 4 s, 6 credits, start image = hook image.
6. **Loop line:** the ending repeats the hook line exactly, with "So yeah," in front. The hook line itself must not change between the first and last line.
7. **Numbers/facts:** every beat needs a number where the template asks for one; all must be verified with sources (image 8 is "verifiable only"). The hook must include a number and a payoff. Never invent numbers; if a story has no honest number for a beat, flag it and ask.
8. **Cost per Short with this template:** voiceover ~1.8 + 10 images x 0.25 = 2.5 + hook 6 = about 10.3 credits.
