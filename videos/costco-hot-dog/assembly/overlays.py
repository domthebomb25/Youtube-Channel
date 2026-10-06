"""Per-shot overlay spec for the Costco hot dog video.

sign:  text painted onto a blank sign in the image (baked into the still, moves with it)
       rect = (x0, y0, x1, y1) as fractions of the image; rot = degrees counter-clockwise
label: text that pops in on top of the moving image
"""

PRICE = dict(style="price")

SIGNS = {
    9:   [dict(rect=(0.060, 0.415, 0.285, 0.655), text="$1.50", **PRICE)],
    15:  [dict(rect=(0.060, 0.415, 0.290, 0.655), text="$1.75?", style="chalk")],
    29:  [dict(rect=(0.700, 0.575, 0.885, 0.765), text="$1.50", **PRICE)],
    50:  [dict(rect=(0.405, 0.470, 0.540, 0.700), text="$1.75?", **PRICE)],
    36:  [dict(center=(0.138, 0.548), size=(0.107, 0.115), rot=5, text="$", style="money"),
          dict(center=(0.379, 0.594), size=(0.115, 0.115), text="$", style="money"),
          dict(center=(0.560, 0.358), size=(0.110, 0.115), rot=5, text="$", style="money"),
          dict(center=(0.735, 0.566), size=(0.093, 0.154), text="$", style="money"),
          dict(center=(0.890, 0.328), size=(0.105, 0.116), text="$", style="money")],
    37:  [dict(center=(0.489, 0.219), size=(0.20, 0.15), rot=8, text="$", style="money")],
    63:  [dict(center=(0.175, 0.536), size=(0.20, 0.21), rot=1, text="$", style="money_up")],
    74:  [dict(center=(0.338, 0.628), size=(0.23, 0.28), rot=3, text="$", style="money_up")],
    99:  [dict(center=(0.474, 0.462), size=(0.22, 0.40), text="$", style="money_up")],
    100: [dict(center=(0.505, 0.423), size=(0.31, 0.33), rot=1, text="$1.50", **PRICE)],
    104: [dict(center=(0.526, 0.430), size=(0.24, 0.16), rot=15, text="MEMBERSHIP", style="ticket")],
    143: [dict(center=(0.314, 0.367), size=(0.33, 0.30), rot=-2, text="NEBRASKA", style="highway")],
    69:  [dict(rect=(0.255, 0.150, 0.635, 0.660), text="$1.50", **PRICE)],
    92:  [dict(rect=(0.570, 0.160, 0.835, 0.685), text="$1.50", **PRICE)],
    94:  [dict(center=(0.330, 0.560), size=(0.20, 0.30), rot=-22, text="$1.50", **PRICE)],
    98:  [dict(rect=(0.060, 0.410, 0.285, 0.655), text="$1.50", **PRICE)],
    132: [dict(rect=(0.660, 0.810, 0.825, 0.945), text="$4.99", **PRICE)],
    160: [dict(rect=(0.260, 0.210, 0.750, 0.810), text="$1.50", **PRICE)],
    169: [dict(rect=(0.060, 0.415, 0.285, 0.655), text="$1.50", **PRICE)],
    170: [dict(rect=(0.340, 0.140, 0.710, 0.350), text="1985", style="calendar")],
}

# Reused shots: (source image, signs from that source apply too)
REUSE = {2: 1, 45: 12, 95: 92, 108: 152, 167: 1}

LABELS = {
    2:   [dict(kind="stamp", text="40 YEARS", pos=(0.70, 0.30))],
    3:   [dict(kind="year", text="1985")],
    12:  [dict(kind="name", text="CRAIG JELINEK", sub="Costco CEO, 2012–2023")],
    26:  [dict(kind="year", text="1983")],
    28:  [dict(kind="tag", text="1/4 LB · ALL BEEF")],
    31:  [dict(kind="big", text="INFLATION")],
    34:  [dict(kind="big", text="COSTS")],
    41:  [dict(kind="tag", text="+10% BIGGER")],
    42:  [dict(kind="tag", text="12 OZ CAN")],
    43:  [dict(kind="tag", text="20 OZ + FREE REFILLS")],
    45:  [dict(kind="name", text="CRAIG JELINEK", sub="Costco CEO, 2012–2023")],
    47:  [dict(kind="name", text="JIM SINEGAL", sub="Costco co-founder")],
    54:  [dict(kind="big", text="“FIGURE IT OUT.”", pos=(0.5, 0.86))],
    64:  [dict(kind="tag", text="RAISE PRICES")],
    66:  [dict(kind="tag", text="LOW-PRICE LEADER")],
    83:  [dict(kind="tag", text="TRACY, CALIFORNIA")],
    84:  [dict(kind="tag", text="MORRIS, ILLINOIS")],
    86:  [dict(kind="tag", text="KIRKLAND SIGNATURE")],
    90:  [dict(kind="year", text="2013"), dict(kind="tag", text="COKE OUT · PEPSI IN")],
    93:  [dict(kind="year", text="2025"), dict(kind="tag", text="BACK TO COKE")],
    95:  [dict(kind="stamp", text="STILL $1.50", pos=(0.30, 0.30))],
    96:  [dict(kind="year", text="2026"), dict(kind="tag", text="+ WATER OPTION")],
    108: [dict(kind="paid", text="MEMBERSHIP PAID", pos=(0.30, 0.15))],
    133: [dict(kind="year", text="SINCE 2009")],
    138: [dict(kind="name", text="RICHARD GALANTI", sub="Costco's former CFO")],
    144: [dict(kind="tag", text="OPENED 2019")],
    147: [dict(kind="tag", text="UP TO 2 MILLION / WEEK")],
    148: [dict(kind="sticker", text="$4.99", pos=(0.49, 0.40))],
    157: [dict(kind="big", text="MISTAKE?", pos=(0.5, 0.86))],
    163: [dict(kind="tag", text="$1.50")],
    171: [dict(kind="year", text="1985")],
    173: [dict(kind="tag", text="NEW FORMULA")],
    174: [dict(kind="tag", text="BLIND TASTE TEST")],
}

# Motion overrides. Default cycles through MOTION_CYCLE.
MOTION_CYCLE = ["in", "right", "out", "left", "in", "up"]
MOTION = {
    1: "in",
    2: dict(kind="focus", at=(0.17, 0.53), z0=1.15, z1=1.9),
    95: dict(kind="focus", at=(0.70, 0.42), z0=1.1, z1=1.6),
    167: "out",
    176: "hold",
}

GRAPHICS = {7, 8, 19, 33, 59, 60, 106, 107, 111, 112, 115, 125, 136, 145}

END_TAIL = 12.0  # seconds of end-screen hold after the voiceover
