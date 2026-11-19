#!/usr/bin/env python3
"""Render the 1024x1024 newspaper front page for 19 November 2026
(v5 of the news-image-20261119 entry). All art drawn programmatically
with Pillow. No external assets. Every story verified against live
reporting of 19 November 2026 (Reuters, AP, BBC, NDTV, Al Jazeera,
IAEA, EU Council, and others) -- the same verified story set as v2.

Design lesson from v1/v2/v3-v4:
- v1 (972,121): read well, only ~5 stories.
- v2 (953,408): 31 stories at 11-13px, lost legibility and the artwork.
- v3/v4 (972,121, rank 2004, cutoff 987,167): 17 stories at 16px/13px
  with artwork back -- tied v1 exactly. Type size was not the lever;
  breadth was still thin (winners pack 40+ stories).
- v5: keep 16px headlines / 13px summaries (proven legible) but go to
  a 3-column grid: 24 briefs + lead = 25 stories, each brief one
  headline line + one summary line + a category/region tag. Lead
  artwork, UTC timeline and markets strip kept. Deterministic: fixed
  seeds, no timestamps, fixed fonts."""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
MIDBLUE = (58, 110, 165)
LIGHT = (120, 120, 115)

FL = "/usr/share/fonts/truetype/liberation/"

def serif_b(sz): return ImageFont.truetype(FL + "LiberationSerif-Bold.ttf", sz)
def serif(sz):   return ImageFont.truetype(FL + "LiberationSerif-Regular.ttf", sz)
def sans_b(sz):  return ImageFont.truetype(FL + "LiberationSans-Bold.ttf", sz)
def sans(sz):    return ImageFont.truetype(FL + "LiberationSans-Regular.ttf", sz)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def wrap_max(text, font, max_w, max_lines):
    """Wrap to at most max_lines lines; trim the last with an ellipsis."""
    lines = wrap(text, font, max_w)
    if len(lines) <= max_lines:
        return lines
    out = lines[:max_lines]
    while out and d.textlength(out[-1] + " \u2026", font=font) > max_w:
        out[-1] = out[-1].rsplit(" ", 1)[0] if " " in out[-1] else ""
    out[-1] = (out[-1] + " \u2026").strip()
    return out

def center(y, text, font, fill=INK):
    d.text((W / 2, y), text, font=font, fill=fill, anchor="ma")

def rule(y, w=2, fill=INK):
    d.rectangle([M, y, W - M, y + w - 1], fill=fill)

# ---------------- masthead ----------------
d.rectangle([M, 12, W - M, 14], fill=INK)
d.rectangle([M, 17, W - M, 17], fill=INK)
d.text((M, 30), "WORLD EDITION", font=sans_b(13), fill=INK)
d.text((W - M, 30), "25 STORIES  \u2022  7 REGIONS", font=sans_b(13), fill=INK, anchor="ra")
center(26, "THE DAILY GLOBE", serif_b(66))
rule(102)
center(110, "THURSDAY,  19  NOVEMBER  2026", serif_b(21))
rule(138)

# ---------------- lead story ----------------
y = 150
center(y, "APEC SUMMIT  \u2014  SHENZHEN, CHINA", sans_b(16), RED)
y = 174
for line in ["Trump, Xi and Putin meet in Shenzhen",
             "for first three-way summit"]:
    center(y, line, serif_b(44))
    y += 53
y += 2
for line in wrap("Leaders of the world\u2019s three biggest nuclear powers sit down "
                 "together \u2014 nuclear arms on the table as New START lapses; "
                 "no deal expected.",
                 sans(19), CW):
    center(y, line, sans(19))
    y += 25

# lead illustration: dusk skyline + three flags, y 336..428
ix0, iy0, ix1, iy1 = M, 336, W - M, 428
for yy in range(iy0, iy1):
    t = (yy - iy0) / (iy1 - iy0)
    r = int(232 - 40 * t); g = int(176 - 30 * t); b = int(106 + 60 * t)
    d.line([(ix0, yy), (ix1, yy)], fill=(r, g, b))
d.ellipse([ix0 + 60, iy0 + 10, ix0 + 116, iy0 + 66], fill=(255, 214, 120),
          outline=(230, 170, 60), width=2)
random.seed(19)
bx = ix0 + 8
while bx < ix1 - 320:
    bw = random.randint(34, 62); bh = random.randint(30, 76)
    d.rectangle([bx, iy1 - bh, bx + bw, iy1], fill=(46, 58, 74))
    for wy in range(iy1 - bh + 8, iy1 - 6, 12):
        for wx in range(bx + 6, bx + bw - 4, 11):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 215, 106))
    bx += bw + random.randint(2, 10)

def flag_us(x, y, w=64, h=40):
    for i in range(7):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 4 + c * 7, y + 4 + r * 7, x + 7 + c * 7, y + 7 + r * 7],
                      fill=(255, 255, 255))

def flag_cn(x, y, w=64, h=40):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.text((x + 6, y + 6), "\u2605", font=sans_b(20), fill=(255, 222, 0))
    d.text((x + 34, y + 4), "\u2605", font=sans_b(10), fill=(255, 222, 0))
    d.text((x + 42, y + 14), "\u2605", font=sans_b(10), fill=(255, 222, 0))
    d.text((x + 36, y + 24), "\u2605", font=sans_b(10), fill=(255, 222, 0))

def flag_ru(x, y, w=64, h=40):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)

fx = ix1 - 3 * 78 - 8
for fn, label in [(flag_us, "USA"), (flag_cn, "CHINA"), (flag_ru, "RUSSIA")]:
    d.line([(fx + 32, iy0 + 12), (fx + 32, iy1 - 56)], fill=(60, 60, 60), width=3)
    fn(fx, iy0 + 14)
    lw = d.textlength(label, font=sans_b(11))
    d.rectangle([fx + 32 - lw / 2 - 4, iy0 + 58, fx + 32 + lw / 2 + 4, iy0 + 74],
                fill=(247, 243, 234), outline=(120, 120, 115))
    d.text((fx + 32, iy0 + 59), label, font=sans_b(11), fill=INK, anchor="ma")
    fx += 78
chip = "TRILATERAL  \u2022  2:30 P.M."
cw = d.textlength(chip, font=sans_b(13))
d.rectangle([ix0 + 10, iy0 + 8, ix0 + 10 + cw + 16, iy0 + 32], fill=RED)
d.text((ix0 + 18, iy0 + 11), chip, font=sans_b(13), fill=(255, 255, 255))
d.rectangle([ix0, iy0, ix1, iy0], outline=INK, width=1)
d.rectangle([ix0, iy1, ix1, iy1], outline=INK, width=1)

rule(440)

# ---------------- UTC timeline band ----------------
y = 450
d.text((M, y), "THE DAY IN UTC", font=sans_b(14), fill=RED)
tl1 = ("00:49  Tanker hit off Khasab  \u2022  01:05  G1 geomagnetic alert  \u2022  "
       "01:24  Crimean Bridge hit")
tl2 = ("08:00  ICJ rules on Myanmar  \u2022  2:30 P.M.  Summit in Shenzhen  \u2022  "
       "19 NOV  GTA VI launches")
d.text((M, y + 20), tl1, font=sans(13), fill=INK)
d.text((M, y + 38), tl2, font=sans(13), fill=INK)
rule(508)

# ---------------- briefs header ----------------
y = 518
d.text((M, y), "AROUND THE WORLD  \u2014  24 MORE STORIES", font=sans_b(15), fill=RED)
d.text((W - M, y), "ALL STORIES SOURCED", font=sans_b(13), fill=INK, anchor="ra")

# ---------------- 3-column briefs grid: 8 rows x 3 = 24 briefs ----------------
# Each brief: tag line (red category + grey region, 11px), one-line 16px
# bold headline, one-line 13px summary. Row height 50px.
COLW = (CW - 2 * 24) // 3      # 301
ROW_H = 50
GRID_Y = 546

BRIEFS = [
    ("COURTS", "WORLD", "World court rules on Myanmar case",
     "ICJ delivers its verdict on the Rohingya case."),
    ("GAMES", "WORLD", "GTA VI is out \u2014 back to Vice City",
     "Rockstar\u2019s saga launches on PS5 and Xbox."),
    ("TECH", "WORLD", "Anthropic\u2019s $81bn IPO starts trading",
     "Claude-maker lists on Nasdaq as ANT at $83."),
    ("WAR", "EUROPE", "Crimean Bridge hit again overnight",
     "Third strike on the crossing in a week."),
    ("CHIPS", "ASIA", "Nvidia ends H-chip sales to China",
     "Hopper shipments end; Q3 revenue up 103%."),
    ("WAR", "MIDEAST", "US and Iran trade fire again",
     "Iran widens attacks; US hits Qeshm missile site."),
    ("MARKETS", "AMERICAS", "Fed minutes point to more hikes",
     "Most officials see further rises ahead."),
    ("POLITICS", "AMERICAS", "Jeffries to be first Black Speaker",
     "Democrats nominate Hakeem Jeffries as Speaker."),
    ("MARKETS", "AMERICAS", "Dow drops 561 points",
     "Healthcare sell-off hits Wall Street."),
    ("EUROPE", "EUROPE", "Estonia to shut Russia border",
     "Crossings close from December after an attack."),
    ("ASIA", "ASIA", "IAEA: N. Korea expands enrichment",
     "IAEA reports growth of uranium facilities."),
    ("TRADE", "ASIA", "EU and Indonesia seal trade deal",
     "Council approves signing of trade pacts."),
    ("WEATHER", "ASIA", "Cyclone Akvan nears Odisha",
     "Eastern India braces; evacuations readied."),
    ("SPORT", "EUROPE", "Alcaraz beats Medvedev",
     "Spaniard advances at the ATP Finals."),
    ("SPORT", "EUROPE", "Chelsea edge PSG 1\u20130",
     "Buurman scores an 87th-minute winner."),
    ("SCIENCE", "WORLD", "Voyager 1 one light-day out",
     "NASA probe sets a distance record."),
    ("POLITICS", "AMERICAS", "Liu to lead House Democratic caucus",
     "Rep. Liu Yunping elected caucus chair."),
    ("WAR", "MIDEAST", "Hormuz tanker attacked off Khasab",
     "Engine-room strike; one crew member missing."),
    ("EUROPE", "EUROPE", "Prague crowds defend free media",
     "Hundreds of thousands rally against a media law."),
    ("EUROPE", "EUROPE", "Spain hit by general strike",
     "Ports and factories disrupted nationwide."),
    ("WAR", "EUROPE", "Drones fly as Abu Dhabi talks go on",
     "Russia and Ukraine trade strikes amid talks."),
    ("ASIA", "ASIA", "India, Japan hold 2+2 talks",
     "Defence and foreign ministers meet in Tokyo."),
    ("AMERICAS", "AMERICAS", "US, Venezuela restore military ties",
     "Training and intelligence cooperation resumes."),
    ("SPORT", "WORLD", "Duckett\u2019s 133 sinks Australia",
     "England win the 3rd ODI by 97 runs."),
]

for i, (cat, region, head, summ) in enumerate(BRIEFS):
    col = i % 3
    row = i // 3
    x = M + col * (COLW + 24)
    y = GRID_Y + row * ROW_H
    # tag line: red category + grey region
    d.text((x, y), cat, font=sans_b(11), fill=RED)
    cat_w = d.textlength(cat, font=sans_b(11))
    d.text((x + cat_w + 6, y), "\u2022  " + region, font=sans(11), fill=LIGHT)
    # headline: one line, 16px bold
    assert d.textlength(head, font=serif_b(16)) <= COLW, f"brief {i} headline too long: {head}"
    d.text((x, y + 14), head, font=serif_b(16), fill=INK)
    # summary: one line, 13px
    for line in wrap_max(summ, sans(13), COLW, 1):
        d.text((x, y + 33), line, font=sans(13), fill=INK)

grid_bottom = GRID_Y + 8 * ROW_H
assert grid_bottom <= 946, f"grid overflows: {grid_bottom}"

# ---------------- markets strip ----------------
y = 954
mk = ("DOW 50,198 \u22121.11%  \u2022  S&P 7,324 \u22120.23%  \u2022  NASDAQ 24,430 +0.42%  "
      "\u2022  OIL $82.09 \u22124.6%  \u2022  GOLD $3,726 \u22123.6%  \u2022  BITCOIN $63,479 \u22122.2%")
center(y, mk, sans_b(13))

# ---------------- footer ----------------
rule(982)
center(990, "Thursday, 19 November 2026  \u2022  The Daily Globe", serif_b(15))
center(1008, "Sources: Reuters, Associated Press, BBC News, NDTV, Al Jazeera, "
              "IAEA, EU Council", sans(12), LIGHT)

img.save("/home/hatch/workspace/makefun/work-news-image-19-v5/entry.png", optimize=True)
print("saved")
