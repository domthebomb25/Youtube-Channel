"""Text + graphic drawing helpers (PIL) in the stickman channel style."""
import math
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONTS = Path(__file__).parent / "fonts"
W, H = 1920, 1080

INK = (20, 20, 20)
WHITE = (255, 255, 255)
CREAM = (255, 250, 236)
SKY = (78, 160, 232)
YELLOW = (247, 205, 60)
MUSTARD = (222, 170, 40)
RED = (214, 40, 40)
GREEN = (46, 160, 67)
GREY = (190, 190, 190)


@lru_cache(None)
def font(name, size):
    return ImageFont.truetype(str(FONTS / f"{name}.ttf"), size)


def text_size(d, text, f, stroke=0):
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    return x1 - x0, y1 - y0, x0, y0


def draw_text(d, xy, text, f, fill=INK, stroke=0, stroke_fill=INK, anchor="mm"):
    d.text(xy, text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, anchor=anchor)


def fit_font(name, text, box_w, box_h, start=400, stroke_frac=0.0):
    size = start
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while size > 8:
        f = font(name, size)
        s = int(size * stroke_frac)
        w, h, _, _ = text_size(probe, text, f, s)
        if w <= box_w and h <= box_h:
            return f, s
        size = int(size * 0.94)
    return font(name, 8), 0


# ---------- signs painted into the still ----------

def paint_sign(img, spec):
    """Paint text onto a blank sign region of `img` (RGBA, any size)."""
    iw, ih = img.size
    style = spec.get("style", "price")
    if "rect" in spec:
        x0, y0, x1, y1 = spec["rect"]
        cx, cy = (x0 + x1) / 2 * iw, (y0 + y1) / 2 * ih
        bw, bh = (x1 - x0) * iw, (y1 - y0) * ih
        rot = 0
    else:
        cx, cy = spec["center"][0] * iw, spec["center"][1] * ih
        bw, bh = spec["size"][0] * iw, spec["size"][1] * ih
        rot = spec.get("rot", 0)
    layer = Image.new("RGBA", (int(bw * 1.6), int(bh * 1.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    lc = (layer.width / 2, layer.height / 2)
    if style == "chalk":
        pad = 0.06
        d.rectangle([lc[0] - bw * (0.5 - pad), lc[1] - bh * (0.5 - pad),
                     lc[0] + bw * (0.5 - pad), lc[1] + bh * (0.5 - pad)], fill=(34, 40, 38, 255))
        f, s = fit_font("PatrickHand", spec["text"], bw * 0.80, bh * 0.70)
        draw_text(d, lc, spec["text"], f, fill=(245, 245, 235))
    elif style == "calendar":
        f, s = fit_font("LuckiestGuy", spec["text"], bw * 0.75, bh * 0.70, stroke_frac=0.0)
        draw_text(d, (lc[0], lc[1] + bh * 0.04), spec["text"], f, fill=RED)
    elif style == "dates":
        # 1..days laid out in a cols x rows grid filling the box
        cols, rows, days = spec.get("cols", 7), spec.get("rows", 5), spec.get("days", 30)
        cw, rh = bw / cols, bh / rows
        f = font("LuckiestGuy", int(min(cw, rh) * 0.5))
        for i in range(days):
            c, r = i % cols, i // cols
            x = lc[0] - bw / 2 + cw * (c + 0.5)
            y = lc[1] - bh / 2 + rh * (r + 0.5)
            draw_text(d, (x, y + rh * 0.04), str(i + 1), f, fill=INK)
    elif style == "highway":
        f, s = fit_font("Anton", spec["text"], bw * 0.86, bh * 0.50)
        draw_text(d, lc, spec["text"], f, fill=WHITE)
    elif style == "ticket":
        f, s = fit_font("LuckiestGuy", spec["text"], bw * 0.88, bh * 0.60)
        draw_text(d, (lc[0], lc[1] + bh * 0.04), spec["text"], f, fill=(92, 58, 8))
    elif style in ("money", "money_up"):
        arrow = style == "money_up"
        f, s = fit_font("LuckiestGuy", "$", bw * (0.45 if arrow else 0.8), bh * (0.70 if arrow else 0.88), stroke_frac=0.06)
        tw, th, _, _ = text_size(d, "$", f, s)
        gap = bw * 0.06
        aw = min(bw * 0.32, th * 0.62) if arrow else 0
        total = tw + (gap + aw if arrow else 0)
        x = lc[0] - total / 2
        draw_text(d, (x + tw / 2, lc[1] + bh * 0.04), "$", f, fill=GREEN, stroke=s, stroke_fill=INK)
        if arrow:
            ax, ah = x + tw + gap, th * 0.9
            top, bot = lc[1] - ah / 2, lc[1] + ah / 2
            head = ah * 0.42
            pts = [(ax + aw / 2, top), (ax + aw, top + head), (ax + aw * 0.68, top + head),
                   (ax + aw * 0.68, bot), (ax + aw * 0.32, bot), (ax + aw * 0.32, top + head), (ax, top + head)]
            d.polygon(pts, fill=RED, outline=INK, width=max(2, int(s * 0.8)))
    else:
        f, s = fit_font("LuckiestGuy", spec["text"], bw * 0.80, bh * 0.66, stroke_frac=0.05)
        draw_text(d, (lc[0], lc[1] + bh * 0.04), spec["text"], f, fill=RED, stroke=s, stroke_fill=INK)
    if rot:
        layer = layer.rotate(rot, resample=Image.BICUBIC, expand=False)
    img.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))
    return img


# ---------- pop-in labels over the moving image ----------

def rounded_box(d, box, fill, outline=INK, width=8, r=26):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def label_layer(specs):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for sp in specs:
        k, t = sp["kind"], sp["text"]
        if k == "year":
            f = font("LuckiestGuy", 84)
            w, h, _, _ = text_size(d, t, f)
            box = (56, 48, 56 + w + 70, 48 + h + 56)
            rounded_box(d, box, YELLOW)
            draw_text(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2 + 4), t, f)
        elif k == "tag":
            f = font("LuckiestGuy", 76)
            w, h, _, _ = text_size(d, t, f)
            cx = sp.get("pos", (0.5, 0.0))[0] * W
            top = 60 if not sp.get("pos") else sp["pos"][1] * H
            box = (cx - w / 2 - 40, top, cx + w / 2 + 40, top + h + 50)
            rounded_box(d, box, WHITE)
            draw_text(d, (cx, (box[1] + box[3]) / 2 + 4), t, f)
        elif k == "big":
            f = font("LuckiestGuy", 150)
            pos = sp.get("pos", (0.5, 0.15))
            draw_text(d, (pos[0] * W, pos[1] * H), t, f, fill=WHITE, stroke=12)
        elif k == "name":
            f = font("LuckiestGuy", 72)
            f2 = font("PatrickHand", 52)
            w, h, _, _ = text_size(d, t, f)
            w2, h2, _, _ = text_size(d, sp["sub"], f2)
            bw = max(w, w2) + 80
            x0, y1 = 60, H - 60
            y0 = y1 - (h + h2 + 80)
            rounded_box(d, (x0, y0, x0 + bw, y1), WHITE)
            d.rectangle((x0 + 4, y0 + 4, x0 + 28, y1 - 4), fill=MUSTARD)
            draw_text(d, (x0 + 50, y0 + 26), t, f, anchor="lt")
            draw_text(d, (x0 + 50, y0 + 40 + h), sp["sub"], f2, fill=(60, 60, 60), anchor="lt")
        elif k == "sticker":
            f = font("LuckiestGuy", 64)
            w, h, _, _ = text_size(d, t, f)
            cx, cy = sp["pos"][0] * W, sp["pos"][1] * H
            box = (cx - w / 2 - 30, cy - h / 2 - 24, cx + w / 2 + 30, cy + h / 2 + 24)
            rounded_box(d, box, YELLOW, width=6, r=16)
            draw_text(d, (cx, cy + 3), t, f, fill=RED)
        elif k == "paid":
            f = font("LuckiestGuy", 70)
            ck = font("DejaVuSans", 70)
            w, h, _, _ = text_size(d, t, f)
            cw, _, _, _ = text_size(d, "\u2714", ck)
            cx, cy = sp["pos"][0] * W, sp["pos"][1] * H
            tw = w + 24 + cw
            box = (cx - tw / 2 - 40, cy - h / 2 - 30, cx + tw / 2 + 40, cy + h / 2 + 30)
            rounded_box(d, box, GREEN)
            draw_text(d, (cx - tw / 2, cy + 4), t, f, fill=WHITE, anchor="lm")
            draw_text(d, (cx + tw / 2 - cw, cy + 2), "\u2714", ck, fill=WHITE, anchor="lm")
        elif k == "stamp":
            f = font("LuckiestGuy", 130)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            w, h, _, _ = text_size(ld, t, f)
            cx, cy = W / 2, H / 2
            box = (cx - w / 2 - 50, cy - h / 2 - 40, cx + w / 2 + 50, cy + h / 2 + 40)
            ld.rounded_rectangle(box, radius=20, outline=RED, width=16, fill=(255, 255, 255, 215))
            draw_text(ld, (cx, cy + 6), t, f, fill=RED)
            layer = layer.rotate(10, resample=Image.BICUBIC)
            px, py = sp["pos"]
            img.alpha_composite(layer, (int(px * W - W / 2), int(py * H - H / 2)))
            d = ImageDraw.Draw(img)
    return img


# ---------- animated graphics (G shots) ----------

def ease(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


def background():
    img = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(img)
    for cx, cy, s in [(250, 150, 1.0), (1650, 120, 0.8), (1500, 980, 0.0)]:
        if s == 0:
            continue
        for dx, dy, r in [(-70, 10, 55), (0, -15, 75), (75, 10, 55)]:
            d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=WHITE)
    # card
    rounded_box(d, (150, 170, W - 150, H - 90), CREAM, width=10, r=40)
    return img


def header(d, text, y=110, size=92):
    draw_text(d, (W / 2, y), text, font("LuckiestGuy", size), fill=WHITE, stroke=10)


def coin_stack(d, cx, base_y, n, coin_h=34, coin_w=200):
    for i in range(n):
        y = base_y - i * coin_h
        d.ellipse((cx - coin_w / 2, y - coin_h * 0.9, cx + coin_w / 2, y + coin_h * 0.9), fill=MUSTARD, outline=INK, width=5)
        d.ellipse((cx - coin_w / 2, y - coin_h * 1.4, cx + coin_w / 2, y + coin_h * 0.4), fill=YELLOW, outline=INK, width=5)


def g_coins(t, dur, final=False):
    img = background()
    d = ImageDraw.Draw(img)
    header(d, "SAME BUYING POWER")
    left_n, right_n = 6, 19
    p = 1.0 if final else ease(t / (dur * 0.75))
    base, ch = 900, 24
    coin_stack(d, 620, base, left_n, coin_h=ch)
    coin_stack(d, 1300, base, max(1, round(right_n * p)), coin_h=ch)
    f = font("LuckiestGuy", 80)
    draw_text(d, (620, base - left_n * ch - 100), "$1.50", f, fill=RED, stroke=4)
    draw_text(d, (620, 975), "1985", font("LuckiestGuy", 64))
    draw_text(d, (1300, 975), "TODAY", font("LuckiestGuy", 64))
    top = base - max(1, round(right_n * p)) * ch
    if p > 0.95 or final:
        draw_text(d, (1300, top - 100), "$4.66", f, fill=RED, stroke=4)
    if final:
        a = ease(t / 0.5)
        x0 = 860
        d.line((x0, 840, x0 + 140 * a, 840 - 400 * a), fill=GREEN, width=26)
        if a > 0.9:
            tip = (x0 + 140, 440)
            d.polygon([(tip[0] - 50, tip[1] + 50), (tip[0] + 50, tip[1] + 10), (tip[0] + 10, tip[1] - 60)], fill=GREEN)
            draw_text(d, (935, 640), "×3", font("LuckiestGuy", 110), fill=GREEN, stroke=6, stroke_fill=WHITE)
    return img


def g_formula(t, dur):
    img = background()
    d = ImageDraw.Draw(img)
    header(d, "THE NORMAL RULE")
    f = font("LuckiestGuy", 104)
    draw_text(d, (W / 2, 420), "LOSING MONEY", f, fill=RED)
    a = ease((t - 0.3) / 0.4)
    if a > 0:
        draw_text(d, (W / 2, 590), "↓", font("LuckiestGuy", 130), fill=INK)
    if t > 0.7:
        draw_text(d, (W / 2, 780), "RAISE THE PRICE", f, fill=GREEN)
    if t > 1.1:
        draw_text(d, (1650, 780), "✔", font("DejaVuSans", 140) if (FONTS / "DejaVuSans.ttf").exists() else f, fill=GREEN)
    return img


def g_third(t, dur):
    img = background()
    d = ImageDraw.Draw(img)
    header(d, "WHAT $1.50 BUYS")
    p = ease(t / (dur * 0.6))
    for cx, label, frac in [(620, "1985", 1.0), (1300, "TODAY", 1 - (2 / 3) * p)]:
        box = (cx - 230, 330, cx + 230, 790)
        d.ellipse(box, fill=(225, 225, 225), outline=INK, width=8)
        d.pieslice(box, -90, -90 + 360 * frac, fill=YELLOW, outline=INK, width=8)
        draw_text(d, (cx, 880), label, font("LuckiestGuy", 70))
    if p > 0.95:
        draw_text(d, (1300, 560), "1/3", font("LuckiestGuy", 120), fill=RED, stroke=8, stroke_fill=WHITE)
    return img


def g_meter(t, dur, title, pct, sub):
    img = background()
    d = ImageDraw.Draw(img)
    header(d, title, size=84)
    p = ease(t / (dur * 0.6))
    x0, x1, y0, y1 = 300, 1620, 520, 640
    d.rounded_rectangle((x0, y0, x1, y1), radius=30, fill=WHITE, outline=INK, width=8)
    scale = 25.0
    fill_x = x0 + (x1 - x0) * min(1, pct * p / scale)
    if fill_x > x0 + 20:
        d.rounded_rectangle((x0 + 6, y0 + 6, fill_x, y1 - 6), radius=26, fill=GREEN)
    for v in range(0, 26, 5):
        x = x0 + (x1 - x0) * v / scale
        d.line((x, y1 + 10, x, y1 + 34), fill=INK, width=5)
        draw_text(d, (x, y1 + 70), f"{v}%", font("LuckiestGuy", 44))
    draw_text(d, (fill_x, y0 - 90), f"{pct * p:.0f}%", font("LuckiestGuy", 110), fill=GREEN, stroke=6, stroke_fill=WHITE)
    draw_text(d, (W / 2, 900), sub, font("LuckiestGuy", 60))
    return img


def fmt_num(v, prefix=""):
    return prefix + f"{int(v):,}"


def g_counter(t, dur, title, target, prefix="", suffix="", sub=""):
    img = background()
    d = ImageDraw.Draw(img)
    header(d, title, size=84)
    p = ease(t / (dur * 0.7))
    s = fmt_num(target * p, prefix) + suffix
    f, st = fit_font("LuckiestGuy", fmt_num(target, prefix) + suffix, 1450, 260, start=230, stroke_frac=0.04)
    draw_text(d, (W / 2, 560), s, f, fill=RED, stroke=st, stroke_fill=INK)
    if sub:
        draw_text(d, (W / 2, 840), sub, font("LuckiestGuy", 64))
    return img


def g_pie_half(t, dur):
    img = background()
    d = ImageDraw.Draw(img)
    header(d, "COSTCO'S OPERATING PROFIT", size=80)
    p = ease(t / (dur * 0.6))
    box = (330, 300, 830, 800)
    d.ellipse(box, fill=(225, 225, 225), outline=INK, width=8)
    d.pieslice(box, -90, -90 + 360 * 0.51 * p, fill=YELLOW, outline=INK, width=8)
    f = font("LuckiestGuy", 70)
    d.rounded_rectangle((960, 380, 1010, 430), radius=8, fill=YELLOW, outline=INK, width=5)
    draw_text(d, (1040, 405), "MEMBERSHIP FEES", f, anchor="lm")
    d.rounded_rectangle((960, 520, 1010, 570), radius=8, fill=(225, 225, 225), outline=INK, width=5)
    draw_text(d, (1040, 545), "EVERYTHING ELSE", f, anchor="lm")
    if p > 0.9:
        draw_text(d, (1300, 720), "≈ HALF", font("LuckiestGuy", 130), fill=RED, stroke=6, stroke_fill=WHITE)
    draw_text(d, (W / 2, 900), "FISCAL 2025", font("LuckiestGuy", 52), fill=(90, 90, 90))
    return img


def g_bars(t, dur):
    img = background()
    d = ImageDraw.Draw(img)
    header(d, "COSTCO REVENUE VS HOT DOGS", size=78)
    p = ease(t / (dur * 0.6))
    base, top = 840, 300
    hmax = base - top
    for cx, val, label, col in [(700, 275.2, "TOTAL REVENUE", MUSTARD), (1220, 0.37, "HOT DOG COMBOS", RED)]:
        h = max(4, hmax * (val / 275.2) * p)
        d.rectangle((cx - 140, base - h, cx + 140, base), fill=col, outline=INK, width=6)
        draw_text(d, (cx, base + 60), label, font("LuckiestGuy", 54))
    draw_text(d, (700, base - hmax * p - 60), f"${275.2 * p:,.0f}B", font("LuckiestGuy", 80), fill=INK)
    if p > 0.9:
        draw_text(d, (1220, base - 70), "$0.37B", font("LuckiestGuy", 80), fill=RED, stroke=5, stroke_fill=WHITE)
    d.line((300, base, 1620, base), fill=INK, width=8)
    return img


def stick_person(d, cx, base, color, scale=1.0):
    r = 34 * scale
    head_c = (cx, base - 210 * scale)
    d.ellipse((head_c[0] - r, head_c[1] - r, head_c[0] + r, head_c[1] + r), fill=WHITE, outline=color, width=int(8 * scale))
    neck = base - 175 * scale
    hip = base - 80 * scale
    w = int(10 * scale)
    d.line((cx, neck, cx, hip), fill=color, width=w)
    d.line((cx, neck + 20 * scale, cx - 40 * scale, neck + 80 * scale), fill=color, width=w)
    d.line((cx, neck + 20 * scale, cx + 40 * scale, neck + 80 * scale), fill=color, width=w)
    d.line((cx, hip, cx - 35 * scale, base), fill=color, width=w)
    d.line((cx, hip, cx + 35 * scale, base), fill=color, width=w)


def g_renew(t, dur):
    img = background()
    d = ImageDraw.Draw(img)
    header(d, "MEMBERS WHO RENEW", size=84)
    p = ease(t / (dur * 0.6))
    lit = round(9 * p)
    for i in range(10):
        cx = 330 + i * 140
        stick_person(d, cx, 760, GREEN if i < lit else (150, 150, 150), 1.0)
    draw_text(d, (W / 2, 880), "92.3%  ·  U.S. & CANADA", font("LuckiestGuy", 76), fill=GREEN, stroke=5, stroke_fill=WHITE)
    return img


GRAPHIC_FN = {
    7: lambda t, dur: g_coins(t, dur),
    8: lambda t, dur: g_coins(t, dur, final=True),
    19: g_formula,
    33: g_third,
    59: lambda t, dur: g_meter(t, dur, "MARKUP CAP: BRAND NAMES", 14, "COSTCO CAPS MARKUP AT ABOUT 14%"),
    60: lambda t, dur: g_meter(t, dur, "MARKUP CAP: KIRKLAND", 15, "ITS OWN BRAND: ABOUT 15%"),
    106: lambda t, dur: g_counter(t, dur, "MEMBERSHIP FEES · FY2025", 5_320_000_000, prefix="$"),
    107: g_pie_half,
    111: lambda t, dur: g_counter(t, dur, "HOT DOG COMBOS SOLD · FY2025", 245_000_000, sub="ABOUT 245 MILLION"),
    112: lambda t, dur: g_counter(t, dur, "HOT DOG SALES", 367_000_000, prefix="$", sub="≈ $367 MILLION"),
    115: g_bars,
    125: g_renew,
    136: lambda t, dur: g_counter(t, dur, "CHICKENS SOLD · FY2025", 157_000_000, suffix="+", sub="157 MILLION+ ROTISSERIE CHICKENS"),
    145: lambda t, dur: g_counter(t, dur, "NEBRASKA CHICKEN PLANT", 400_000_000, prefix="$", suffix="+", sub="FARMS · FEED MILL · PROCESSING PLANT"),
}
