# Free assembly states for Section 3 (local, 0 credits). Run from film2-assets/section3.
# 71-state3 = the generated image (all three rows lit). 71 / 71-state2 are made by dimming rows locally.
# 69-state = 69 + "$20,000,000 – $30,000,000" text under the contract.
import os, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
if not os.path.exists('71-state3.png'):
    shutil.copy('71.png', '71-state3.png')          # generated all-lit image
full = Image.open('71-state3.png').convert('RGB')
bands = {1:(0,38,1920,352), 2:(0,380,1920,698), 3:(0,726,1920,1042)}
def dim(img, rows):
    out = img.copy()
    for r in rows:
        box = bands[r]; reg = out.crop(box)
        reg = ImageEnhance.Color(reg).enhance(0.35)
        reg = ImageEnhance.Brightness(reg).enhance(0.38)
        out.paste(reg, box[:2])
    return out
dim(full,[2,3]).save('71.png')
dim(full,[3]).save('71-state2.png')
# 69-state
im = Image.open('69.png').convert('RGB')
text = "$20,000,000 – $30,000,000"
font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', 118)
glow = Image.new('RGBA', im.size, (0,0,0,0)); d = ImageDraw.Draw(glow)
w = d.textlength(text, font=font); x = (1920-w)/2; y = 770
d.text((x,y), text, font=font, fill=(255,255,255,255), stroke_width=7, stroke_fill=(255,255,255,255))
g = glow.filter(ImageFilter.GaussianBlur(14))
base = im.convert('RGBA'); base.alpha_composite(g)
d2 = ImageDraw.Draw(base)
d2.text((x,y), text, font=font, fill=(255,255,255), stroke_width=7, stroke_fill=(10,20,50))
d2.text((x,y), text, font=font, fill=(255,255,255))
base.convert('RGB').save('69-state.png')
