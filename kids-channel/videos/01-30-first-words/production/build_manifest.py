"""Builds the shot manifest for video 1: which picture each clip starts from and what each clip shows."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

POPPY = ("Stylized 3D animated scene, the exact same character as the reference images: warm friendly preschool teacher "
         "with warm tan skin, large sparkling green eyes, long curly honey-brown hair held back by a soft pastel-yellow "
         "headband, no earrings, dark charcoal-grey long-sleeve shirt, plain kelly-green apron with an embroidered row of "
         "rainbow crayons. Medium close-up, chest-up, centered, facing the camera and looking directly into the lens with "
         "a warm closed-mouth smile, face and lips large, clear and well lit. {action} Same bright cozy playroom: pale-blue "
         "wall, toy shelves, rainbow picture, softly blurred. Soft global illumination, polished family-film 3D animation "
         "quality. Exactly five fingers on each hand. No text, no logos.")
OBJECT = ("Stylized 3D animated scene in the same bright cozy playroom style as the reference image. {scene} Cheerful, "
          "simple, high contrast, easy for a toddler to see, the subject large and centered. Soft global illumination, "
          "polished family-film 3D animation quality. No text, no logos.")

# Miss Poppy start frames (shared by the talking clips for that word)
P = {
 "intro":  "She waves hello with one open hand.",
 "hi":     "She waves hi with one open hand raised beside her face.",
 "mama":   "She holds a small framed picture of a mommy hugging a baby beside her face.",
 "dada":   "She holds a small framed picture of a daddy lifting a giggling baby beside her face.",
 "baby":   "She cradles a soft baby doll in a pink blanket in her arms.",
 "bye":    "She holds a little yellow rubber duck in one hand and waves with the other.",
 "car":    "She holds a small shiny red toy car with big friendly eyes beside her face.",
 "book":   "She holds a colorful toddler picture book open beside her face.",
 "bubbles":"She holds a bubble wand up, a few shiny soap bubbles floating around her.",
 "block":  "She holds a stack of three colorful wooden alphabet blocks beside her face.",
 "wiggle": "She stands ready to dance, both hands raised happily, slightly wider framing showing her waist.",
 "farm":   "She holds a small red wooden toy barn beside her face.",
 "dog":    "She holds a soft plush brown puppy beside her face.",
 "cat":    "She holds a soft plush grey kitten beside her face.",
 "cow":    "She holds a soft plush black-and-white cow beside her face.",
 "duck":   "She holds a little yellow rubber duck beside her face.",
 "fish":   "She holds a soft plush orange fish beside her face.",
 "food":   "She sits at a little wooden play table with a toy plate, hands on the table.",
 "milk":   "She holds a cup of milk beside her face.",
 "apple":  "She holds a shiny red apple beside her face.",
 "banana": "She holds a yellow banana beside her face.",
 "cookie": "She holds a round chocolate-chip cookie beside her face.",
 "eat":    "She holds a little spoon of food near her mouth.",
 "clap":   "Her hands are together mid-clap in front of her chest.",
 "up":     "She holds the string of a red balloon floating above her.",
 "go":     "She holds a small colorful wooden toy train beside her face.",
 "alldone":"Both of her hands are raised up beside her shoulders, palms open, an empty toy plate in front of her.",
 "hug":    "She hugs a soft teddy bear against her chest.",
 "shoe":   "She holds one small sneaker beside her face.",
 "hat":    "She holds a sunny yellow sun hat beside her face.",
 "bath":   "She holds a little yellow rubber duck with a few soap bubbles around it.",
 "moon":   "She holds a soft plush crescent moon beside her face.",
 "night":  "She holds a sleepy teddy bear in pajamas, head tilted gently.",
 "outro":  "She waves goodbye with one open hand.",
}
# Toy / animal start frames
O = {
 "mama":   "A storybook-style 3D scene of a mommy hugging her baby, a soft pink heart floating up above them.",
 "dada":   "A storybook-style 3D scene of a daddy lifting a giggling baby up high in the air.",
 "baby":   "A giggling baby peeking out from under a soft blanket on the play rug, peekaboo.",
 "bye":    "A little yellow duck on the polka-dot rug waving its wing goodbye, turning to waddle away.",
 "book":   "A colorful toddler picture book lying open on the polka-dot rug, pages lifting.",
 "bubbles":"Big shiny soap bubbles floating in the air in front of the toy shelves.",
 "block":  "A tall stack of colorful wooden alphabet blocks on the polka-dot rug, starting to wobble.",
 "dog":    "A cute cartoon brown puppy sitting on the polka-dot rug wagging its tail.",
 "cat":    "A cute cartoon grey kitten on the polka-dot rug stretching and yawning.",
 "cow":    "A cute cartoon black-and-white cow in a sunny green field chewing grass.",
 "duck":   "A cute little yellow duck splashing in a small blue pond.",
 "fish":   "A cute orange cartoon fish swimming in clear blue water, blowing bubbles.",
 "milk":   "A cup of milk on a little wooden table with a tiny splash.",
 "apple":  "A shiny red apple on a little wooden table, one bite taken out of it.",
 "banana": "A yellow banana on a little wooden table, half peeled.",
 "cookie": "A round chocolate-chip cookie on a small plate with a few crumbs.",
 "eat":    "A little spoon scooping yummy orange food from a toddler bowl.",
 "up":     "A red balloon floating up toward a sunny blue sky with fluffy clouds.",
 "go":     "A colorful wooden toy train with a smiling face on a toy track, ready to go.",
 "alldone":"An empty, clean toddler plate and spoon on a little wooden table.",
 "hug":    "A soft teddy bear on the polka-dot rug opening its arms wide for a hug.",
 "shoe":   "Two small colorful sneakers on the polka-dot rug, about to hop.",
 "hat":    "A sunny yellow sun hat flying through the air toward a teddy bear sitting on the rug.",
 "bath":   "A yellow rubber duck floating in a bubbly bathtub with splashing water.",
 "moon":   "A sleepy smiling crescent moon rising in a dark-blue starry night sky.",
 "night":  "A teddy bear in pajamas yawning and snuggling into a cozy little bed.",
}

# which Poppy frame each talking line uses, and which object frame each narration line uses
TALK_FRAME = {0:"intro",1:"intro",2:"hi",3:"hi",5:"mama",6:"mama",8:"dada",9:"dada",11:"baby",12:"baby",14:"bye",15:"bye",
  21:"car",22:"car",24:"book",25:"book",27:"bubbles",28:"bubbles",30:"block",31:"block",32:"wiggle",33:"farm",
  35:"dog",36:"dog",38:"cat",39:"cat",41:"cow",42:"cow",44:"duck",45:"duck",47:"fish",48:"fish",49:"food",
  51:"milk",52:"milk",54:"apple",55:"apple",57:"banana",58:"banana",60:"cookie",61:"cookie",63:"eat",64:"eat",
  65:"clap",67:"bubbles",68:"bubbles",70:"up",71:"up",73:"go",74:"go",76:"alldone",77:"alldone",79:"hug",80:"hug",
  82:"shoe",83:"shoe",85:"hat",86:"hat",88:"bath",89:"bath",91:"moon",92:"moon",94:"night",95:"night",
  96:"outro",98:"outro",99:"outro"}
VO_FRAME = {4:"mama",7:"dada",10:"baby",13:"bye",23:"book",26:"bubbles",29:"block",34:"dog",37:"cat",40:"cow",43:"duck",
  46:"fish",50:"milk",53:"apple",56:"banana",59:"cookie",62:"eat",66:"bubbles",69:"up",72:"go",75:"alldone",78:"hug",
  81:"shoe",84:"hat",87:"bath",90:"moon",93:"night"}
# already made in the 30-second preview
DONE = {16,17,18,19,20}

m = {"poppy_frames": {k: POPPY.format(action=v) for k, v in P.items()},
     "object_frames": {k: OBJECT.format(scene=v) for k, v in O.items()},
     "talk_frame": TALK_FRAME, "vo_frame": VO_FRAME, "done": sorted(DONE)}
json.dump(m, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
print(len(P), "poppy frames,", len(O), "object frames,", len(TALK_FRAME), "talk lines,", len(VO_FRAME), "narration lines")
