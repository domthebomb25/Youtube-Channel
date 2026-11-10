# Centre-crop raw 2688x1520 Higgsfield outputs to 16:9 and resize to 1920x1080 masters (Section 5).
import sys
from PIL import Image
for n in sys.argv[1:]:
    im=Image.open(f'raw5/{n}.png').convert('RGB'); w,h=im.size
    th=int(w*9/16)
    c=im.crop((0,(h-th)//2,w,(h-th)//2+th)) if th<=h else im.crop(((w-int(h*16/9))//2,0,(w-int(h*16/9))//2+int(h*16/9),h))
    c.resize((1920,1080),Image.LANCZOS).save(f'section5/{n}.png')
