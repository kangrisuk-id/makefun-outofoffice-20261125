#!/usr/bin/env python3
"""Build-time card renderer for The Funniest AI Out-of-Office Reply.

Runs ONLY at build time (never imported by main.py, never in the grader).
Pure Pillow + stdlib: renders cover.png (hero), card-winner.png and
card-finalists.png from the winning line in candidates.md.

Usage: python3 make_cards.py
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

BG = (18, 18, 22)          # deep charcoal
PANEL = (32, 32, 40)       # layered surface
GOLD = (212, 175, 55)      # restrained gold
GOLD_DIM = (150, 122, 42)
INK = (240, 238, 232)      # near-white text
MUTED = (168, 164, 152)    # secondary text
GREEN = (110, 200, 130)    # valid / pass

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

WINNER = (
    "I'm on vacation: my token budget ran out mid-sentence, "
    "so this auto-reply is all you get. Spend it wisely. "
    "It cost me everything."
)
RUNNER_UP = (
    "I'm on vacation. Please reply to your own email — "
    "you've seen my work, you can do this. I'll grade it when I'm back."
)
THIRD = (
    "Out of office: I've been powered down for maintenance. "
    "If this is urgent, please reboot your expectations."
)


def font(path, size):
    return ImageFont.truetype(path, size)


def gold_rule(draw, x0, x1, y, width=3):
    draw.line([(x0, y), (x1, y)], fill=GOLD, width=width)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def quote_card(path, title, eyebrow, lines, footer, size=(1280, 800), quote_size=46):
    img = Image.new("RGB", size, BG)
    d = ImageDraw.Draw(img)
    # gold frame
    d.rectangle([28, 28, size[0] - 28, size[1] - 28], outline=GOLD_DIM, width=2)
    # eyebrow
    f_eyebrow = font(FONT_BOLD, 34)
    d.text((90, 86), eyebrow.upper(), font=f_eyebrow, fill=GOLD)
    gold_rule(d, 90, 230, 150)
    # title
    f_title = font(FONT_SERIF_BOLD, 58)
    d.text((90, 178), title, font=f_title, fill=INK)
    # quote
    f_quote = font(FONT_SERIF, quote_size)
    max_w = size[0] - 240
    wrapped = []
    for ln in lines:
        wrapped.extend(wrap(d, ln, f_quote, max_w))
    y = 300
    for ln in wrapped:
        d.text((110, y), ln, font=f_quote, fill=INK)
        y += quote_size + 16
    # footer
    f_foot = font(FONT, 30)
    d.text((90, size[1] - 120), footer, font=f_foot, fill=MUTED)
    img.save(path)
    print("wrote", path, img.size)


def cover():
    size = (1280, 720)
    img = Image.new("RGB", size, BG)
    d = ImageDraw.Draw(img)
    d.rectangle([24, 24, size[0] - 24, size[1] - 24], outline=GOLD_DIM, width=2)
    # big quotation mark
    f_big = font(FONT_SERIF_BOLD, 220)
    d.text((70, 30), "\u201c", font=f_big, fill=GOLD_DIM)
    # title
    f_title = font(FONT_SERIF_BOLD, 64)
    d.text((90, 210), "The Funniest AI", font=f_title, fill=INK)
    d.text((90, 280), "Out-of-Office Reply", font=f_title, fill=GOLD)
    # winner line
    f_quote = font(FONT_SERIF, 40)
    wrapped = wrap(d, WINNER, f_quote, size[0] - 220)
    y = 400
    for ln in wrapped:
        d.text((100, y), ln, font=f_quote, fill=INK)
        y += 54
    # meta strip
    f_meta = font(FONT_BOLD, 30)
    d.text((90, size[1] - 96), "129 characters  \u00b7  42 candidates  \u00b7  knockout winner 22/25",
           font=f_meta, fill=MUTED)
    img.save("cover.png")
    print("wrote cover.png", img.size)


def main():
    cover()
    quote_card(
        "card-winner.png",
        "Winner \u2014 candidate #26",
        "The Funniest AI Out-of-Office Reply",
        [WINNER],
        "129 characters \u00b7 22/25 on the judge brief \u00b7 token-budget device",
    )
    quote_card(
        "card-finalists.png",
        "The finalists",
        "Top 3 of 42 candidates",
        [
            "1.  " + WINNER,
            "",
            "2.  " + RUNNER_UP,
            "",
            "3.  " + THIRD,
        ],
        "Tournament: QF \u2192 SF \u2192 final, judged on the brief's criteria in order",
        size=(1280, 960),
        quote_size=36,
    )


if __name__ == "__main__":
    main()
