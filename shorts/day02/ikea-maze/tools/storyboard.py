"""Build the storyboard sheet (10 stills + image 1 again) with script lines under each shot. Run from images/."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, glob, sys
title = sys.argv[1] if len(sys.argv) > 1 else "IKEA MAZE - STORYBOARD"
fp = glob.glob('/usr/share/fonts/**/DejaVuSans*.ttf', recursive=True)
fb = ImageFont.truetype([f for f in fp if f.endswith('DejaVuSans-Bold.ttf')][0], 22)
fr = ImageFont.truetype([f for f in fp if f.endswith('DejaVuSans.ttf')][0], 20)
shots = [(1,'0:00-0:02.4','"Why is IKEA built like a maze?" (hook text on screen)'),
(2,'0:02.4-0:05.7','"There is only one path - and it walks you past everything they sell."'),
(3,'0:05.7-0:09.6','"Nearly ten thousand products, and you pass almost every one." (spoken by 0:08.8)'),
(4,'0:09.6-0:12.4','"But here\'s the trick. The path keeps turning,"'),
(5,'0:12.4-0:14.8','"past rooms set up like real homes -"'),
(6,'0:14.8-0:17.0','"so you picture them in yours."'),
(7,'0:17.0-0:19.1','"Skip something, and going back"'),
(8,'0:19.1-0:20.5','"means the whole maze again."'),
(9,'0:20.5-0:22.9','"So it lands in the cart -"'),
(10,'0:22.9-0:25.7','"just in case. You came for one lamp -" (small FOLLOW + New business story tomorrow.)'),
(11,'0:25.7-0:28.1','"that is why IKEA is built like a maze." (same file as shot 1, clean loop frame)')]
img = {i: Image.open(f'img{i}.png').convert('RGB') for i in range(1, 11)}; img[11] = img[1]
CW, IH, TH, cols, pad = 330, 587, 170, 6, 12
S = Image.new('RGB', (cols*(CW+pad)+pad, 2*(IH+TH+pad)+pad+60), (24, 24, 28)); d = ImageDraw.Draw(S)
d.text((pad, 16), title, font=fb, fill=(255, 215, 0))
for k, (n, t, line) in enumerate(shots):
    x = pad + (k % cols)*(CW+pad); y = 60 + pad + (k//cols)*(IH+TH+pad)
    S.paste(img[n].resize((CW, IH)), (x, y)); d.rectangle((x, y+IH, x+CW, y+IH+TH), fill=(40, 40, 48))
    d.text((x+8, y+IH+6), f'SHOT {k+1}' + ('  (image 1 again)' if k == 10 else f'  (image {n})'), font=fb, fill=(255, 215, 0))
    d.text((x+8, y+IH+32), t, font=fr, fill=(170, 200, 255))
    for j, l in enumerate(textwrap.wrap(line, 29)[:4]): d.text((x+8, y+IH+58+j*24), l, font=fr, fill=(255, 255, 255))
S.convert('RGB').save('storyboard_v5.jpg', quality=88)
S.resize((S.width//2, S.height//2)).convert('RGB').save('storyboard_v5_small.jpg', quality=85)
