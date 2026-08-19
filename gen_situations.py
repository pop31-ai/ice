# -*- coding: utf-8 -*-
"""Ситуация — иллюстрация: 6 событий лагеря x 13 серий = 78 полиарт-картины.
Каждое событие (шторм, рождение, голод, рекорд, заряд, улов) получает крупную
зарисовку в фирменном стиле полиарт-φ. Галлерея situations.html + PNG в situations/."""
import os
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from matplotlib import font_manager as _fm

import gen_covers as cs
import gen_pdf_journals as g

BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, "situations")
os.makedirs(OUT, exist_ok=True)

_TTF = os.path.join(os.path.dirname(_fm.__file__), "mpl-data", "fonts", "ttf")
FB = lambda s: ImageFont.truetype(os.path.join(_TTF, "DejaVuSans-Bold.ttf"), s)
F = lambda s: ImageFont.truetype(os.path.join(_TTF, "DejaVuSans.ttf"), s)

SITU = [
    ("storm", "ШТОРМ", "×2.5 таяния на 10 секунд — чернила мира густеют", "#b8c4ff"),
    ("birth", "РОЖДЕНИЕ", "рыба ≥25: каждые 6 секунд лагерь получает нового человека", "#9fe0ff"),
    ("hunger", "ГОЛОД", "3 секунды без рыбы — и человек тает тише снега", "#ffb3b3"),
    ("record", "РЕКОРД", "время×10 + люди×50 — вечность ведёт счёт", "#ffdf7e"),
    ("frost", "ЗАРЯД", "−3 маны → +2.5% льда: холод отвечает на поклон", "#c7b6ff"),
    ("catch", "УЛОВ", "клик по воде даёт +6 рыбы: море помнит добрые жесты", "#8fe3c8"),
]


def scene(kind, od, W, H, pal, seed):
    rng = np.random.default_rng(seed)
    sky1, sky2, sun, accent, mid, dark, chip = pal
    a = np.array(Image.new("RGB", (1, 1), accent).getpixel((0, 0)))
    m = np.array(Image.new("RGB", (1, 1), mid).getpixel((0, 0)))
    d = np.array(Image.new("RGB", (1, 1), dark).getpixel((0, 0)))
    if kind == "storm":
        cx, cy = W * 0.5, H * 0.42
        for r in range(6, 20):
            rr = r * 26
            od.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=20 + r * 8, end=200 + r * 9,
                   fill=tuple(list((a * (1 - r / 22) + d * (r / 22)).astype(int)) + [150]), width=9)
        for k in range(9):
            x0 = rng.uniform(0, W); y0 = x0 * 0.35 + rng.uniform(-40, 40)
            od.line([(x0, y0), (x0 + 180, y0 + 70)], fill=tuple(list(d) + [110]), width=5)
    elif kind == "birth":
        cx, cy = W * 0.5, H * 0.44
        r = 130
        for k in range(6):
            ang = k * np.pi / 3
            tip = (cx + r * np.cos(ang), cy + r * np.sin(ang))
            ctrl = (cx + 2.0 * r * np.cos(ang + 0.32), cy + 2.0 * r * np.sin(ang + 0.32))
            c0 = (cx, cy)
            uu = np.linspace(0, 1, 30)
            pts = []
            for u in uu:
                v = (1 - u) ** 2 * np.array(c0) + 2 * u * (1 - u) * np.array(ctrl) + u ** 2 * np.array(tip)
                pts.append((int(v[0]), int(v[1])))
            od.line(pts, fill=tuple(list(a) + [190]), width=6)
        od.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=tuple(list(m) + [255]), width=4)
        od.line([(cx, cy - 60), (cx, cy - 120)], fill=tuple(list(d) + [180]), width=5)
    elif kind == "hunger":
        cx, cy = W * 0.5, H * 0.42
        uu = np.linspace(0, 1, 40)
        pts = []
        for u in uu:
            th = u * np.pi * 2
            rr = 150 * (1 - u) ** 0.7
            pts.append((cx + rr * np.cos(th), cy + rr * np.sin(th)))
        od.line(pts, fill=tuple(list(d) + [170]), width=6)
        for k in range(-2, 3):
            od.line([(cx - 220, cy + k * 36), (cx + 220, cy + k * 36 + 14)],
                    fill=tuple(list(d) + [80]), width=4)
    elif kind == "record":
        cx, cy = W * 0.5, H * 0.42
        od.polygon([(cx - 150, cy + 80), (cx + 150, cy + 80), (cx + 100, cy - 40), (cx - 100, cy - 40)],
                   fill=tuple(list(m) + [190]), outline=tuple(list(d) + [255]))
        od.polygon([(cx - 60, cy - 40), (cx + 60, cy - 40), (cx + 60, cy - 90), (cx - 60, cy - 90)],
                   outline=tuple(list(m) + [240]), width=6)
        for k in range(8):
            ang = k * np.pi / 4
            x, y = cx + 220 * np.cos(ang), cy - 150 + 220 * np.sin(ang) * 0.6
            rr = 14
            od.polygon([(x - rr, y - rr * 0.4), (x + rr, y - rr * 0.4), (x + rr * 0.5, y + rr * 0.6),
                        (x - rr * 0.5, y + rr * 0.6)],
                       fill=tuple(list(a) + [230]))
    elif kind == "frost":
        cx, cy = W * 0.5, H * 0.44
        for k in range(6):
            ang = k * np.pi / 3
            tip = (cx + 170 * np.cos(ang), cy + 170 * np.sin(ang))
            od.line([(cx, cy), tip], fill=tuple(list(a) + [170]), width=8)
            for s in (-1, 1):
                p1 = (cx + 85 * np.cos(ang + s * 0.4), cy + 85 * np.sin(ang + s * 0.4))
                p2 = (cx + 120 * np.cos(ang + s * 0.16), cy + 120 * np.sin(ang + s * 0.16))
                od.line([p1, p2], fill=tuple(list(a) + [140]), width=5)
        od.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline=tuple(list(a) + [255]), width=5)
    elif kind == "catch":
        cx, cy = W * 0.5, H * 0.44
        uu = np.linspace(0, 1, 60)
        pts = []
        for u in uu:
            x = cx - 170 + 340 * u
            y = cy + 90 * np.sin(u * np.pi) * np.sin(u * np.pi * 3.0)
            pts.append((x, y))
        od.line(pts, fill=tuple(list(m) + [220]), width=10)
        od.line([(cx - 170, cy + 6), (cx + 170, cy + 6)], fill=tuple(list(d) + [120]), width=4)
        for k in range(-3, 4):
            y = cy + 6 + k * 26
            od.line([(cx - 170, y), (cx + 170, y + (10 if k % 2 else -10))],
                    fill=tuple(list(d) + [90]), width=4)


def make_situation(jno, slot):
    name, slug, slogan = g.JOURNALS[jno]
    sky1, sky2, sun, accent, mid, dark, chip = g.PAL[jno]
    c1 = cs.rgbc(sky1); c2 = cs.rgbc(sky2)
    if jno >= 11:
        c1, c2 = np.array([13, 10, 18]), np.array([28, 20, 39])
    kind, label, desc, tagc = SITU[slot]
    seed = jno * 131 + slot * 7 + 11
    im = cs.polyart_sky(600, 840, c1, c2, accent, mid, chip, seed)
    ov = Image.new("RGBA", (600, 840), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    scene(kind, od, 600, 840, g.PAL[jno], seed)
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 599, 839], outline=tuple(cs.rgbc(sun if jno >= 11 else accent).astype(int)), width=6)
    d.rectangle([8, 8, 591, 831], outline=tuple(cs.rgbc(sun if jno >= 11 else accent).astype(int)), width=2)
    d.rounded_rectangle([24, 20, 576, 92], radius=12, fill=tuple(cs.rgbc(sun if jno >= 11 else accent).astype(int)))
    t = FB(34)
    tw = d.textlength(label, font=t)
    d.text(((600 - tw) / 2, 30), label, font=t, fill="#0d0a12" if jno >= 11 else "#ffffff")
    d.text((30, 100), "серия «%s»" % name, font=FB(16),
           fill=tuple(cs.rgbc(chip).astype(int)) if jno < 11 else tuple(np.array([255, 253, 245]).astype(int)))
    d.multiline_text((30, 754), desc, font=FB(15),
                     fill=tuple(cs.rgbc(chip).astype(int)) if jno < 11 else tuple(np.array([255, 253, 245]).astype(int)))
    out = os.path.join(OUT, "%s-%02d.png" % (kind, jno))
    im.save(out)
    return out


if __name__ == "__main__":
    n = 0
    for slot in range(len(SITU)):
        for jno in range(1, len(g.JOURNALS) + 1):
            make_situation(jno, slot)
            n += 1

    blocks = []
    for slot, (kind, label, desc, tagc) in enumerate(SITU):
        thumbs = []
        for jno in range(1, len(g.JOURNALS) + 1):
            name, slug, slogan = g.JOURNALS[jno]
            p = "situations/%s-%02d.png" % (kind, jno)
            thumbs.append('<div class="iss"><img src="%s" width="150"><div class="ino">%s</div></div>' % (p, name))
        blocks.append(
            '<div class="sg"><h2>%s <small>%s</small></h2>'
            '<p class="devis">%s</p><div class="row">%s</div></div>'
            % (label, "ситуация → иллюстрация", desc, "".join(thumbs)))

    html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ситуация — иллюстрация · Ледяной Пресс-Центр</title>
<style>
  body { margin:0; font-family:'Segoe UI',system-ui,sans-serif; color:#eaf6ff;
         background:radial-gradient(1200px 700px at 20% -10%, #2b5d8a, #0d1b2a 60%, #071220);
         padding:26px; }
  a { color:inherit; }
  .wrap { max-width:1180px; margin:0 auto; }
  h1 { font-size:30px; letter-spacing:1px; }
  h1 small { display:block; font-size:13px; opacity:.7; font-weight:400; margin-top:4px; }
  .top a { display:inline-block; margin:6px 12px 6px 0; background:linear-gradient(180deg,#4aa8e0,#2f7fc0);
           padding:10px 20px; border-radius:10px; font-weight:700; font-size:14px; }
  .sg { margin:40px 0; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12);
        border-radius:18px; padding:20px; }
  .sg h2 { margin:0; font-size:24px; }
  .sg h2 small { font-size:12px; opacity:.6; font-weight:400; }
  .devis { opacity:.75; font-size:13px; margin:6px 0 14px; }
  .row { display:flex; flex-wrap:wrap; gap:15px; justify-content:center; }
  .iss { text-align:center; width:150px; }
  .iss img { border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,.5); }
  .ino { font-size:11px; margin-top:6px; opacity:.85; }
  footer { margin-top:36px; opacity:.6; font-size:12px; border-top:1px solid rgba(255,255,255,.15); padding-top:12px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>🖼 Ситуация — иллюстрация 🧊<small>каждое событие лагеря отвечает картиной: %d ситуаций × %d серий = %d полиарт-зарисовок</small></h1>
  <div class="top">
    <a href="index.html">🎮 Игра</a>
    <a href="press-center.html">📰 Пресс-Центр</a>
    <a href="kiosk.html">🗞 Киоск</a>
    <a href="polyart.html">✨ Полиарт-φ</a>
    <a href="wiki-ice.html">📖 Энциклопедия</a>
    <a href="epochs.html">📅 Лента эпох</a>
    <a href="heroes.html">🎭 Досье героев</a>
  </div>
  @@BLOCKS@@
  <footer>Игра «Ледяные человечки» · github.com/pop31-ai/ice · «Каждая ситуация достойна картины — и получает её».</footer>
</div>
</body>
</html>
"""
    open(os.path.join(BASE, "situations.html"), "w", encoding="utf-8").write(
        html.replace("@@BLOCKS@@", "".join(blocks))
            .replace("%d ситуаций × %d серий = %d полиарт-зарисовок",
                     "%d ситуаций × %d серий = %d полиарт-зарисовок"
                     % (len(SITU), len(g.JOURNALS), len(SITU) * len(g.JOURNALS))))
    print("situations: %d images; situations.html written" % n)