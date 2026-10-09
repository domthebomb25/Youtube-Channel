"""Builds Grok lite motion-clip requests for the narration (VO) lines: python3 objreq.py 4 7 ..."""
import json, sys, subprocess, math
m = json.load(open('manifest.json')); names = json.load(open('image_index.json')); jobs = json.load(open('img_jobs.json'))
MOTION = {
 4:  "The mommy gently hugs and rocks her baby, both smiling, a soft pink heart floats up and sparkles.",
 7:  "The daddy lifts the giggling baby up, up, up high into the air, the baby laughs and kicks happily.",
 10: "The baby pulls the blanket down and peeks out with a big happy surprised face, peekaboo.",
 13: "The little yellow duck waves its wing goodbye, then turns and waddles slowly away across the rug.",
 23: "The picture book slowly opens wider, pages gently turning, a soft magical sparkle rises from the pages.",
 26: "The shiny soap bubbles float gently, then pop one by one with tiny sparkles.",
 29: "The tall block tower wobbles more and more, then topples over softly onto the rug.",
 34: "The puppy wags its tail happily, tilts its head and barks, woof woof, bouncing on its front paws.",
 37: "The kitten stretches, yawns wide, then sits up and meows sweetly.",
 40: "The cow lifts its head, chews, then opens its mouth wide and moos happily.",
 43: "The little duck splashes and flaps its wings in the pond, quacking happily.",
 46: "The orange fish swims happily side to side, blowing little bubbles.",
 50: "A gentle splash of milk swirls in the cup, little droplets sparkling.",
 53: "The apple wobbles and a happy crunchy bite sparkle pops out, small crumbs bouncing.",
 56: "The banana peel slowly opens down, one strip at a time, peel, peel, peel.",
 59: "The cookie wobbles, then a bite disappears with a few crumbs bouncing, munch munch.",
 62: "The spoon scoops the orange food and lifts it up toward the camera, open wide.",
 66: "The soap bubbles pop one by one until there are no bubbles left, the playroom quiet.",
 69: "The red balloon floats up, up, up into the sunny blue sky past fluffy clouds.",
 72: "The smiling toy train wiggles and puffs a little steam, getting ready to go but staying in place.",
 75: "The empty plate gently spins once and the spoon taps it, all clean.",
 78: "The teddy bear opens its arms wide and gives a big warm hug, a soft heart floats up.",
 81: "The two little sneakers hop, hop, hop happily across the rug.",
 84: "The yellow sun hat flies through the air and lands boing on the teddy bear's head, the teddy smiles.",
 87: "The rubber duck bobs in the bubbly bath, water splashing, splish splash.",
 90: "The sleepy crescent moon rises slowly and the stars twinkle softly in the night sky.",
 93: "The teddy bear yawns, snuggles under the blanket and closes its eyes.",
}
out = []
for s in sys.argv[1:]:
    i = int(s); frame = "O_" + m["vo_frame"][str(i)]; img = jobs[str(names.index(frame))]
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'../voice-lines/line-{i:03d}.mp3']))
    out.append({"index": i, "params": {"model": "grok_video_v15_lite", "aspect_ratio": "16:9", "duration": max(4, math.ceil(d + 1.5)),
        "resolution": "720p", "use_unlim": False, "declined_preset_id": "24bae836-2c4a-48e0-89b6-49fcc0b21612",
        "medias": [{"value": img, "role": "start_image"}],
        "prompt": MOTION[i] + " Cheerful cartoon 3D animation for toddlers, steady camera. No text."}})
print(json.dumps(out)); print(sum(o["params"]["duration"] for o in out), "credits", file=sys.stderr)
