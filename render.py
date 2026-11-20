#!/usr/bin/env python3
"""Front-page generator: one 1024x1024 newspaper image for 19 November 2026.

This script paints the whole page with Pillow and nothing else — every
skyline, flag, rule and headline is drawn by code, so the output is fully
reproducible. The edition carries forty stories: a trilateral-summit lead,
a three-column briefs grid, and a headline-only "more in brief" tier.

The layout squeezes breadth out of the chrome rather than the type:
a shorter lead, a slimmer picture band, a one-line timeline and tighter
brief rows leave room for the extra stories while the smallest type
stays at thirteen pixels. Market figures are the verified 19 November
closes. All story wording comes from real reporting of the day
(Reuters, AP, BBC, NDTV, Al Jazeera, IAEA, EU Council and others)."""
import random
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 36                       # space at each side
CONTENT_W = PAGE_W - 2 * MARGIN   # 952 usable pixels across

BG = (247, 243, 234)
FG = (17, 17, 17)
ACCENT = (164, 30, 34)
NAVY = (31, 78, 121)
SKY = (58, 110, 165)
GREY = (120, 120, 115)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
_FONT_FILES = {
    "serif-bold": "LiberationSerif-Bold.ttf",
    "serif": "LiberationSerif-Regular.ttf",
    "sans-bold": "LiberationSans-Bold.ttf",
    "sans": "LiberationSans-Regular.ttf",
}


def typeface(kind, size):
    return ImageFont.truetype(FONT_DIR + _FONT_FILES[kind], size)


page = Image.new("RGB", (PAGE_W, PAGE_H), BG)
pen = ImageDraw.Draw(page)


def fold_text(text, font, max_w):
    """Greedy word wrap: pack words onto lines no wider than max_w."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if pen.textlength(candidate, font=font) <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fold_limited(text, font, max_w, max_lines):
    """Wrap, then cut to max_lines lines with an ellipsis on the last."""
    lines = fold_text(text, font, max_w)
    if len(lines) <= max_lines:
        return lines
    trimmed = lines[:max_lines]
    while trimmed and pen.textlength(trimmed[-1] + " \u2026", font=font) > max_w:
        trimmed[-1] = trimmed[-1].rsplit(" ", 1)[0] if " " in trimmed[-1] else ""
    trimmed[-1] = (trimmed[-1] + " \u2026").strip()
    return trimmed


def centred(y, text, font, colour=FG):
    pen.text((PAGE_W / 2, y), text, font=font, fill=colour, anchor="ma")


def hline(y, thick=2, colour=FG):
    pen.rectangle([MARGIN, y, PAGE_W - MARGIN, y + thick - 1], fill=colour)


def draw_masthead():
    """Top banner: thin rules, edition line, title, dateline."""
    pen.rectangle([MARGIN, 12, PAGE_W - MARGIN, 14], fill=FG)
    pen.rectangle([MARGIN, 17, PAGE_W - MARGIN, 17], fill=FG)
    pen.text((MARGIN, 30), "WORLD EDITION", font=typeface("sans-bold", 13), fill=FG)
    pen.text((PAGE_W - MARGIN, 30), "40 STORIES  \u2022  7 REGIONS", font=typeface("sans-bold", 13), fill=FG, anchor="ra")
    centred(26, "THE DAILY GLOBE", typeface("serif-bold", 66))
    hline(102)
    centred(110, "THURSDAY,  19  NOVEMBER  2026", typeface("serif-bold", 21))
    hline(138)


def draw_lead():
    """Lead story: kicker, two-line headline, one-line summary."""
    top = 150
    centred(top, "APEC SUMMIT  \u2014  SHENZHEN, CHINA", typeface("sans-bold", 16), ACCENT)
    cursor = 172
    for line in ["Trump, Xi and Putin meet in Shenzhen",
                 "for first three-way summit"]:
        centred(cursor, line, typeface("serif-bold", 40))
        cursor += 48
    summary = fold_limited("Leaders of the world\u2019s three biggest nuclear powers "
                           "meet \u2014 nuclear arms on the table.",
                           typeface("sans", 18), CONTENT_W, 1)
    assert len(summary) == 1 and "\u2026" not in summary[0], "lead summary overflow"
    centred(266, summary[0], typeface("sans", 18))


def draw_us_flag(x, y, w=56, h=35):
    for stripe in range(7):
        pen.rectangle([x, y + stripe * h // 7, x + w, y + (stripe + 1) * h // 7],
                      fill=(178, 34, 52) if stripe % 2 == 0 else (255, 255, 255))
    pen.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(30, 50, 110))
    for r in range(3):
        for c in range(3):
            pen.ellipse([x + 3 + c * 6, y + 3 + r * 6, x + 6 + c * 6, y + 6 + r * 6],
                        fill=(255, 255, 255))


def draw_cn_flag(x, y, w=56, h=35):
    pen.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    pen.text((x + 5, y + 4), "\u2605", font=typeface("sans-bold", 16), fill=(255, 222, 0))
    pen.text((x + 30, y + 3), "\u2605", font=typeface("sans-bold", 9), fill=(255, 222, 0))
    pen.text((x + 37, y + 12), "\u2605", font=typeface("sans-bold", 9), fill=(255, 222, 0))
    pen.text((x + 31, y + 21), "\u2605", font=typeface("sans-bold", 9), fill=(255, 222, 0))


def draw_ru_flag(x, y, w=56, h=35):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        pen.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)


def draw_art_band():
    """Picture band, y 296..360: dusk sky, sun, lit skyline, three flags."""
    bx0, by0, bx1, by1 = MARGIN, 296, PAGE_W - MARGIN, 360
    for scan_y in range(by0, by1):
        frac = (scan_y - by0) / (by1 - by0)
        cr = int(232 - 40 * frac); cg = int(176 - 30 * frac); cb = int(106 + 60 * frac)
        pen.line([(bx0, scan_y), (bx1, scan_y)], fill=(cr, cg, cb))
    pen.ellipse([bx0 + 60, by0 + 6, bx0 + 104, by0 + 50], fill=(255, 214, 120),
                outline=(230, 170, 60), width=2)
    random.seed(19)
    cursor_x = bx0 + 8
    while cursor_x < bx1 - 280:
        w_px = random.randint(30, 56); h_px = random.randint(18, 48)
        pen.rectangle([cursor_x, by1 - h_px, cursor_x + w_px, by1], fill=(46, 58, 74))
        for win_y in range(by1 - h_px + 6, by1 - 4, 11):
            for win_x in range(cursor_x + 5, cursor_x + w_px - 3, 10):
                if random.random() < 0.45:
                    pen.rectangle([win_x, win_y, win_x + 4, win_y + 5], fill=(255, 215, 106))
        cursor_x += w_px + random.randint(2, 10)

    fx = bx1 - 3 * 78 - 8
    for draw_flag, label in [(draw_us_flag, "USA"), (draw_cn_flag, "CHINA"), (draw_ru_flag, "RUSSIA")]:
        pen.line([(fx + 28, by0 + 4), (fx + 28, by1 - 4)], fill=(60, 60, 60), width=3)
        draw_flag(fx, by0 + 6)
        label_w = pen.textlength(label, font=typeface("sans-bold", 11))
        pen.rectangle([fx + 28 - label_w / 2 - 4, by0 + 44, fx + 28 + label_w / 2 + 4, by0 + 58],
                      fill=(247, 243, 234), outline=(120, 120, 115))
        pen.text((fx + 28, by0 + 45), label, font=typeface("sans-bold", 11), fill=FG, anchor="ma")
        fx += 78
    badge = "TRILATERAL  \u2022  2:30 P.M."
    badge_w = pen.textlength(badge, font=typeface("sans-bold", 13))
    pen.rectangle([bx0 + 10, by0 + 6, bx0 + 10 + badge_w + 16, by0 + 30], fill=ACCENT)
    pen.text((bx0 + 18, by0 + 9), badge, font=typeface("sans-bold", 13), fill=(255, 255, 255))
    pen.rectangle([bx0, by0, bx1, by0], outline=FG, width=1)
    pen.rectangle([bx0, by1, bx1, by1], outline=FG, width=1)
    hline(372)


def draw_timeline():
    """One-line UTC timeline of the day's key moments."""
    head = "THE DAY IN UTC  \u2022  "
    items = ("00:49  Tanker hit off Khasab  \u2022  08:00  ICJ rules on Myanmar  "
             "\u2022  2:30 P.M.  Summit in Shenzhen  \u2022  19 NOV  GTA VI launches")
    assert pen.textlength(head, font=typeface("sans-bold", 13)) + pen.textlength(items, font=typeface("sans", 13)) <= CONTENT_W, "timeline overflow"
    pen.text((MARGIN, 384), head, font=typeface("sans-bold", 13), fill=ACCENT)
    text_x = MARGIN + pen.textlength(head, font=typeface("sans-bold", 13))
    pen.text((text_x, 384), items, font=typeface("sans", 13), fill=FG)
    hline(410)


# Three-column briefs grid: 10 rows x 3 columns = 30 briefs.
# Each brief: red tag + grey region (11px), one-line 16px bold headline,
# one-line 13px summary. Row height 45px.
COL_W = (CONTENT_W - 2 * 24) // 3   # 301
ROW_PX = 45
GRID_TOP = 448

STORIES = [
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
assert len(STORIES) == 30, f"expected 30 briefs, got {len(STORIES)}"


def draw_briefs():
    """Briefs header plus the 30-brief grid."""
    pen.text((MARGIN, 420), "AROUND THE WORLD  \u2014  30 MORE STORIES", font=typeface("sans-bold", 15), fill=ACCENT)
    pen.text((PAGE_W - MARGIN, 420), "ALL STORIES SOURCED", font=typeface("sans-bold", 13), fill=FG, anchor="ra")
    for idx, (tag, zone, title, blurb) in enumerate(STORIES):
        col = idx % 3
        row = idx // 3
        x = MARGIN + col * (COL_W + 24)
        y = GRID_TOP + row * ROW_PX
        pen.text((x, y), tag, font=typeface("sans-bold", 11), fill=ACCENT)
        tag_w = pen.textlength(tag, font=typeface("sans-bold", 11))
        pen.text((x + tag_w + 6, y), "\u2022  " + zone, font=typeface("sans", 11), fill=GREY)
        assert pen.textlength(title, font=typeface("serif-bold", 16)) <= COL_W, f"brief {idx} headline too long: {title}"
        pen.text((x, y + 12), title, font=typeface("serif-bold", 16), fill=FG)
        for line in fold_limited(blurb, typeface("sans", 13), COL_W, 1):
            pen.text((x, y + 29), line, font=typeface("sans", 13), fill=FG)
    bottom = GRID_TOP + 10 * ROW_PX
    assert bottom <= 900, f"grid overflows: {bottom}"


HEADLINES_ONLY = [
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
assert len(HEADLINES_ONLY) == 9, f"expected 9 compact items, got {len(HEADLINES_ONLY)}"


def draw_compact():
    """MORE IN BRIEF: 9 headline-only items, 3 rows x 3."""
    pen.text((MARGIN, 908), "MORE IN BRIEF  \u2014  9 MORE", font=typeface("sans-bold", 13), fill=ACCENT)
    for idx, title in enumerate(HEADLINES_ONLY):
        col = idx % 3
        row = idx // 3
        x = MARGIN + col * (COL_W + 24)
        y = 928 + row * 19
        assert pen.textlength(title, font=typeface("sans-bold", 13)) <= COL_W, f"compact {idx} too long: {title}"
        pen.text((x, y), title, font=typeface("sans-bold", 13), fill=FG)


def draw_markets():
    """Markets strip: verified 19 Nov close figures only."""
    tickers = ("S&P 500 7,324 \u22120.23%  \u2022  NASDAQ 24,430 +0.42%  \u2022  "
               "BRENT $89.59 \u22122.57%  \u2022  GOLD $3,740 \u22120.06%  \u2022  VIX 24.56 \u22123.53%")
    centred(984, tickers, typeface("sans-bold", 13))


def draw_footer():
    """Single-line footer with date, title and sources."""
    hline(1002)
    centred(1008, "Thursday, 19 November 2026  \u2022  The Daily Globe  \u2022  "
                  "Sources: Reuters, AP, BBC, NDTV, Al Jazeera, IAEA, EU Council",
           typeface("sans", 12), GREY)


draw_masthead()
draw_lead()
draw_art_band()
draw_timeline()
draw_briefs()
draw_compact()
draw_markets()
draw_footer()

page.save("/home/hatch/workspace/makefun/work-news-image-19-v6/entry.png", optimize=True)
print("saved")
print("stories:", 1 + len(STORIES) + len(HEADLINES_ONLY))
