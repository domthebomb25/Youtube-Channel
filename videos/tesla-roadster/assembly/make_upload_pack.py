"""Builds UPLOAD.md and the SEO/upload-pack PDF for the Tesla Roadster long video. usage: make_upload_pack.py OUT.pdf"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, KeepTogether
from xml.sax.saxutils import escape
F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("D", F + "DejaVuSans.ttf")); pdfmetrics.registerFont(TTFont("DB", F + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("M", F + "DejaVuSansMono.ttf"))
H1 = ParagraphStyle("h1", fontName="DB", fontSize=18, leading=22, spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="DB", fontSize=13, leading=16, spaceBefore=12, spaceAfter=4, textColor=colors.HexColor("#0b3d91"))
P = ParagraphStyle("p", fontName="D", fontSize=9.5, leading=13, spaceAfter=3)
WHY = ParagraphStyle("why", parent=P, textColor=colors.HexColor("#555555"), fontSize=8.5, leading=11.5)
BOX = ParagraphStyle("box", fontName="M", fontSize=7.8, leading=10.2)

TITLES = ["Tesla's New Roadster Can Fly. Here's How It Prints Money",
          "Why Tesla Built a Flying Roadster (It's Not About the Car)",
          "Tesla Roadster Reveal: The Real Reason It Can Fly"]
DESC = """Tesla's new Roadster can fly. But that's not the genius part. Here's how a few seconds of flight could turn reservations into one of the smartest marketing plays in car history.

Tesla didn't just build a flying car to sell you a flying car. They built it to print money. (Reveal event: Thursday, Oct 15, 2026.)

In this video: how the cold-gas thrusters work, what the Performance, Thrust and Rocket versions cost, why production doesn't start until 2028, what Tesla did with the 2017 Roadster deposits, and why a "halo product" makes the normal cars feel special. The reservation math in the video is my own estimate, not a Tesla figure. Details were reported at the reveal and some were still unconfirmed.

Subscribe for more business stories told simply with stick figures:
https://www.youtube.com/@TheBusinessStickHQ?sub_confirmation=1

Chapters
0:00 Can Tesla's new car really fly?
0:17 The reveal and the jump
0:38 How the thrusters work
1:02 Why build a car that flies for seconds?
1:11 Reservation prices: $50K, $250K, Rocket
1:43 The math: hundreds of millions in deposits
2:07 A free loan from fans
2:15 Tesla did this before (the 2017 Roadster)
2:40 Why now? Tesla sales and BYD
2:59 The halo product strategy
3:19 So, can it fly? The verdict
3:39 Would you put $50,000 down?

Sources
- Reveal event, ramp jump, thruster landing and Elon Musk's "basically fly like a rocket" quote: TechCrunch, NBC News, Electrek (Oct 15-16, 2026).
- Trims, prices, $5,000 card + $45,000 wire deposit, 2028 production, "not approved for public road use": Tesla's reservation page and the reveal coverage above.
- 0-60 claims (Tesla's own figures) and the 0.81 s live run: reveal coverage; the live timer had problems.
- 2017 Roadster deposits and 2020 production target: Tesla's past SEC filings and 2017 launch coverage.
- Tesla Q3 2026 deliveries (486,532, down about 2% year over year, above analyst expectations) and BYD vs. Tesla in Europe (BYD's numbers include plug-in hybrids): Electrek.
- "No interest / no escrow" comes from Tesla's past SEC filings, not confirmed in the 2026 reservation terms.

All illustrations are original stick-figure drawings and the narrator is an AI voice. This video is for entertainment and education. It is not sponsored by or affiliated with Tesla or SpaceX.

#Tesla #TeslaRoadster #BusinessStories"""
TAGS = ("tesla roadster, tesla roadster 2026, tesla flying car, tesla roadster reveal, tesla roadster price, tesla roadster reservation, "
        "tesla roadster spacex, tesla cold gas thrusters, elon musk roadster, tesla roadster 0-60, tesla roadster production 2028, "
        "tesla halo product, tesla business strategy, tesla deposits, business stories, the business stick")
PIN = "Would you put $50,000 down for a car you might have to wait years for? Tell me below. (Sources for everything are in the description.)"
SHORT_PIN = "Full breakdown of how Tesla's flying Roadster prints money: [PASTE LONG VIDEO LINK]"

def box(txt):
    t = Table([[Preformatted(txt, BOX)]], colWidths=[6.9 * inch])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#2f6fdd"), None, (3, 2)), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f6ff")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t
def wrap(txt, w=105):
    import textwrap
    return "\n".join("\n".join(textwrap.wrap(l, w)) if l.strip() else "" for l in txt.split("\n"))

STEPS_A = [
 ("Step 1: Start the upload (do this first)", [
  "Go to studio.youtube.com on your computer, click Create, then Upload videos.",
  "Pick Tesla-Roadster-final-1080p.mp4 and let it upload in the background while you fill in the rest.",
  "Have ready: the thumbnail (TESLA'S NEW CAR CAN FLY?) and tesla-roadster-english.srt (captions)."]),
]
STEPS_B = [
 ("Step 2: Details page", None),
]
SETTINGS = [
 "Thumbnail: Upload thumbnail, pick your TESLA'S NEW CAR CAN FLY? image.",
 "Playlist: Select, then tick Business Stories, then Done.",
 "Audience: No, it's not made for kids.",
 "Show more, then Altered content: No (stick-figure cartoons; the narrator isn't a real person).",
 "Paid promotion: leave unticked.",
 "Tags: paste the tags box above.",
 "Language: English. Caption certification: None. Recording date/location: skip.",
 "License: Standard YouTube License. Allow embedding: ticked. Publish to subscriptions feed: ticked.",
 "Shorts remixing: Allow video and audio remixing.",
 "Category: Education.",
 "Comments: On, sorted by Top. Show how many viewers like this video: ticked.",
]
STEPS_C = [
 ("Step 3: Video elements page", [
  "Subtitles: Add, English, Upload file, With timing, pick tesla-roadster-english.srt, check the first lines, Done.",
  "End screen and cards: skip this time. The video ends right on the closing question, so an end screen would cover it. Add one later if you add an end card.",
  "Click Next."]),
 ("Step 4: Checks", ["Wait for 'No issues found' (a few minutes), then Next."]),
 ("Step 5: Visibility", [
  "Choose Public and Publish at 9:00 AM (or Schedule for 9:00 AM). Leave Premiere off.",
  "Wait for 'Processing HD' to finish first so the first viewers see it sharp."]),
 ("Step 6: The first hour (be online)", [
  "Post the pinned-comment text below on the video, then click the three dots on it and choose Pin.",
  "Reply to every comment in the first day and tap the heart on them.",
  "Optional: Studio, Customization, Layout, then feature this video for returning subscribers.",
  "Don't change the title or thumbnail for 2-3 days."]),
 ("Step 7: Link today's Shorts to it", [
  "Yesterday's Tesla Short (Oct 16): open it in Studio (Content, Shorts, edit). If Related video is editable, set it to the long video. If not, post and pin the Short comment below with the long video link.",
  "Today's scheduled Tesla Short: open it in Studio, change the schedule to 3:00 PM today (VidIQ shows your peak at 3-5 PM), and set Related video to the long video.",
  "If the picker doesn't list the long video yet, wait until it's public and try again before 3 PM."]),
]
SHORTS = [
 "Public, and Altered/synthetic content: No.",
 "Not made for kids.",
 "Title = caption + hashtags (100 characters or fewer). Don't trim the video.",
 "Related video: the Tesla Roadster long video (every Short, every time).",
 "Comments: On.",
 "Upload the original file, never a re-download. Category: Education if shown."]

def build(pdf):
    s = [Paragraph("Tesla Roadster long video: SEO and upload pack", H1),
         Paragraph("Channel: The Business Stick HQ (@TheBusinessStickHQ). Copy everything inside the blue boxes: highlight, Ctrl+C, then paste. Plan: long video at 9:00 AM Saturday, today's Tesla Short at 3:00 PM.", P)]
    s += [Paragraph("Title (pick one; A is my recommendation)", H2),
          Paragraph("Your thumbnail already asks the question (TESLA'S NEW CAR CAN FLY?), so the title answers it and adds the money angle instead of repeating it. Keep the words 'Tesla Roadster' near the front for search.", WHY)]
    for t, l in zip(TITLES, "ABC"): s += [Paragraph(f"Option {l}", P), box(t)]
    s += [Paragraph("Description (copy the whole box)", H2),
          Paragraph("The first two lines show in search results. Chapters create clickable sections. Sources build trust. The 3 hashtags at the bottom appear as blue links above the title. The estimate is labeled as my own, and the 'no interest / no escrow' claim is labeled as from past filings, to match the fact-check.", WHY),
          box(wrap(DESC)),
          Paragraph("Tags (paste into Tags under Show more)", H2), box(wrap(TAGS, 100)),
          Paragraph("Pinned comment for the long video", H2), box(wrap(PIN)),
          Paragraph("Pinned comment for yesterday's Tesla Short (if Related video can't be edited)", H2), box(wrap(SHORT_PIN))]
    s.append(Paragraph("Step by step", H2))
    for h, items in STEPS_A + [("Step 2: Details page", [])]:
        s.append(Paragraph(h, P)); [s.append(Paragraph("[ ] " + escape(i), P)) for i in items]
    s.append(Paragraph("On the Details page: paste the Title, then the Description, then set:", P))
    for i in SETTINGS: s.append(Paragraph("[ ] " + escape(i), P))
    s.append(Paragraph("Click Next.", P))
    for h, items in STEPS_C:
        s.append(Paragraph(h, P)); [s.append(Paragraph("[ ] " + escape(i), P)) for i in items]
    s += [Paragraph("Today's Tesla Short: every YouTube Shorts setting", H2)]
    for i in SHORTS: s.append(Paragraph("[ ] " + escape(i), P))
    s += [Paragraph("Check how it's doing", H2), Paragraph("After 48 hours and again after 7 days: Studio, Analytics. A click-through rate of 4-10% is healthy for a new channel. Watch audience retention at 0:30 and send me a screenshot.", P),
          Paragraph("Don'ts: don't change the title or thumbnail for 2-3 days; don't buy views or sub-for-sub; keep to 3 hashtags.", P),
          Paragraph("Estimate, not a promise: no title or time slot guarantees views. These choices just give the video its best shot.", WHY)]
    SimpleDocTemplate(pdf, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch, title="Tesla Roadster SEO and upload pack").build(s)

def md():
    L = ["# Tesla Roadster long video: SEO and upload pack", "", "## Titles (A recommended)"] + [f"- {l}: {t}" for l, t in zip("ABC", TITLES)]
    L += ["", "## Description", "```", DESC, "```", "", "## Tags", TAGS, "", "## Pinned comment", PIN, "", "## Short pinned comment", SHORT_PIN, "", "## Details-page settings"]
    L += [f"- {i}" for i in SETTINGS] + ["", "## Shorts settings"] + [f"- {i}" for i in SHORTS]
    return "\n".join(L) + "\n"
if __name__ == "__main__":
    build(sys.argv[1]); (Path(__file__).resolve().parent.parent / "UPLOAD.md").write_text(md()); (Path(__file__).resolve().parent.parent / "YouTube-Description.txt").write_text(DESC + "\n"); print("ok")
