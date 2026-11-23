#!/usr/bin/env python3
"""
build_image.py — draws entry.png for the make.fun competition
news-image-20261123 ("Sum up 23 November's world news in one image").

The picture is a classic newspaper front page, drawn entirely with Pillow
primitives (rectangles, lines, polygons, ellipses) plus Pillow-rendered text.
No external artwork is used, so the result is fully reproducible: run this
script and it rewrites entry.png next to itself, byte for byte.

Layout (1024 x 1024):
  * masthead  — "THE WORLD IN ONE DAY" over a black date band
  * lead      — Ukraine sinks the Russian corvette Merkury off Libya
  * grid 2x2  — Indonesia factory fire / Asia AI sell-off /
                Belgium strike shuts airspace / Modi hosts Nepal's PM
  * wide      — rescuers search the Dymer rubble near Kyiv
  * strip     — UN & US condemn the Khartoum drone strikes

Every story below was reported on Monday 23 November 2026 and checked
against at least two independent reports before it was drawn.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette ---
PAPER = (247, 243, 233)      # warm off-white newsprint
PANEL = (253, 251, 245)      # slightly lighter panel fill
INK = (18, 18, 18)           # near-black ink
GRAY = (74, 74, 74)          # sub-caption grey
RED = (178, 30, 40)          # the one accent colour
SEA = (16, 42, 74)           # deep sea for the lead scene
WHITE = (255, 255, 255)
GOLD = (232, 184, 32)
ORANGE = (232, 116, 28)
SMOKE = (150, 148, 142)

W = H = 1024
MARGIN = 28
RIGHT = W - MARGIN

# ------------------------------------------------------------------ fonts ---
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- helpers ---
def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using real glyph widths."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def panel_box(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=2)


def story_text(draw, x, y, headline, sub, width, hsize=25, lh=31):
    """Headline (wrapped, bold caps) followed by a short summary caption."""
    hfont = font(SANS_BOLD, hsize)
    for line in wrap(draw, headline, hfont, width):
        draw.text((x, y), line, font=hfont, fill=INK)
        y += lh
    y += 5
    sfont = font(SANS_BOLD, 17)
    for line in wrap(draw, sub, sfont, width):
        draw.text((x, y), line, font=sfont, fill=GRAY)
        y += 21
    return y


# ---------------------------------------------------------------- visuals ---
def draw_sea_battle(draw, x0, y0, x1, y1):
    """Night sea off Benghazi: a corvette, two sea drones, one explosion."""
    draw.rectangle([x0, y0, x1, y1], fill=SEA)
    # moon and stars
    draw.ellipse([x1 - 52, y0 + 12, x1 - 24, y0 + 40], fill=(238, 238, 220))
    for sx, sy in [(18, 14), (60, 30), (110, 10), (150, 26), (205, 14)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=WHITE)
    water = y1 - 52
    # corvette silhouette: hull, deckhouse, mast
    hx0, hx1 = x0 + 118, x0 + 262
    draw.polygon([(hx0, water), (hx1, water), (hx1 - 16, water + 16),
                  (hx0 + 10, water + 16)], fill=(10, 12, 16))
    draw.rectangle([hx0 + 34, water - 16, hx0 + 96, water], fill=(10, 12, 16))
    draw.rectangle([hx0 + 52, water - 30, hx0 + 78, water - 16], fill=(10, 12, 16))
    draw.line([hx0 + 65, water - 30, hx0 + 65, water - 46], fill=(10, 12, 16), width=4)
    draw.line([hx0 + 20, water - 8, hx0 + 34, water], fill=(10, 12, 16), width=4)
    # explosion burst at the stern
    import math
    cx, cy = hx0 + 8, water - 6
    for i in range(12):
        ang = i * math.pi / 6
        r = 26 if i % 2 == 0 else 15
        draw.line([cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang)],
                  fill=ORANGE, width=4)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=GOLD)
    # two sea-drone boats with wakes, closing in from the left
    for bx, by, s in [(x0 + 26, water + 18, 1), (x0 + 74, water + 30, 1)]:
        draw.polygon([(bx, by), (bx + 44 * s, by), (bx + 36 * s, by + 9 * s),
                      (bx + 6 * s, by + 9 * s)], fill=(200, 208, 220))
        draw.line([bx - 16, by + 4, bx, by + 4], fill=WHITE, width=2)
        draw.line([bx - 10, by + 9, bx + 2, by + 9], fill=WHITE, width=2)
    # wave strokes
    for i in range(6):
        wx = x0 + 14 + i * 46
        draw.arc([wx, y1 - 26, wx + 30, y1 - 12], 180, 360, fill=(120, 160, 205), width=2)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_fire(draw, x, y):
    """A factory block with flames on the roof and smoke above."""
    bx0, by0, bx1, by1 = x + 8, y + 44, x + 110, y + 138
    # smoke puffs
    for cx, cy, r in [(x + 34, y + 16, 13), (x + 58, y + 8, 16), (x + 84, y + 15, 12)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # flames: layered triangles along the roofline
    for fx, fh, col in [(14, 30, ORANGE), (34, 40, ORANGE), (56, 34, ORANGE),
                        (78, 42, ORANGE), (96, 28, ORANGE),
                        (24, 22, GOLD), (46, 28, GOLD), (68, 24, GOLD), (88, 20, GOLD)]:
        draw.polygon([(x + fx, by0), (x + fx + 9, by0 - fh), (x + fx + 18, by0)], fill=col)
    # building body with a window grid
    draw.rectangle([bx0, by0, bx1, by1], fill=(96, 92, 88), outline=INK, width=2)
    for r in range(3):
        for c in range(4):
            wx = bx0 + 10 + c * 25
            wy = by0 + 12 + r * 28
            draw.rectangle([wx, wy, wx + 15, wy + 17], fill=(38, 38, 42))
    draw.rectangle([bx0, by1 - 4, bx1, by1], fill=INK)


def draw_chart(draw, x, y, w, h):
    """A plunging red stock chart for the AI sell-off."""
    draw.line([x, y + 6, x, y + h], fill=INK, width=3)          # y axis
    draw.line([x, y + h, x + w, y + h], fill=INK, width=3)      # x axis
    for i in range(1, 4):                                        # gridlines
        gy = y + h * i // 4
        draw.line([x + 2, gy, x + w, gy], fill=(205, 200, 188), width=1)
    pts = [(x + 6, y + 14), (x + 24, y + 10), (x + 40, y + 26), (x + 54, y + 20),
           (x + 68, y + 44), (x + 80, y + 38), (x + 90, y + 62), (x + 98, y + 74)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex + 2, ey - 8), (ex + 14, ey + 5), (ex + 2, ey + 8)], fill=RED)


def draw_grounded_plane(draw, x, y):
    """A passenger jet under a red no-fly slash: the grounded fleet."""
    cx, cy = x + 59, y + 58
    # tail fin and wing behind the fuselage
    draw.polygon([(cx - 40, cy - 8), (cx - 56, cy - 32), (cx - 30, cy - 10)],
                 fill=(70, 76, 86))
    draw.polygon([(cx - 2, cy + 4), (cx - 22, cy + 28), (cx - 4, cy + 28),
                  (cx + 14, cy + 6)], fill=(70, 76, 86))
    # fuselage, nose to the right
    draw.ellipse([cx - 50, cy - 11, cx + 50, cy + 11], fill=(38, 42, 50))
    draw.polygon([(cx + 38, cy - 11), (cx + 56, cy - 2), (cx + 56, cy + 2),
                  (cx + 38, cy + 11)], fill=(38, 42, 50))
    # windows
    for i in range(6):
        draw.ellipse([cx - 28 + i * 12, cy - 5, cx - 23 + i * 12, cy], fill=WHITE)
    # ground line
    draw.line([x + 4, y + 118, x + 114, y + 118], fill=INK, width=3)
    # prohibition ring
    draw.ellipse([x + 12, y + 8, x + 106, y + 102], outline=RED, width=7)
    draw.line([x + 25, y + 89, x + 93, y + 21], fill=RED, width=7)


def draw_flags_india_nepal(draw, x, y):
    """The flags of India and Nepal, side by side on one pole pair."""
    # India: saffron / white / green with a navy wheel
    fx, fy, fw, fh = x + 2, y + 26, 52, 54
    draw.line([fx - 3, y + 18, fx - 3, y + fh + 52], fill=GRAY, width=3)
    draw.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(247, 144, 30))
    draw.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=WHITE)
    draw.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(4, 106, 56))
    ccx, ccy = fx + fw // 2, fy + fh // 2
    draw.ellipse([ccx - 7, ccy - 7, ccx + 7, ccy + 7], outline=(0, 0, 128), width=2)
    draw.ellipse([ccx - 1, ccy - 1, ccx + 1, ccy + 1], fill=(0, 0, 128))
    draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)
    # Nepal: crimson double pennon with a blue border, sun and moon
    nx, ny = x + 66, y + 22
    draw.line([nx - 3, y + 18, nx - 3, y + fh + 52], fill=GRAY, width=3)
    pts = [(nx, ny), (nx + 44, ny + 22), (nx + 14, ny + 30), (nx + 40, ny + 56),
           (nx, ny + 62)]
    draw.polygon(pts, fill=(220, 20, 60))
    draw.line(pts + [pts[0]], fill=(0, 56, 147), width=3, joint="curve")
    draw.ellipse([nx + 8, ny + 10, nx + 16, ny + 18], fill=WHITE)          # moon
    sx, sy = nx + 12, ny + 40                                              # sun
    draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=WHITE)
    for dx, dy in [(-8, 0), (8, 0), (0, -8), (0, 8)]:
        draw.ellipse([sx + dx - 2, sy + dy - 2, sx + dx + 2, sy + dy + 2], fill=WHITE)


def draw_rubble(draw, x, y, w):
    """A collapsed apartment block: tilted slabs, rubble and a rescue crane."""
    base = y + 96
    # standing stump of the block, cracked
    draw.rectangle([x + 6, y + 30, x + 52, base], fill=(168, 162, 152), outline=INK, width=2)
    for r in range(3):
        for c in range(2):
            draw.rectangle([x + 14 + c * 20, y + 38 + r * 20,
                            x + 26 + c * 20, y + 50 + r * 20], fill=(52, 52, 56))
    draw.line([x + 30, y + 30, x + 22, y + 58, x + 34, y + 84], fill=INK, width=2)
    # tilted fallen slabs
    draw.polygon([(x + 58, base), (x + 66, y + 44), (x + 84, y + 50), (x + 78, base)],
                 fill=(188, 182, 170), outline=INK)
    draw.polygon([(x + 84, base), (x + 104, y + 58), (x + 122, y + 66), (x + 110, base)],
                 fill=(172, 166, 156), outline=INK)
    # rubble mound with debris chunks on its slopes
    draw.polygon([(x + 44, base), (x + 96, y + 70), (x + 150, base)], fill=(140, 134, 124))
    for rx, ry, rr in [(66, 86, 5), (84, 78, 4), (112, 80, 5), (128, 88, 4), (94, 90, 3)]:
        draw.ellipse([x + rx - rr, y + ry - rr, x + rx + rr, y + ry + rr],
                     fill=(110, 104, 96))
    # crane arm reaching over the wreckage
    draw.line([x + w - 8, y + 10, x + 96, y + 22], fill=INK, width=4)
    draw.line([x + w - 8, y + 10, x + w - 8, base], fill=INK, width=4)
    draw.line([x + 128, y + 19, x + 128, y + 44], fill=INK, width=2)
    draw.rectangle([x + 120, y + 44, x + 136, y + 52], outline=INK, width=2)
    # two rescuers in orange standing on the mound
    for px, py in [(76, 74), (118, 76)]:
        draw.ellipse([x + px - 4, y + py, x + px + 4, y + py + 8], fill=ORANGE)
        draw.line([x + px, y + py + 8, x + px, y + py + 20], fill=ORANGE, width=4)
    draw.line([x, base + 6, x + w, base + 6], fill=INK, width=2)


# ------------------------------------------------------------------- page ---
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # double frame
    d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=3)
    d.rectangle([18, 18, W - 18, H - 18], outline=INK, width=1)

    # ---- masthead ------------------------------------------------------
    centered(d, W // 2, 34, "THE WORLD IN ONE DAY", font(SERIF_BOLD, 64), INK)
    d.rectangle([MARGIN, 116, RIGHT, 172], fill=INK)
    centered(d, W // 2, 124, "MONDAY 23 NOVEMBER 2026", font(SANS_BOLD, 44), WHITE)
    d.rectangle([MARGIN, 184, RIGHT, 189], fill=RED)

    # ---- lead story ----------------------------------------------------
    panel_box(d, MARGIN, 202, RIGHT, 420)
    d.rectangle([356, 216, 502, 242], fill=RED)
    d.text((368, 220), "TOP STORY", font=font(SANS_BOLD, 18), fill=WHITE)
    draw_sea_battle(d, 44, 216, 336, 404)
    story_text(d, 356, 250,
               "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
               "Zelensky confirms seven naval drones sank the corvette "
               "Merkury at Benghazi, destroyed a Ka-27 helicopter and "
               "hit the cargo ship MV Angara",
               RIGHT - 356 - 16, hsize=39, lh=47)

    # ---- 2 x 2 grid ------------------------------------------------------
    rows = [(434, 598), (610, 774)]
    cols = [(MARGIN, 500), (524, RIGHT)]
    stories = [
        ("fire", "FACTORY FIRE TOLL HITS 24 IN INDONESIA",
         "Candy factory in Cikande, near Jakarta; about 30 still missing"),
        ("chart", "AI SELL-OFF SLAMS ASIAN MARKETS AGAIN",
         "KOSPI down over 5% midday; Taiwan bans short sales"),
        ("plane", "STRIKE SHUTS BELGIUM'S SKIES FOR A DAY",
         "Nationwide austerity strike; 60,000 passengers hit"),
        ("flags", "MODI HOSTS NEPAL'S PM IN NEW DELHI",
         "Ceremonial welcome for Balendra Shah and 100 minutes of "
         "talks; Ayodhya-Janakpur train link announced"),
    ]
    for (kind, head, sub), (gy0, gy1), (gx0, gx1) in zip(
            stories, [rows[0], rows[0], rows[1], rows[1]],
            [cols[0], cols[1], cols[0], cols[1]]):
        panel_box(d, gx0, gy0, gx1, gy1)
        vx, vy = gx0 + 16, gy0 + 14           # visual strip, 118 wide
        if kind == "fire":
            draw_fire(d, vx, vy)
        elif kind == "chart":
            draw_chart(d, vx, vy + 22, 100, 84)
        elif kind == "plane":
            draw_grounded_plane(d, vx, vy)
        elif kind == "flags":
            draw_flags_india_nepal(d, vx, vy)
        story_text(d, gx0 + 148, gy0 + 14, head, sub, gx1 - (gx0 + 148) - 14)

    # ---- wide panel: Dymer rescue ---------------------------------------
    panel_box(d, MARGIN, 786, RIGHT, 906)
    draw_rubble(d, 48, 796, 216)
    story_text(d, 300, 800,
               "BOY, 7, PULLED ALIVE FROM KYIV RUBBLE",
               "Rescuers search the flattened Dymer apartment block after a "
               "Russian strike near Kyiv; at least 11 killed, incl. a teenager",
               RIGHT - 300 - 16, hsize=28, lh=34)

    # ---- bottom strip -----------------------------------------------------
    d.rectangle([MARGIN, 918, RIGHT, 970], fill=INK)
    centered(d, W // 2, 932, "ALSO MONDAY: UN & US CONDEMN DRONE STRIKES ON KHARTOUM",
             font(SANS_BOLD, 25), WHITE)
    centered(d, W // 2, 980, "Compiled from world news reports of Monday 23 November 2026",
             font(SANS, 15), GRAY)

    img.save("entry.png", optimize=True)
    print("entry.png written:", img.size)


if __name__ == "__main__":
    build()
