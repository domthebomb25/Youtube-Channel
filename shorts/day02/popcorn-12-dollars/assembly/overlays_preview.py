"""Preview of the on-screen text overlays on the still images (the render draws the same text)."""
from PIL import Image, ImageDraw, ImageFont
import glob
BOLD = glob.glob('/usr/share/fonts/**/DejaVuSans-Bold.ttf', recursive=True)[0]

def text_layer(size, text, center, px, fill, angle=0, stroke=0, stroke_fill=None):
    f = ImageFont.truetype(BOLD, px)
    t = Image.new('RGBA', size, (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    bb = d.multiline_textbbox((0, 0), text, font=f, stroke_width=stroke, align='center')
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.multiline_text((center[0] - w / 2 - bb[0], center[1] - h / 2 - bb[1]), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, align='center', spacing=2)
    if angle:
        t = t.rotate(angle, center=center, resample=Image.BICUBIC)
    return t

def apply(img, **kw):
    im = Image.open(img).convert('RGBA')
    im.alpha_composite(text_layer(im.size, **kw)); return im.convert('RGB')

if __name__ == '__main__':
    import json, sys
    spec = json.load(open(sys.argv[1]))
    for name, kw in spec.items():
        kw['center'] = tuple(kw['center']); kw['fill'] = tuple(kw['fill'])
        apply(f'img{name}.png', **kw).save(f'ov{name}.png')
