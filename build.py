"""Builds entry.png: one front page of Wednesday 18 November 2026's world news.

Drawn with Pillow at 1024x1024, no network. main.py copies the PNG to the
output directory the grader gives it, so both of its runs write equal bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK = (246, 244, 238)
PAPER = (247, 244, 236)
RULE = (32, 34, 40)
BLACK = (24, 26, 32)
GREY = (96, 100, 108)
RED = (168, 42, 36)
BLUE = (28, 62, 120)
GREEN = (34, 92, 72)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def fit(d, s, path, size, width, floor=11):
    while size > floor and d.textlength(s, font=f(path, size)) > width:
        size -= 1
    return f(path, size)


def wrap(d, s, ft, width):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=ft) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, w, kicker, head, body, kicker_col=RED, head_size=30, body_size=16):
    d.text((x, y), kicker.upper(), font=f(BOLD, 15), fill=kicker_col)
    hf = fit(d, head, BOLD, head_size, w)
    yy = y + 24
    for ln in wrap(d, head, hf, w):
        d.text((x, yy), ln, font=hf, fill=BLACK)
        yy += hf.size + 4
    bf = f(SERIF, body_size)
    for ln in wrap(d, body, bf, w):
        d.text((x, yy), ln, font=bf, fill=GREY)
        yy += body_size + 5
    return yy


def main(out="entry.png"):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- nameplate ----------------------------------------------------
    d.rectangle([0, 0, W, 176], fill=BLACK)
    d.text((28, 14), "THE WORLD", font=f(SERIF, 64), fill=INK)
    d.text((30, 90), "WEDNESDAY 18 NOVEMBER 2026", font=f(BOLD, 26), fill=(240, 206, 128))
    d.text((30, 128), "Nine stories from four continents on one page", font=f(REG, 19), fill=(178, 182, 190))
    d.text((W - 214, 22), "THE DAY IN BRIEF", font=f(BOLD, 20), fill=(240, 206, 128))
    d.text((W - 214, 54), "Iran strikes Gulf hosts", font=f(REG, 17), fill=INK)
    d.text((W - 214, 78), "APEC opens in Shenzhen", font=f(REG, 17), fill=INK)
    d.text((W - 214, 102), "EU offers Kyiv 45bn euros", font=f(REG, 17), fill=INK)
    d.text((W - 214, 126), "US loses measles status", font=f(REG, 17), fill=INK)
    d.rectangle([0, 176, W, 182], fill=RED)

    # ---- lead ---------------------------------------------------------
    lx, ly, lw = 28, 200, 616
    d.text((lx, ly), "IRAN AND THE GULF", font=f(BOLD, 16), fill=RED)
    hf = f(BOLD, 42)
    yy = ly + 24
    for ln in wrap(d, "Iranian drones and missiles hit US bases in Kuwait and Bahrain", hf, lw):
        d.text((lx, yy), ln, font=hf, fill=BLACK)
        yy += 48
    lead_body = ("Tehran said it struck US drone and missile sites in the Gulf overnight, "
                 "its first attack on Kuwait, after American aircraft hit Qeshm Island in the "
                 "Strait of Hormuz. Kuwait and Bahrain said they intercepted most of the waves; "
                 "Washington reported damage but no deaths. The strikes came hours after the US "
                 "president said talks with Iran were still possible.")
    for ln in wrap(d, lead_body, f(SERIF, 19), lw):
        d.text((lx, yy + 6), ln, font=f(SERIF, 19), fill=(52, 54, 60))
        yy += 27

    # ---- side column --------------------------------------------------
    sx, sw = 676, 320
    d.line([sx - 20, ly - 6, sx - 20, 660], fill=(206, 202, 192), width=2)
    y = ly
    y = block(d, sx, y, sw, "Shenzhen, China", "Xi meets Trump at the airport as APEC opens",
              "The US, Chinese and Russian leaders gather for the first three-way summit, set for Thursday.", BLUE, 25, 15) + 14
    d.line([sx, y, sx + sw, y], fill=(206, 202, 192), width=2)
    y = block(d, sx, y + 14, sw, "Brussels", "EU proposes a 45bn-euro loan for Ukraine",
              "Repayable only if Russia pays reparations, it would cover Kyiv through 2027.", GREEN, 25, 15) + 14
    d.line([sx, y, sx + sw, y], fill=(206, 202, 192), width=2)
    y = block(d, sx, y + 14, sw, "New York", "Van Gogh sells for a record $190.4m",
              "Châtaigniers en fleurs went under the hammer after a title dispute.", RED, 25, 15) + 14
    d.line([sx, y, sx + sw, y], fill=(206, 202, 192), width=2)
    block(d, sx, y + 14, sw, "Caracas", "US and Venezuela restore military ties",
          "Hegseth signed a training and intelligence-sharing deal.", BLUE, 25, 15)

    # ---- lower grid ---------------------------------------------------
    gy = 690
    d.line([28, gy - 18, W - 28, gy - 18], fill=RULE, width=3)
    cols = [
        ("Atlanta, US", "US loses measles elimination status",
         "More than 5,400 cases this year, the worst outbreak in three decades, the CDC's panel found.", RED),
        ("Alaska, US", "Peltola takes the last Senate seat",
         "The Democrat beats Dan Sullivan, so her party now holds 56 seats in the chamber.", BLUE),
        ("Accra, Ghana", "A $60m presidential jet angers voters",
         "The purchase lands badly as households face rising prices and a squeeze on services.", GREEN),
        ("Antalya, Turkiye", "COP31 turns to cities and the vulnerable",
         "Delegates pressed for money to protect urban areas and the people climate change hits first.", RED),
    ]
    cw = (W - 56 - 3 * 26) // 4
    for i, (kicker, head, body, col) in enumerate(cols):
        x = 28 + i * (cw + 26)
        if i:
            d.line([x - 16, gy - 6, x - 16, gy + 250], fill=(206, 202, 192), width=2)
        block(d, x + 6, gy, cw - 6, kicker, head, body, col, 21)

    d.rectangle([0, H - 34, W, H], fill=BLACK)
    d.text((28, H - 26), "Compiled from the day's reporting worldwide, 18 November 2026", font=f(REG, 15), fill=(186, 190, 198))

    img.save(out, optimize=True)
    return out


if __name__ == "__main__":
    print(main())
