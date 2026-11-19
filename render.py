#!/usr/bin/env python3
"""Render the 1024x1024 newspaper front page for 19 November 2026.
All art is drawn programmatically with Pillow. No external assets.
Every story verified against live reporting (Reuters, AP, BBC, HRW,
The Guardian) on 19 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import math
import random

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
MIDBLUE = (58, 110, 165)
LIGHT = (120, 120, 115)
NEON_PINK = (255, 64, 160)
NEON_CYAN = (64, 224, 255)

FD = "/usr/share/fonts/truetype/dejavu/"
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

def center(y, text, font, fill=INK):
    d.text((W / 2, y), text, font=font, fill=fill, anchor="ma")

def rule(y, w=2, fill=INK):
    d.rectangle([M, y, W - M, y + w - 1], fill=fill)

# ---------------- masthead ----------------
d.rectangle([M, 12, W - M, 14], fill=INK)
d.rectangle([M, 17, W - M, 17], fill=INK)
d.text((M, 30), "WORLD EDITION", font=sans_b(13), fill=INK)
d.text((W - M, 30), "ONE PAGE  \u2022  FREE", font=sans_b(13), fill=INK, anchor="ra")
center(26, "THE DAILY GLOBE", serif_b(66))
rule(102)
center(110, "THURSDAY,  19  NOVEMBER  2026", serif_b(21))
rule(138)

# ---------------- lead story ----------------
y = 152
center(y, "APEC SUMMIT  \u2014  SHENZHEN, CHINA", sans_b(16), RED)
y = 176
for line in ["Trump, Xi and Putin meet in Shenzhen",
             "for first three-way summit"]:
    center(y, line, serif_b(44))
    y += 53
y += 4
for line in wrap("Leaders of the world\u2019s three biggest nuclear powers sit down "
                 "together \u2014 nuclear arms on the table as New START lapses; "
                 "no deal expected.",
                 sans(19), CW):
    center(y, line, sans(19))
    y += 25

# lead illustration: dusk skyline + three flags, y 330..450
ix0, iy0, ix1, iy1 = M, 330, W - M, 450
for yy in range(iy0, iy1):
    t = (yy - iy0) / (iy1 - iy0)
    r = int(232 - 40 * t); g = int(176 - 30 * t); b = int(106 + 60 * t)
    d.line([(ix0, yy), (ix1, yy)], fill=(r, g, b))
d.ellipse([ix0 + 60, iy0 + 12, ix0 + 116, iy0 + 68], fill=(255, 214, 120),
          outline=(230, 170, 60), width=2)
random.seed(19)
bx = ix0 + 8
while bx < ix1 - 320:
    bw = random.randint(34, 62); bh = random.randint(34, 92)
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
    d.line([(fx + 32, iy0 + 14), (fx + 32, iy1 - 58)], fill=(60, 60, 60), width=3)
    fn(fx, iy0 + 16)
    lw = d.textlength(label, font=sans_b(11))
    d.rectangle([fx + 32 - lw / 2 - 4, iy0 + 60, fx + 32 + lw / 2 + 4, iy0 + 76],
                fill=(247, 243, 234), outline=(120, 120, 115))
    d.text((fx + 32, iy0 + 61), label, font=sans_b(11), fill=INK, anchor="ma")
    fx += 78
# time chip, left of the flags
chip = "TRILATERAL  \u2022  2:30 P.M."
cw = d.textlength(chip, font=sans_b(13))
d.rectangle([ix0 + 10, iy0 + 10, ix0 + 10 + cw + 16, iy0 + 34],
            fill=RED)
d.text((ix0 + 18, iy0 + 13), chip, font=sans_b(13), fill=(255, 255, 255))
d.rectangle([ix0, iy0, ix1, iy0], outline=INK, width=1)
d.rectangle([ix0, iy1, ix1, iy1], outline=INK, width=1)

rule(464)

# ---------------- row 2: two columns ----------------
COLW = (CW - 20) // 2   # 466
def kicker(x, y, text):
    d.text((x, y), text, font=sans_b(15), fill=RED)

# left: ICJ Rohingya verdict
x = M; y = 478
kicker(x, y, "THE HAGUE  \u2014  WORLD COURT")
y = 500
for line in wrap("World court rules today on Myanmar genocide case", serif_b(25), COLW):
    d.text((x, y), line, font=serif_b(25), fill=INK); y += 30
y += 4
for line in wrap("ICJ delivers its final judgment in The Gambia\u2019s case over the "
                 "2017 Rohingya crackdown; 730,000 fled to Bangladesh.",
                 sans(16), COLW):
    d.text((x, y), line, font=sans(16), fill=INK); y += 21
# scales of justice, y 616..716
sx0, sy0, sx1, sy1 = x, 616, x + COLW, 716
d.rectangle([sx0, sy0, sx1, sy1], fill=(232, 228, 218), outline=INK, width=1)
cx, top = (sx0 + sx1) // 2, sy0 + 10
d.rectangle([cx - 3, top + 14, cx + 3, sy1 - 14], fill=INK)
d.ellipse([cx - 7, top, cx + 7, top + 14], fill=INK)
d.line([(cx - 78, top + 22), (cx + 78, top + 22)], fill=INK, width=3)
for sgn in (-1, 1):
    px = cx + sgn * 78
    d.line([(px, top + 22), (px, top + 48)], fill=INK, width=2)
    d.polygon([(px - 34, top + 48), (px + 34, top + 48), (px, top + 72)],
              outline=INK, width=2)
d.rectangle([cx - 52, sy1 - 14, cx + 52, sy1 - 8], fill=INK)
d.text((sx0 + 10, sy0 + 8), "THE GAMBIA v. MYANMAR", font=sans_b(12), fill=INK)
d.text((sx1 - 10, sy1 - 26), "8:00 GMT", font=sans_b(12), fill=INK, anchor="ra")

# right: GTA VI launch
x = M + COLW + 20; y = 478
kicker(x, y, "CULTURE  \u2014  GAMES")
y = 500
for line in wrap("GTA VI is out \u2014 welcome back to Vice City", serif_b(25), COLW):
    d.text((x, y), line, font=serif_b(25), fill=INK); y += 30
y += 4
for line in wrap("Rockstar\u2019s crime saga launches on PS5 and Xbox, 13 years after "
                 "GTA V; fans take the day off to play.",
                 sans(16), COLW):
    d.text((x, y), line, font=sans(16), fill=INK); y += 21
# neon Vice City skyline, y 616..716
vx0, vy0, vx1, vy1 = x, 616, x + COLW, 716
d.rectangle([vx0, vy0, vx1, vy1], fill=(24, 16, 44), outline=INK, width=1)
d.ellipse([vx0 + 190, vy0 + 10, vx0 + 250, vy0 + 70], fill=NEON_PINK)
random.seed(91)
nx = vx0 + 8
while nx < vx1 - 30:
    bw = random.randint(26, 48); bh = random.randint(28, 78)
    col = (58, 40, 110) if random.random() < 0.6 else (90, 50, 120)
    d.rectangle([nx, vy1 - bh, nx + bw, vy1], fill=col)
    for wy in range(vy1 - bh + 6, vy1 - 4, 10):
        for wx in range(nx + 5, nx + bw - 3, 9):
            if random.random() < 0.5:
                d.rectangle([wx, wy, wx + 3, wy + 4],
                            fill=NEON_CYAN if random.random() < 0.5 else (255, 220, 120))
    nx += bw + random.randint(2, 8)
d.text((vx0 + 10, vy0 + 8), "VICE CITY", font=sans_b(13), fill=(255, 255, 255))
d.text((vx1 - 10, vy0 + 8), "PS5  \u2022  XBOX", font=sans_b(12), fill=(255, 255, 255),
       anchor="ra")

rule(730)

# ---------------- row 3: two columns ----------------
def stat_chip(x, y, big, label, color=INK):
    d.text((x, y), big, font=serif_b(34), fill=color)
    bw = d.textlength(big, font=serif_b(34))
    d.text((x + bw + 10, y + 8), label, font=sans(14), fill=INK)

# left: Anthropic IPO debut
x = M; y = 744
kicker(x, y, "TECH & MARKETS")
y = 766
for line in wrap("Anthropic\u2019s record $81bn IPO starts trading", serif_b(25), COLW):
    d.text((x, y), line, font=serif_b(25), fill=INK); y += 30
y += 2
for line in wrap("Claude-maker lists on Nasdaq as ANT at $83 a share, valued near "
                 "$1.5 trillion \u2014 the biggest IPO ever.",
                 sans(16), COLW):
    d.text((x, y), line, font=sans(16), fill=INK); y += 21
# rising chart, y 876..910
cx0, cy0, cx1, cy1 = x, 876, x + COLW, 910
d.rectangle([cx0, cy0, cx1, cy1], fill=(255, 255, 255), outline=INK, width=1)
pts = [(cx0 + 8 + i * 52, cy1 - 6 - i * 3) for i in range(9)]
d.line(pts, fill=MIDBLUE, width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
d.text((cx1 - 8, cy0 + 4), "$83", font=sans_b(13), fill=RED, anchor="ra")

# right: Crimean Bridge
x = M + COLW + 20; y = 744
kicker(x, y, "UKRAINE WAR  \u2014  CRIMEA")
y = 766
for line in wrap("Crimean Bridge hit again overnight", serif_b(25), COLW):
    d.text((x, y), line, font=serif_b(25), fill=INK); y += 30
y += 2
for line in wrap("Third strike on the crossing in a week; traffic halted as the "
                 "governor confirms damage checks.",
                 sans(16), COLW):
    d.text((x, y), line, font=sans(16), fill=INK); y += 21
stat_chip(x, 876, "3rd", "strike on the bridge\nin one week", RED)

rule(922)

# ---------------- in brief ticker ----------------
y = 934
d.text((M, y), "IN BRIEF", font=sans_b(15), fill=RED)
tick = ("Gulf: Saudi Arabia says danger passed in three southern cities  \u2022  "
        "Hormuz tanker attacked, one crew missing  \u2022  Israel\u2019s Herzog taps "
        "Eisenkot to form government  \u2022  Fed minutes point to more rate hikes  \u2022  "
        "Van Gogh sells for record $190.4m")
lines = wrap(tick, sans(15), CW - 92)
ty = y
for line in lines:
    d.text((M + 92, ty), line, font=sans(15), fill=INK); ty += 19

# ---------------- footer ----------------
rule(978)
center(986, "Thursday, 19 November 2026  \u2022  The Daily Globe", serif_b(15))
center(1004, "Sources: Reuters, Associated Press, BBC News, Human Rights Watch, "
              "The Guardian", sans(12), LIGHT)

img.save("/home/hatch/workspace/makefun/work-news-image-19/entry.png", optimize=True)
print("saved")
