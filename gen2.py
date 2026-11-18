#!/usr/bin/env python3
"""Draw the one-page world-news front page for Wednesday 18 November 2026.

Own work only: every mark is drawn here with Pillow. No photograph, no map data,
no network. The page carries 47 headlines from six continents, the day's numbers
and the date the stories belong to.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (245, 241, 232)
INK = (20, 20, 20)
RED = (161, 30, 24)
MUTED = (100, 95, 85)
HAIR = (198, 190, 176)
NAVY = (15, 25, 43)
CREAM = (245, 241, 232)
GOLD = (214, 178, 108)
GREY_ON_NAVY = (168, 166, 158)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"

M = 40
_cache = {}


def fnt(path, size):
    key = (path, round(size, 1))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, int(round(size)))
    return _cache[key]


def wrap(d, text, font, width, max_lines):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        kept = lines[:max_lines]
        last = kept[-1]
        while last and d.textlength(last + "…", font=font) > width:
            last = last[:-1]
        kept[-1] = last.rstrip() + "…"
        lines = kept
    return lines


def text_block(d, xy, text, font, width, max_lines, fill=INK, leading=1.16, gap=0):
    x, y = xy
    lines = wrap(d, text, font, width, max_lines)
    lh = int(font.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y + gap


def tracked(d, xy, text, font, fill, spacing=1.6):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing
    return x


def rule(d, y, x0=M, x1=W - M, width=1, color=INK):
    d.rectangle([x0, y, x1 - 1, y + width - 1], fill=color)


def globe(d, cx, cy, r):
    """Drawn sphere with a graticule; no third-party map data."""
    for i in range(r, 0, -1):
        t = i / r
        shade = int(19 + 30 * (1.0 - t * t))
        d.ellipse([cx - i, cy - i, cx + i, cy + i],
                  fill=(shade, int(shade * 1.55), int(shade * 2.25)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(80, 108, 143), width=2)
    grid = (60, 85, 116)
    for k in (-0.66, -0.33, 0.0, 0.33, 0.66):
        ry = int(abs(k) * r)
        if ry < 2:
            d.line([cx - r, cy, cx + r, cy], fill=grid, width=1)
        else:
            d.arc([cx - r, cy - ry, cx + r, cy + ry], 0, 180, fill=grid, width=1)
            d.arc([cx - r, cy - ry, cx + r, cy + ry], 180, 360, fill=grid, width=1)
    for k in (0.30, 0.64, 0.92):
        w = int(r * k)
        d.arc([cx - w, cy - r, cx + w, cy + r], 90, 270, fill=grid, width=1)
        d.arc([cx - w, cy - r, cx + w, cy + r], 270, 90, fill=grid, width=1)
    d.line([cx, cy - r, cx, cy + r], fill=grid, width=1)


def marker(d, d_, x, y, label, left=False):
    d_.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED, outline=CREAM, width=1)
    f = fnt(SANS_B, 6.5)
    tw = d_.textlength(label, font=f)
    lx = x - 6 - tw if left else x + 6
    d_.text((lx, y - 4), label, font=f, fill=CREAM)


REGIONS = [
    ("ASIA", [
        ("ICJ weighs genocide verdict against Myanmar",
         "Judges in The Hague hear The Gambia's case over the Rohingya; Myanmar denies intent."),
        "North Korea adds to its Yongbyon plant",
        "India widens online censorship after protests",
        "Trump meets Imelda Marcos in Manila",
        "Seoul's exams hit by AI cheating",
    ]),
    ("MIDDLE EAST", [
        ("US strikes Iran's Qeshm Island; the Gulf braces",
         "Tehran hit Bahrain after the raid; Kuwait reports drones; Hormuz insurance reaches $64m."),
        "Israel opens a new ground push in Gaza",
        "Gaza doctor Abu Safia held without charge",
        "Lebanon's rebuild is slow, World Bank says",
        "Knesset chaos as a new speaker is elected",
    ]),
    ("EUROPE", [
        ("Ukraine hits the Kerch Bridge again as five die",
         "Kyiv says the road span was damaged for the second time in two days."),
        "EU offers Kyiv a €45bn loan",
        "Five EU states plan Rwanda return hubs",
        "UK and EU draft a 'reset' on trade",
        "France: Philippe bids for the Élysée with cuts",
    ]),
    ("AFRICA", [
        ("Somalia fighting displaces 18,000 in Baidoa",
         "Clashes between clan militias and government forces empty neighbourhoods."),
        "Nigeria's campaign trail turns violent",
        "ANC delays its coalition briefing",
        "Zambia and Zimbabwe face an aid cliffhanger",
        "Egypt: Mada Masr editor due in court",
    ]),
    ("NORTH AMERICA", [
        ("Democrats nominate Jeffries for Speaker",
         "He would be the first Black speaker of the House if elected."),
        "Peltola flips Alaska's Senate seat",
        "Measles: US, Mexico and Bolivia lose status",
        "US egg producer culls 1.8m birds",
        "Nvidia beats forecasts; Huang to testify",
    ]),
    ("SOUTH AMERICA", [
        ("Costa Rican journalist shot dead",
         "The first such killing in the country in 25 years."),
        "Brazil's isolated tribe emerges amid threats",
        "Pesticides linked to 1,605 poisonings",
        "Mexico hails a 'very good' Trump meeting",
        "El Salvador's mega-prison model debated",
    ]),
    ("OCEANIA", [
        ("Australia's 'phantom forests' questioned",
         "A report says carbon credits rest on forests that do not exist."),
        "Bupa shuts some GP clinics",
        "Sydney to lead the housing recovery",
        "One Nation's refugee cut denounced",
        "US envoy calls Auckland's mayor a 'boomer'",
    ]),
]

BRIEFS = [
    ("TECH", [("China seeks advanced Nvidia chips, report says", "for AI weapons, despite US curbs"),
              ("Anthropic IPO details reported", "as the AI race widens")]),
    ("CULTURE", [("Robert Pattinson cast as the new James Bond", "the surprise choice"),
                 ("GTA VI arrives to glowing reviews", "a 'gaming triumph', critics say"),
                 ("Glastonbury: Styles, Eilish and Cher", "to headline in June")]),
    ("HEALTH · SPORT", [("WHO sounds alarm over antibiotic resistance", "a global health warning"),
                        ("E. coli toxin linked to bowel cancer rise", "among the under-50s"),
                        ("Zverev notified of abuse lawsuit", "during the ATP Finals")]),
]

NUMBERS = [("€45bn", "EU loan for Ukraine"), ("7,700", "US measles cases, 13 deaths"),
           ("1.8m", "birds culled over bird flu"), ("18,000", "displaced in Baidoa"),
           ("$64m", "Hormuz war-risk insurance")]


def region(d, x, y, w, name, items, lead_size, short_size, bottom):
    d.text((x, y), name, font=fnt(SANS_B, 9.5), fill=RED)
    rule(d, y + 14, x, x + w, width=1, color=RED)
    yy = y + 20
    head, deck = items[0]
    yy = text_block(d, (x, yy), head, fnt(SERIF_B, lead_size), w, 2, INK, 1.12)
    yy = text_block(d, (x, yy + 2), deck, fnt(SANS, 8.2), w, 2, MUTED, 1.22, 5)
    for head in items[1:]:
        d.text((x, yy), "•", font=fnt(SANS_B, 7.5), fill=RED)
        yy = text_block(d, (x + 8, yy - 1), head, fnt(SANS_B, short_size), w - 8, 2, INK, 1.16, 4)
    if yy > bottom:
        print("OVERFLOW", name, yy, ">", bottom)
    return yy


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((M, 18), "THE WORLD IN ONE DAY", font=fnt(SERIF_B, 40), fill=INK)
    d.text((M, 64), "EVERY STORY BELOW BROKE IN THE 24 HOURS OF WEDNESDAY 18 NOVEMBER 2026",
           font=fnt(SANS_B, 8.6), fill=MUTED)
    d.text((W - M - 210, 16), "WEDNESDAY", font=fnt(SANS_B, 9.5), fill=RED)
    d.text((W - M - 210, 28), "18 NOV 2026", font=fnt(SERIF_B, 30), fill=INK)
    d.text((W - M - 210, 64), "47 STORIES · SIX CONTINENTS · ONE PAGE", font=fnt(SANS_B, 7.6), fill=MUTED)
    rule(d, 88, width=3)
    rule(d, 93, width=1, color=RED)

    # hero
    top, bot = 102, 352
    d.rectangle([M, top, W - M - 1, bot], fill=NAVY)
    hx = M + 22
    tracked(d, (hx, top + 14), "APEC · SHENZHEN", fnt(SANS_B, 10.5), RED, 2.0)
    y = text_block(d, (hx, top + 32), "Xi welcomes Trump as a three-way summit takes shape",
                   fnt(SERIF_B, 28), 392, 3, CREAM, 1.1)
    y = text_block(d, (hx, y + 8),
                   "Trump landed in China for APEC talks with Xi; the Kremlin said a Putin meeting "
                   "was possible but no full-scale talks were planned. Xi used the stage to call "
                   "protectionism a dead end.",
                   fnt(SANS, 9.4), 392, 3, (204, 200, 190), 1.36)
    d.line([hx, y + 2, hx + 392, y + 2], fill=(72, 90, 116), width=1)
    yy = y + 10
    for head, note in (("Putin: Europe in a 'humiliating decline'", "The Kremlin confirms contact, not a full summit."),
                       ("Quad adds an AI and minerals pact", "Albanese joins leaders in Manila as security tops the agenda.")):
        d.text((hx, yy + 1), "■", font=fnt(SANS_B, 6.5), fill=RED)
        d.text((hx + 11, yy), head, font=fnt(SANS_B, 8.8), fill=CREAM)
        d.text((hx + 11, yy + 11), note, font=fnt(SANS, 7.6), fill=GREY_ON_NAVY)
        yy += 25

    gx, gy, gr = 858, 224, 86
    globe(d, gx, gy, gr)
    marker(d, d, 826, 190, "SHENZHEN", True)
    marker(d, d, 872, 214, "QESHM")
    marker(d, d, 838, 246, "KYIV", True)
    d.text((760, 322), "THREE FLASHPOINTS, ONE WEEK", font=fnt(SANS_B, 7.4), fill=GOLD)
    d.text((760, 332), "Gulf strikes · the Kerch bridge · APEC", font=fnt(SANS, 6.6), fill=GREY_ON_NAVY)

    # region rows
    gap1 = 12
    w1 = (W - 2 * M - 2 * gap1) // 3
    row1, bottom1 = 362, 566
    for i, (name, items) in enumerate(REGIONS[:3]):
        region(d, M + i * (w1 + gap1), row1, w1, name, items, 13.4, 9.3, bottom1)
    rule(d, 574, width=1, color=HAIR)

    gap2 = 10
    w2 = (W - 2 * M - 3 * gap2) // 4
    row2, bottom2 = 580, 784
    for i, (name, items) in enumerate(REGIONS[3:]):
        region(d, M + i * (w2 + gap2), row2, w2, name, items, 11.6, 8.7, bottom2)
    rule(d, 790, width=1, color=HAIR)

    # numbers
    ny = 796
    d.text((M, ny), "THE DAY IN NUMBERS", font=fnt(SANS_B, 9), fill=RED)
    rule(d, ny + 13, width=1, color=RED)
    cw = (W - 2 * M) // 5
    for i, (big, cap) in enumerate(NUMBERS):
        x = M + i * cw
        d.text((x, ny + 20), big, font=fnt(SERIF_B, 24), fill=INK)
        text_block(d, (x, ny + 47), cap, fnt(SANS, 7.0), cw - 14, 2, MUTED, 1.2)

    # briefs
    by = 876
    d.text((M, by), "WORLD IN BRIEF", font=fnt(SANS_B, 9), fill=RED)
    rule(d, by + 13, width=1, color=RED)
    bw = (W - 2 * M - 2 * 14) // 3
    for i, (tag, items) in enumerate(BRIEFS):
        x = M + i * (bw + 14)
        d.text((x, by + 19), tag, font=fnt(SANS_B, 7.0), fill=NAVY)
        yy = by + 30
        for head, note in items:
            d.text((x, yy), "•", font=fnt(SANS_B, 7.0), fill=RED)
            yy = text_block(d, (x + 8, yy - 1), head, fnt(SANS_B, 8.6), bw - 8, 1, INK, 1.16)
            d.text((x + 8, yy), note, font=fnt(SANS, 7.2), fill=MUTED)
            yy += 16

    # footer
    rule(d, 1002, width=1, color=INK)
    d.text((M, 1007), "REPORTED 18 NOVEMBER 2026 · AP · REUTERS · AFP · BBC · AL JAZEERA · DW · EURONEWS · FRANCE 24 · ABC · RNZ · NPR · THE GUARDIAN",
           font=fnt(SANS, 6.0), fill=MUTED)
    return img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry2.png")
    im = draw_page()
    im.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes", im.size)
