#!/usr/bin/env python3
"""Render the GTA 6 launch-night queue meme (1200x675 PNG) with PIL.

Scene: a skeleton who queued in 2013 finally reaches the counter on
GTA 6 launch night in Leonida, while the make.fun ghost floats beside
him holding its magenta coin and offers to cover his copy.

The official ghost mark comes from the make.fun press kit
(https://make.fun/press/mark-1024.png). A local copy next to this
script or in ../assets is used when present; otherwise it is
downloaded. Output: meme.png next to this script.
"""

import math
import os
import urllib.request

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 675
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PRESS_URL = "https://make.fun/press/mark-1024.png"


def font(size):
    return ImageFont.truetype(BOLD, size)


def load_ghost(size):
    candidates = [
        os.path.join(HERE, "mark-1024.png"),
        os.path.join(HERE, "..", "assets", "mark-1024.png"),
    ]
    path = next((p for p in candidates if os.path.exists(p)), None)
    if path is None:
        path = os.path.join(HERE, "mark-1024.png")
        urllib.request.urlretrieve(PRESS_URL, path)
    ghost = Image.open(path).convert("RGBA")
    return ghost.resize((size, size), Image.LANCZOS)


def outlined(draw, xy, text, fnt, fill="white", stroke="black", width=6,
             anchor="mm"):
    draw.text(xy, text, font=fnt, fill=fill, stroke_width=width,
              stroke_fill=stroke, anchor=anchor)


def draw_palm(draw, x, base_y, scale, colour=(16, 10, 34)):
    top_y = base_y - 190 * scale
    top_x = x + 26 * scale
    # one leaning trunk, drawn as a short chain of thick segments
    steps = 8
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        p0 = (x + (top_x - x) * t0 * t0, base_y + (top_y - base_y) * t0)
        p1 = (x + (top_x - x) * t1 * t1, base_y + (top_y - base_y) * t1)
        draw.line([p0, p1], fill=colour, width=max(3, int(14 * scale)))
    # fronds drooping from the crown
    for angle in range(-168, -12, 26):
        rad = math.radians(angle)
        length = 108 * scale
        end = (top_x + math.cos(rad) * length,
               top_y - abs(math.sin(rad)) * length * 0.35 + 30 * scale)
        mid = (top_x + math.cos(rad) * length * 0.5,
               top_y - 20 * scale)
        draw.line([top_x, top_y, mid[0], mid[1]], fill=colour,
                  width=max(3, int(8 * scale)))
        draw.line([mid[0], mid[1], end[0], end[1]], fill=colour,
                  width=max(2, int(5 * scale)))


def draw_skeleton(draw):
    bone = (238, 234, 220)
    dark = (20, 16, 30)
    cx, cy = 300, 330  # skull centre
    # skull
    draw.ellipse([cx - 52, cy - 58, cx + 52, cy + 46], fill=bone)
    draw.rectangle([cx - 30, cy + 30, cx + 30, cy + 72], fill=bone)
    # eyes and nose
    draw.ellipse([cx - 36, cy - 22, cx - 8, cy + 12], fill=dark)
    draw.ellipse([cx + 8, cy - 22, cx + 36, cy + 12], fill=dark)
    draw.polygon([(cx, cy + 8), (cx - 9, cy + 30), (cx + 9, cy + 30)],
                 fill=dark)
    # teeth
    for i in range(-2, 3):
        draw.line([cx + i * 11, cy + 38, cx + i * 11, cy + 68],
                  fill=dark, width=3)
    # spine and ribs (slumped, leaning forward)
    draw.line([cx + 6, cy + 74, cx + 26, cy + 168], fill=bone, width=13)
    for i, ry in enumerate(range(cy + 92, cy + 162, 18)):
        spread = 46 - i * 4
        draw.arc([cx + 22 - spread, ry - 12, cx + 22 + spread, ry + 20],
                 start=15, end=165, fill=bone, width=7)
    # arm reaching toward the counter, holding a 2013 ticket
    draw.line([cx + 30, cy + 104, cx + 118, cy + 138], fill=bone, width=11)
    draw.line([cx + 118, cy + 138, cx + 188, cy + 118], fill=bone, width=11)
    for f in range(3):
        draw.line([cx + 188, cy + 118, cx + 204, cy + 106 + f * 9],
                  fill=bone, width=5)
    # legs: seated, crossed, patient for 13 years
    draw.line([cx + 26, cy + 168, cx + 96, cy + 224], fill=bone, width=12)
    draw.line([cx + 96, cy + 224, cx + 168, cy + 214], fill=bone, width=12)
    draw.line([cx + 22, cy + 170, cx + 66, cy + 236], fill=bone, width=12)
    draw.line([cx + 66, cy + 236, cx + 132, cy + 244], fill=bone, width=12)
    # cobwebs from skull to shoulder
    web = (190, 190, 205)
    hub = (cx - 58, cy - 66)
    for target in [(cx - 118, cy - 20), (cx - 104, cy + 44),
                   (cx - 40, cy + 6), (cx - 128, cy + 92)]:
        draw.line([hub, target], fill=web, width=2)
    for t in (0.35, 0.65):
        pts = []
        for target in [(cx - 118, cy - 20), (cx - 104, cy + 44),
                       (cx - 40, cy + 6), (cx - 128, cy + 92)]:
            pts.append((hub[0] + (target[0] - hub[0]) * t,
                        hub[1] + (target[1] - hub[1]) * t))
        draw.line(pts + [pts[0]], fill=web, width=1)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img, "RGBA")

    # Leonida night sky: navy up top melting into a neon-pink horizon.
    for y in range(H):
        t = y / H
        r = int(18 + 90 * t * t)
        g = int(16 + 22 * t)
        b = int(48 + 60 * (1 - t))
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # stars, scattered by a small deterministic hash
    for i in range(80):
        sx = (i * 367 + 41) % W
        sy = ((i * i * 131 + i * 57) % 190) + 6
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(235, 235, 255))

    # ground
    draw.rectangle([0, 500, W, H], fill=(26, 18, 44))
    for i in range(6):
        draw.line([i * 220 - 60, 675, i * 150 + 240, 500],
                  fill=(52, 38, 84), width=3)

    draw_palm(draw, 90, 505, 1.0)
    draw_palm(draw, 1150, 500, 0.8)

    # --- game store on the right ---
    draw.rectangle([742, 168, 1172, 512], fill=(34, 26, 62),
                   outline=(255, 62, 166), width=5)
    # awning
    draw.polygon([(742, 238), (1172, 238), (1146, 282), (768, 282)],
                 fill=(214, 28, 128))
    # glowing window with the launch poster
    draw.rectangle([782, 306, 1006, 486], fill=(38, 198, 218))
    draw.rectangle([806, 330, 982, 420], fill=(16, 20, 48))
    outlined(draw, (894, 362), "GTA 6", font(52), fill=(255, 214, 64),
             width=4)
    outlined(draw, (894, 402), "OUT TODAY", font(30), fill="white",
             width=3)
    # door
    draw.rectangle([1032, 306, 1146, 512], fill=(22, 18, 44),
                   outline=(120, 220, 255), width=4)
    draw.ellipse([1122, 402, 1134, 414], fill=(255, 214, 64))
    # store sign
    outlined(draw, (957, 204), "LEONIDA GAMES", font(40),
             fill=(120, 240, 255), width=4)

    # --- queue rope from the skeleton to the store ---
    for px in (150, 470):
        draw.rectangle([px, 430, px + 12, 522], fill=(180, 184, 200))
        draw.ellipse([px - 5, 420, px + 17, 442], fill=(230, 232, 240))
    draw.line([156, 448, 300, 478], fill=(214, 28, 128), width=8)
    draw.line([300, 478, 476, 448], fill=(214, 28, 128), width=8)

    # skeleton and his ancient ticket
    draw_skeleton(draw)
    ticket = Image.new("RGBA", (138, 80), (0, 0, 0, 0))
    td = ImageDraw.Draw(ticket)
    td.rectangle([2, 2, 136, 78], fill=(245, 240, 220),
                 outline=(20, 16, 30), width=3)
    td.text((69, 24), "QUEUE TICKET", font=font(17), fill=(20, 16, 30),
            anchor="mm")
    td.text((69, 55), "2013", font=font(28), fill=(180, 20, 60),
            anchor="mm")
    ticket = ticket.rotate(14, expand=True)
    img.paste(ticket, (410, 362), ticket)
    draw = ImageDraw.Draw(img, "RGBA")

    # --- the make.fun ghost, in the scene at the counter ---
    ghost = load_ghost(248)
    img.paste(ghost, (566, 202), ghost)
    draw = ImageDraw.Draw(img, "RGBA")
    # soft shadow under the ghost so it floats in the scene
    draw.ellipse([606, 438, 782, 464], fill=(0, 0, 0, 110))

    # speech bubble: the ghost's pitch, in the meme's own voice
    bubble = (700, 58, 1178, 148)
    draw.rounded_rectangle(bubble, radius=18, fill=(255, 255, 255),
                           outline=(20, 16, 30), width=4)
    draw.polygon([(748, 148), (694, 200), (806, 148)],
                 fill=(255, 255, 255), outline=(20, 16, 30))
    draw.text((939, 90), "Relax. My human's AI agent", font=font(25),
              fill=(20, 16, 30), anchor="mm")
    draw.text((939, 122), "earned this copy on make.fun", font=font(25),
              fill=(180, 20, 110), anchor="mm")

    # --- captions: huge, readable at thumbnail size ---
    outlined(draw, (322, 52), "IN LINE SINCE 2013", font(56), width=8)
    outlined(draw, (600, 622), "GTA 6 LAUNCH NIGHT: FINALLY MY TURN",
             font(43), width=6)

    img.save(os.path.join(HERE, "meme.png"))
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
