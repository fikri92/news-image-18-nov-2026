#!/usr/bin/env python3
"""Render a one-page newspaper front page for the world news of Wednesday 18 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 242, 233)
INK = (18, 18, 18)
ACCENT = (163, 30, 24)
MUTED = (92, 88, 82)
HAIR = (160, 154, 144)
DARK = (22, 22, 22)
ON_DARK = (246, 242, 233)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SERIF = F + "DejaVuSerif.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"
MONO = F + "DejaVuSansMono.ttf"
M = 44


def fnt(p, s):
    return ImageFont.truetype(p, s)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, f, width, fill=INK, leading=1.24, max_lines=None):
    x, y = xy
    lines = wrap(d, text, f, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(f.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def rule(d, y, x0=M, x1=W - M, width=2, color=INK):
    d.rectangle([x0, y, x1, y + width - 1], fill=color)


def label(d, xy, text, color=ACCENT, size=14):
    x, y = xy
    d.text((x, y), " ".join(text.upper()), font=fnt(SANS_B, size), fill=color)
    return y + int(size * 1.55)


def main(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- dark masthead ----------------
    d.rectangle([0, 0, W, 124], fill=DARK)
    d.rectangle([0, 124, W, 130], fill=ACCENT)
    d.text((M, 26), "THE WORLD IN ONE DAY", font=fnt(SERIF_B, 50), fill=ON_DARK)
    d.text((W - M, 34), "No. 18 \u00b7 2026", font=fnt(MONO, 14), fill=(190, 184, 174), anchor="ra")
    date_s, date_f = "WEDNESDAY, 18 NOVEMBER 2026", fnt(SANS_B, 15)
    d.text((M, 88), date_s, font=date_f, fill=ON_DARK)
    dw = d.textlength(date_s, font=date_f)
    d.text((M + dw + 16, 89), "\u00b7  every story below broke in the last 24 hours",
           font=fnt(SANS, 13), fill=(186, 180, 170))

    y = 150

    # ---------------- lead + right column ----------------
    left_w = 588
    x2 = M + left_w + 26
    right_w = W - M - x2
    d.rectangle([x2 - 13, y, x2 - 12, y + 292], fill=HAIR)

    ly = label(d, (M, y), "Asia \u00b7 APEC")
    ly = para(d, (M, ly - 2), "Trump lands in China as Xi and Putin assail the West", fnt(SERIF_B, 36), left_w, leading=1.08)
    ly += 6
    ly = para(d, (M, ly), "In Shenzhen the three leaders trade warnings over \u201cprotectionism\u201d and sanctions. "
                          "Trump says a meeting with Kim Jong Un depends on Xi. In Manila, the Quad pledged "
                          "maritime security and critical minerals.",
              fnt(SERIF, 16), left_w, fill=(44, 42, 38), leading=1.26)
    ly += 12
    rule(d, ly, M, M + left_w, width=1, color=HAIR)
    ly += 10
    d.text((M, ly), "ALSO TODAY", font=fnt(SANS_B, 12), fill=MUTED)
    ly += 18
    ly = para(d, (M, ly), "Kyiv says it struck the Kerch Bridge for the second time in two days, damaging "
                          "the road span while rail service resumed.", fnt(SERIF, 14), left_w,
              fill=(60, 57, 52), leading=1.2, max_lines=2)

    ry = label(d, (x2, y), "Middle East")
    ry = para(d, (x2, ry - 2), "US strikes Iran's Qeshm Island", fnt(SERIF_B, 24), right_w, leading=1.1)
    ry += 4
    ry = para(d, (x2, ry), "Iran's Guards claim the drone attack on a US radar site at Bahrain's Sheikh Isa "
                           "air base; Kuwait reports hostile drones overhead.",
              fnt(SERIF, 15), right_w, fill=(44, 42, 38), leading=1.22)
    ry += 14
    rule(d, ry, x2, W - M, width=1, color=HAIR)
    ry += 12
    ry = label(d, (x2, ry), "Europe")
    ry = para(d, (x2, ry - 2), "EU offers Kyiv \u20ac45bn", fnt(SERIF_B, 24), right_w, leading=1.1)
    ry += 4
    ry = para(d, (x2, ry), "The loan is to be repaid once Russia pays reparations; envoys head to Berlin "
                           "for talks.",
              fnt(SERIF, 15), right_w, fill=(44, 42, 38), leading=1.22)

    y = max(ly, ry) + 10

    # ---------------- pull quote ----------------
    rule(d, y, width=4)
    y += 12
    d.text((M, y), "\u201cProtectionism.\u201d", font=fnt(SERIF, 38), fill=ACCENT)
    qw = d.textlength("\u201cProtectionism.\u201d", font=fnt(SERIF, 38))
    d.text((M + qw + 14, y + 16), "Xi Jinping and Vladimir Putin, on Western trade curbs",
           font=fnt(SANS, 14), fill=MUTED)
    y += 52

    # ---------------- numbers ----------------
    rule(d, y, width=1, color=HAIR)
    y += 10
    label(d, (M, y), "The day in numbers")
    y += 22
    stats = [("\u20ac45bn", "EU loan for Ukraine, repaid after reparations"),
             ("7,700", "US measles cases this year, with 13 deaths"),
             ("150,000", "protesters in France over pay and prices"),
             ("1 day", "light-travel time reached by Voyager 1")]
    cw = (W - 2 * M) // 4
    for i, (num, cap) in enumerate(stats):
        cx = M + i * cw
        d.text((cx, y), num, font=fnt(SERIF_B, 30), fill=ACCENT)
        para(d, (cx, y + 38), cap, fnt(SANS, 11), cw - 16, fill=(60, 58, 54), leading=1.16, max_lines=3)
    y += 92

    # ---------------- business ----------------
    rule(d, y, width=1, color=HAIR)
    y += 10
    label(d, (M, y), "Business \u00b7 technology")
    y += 22
    cells = [("NVIDIA", "Huang offers to return"), ("AI CHIPS", "China warns of retaliation"),
             ("ANTHROPIC", "IPO details reported")]
    for i, (name, val) in enumerate(cells):
        cx = M + i * cw
        d.text((cx, y), name, font=fnt(SANS_B, 12), fill=MUTED)
        para(d, (cx, y + 15), val, fnt(SERIF_B, 14), cw - 16, fill=INK, leading=1.15, max_lines=2)
    y += 62

    # ---------------- briefs ----------------
    rule(d, y, width=4)
    y += 10
    label(d, (M, y), "The world in brief")
    y += 22
    briefs = [
        ("Measles elimination lost",
         "The US, Mexico and Bolivia lose status as cases pass 7,700 with 13 deaths this year."),
        ("Drone attacks widen",
         "Bahrain and Kuwait report new aerial attacks after US strikes on an Iranian missile site."),
        ("North Korea's centrifuges",
         "The IAEA says Yongbyon's uranium-enrichment plant is being expanded."),
        ("OPEC at COP31",
         "The cartel speaks up for fossil fuels as delegates press for a phase-out."),
        ("12 killed in Honduras",
         "Organised-crime attacks strike the country, police say."),
        ("Word of the year: \u201chuman\u201d",
         "Cambridge picks the word in response to fears about AI."),
    ]
    col_w = (W - 2 * M - 30) // 2
    for i, (head, body) in enumerate(briefs):
        cx = M + (i % 2) * (col_w + 30)
        cy = y + (i // 2) * 58
        d.text((cx, cy), head, font=fnt(SANS_B, 13), fill=ACCENT)
        para(d, (cx, cy + 17), body, fnt(SERIF, 12), col_w, fill=(40, 38, 36), leading=1.14, max_lines=2)
    print("content bottom:", y + 58 * ((len(briefs) + 1) // 2), "| footer rule at", H - 44)

    # ---------------- footer ----------------
    rule(d, H - 44, width=1, color=HAIR)
    d.text((M, H - 34), "Compiled from AP, Reuters, Euronews, SBS and CNBC reports filed on 18 November 2026.",
           font=fnt(SANS, 10), fill=MUTED)
    d.text((W - M, H - 34), "ONE DAY \u00b7 ONE PAGE", font=fnt(MONO, 10), fill=MUTED, anchor="ra")

    img.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    print(main(out), os.path.getsize(out), "bytes")
