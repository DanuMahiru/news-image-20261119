#!/usr/bin/env python3
"""Draw the 1024x1024 newspaper front page for Thursday 19 November 2026.

This is the v6 generator for the news-image-20261119 entry. Every piece of
art is drawn in code with Pillow -- no photos, no downloaded assets, no
copied material. All 40 stories are verified against real reporting from
19 November 2026 (Reuters, AP, BBC, NDTV, Al Jazeera, IAEA, EU Council
and others): the 25-story v5 set plus briefs restored from the verified
v2 set and further stories verified from the day's reporting.

Layout idea (v6): reach the winners' breadth of 40 stories without ever
shrinking the type. The lead headline goes 44px -> 40px with a one-line
summary, the picture band 92px -> 64px, the timeline becomes one line,
brief rows tighten 50px -> 45px, and a headline-only "MORE IN BRIEF"
tier adds 9 stories at 13px bold. Lead + 30 briefs + 9 one-liners = 40.
Type never drops below 13px; the main grid keeps 16px bold headlines
with 13px summaries. The markets strip uses only verified 19 Nov close
figures (S&P 500, Nasdaq, Brent, gold, VIX)."""
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
d.text((W - M, 30), "40 STORIES  \u2022  7 REGIONS", font=sans_b(13), fill=INK, anchor="ra")
center(26, "THE DAILY GLOBE", serif_b(66))
rule(102)
center(110, "THURSDAY,  19  NOVEMBER  2026", serif_b(21))
rule(138)

# ---------------- lead story ----------------
y = 150
center(y, "APEC SUMMIT  \u2014  SHENZHEN, CHINA", sans_b(16), RED)
y = 172
for line in ["Trump, Xi and Putin meet in Shenzhen",
             "for first three-way summit"]:
    center(y, line, serif_b(40))
    y += 48
lead_sum = wrap_max("Leaders of the world\u2019s three biggest nuclear powers "
                    "meet \u2014 nuclear arms on the table.",
                    sans(18), CW, 1)
assert len(lead_sum) == 1 and "\u2026" not in lead_sum[0], "lead summary overflow"
center(266, lead_sum[0], sans(18))

# lead illustration: dusk skyline + three flags, y 296..360 (64px band)
ix0, iy0, ix1, iy1 = M, 296, W - M, 360
for yy in range(iy0, iy1):
    t = (yy - iy0) / (iy1 - iy0)
    r = int(232 - 40 * t); g = int(176 - 30 * t); b = int(106 + 60 * t)
    d.line([(ix0, yy), (ix1, yy)], fill=(r, g, b))
d.ellipse([ix0 + 60, iy0 + 6, ix0 + 104, iy0 + 50], fill=(255, 214, 120),
          outline=(230, 170, 60), width=2)
random.seed(19)
bx = ix0 + 8
while bx < ix1 - 280:
    bw = random.randint(30, 56); bh = random.randint(18, 48)
    d.rectangle([bx, iy1 - bh, bx + bw, iy1], fill=(46, 58, 74))
    for wy in range(iy1 - bh + 6, iy1 - 4, 11):
        for wx in range(bx + 5, bx + bw - 3, 10):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 215, 106))
    bx += bw + random.randint(2, 10)

def flag_us(x, y, w=56, h=35):
    for i in range(7):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(30, 50, 110))
    for r in range(3):
        for c in range(3):
            d.ellipse([x + 3 + c * 6, y + 3 + r * 6, x + 6 + c * 6, y + 6 + r * 6],
                      fill=(255, 255, 255))

def flag_cn(x, y, w=56, h=35):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.text((x + 5, y + 4), "\u2605", font=sans_b(16), fill=(255, 222, 0))
    d.text((x + 30, y + 3), "\u2605", font=sans_b(9), fill=(255, 222, 0))
    d.text((x + 37, y + 12), "\u2605", font=sans_b(9), fill=(255, 222, 0))
    d.text((x + 31, y + 21), "\u2605", font=sans_b(9), fill=(255, 222, 0))

def flag_ru(x, y, w=56, h=35):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)

fx = ix1 - 3 * 78 - 8
for fn, label in [(flag_us, "USA"), (flag_cn, "CHINA"), (flag_ru, "RUSSIA")]:
    d.line([(fx + 28, iy0 + 4), (fx + 28, iy1 - 4)], fill=(60, 60, 60), width=3)
    fn(fx, iy0 + 6)
    lw = d.textlength(label, font=sans_b(11))
    d.rectangle([fx + 28 - lw / 2 - 4, iy0 + 44, fx + 28 + lw / 2 + 4, iy0 + 58],
                fill=(247, 243, 234), outline=(120, 120, 115))
    d.text((fx + 28, iy0 + 45), label, font=sans_b(11), fill=INK, anchor="ma")
    fx += 78
chip = "TRILATERAL  \u2022  2:30 P.M."
cw = d.textlength(chip, font=sans_b(13))
d.rectangle([ix0 + 10, iy0 + 6, ix0 + 10 + cw + 16, iy0 + 30], fill=RED)
d.text((ix0 + 18, iy0 + 9), chip, font=sans_b(13), fill=(255, 255, 255))
d.rectangle([ix0, iy0, ix1, iy0], outline=INK, width=1)
d.rectangle([ix0, iy1, ix1, iy1], outline=INK, width=1)

rule(372)

# ---------------- UTC timeline band (single line) ----------------
tl_label = "THE DAY IN UTC  \u2022  "
tl_events = ("00:49  Tanker hit off Khasab  \u2022  08:00  ICJ rules on Myanmar  "
             "\u2022  2:30 P.M.  Summit in Shenzhen  \u2022  19 NOV  GTA VI launches")
assert d.textlength(tl_label, font=sans_b(13)) + d.textlength(tl_events, font=sans(13)) <= CW, "timeline overflow"
d.text((M, 384), tl_label, font=sans_b(13), fill=RED)
lx = M + d.textlength(tl_label, font=sans_b(13))
d.text((lx, 384), tl_events, font=sans(13), fill=INK)
rule(410)

# ---------------- briefs header ----------------
y = 420
d.text((M, y), "AROUND THE WORLD  \u2014  30 MORE STORIES", font=sans_b(15), fill=RED)
d.text((W - M, y), "ALL STORIES SOURCED", font=sans_b(13), fill=INK, anchor="ra")

# ---------------- 3-column briefs grid: 10 rows x 3 = 30 briefs ----------------
# Each brief: tag line (red category + grey region, 11px), one-line 16px
# bold headline, one-line 13px summary. Row height 45px.
COLW = (CW - 2 * 24) // 3      # 301
ROW_H = 45
GRID_Y = 448

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
    ("ASIA", "ASIA", "Delhi schools reopen",
     "Offline classes resume as air curbs lift."),
    ("SPORT", "ASIA", "Sindhu back in world top five",
     "India's badminton star returns to elite."),
    ("MIDEAST", "MIDEAST", "Canada sanctions Israeli settlers",
     "Ottawa targets settlers over West Bank."),
    ("AMERICAS", "AMERICAS", "US pursues $2bn Philippines loans",
     "White House backs $2bn finance package."),
    ("AMERICAS", "AMERICAS", "Panama arrests second suspect",
     "Second arrest in attack on journalist."),
    ("AMERICAS", "AMERICAS", "US sanctions Hezbollah network",
     "Three entities, three people on OFAC list."),
]
assert len(BRIEFS) == 30, f"expected 30 briefs, got {len(BRIEFS)}"

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
    d.text((x, y + 12), head, font=serif_b(16), fill=INK)
    # summary: one line, 13px
    for line in wrap_max(summ, sans(13), COLW, 1):
        d.text((x, y + 29), line, font=sans(13), fill=INK)

grid_bottom = GRID_Y + 10 * ROW_H
assert grid_bottom <= 900, f"grid overflows: {grid_bottom}"

# ---------------- MORE IN BRIEF: 9 headline-only items, 3 rows x 3 ----------------
y = 908
d.text((M, y), "MORE IN BRIEF  \u2014  9 MORE", font=sans_b(13), fill=RED)
COMPACT = [
    "First CME seen on another star",
    "Russian bombers land in Vietnam",
    "EU proposes \u20ac45bn loan for Ukraine",
    "Senate rejects Iran war powers 51\u201348",
    "UK, Norway fund \u00a3100m warships for Kyiv",
    "Denmark approves Greenland pact 109\u20130",
    "Israeli forces cross Gaza ceasefire line",
    "Bangladesh shutdown turns violent",
    "Gas Husky tanker sinks off Bulgaria",
]
assert len(COMPACT) == 9, f"expected 9 compact items, got {len(COMPACT)}"
for i, head in enumerate(COMPACT):
    col = i % 3
    row = i // 3
    x = M + col * (COLW + 24)
    y = 928 + row * 19
    assert d.textlength(head, font=sans_b(13)) <= COLW, f"compact {i} too long: {head}"
    d.text((x, y), head, font=sans_b(13), fill=INK)

# ---------------- markets strip (verified 19 Nov close figures only) ----------------
y = 984
mk = ("S&P 500 7,324 \u22120.23%  \u2022  NASDAQ 24,430 +0.42%  \u2022  "
      "BRENT $89.59 \u22122.57%  \u2022  GOLD $3,740 \u22120.06%  \u2022  VIX 24.56 \u22123.53%")
center(y, mk, sans_b(13))

# ---------------- footer (single line) ----------------
rule(1002)
center(1008, "Thursday, 19 November 2026  \u2022  The Daily Globe  \u2022  "
              "Sources: Reuters, AP, BBC, NDTV, Al Jazeera, IAEA, EU Council",
       sans(12), LIGHT)

img.save("/home/hatch/workspace/makefun/work-news-image-19-v6/entry.png", optimize=True)
print("saved")
print("stories:", 1 + len(BRIEFS) + len(COMPACT))
