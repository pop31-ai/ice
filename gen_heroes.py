# -*- coding: utf-8 -*-
"""Генератор heroes.html — «Досье героев»: 120 шаржей по всем номерам,
арки судеб (HEROES), зарисовки про сковородки рядом с каждой серией."""
import os

import gen_pdf_journals as g
from gen_journal_catalog import HEROES
from ice_lore import PANS

BASE = os.path.dirname(__file__)

blocks = []
for jno in range(1, 13):
    name, slug, slogan = g.JOURNALS[jno]
    pan_kind, pan_text = PANS[(jno + 5) % len(PANS)]
    cells = []
    for issue in range(1, 11):
        hero = HEROES[jno][issue - 1]
        car_p = g.caricature(jno, issue, hero)
        rel = car_p.replace("\\", "/")
        cells.append(
            '<div class="hero">'
            '<div class="himg"><img src="%s" width="120"></div>'
            '<div class="hnum">%s · № %02d/10</div>'
            '<div class="harc">%s</div></div>'
            % (rel, name, issue, hero))
    blocks.append(
        '<div class="ser"><h2>%s <small>10 шаржей · серия</small></h2>'
        '<p class="devis">%s</p>'
        '<div class="row">%s</div>'
        '<div class="note"><span class="ntag">%s · ЗАРИСОВКА 🥘</span> %s</div></div>'
        % (name, slogan, "".join(cells), pan_kind, pan_text))

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Досье героев · Ледяной Пресс-Центр · 120 шаржей</title>
<style>
  body { margin:0; font-family:'Segoe UI',system-ui,sans-serif; color:#eaf6ff;
         background:radial-gradient(1200px 700px at 20% -10%, #2b5d8a, #0d1b2a 60%, #071220);
         padding:26px; }
  a { color:inherit; }
  .wrap { max-width:1180px; margin:0 auto; }
  h1 { font-size:30px; letter-spacing:1px; }
  h1 small { display:block; font-size:13px; opacity:.7; font-weight:400; }
  .top a { display:inline-block; margin:6px 12px 6px 0; background:linear-gradient(180deg,#4aa8e0,#2f7fc0);
           padding:10px 20px; border-radius:10px; font-weight:700; font-size:14px; }
  .ser { margin:40px 0; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12);
         border-radius:18px; padding:20px; }
  .ser h2 { margin:0; font-size:22px; }
  .ser h2 small { font-size:12px; opacity:.6; font-weight:400; }
  .devis { opacity:.75; font-size:13px; margin:6px 0 14px; }
  .row { display:flex; flex-wrap:wrap; gap:14px; justify-content:center; }
  .hero { text-align:center; width:140px; }
  .himg img { border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,.5); background:white; }
  .hnum { font-size:11px; margin-top:6px; opacity:.85; }
  .harc { font-size:10px; opacity:.62; line-height:1.3; }
  .note { margin-top:14px; background:rgba(255,190,80,.1); border-left:3px solid #ffbe50;
          padding:8px 12px; font-size:13px; border-radius:6px; }
  .note .ntag { font-weight:700; color:#ffbe50; margin-right:8px; }
  footer { margin-top:36px; opacity:.6; font-size:12px; border-top:1px solid rgba(255,255,255,.15); padding-top:12px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>🎭 Досье героев 🧊<small>120 шаржей серийных героев — по одному на номер каждой серии; арка продолжается в следующем выпуске ★</small></h1>
  <div class="top">
    <a href="index.html">🎮 Игра</a>
    <a href="kiosk.html">🗞 Киоск</a>
    <a href="wiki-ice.html">📖 Энциклопедия</a>
    <a href="press-center.html">📰 Пресс-Центр</a>
    <a href="fun.html">🎪 Забавный уголок</a>
    <a href="epochs.html">📅 Лента эпох</a>
    <a href="polyart.html">✨ Полиарт-φ</a>
    <a href="situations.html">🖼 Ситуации</a>
  </div>
  @@SERIES@@
  <footer>Игра «Ледяные человечки» · github.com/pop31-ai/ice · каждый шарж — это судьба, а каждая судьба — это зарисовка.</footer>
</div>
</body>
</html>
"""

open(os.path.join(BASE, "heroes.html"), "w", encoding="utf-8").write(
    html.replace("@@SERIES@@", "".join(blocks)))
print("heroes.html written:", 120, "caricatures")