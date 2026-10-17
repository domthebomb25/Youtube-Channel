"""Cartoon-style calendar pages drawn with exact dates (the image model gets digits wrong)."""
import calendar, random, math
from PIL import Image, ImageDraw, ImageFont
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(sz): return ImageFont.truetype(FB, sz)
INK = (15, 15, 20)

def calendar_page(d, box, month, year, circle=None, header=(215, 45, 50), paper=(250, 250, 246), faded=False):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rounded_rectangle((x0 + 12, y0 + 14, x1 + 12, y1 + 14), 26, fill=(0, 0, 0, 70) if False else (30, 30, 40))
    d.rounded_rectangle(box, 26, fill=paper, outline=INK, width=9)
    hh = int(h * 0.20)
    d.rounded_rectangle((x0, y0, x1, y0 + hh), 26, fill=header, outline=INK, width=9)
    d.rectangle((x0 + 5, y0 + hh - 26, x1 - 5, y0 + hh - 2), fill=header)
    d.line((x0 + 5, y0 + hh, x1 - 5, y0 + hh), fill=INK, width=9)
    title = calendar.month_name[month].upper() + (f" {year}" if year else "")
    fs = int(hh * 0.5)
    f = font(fs); tw = d.textlength(title, font=f)
    while tw > w * 0.86 and fs > 10:
        fs -= 2; f = font(fs); tw = d.textlength(title, font=f)
    d.text(((x0 + x1) / 2 - tw / 2, y0 + hh * 0.22), title, font=f, fill=(255, 255, 255))
    for k in range(5):  # rings
        cx = x0 + w * (0.14 + 0.18 * k)
        d.rounded_rectangle((cx - 13, y0 - 36, cx + 13, y0 + 38), 13, fill=(190, 190, 200), outline=INK, width=6)
    cal = calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)
    rows = len(cal)
    gx0, gy0 = x0 + 28, y0 + hh + 22
    cw = (w - 56) / 7
    wd = font(int(cw * 0.26))
    for i, s in enumerate("SMTWTFS"):
        tw = d.textlength(s, font=wd)
        d.text((gx0 + cw * i + cw / 2 - tw / 2, gy0), s, font=wd, fill=(120, 120, 130))
    ry0 = gy0 + int(cw * 0.42)
    rh = (y1 - 26 - ry0) / rows
    nf = font(int(min(cw, rh) * 0.5))
    pos = {}
    for r, week in enumerate(cal):
        for c, day in enumerate(week):
            cx, cy = gx0 + cw * c + cw / 2, ry0 + rh * r + rh / 2
            d.rectangle((gx0 + cw * c + 3, ry0 + rh * r + 3, gx0 + cw * (c + 1) - 3, ry0 + rh * (r + 1) - 3), outline=(170, 170, 175), width=3)
            if day:
                s = str(day); tw = d.textlength(s, font=nf)
                d.text((cx - tw / 2, cy - nf.size * 0.62), s, font=nf, fill=INK)
                pos[day] = (cx, cy)
    if circle:
        cx, cy = pos[circle]; rx, ry = cw * 0.46, rh * 0.46
        random.seed(7)
        for p in range(3):
            pts = []
            for a in range(0, 372, 6):
                t = math.radians(a); j = random.uniform(-3, 3)
                pts.append((cx + (rx + j) * math.cos(t) + p * 2, cy + (ry + j) * math.sin(t) + p))
            d.line(pts, fill=(228, 25, 40), width=11, joint="curve")
    return pos

def tally(d, x, y, n, scale=1.0, col=(40, 30, 20)):
    gap, hgt = int(22 * scale), int(70 * scale)
    k = 0
    while k < n:
        group = min(5, n - k); gx = x
        for i in range(min(group, 4)):
            d.line((gx + i * gap, y, gx + i * gap, y + hgt), fill=col, width=int(8 * scale))
        if group == 5:
            d.line((x - 8, y + hgt - 8, x + 3 * gap + 8, y + 6), fill=col, width=int(8 * scale))
        x += int(4 * gap + 40 * scale); k += group
