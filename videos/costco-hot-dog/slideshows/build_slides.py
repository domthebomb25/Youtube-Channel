"""Build the Day 1-5 slideshows from frames of the final video.

usage: python3 build_slides.py [day ...]
For each day writes slideshows/dayN-<name>/:
  tiktok/NN.jpg      1080x1920 slides (TikTok photo mode)
  instagram/NN.jpg   1080x1350 slides (Instagram carousel, 4:5)
  dayN-<name>.mp4    1080x1920 silent video of the same slides (Facebook Reels / YouTube Shorts; add music in-app)
Slide text: list of lines; a leading "*" makes the line yellow. Last slide is always the end card.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "shorts"))
import make_short as m  # noqa: E402

SRC = ROOT / "final/costco-hot-dog-final-1080p-10mbps.mp4"
END = ["FULL STORY ON YOUTUBE", "THE BUSINESS STICK HQ", "@TheBusinessStickHQ"]

DAYS = {
    1: ("then-vs-now", [
        (1.0,   ["THE COSTCO HOT DOG", "*IN 1985 VS. TODAY 👉"]),
        (62.5,  ["*1985:", "QUARTER-POUND HOT DOG", "+ 12 OZ CAN OF SODA", "*= $1.50"]),
        (101.0, ["*TODAY:", "10% BIGGER HOT DOG", "+ 20 OZ DRINK", "WITH FREE REFILLS = …"]),
        (30.0,  ["*STILL $1.50."]),
        (27.0,  ["$1.50 IN 1985 IS WORTH", "*ABOUT $4.66 TODAY"]),
        (39.5,  ["SO HOW IS", "*THIS POSSIBLE? 🤔"]),
    ]),
    2: ("5-things", [
        (266.5, ["5 THINGS COSTCO DID", "SO IT NEVER HAD TO", "*RAISE THE HOT DOG PRICE 👉"]),
        (208.5, ["*#1", "DROPPED ITS HOT DOG", "SUPPLIER (2009)"]),
        (215.7, ["*#2", "BUILT ITS OWN", "HOT DOG FACTORIES"]),
        (236.0, ["*#3", "SWITCHED FROM COKE", "TO PEPSI (2013)", "TO CUT COSTS"]),
        (244.0, ["*#4", "SWITCHED BACK TO COKE (2025)", "THE PRICE STILL DIDN'T MOVE"]),
        (252.0, ["*#5", "ADDED A WATER OPTION (2026)", "STILL $1.50"]),
        (263.0, ["ANYTHING EXCEPT", "*THE NUMBER ON THE SIGN."]),
    ]),
    3: ("the-math", [
        (302.5, ["COSTCO SOLD 245 MILLION", "HOT DOG COMBOS LAST YEAR.", "*HERE'S THE MATH 👉"]),
        (306.0, ["245 MILLION × $1.50", "*≈ $367 MILLION"]),
        (309.5, ["SOUNDS HUGE…", "BUT COSTCO'S REVENUE IS", "*$275 BILLION"]),
        (313.0, ["THAT'S LESS THAN 1%.", "*A ROUNDING ERROR."]),
        (287.0, ["MEANWHILE, MEMBERSHIP FEES", "*BRING IN $5.3 BILLION"]),
        (336.9, ["AND 92% OF U.S. & CANADA", "*MEMBERS RENEW EVERY YEAR"]),
        (278.5, ["THE HOT DOG ISN'T THE PRODUCT.", "*YOU ARE."]),
    ]),
    4: ("chicken-secret", [
        (352.0, ["COSTCO HAS ANOTHER ITEM", "IT REFUSES TO", "*RAISE THE PRICE ON 👉"]),
        (361.5, ["THE ROTISSERIE CHICKEN:", "*$4.99 SINCE 2009"]),
        (379.5, ["COSTCO GIVES UP", "*$30–40 MILLION A YEAR", "TO KEEP IT THAT PRICE"]),
        (393.5, ["THEN IT BUILT A", "*$400+ MILLION", "CHICKEN OPERATION IN NEBRASKA"]),
        (399.5, ["UP TO 2 MILLION CHICKENS…", "*EVERY SINGLE WEEK"]),
        (410.5, ["AND IT'S USUALLY AT THE", "BACK OF THE STORE.", "*HERE'S WHY 👀"]),
        (414.5, ["YOU WALK PAST", "*EVERYTHING ELSE", "TO GET IT."]),
    ]),
    5: ("would-you-raise-it", [
        (116.5, ["YOU'RE COSTCO'S CEO.", "THE $1.50 HOT DOG IS LOSING MONEY.", "*WHAT DO YOU DO? 👉"]),
        (122.5, ["THIS REALLY HAPPENED.", "THE CEO WANTED TO", "*RAISE IT TO $1.75"]),
        (131.5, ["THE CO-FOUNDER'S ANSWER:", "*\"IF YOU RAISE THE PRICE OF", "*THE HOT DOG, I WILL KILL YOU.\""]),
        (134.6, ["*\"FIGURE IT OUT.\""]),
        (167.5, ["HIS RULE: RAISING PRICES", "*IS LIKE A DRUG.", "DO IT ONCE, AND YOU KEEP DOING IT."]),
        (182.5, ["*SO COSTCO NEVER DID."]),
        (34.5,  ["WOULD YOU HAVE RAISED IT?", "*COMMENT YES OR NO 👇"]),
    ]),
}

# layout per format: canvas size, text-block centre y, picture top y, max font size
FMT = {"tiktok": dict(size=(1080, 1920), text_mid=440, pic_y=720, fs=(140, 120, 104, 92), lines=5),
       "instagram": dict(size=(1080, 1350), text_mid=235, pic_y=470, fs=(116, 100, 86, 76), lines=4)}


def frame(t, out):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", str(SRC), "-frames:v", "1", str(out)],
                   check=True)
    return Image.open(out).convert("RGB")


def wrap(d, words, f, maxw, extra=0):
    """Fewest lines that fit, then the most even split (no lone words on the last line)."""
    from itertools import combinations
    def width(ws, last):
        return d.textlength(" ".join(ws), font=f) + (extra if last else 0)
    n = len(words)
    for k in range(1, n + 1):
        best = None
        for cuts in combinations(range(1, n), k - 1):
            b = (0,) + cuts + (n,)
            rows = [words[b[i]:b[i + 1]] for i in range(k)]
            ws = [width(r, i == k - 1) for i, r in enumerate(rows)]
            if max(ws) <= maxw and (best is None or max(ws) - min(ws) < best[0]):
                best = (max(ws) - min(ws), rows)
        if best:
            return [" ".join(r) for r in best[1]]
    return [" ".join(words)]


def text_block(img, lines, mid, max_fs, max_lines):
    """Lines keep their colour; long lines re-wrap so the text stays big (same size for the whole block)."""
    d = ImageDraw.Draw(img)
    W = img.width
    parsed = []
    for ln in lines:
        yel = ln.startswith("*"); ln = ln.lstrip("*")
        emo = ln[-1] if ord(ln[-1]) > 0x2000 and ln[-1] not in "…×≈–" else None
        parsed.append((ln[:-1].rstrip() if emo else ln, emo, yel))
    cap = max_fs[min(len(parsed), len(max_fs)) - 1]
    for fs in range(cap, 50, -4):
        f = m.font(fs)
        rows = []
        for t, e, yel in parsed:
            sub = wrap(d, t.split(), f, W - 90, int(fs * 1.1) + 14 if e else 0)
            rows += [(s_, e if k == len(sub) - 1 else None, yel) for k, s_ in enumerate(sub)]
        if len(rows) <= max_lines and all(d.textlength(t, font=f) + (int(fs * 1.1) + 14 if e else 0) <= W - 80 for t, e, _ in rows):
            break
    lh = fs * 1.12
    y = mid - (len(rows) - 1) * lh / 2
    for t, e, yel in rows:
        tw = d.textlength(t, font=f); ew = int(fs * 1.1) + 14 if e else 0
        x = (W - tw - ew) / 2
        m.outlined(d, (x, y), t, f, m.YEL if yel else m.WHITE, anchor="lm")
        if e:
            em = m.emoji_img(e, int(fs * 1.0))
            img.alpha_composite(em, (int(x + tw + 14), int(y - em.height / 2)))
        y += lh


def slide(pic, lines, fmt, swipe=False):
    W, H = FMT[fmt]["size"]
    bg = pic.resize((int(pic.width * H / pic.height), H), Image.BILINEAR)
    x0 = (bg.width - W) // 2
    bg = bg.crop((x0, 0, x0 + W, H)).resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(3)).resize((W, H))
    img = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.5).convert("RGBA")
    py = FMT[fmt]["pic_y"]
    img.paste(pic.resize((W, 608), Image.LANCZOS), (0, py))
    ImageDraw.Draw(img).rectangle((0, py - 4, W, py + 611), outline=m.INK, width=6)
    text_block(img, lines, FMT[fmt]["text_mid"], FMT[fmt]["fs"], FMT[fmt]["lines"])
    if swipe:
        f = m.font(64 if fmt == "tiktok" else 54)
        y = py + 608 + (160 if fmt == "tiktok" else 110)
        d = ImageDraw.Draw(img)
        tw = d.textlength("SWIPE", font=f)
        m.outlined(d, ((W - tw - 80) / 2, y), "SWIPE", f, m.WHITE, anchor="lm")
        em = m.emoji_img("👉", 66)
        img.alpha_composite(em, (int((W - tw - 80) / 2 + tw + 14), int(y - em.height / 2)))
    return img.convert("RGB")


def end_slide(fmt):
    card = m.end_card(END)
    if fmt == "tiktok":
        return card
    return card.crop((0, 230, 1080, 1580))


def build(day):
    name, slides = DAYS[day]
    out = HERE / f"day{day}-{name}"
    for fmt in FMT:
        (out / fmt).mkdir(parents=True, exist_ok=True)
    tmp = out / "_frame.png"
    pngs = []
    for i, (t, lines) in enumerate(slides):
        pic = frame(t, tmp)
        for fmt in FMT:
            im = slide(pic, lines, fmt, swipe=(i == 0 and fmt == "instagram") or (i == 0 and fmt == "tiktok"))
            im.save(out / fmt / f"{i + 1:02d}.jpg", quality=92)
        vid = slide(pic, lines, "tiktok")
        p = out / f"_v{i:02d}.png"; vid.save(p); pngs.append((p, max(2.6, 1.2 + 0.22 * sum(len(l.split()) for l in lines))))
    n = len(slides) + 1
    for fmt in FMT:
        end_slide(fmt).save(out / fmt / f"{n:02d}.jpg", quality=92)
    p = out / "_vend.png"; end_slide("tiktok").save(p); pngs.append((p, 3.0))
    tmp.unlink()
    # silent video: each slide holds with a gentle zoom; music gets added in the app
    parts = []
    for k, (p, dur) in enumerate(pngs):
        nfr = int(round(dur * m.FPS))
        seg = out / f"_seg{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(p), "-vf",
                        f"scale=2160:3840,zoompan=z='1+0.035*on/{nfr}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={nfr}:s=1080x1920:fps={m.FPS},setsar=1",
                        "-frames:v", str(nfr), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                        str(seg)], check=True)
        parts.append(seg)
    lst = out / "_list.txt"; lst.write_text("".join(f"file '{s.name}'\n" for s in parts))
    total = sum(d for _, d in pngs)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a", "-t", f"{total:.2f}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", str(out / f"day{day}-{name}.mp4")], check=True)
    for f in parts + [lst] + [p for p, _ in pngs]:
        f.unlink()
    print(out.name, n, "slides,", round(total, 1), "s video")


if __name__ == "__main__":
    for d in (sys.argv[1:] or DAYS):
        build(int(d))
