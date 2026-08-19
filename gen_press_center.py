# -*- coding: utf-8 -*-
"""Генерирует press-center.html — витрину репозитория: игра, 100 статей, 12 журналов."""
import os, glob, urllib.parse

BASE = os.path.dirname(__file__)

def rel(p):
    return urllib.parse.quote(p.replace("\\", "/"))

pdfs = sorted(glob.glob(os.path.join(BASE, "journals_pdf", "*.pdf")))
arts = sorted(glob.glob(os.path.join(BASE, "articles", "*.txt")))
futs = sorted(glob.glob(os.path.join(BASE, "articles", "future", "*.txt")))

card = []
for f in pdfs:
    n = os.path.basename(f)
    disp = n[:-4].replace("journal-", "№ ").replace("-50", "").replace("-01-10-glossy", " · глянец").replace("-01-10", "").replace("-", " ").replace("  ", " ")
    card.append(
        '<a class="jc" href="%s" download>\n'
        '  <div class="jcover">📰</div><div class="jname">%s</div>'
        '  <div class="jsub">10 выпусков · 20 страниц · %s</div></a>'
        % (rel(os.path.join("journals_pdf", n)), disp, "глянцевая мода" if "glossy" in n else "из-под капота"))
cards = "\n".join(card)

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ледяной Пресс-Центр · журналы 2026–2027</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: 'Segoe UI', system-ui, sans-serif; color: #eaf6ff;
         background: linear-gradient(180deg,#0d1b2a 0%,#16324f 50%,#0b1a2c 100%); min-height:100vh; padding: 24px; }
  a { color: inherit; text-decoration: none; }
  .wrap { max-width: 980px; margin: 0 auto; }
  h1 { font-size: 30px; letter-spacing: 1px; }
  h1 small { display:block; font-size:14px; opacity:.75; font-weight:400; margin-top:4px; }
  h2 { font-size: 18px; margin: 26px 0 10px; border-bottom: 1px solid rgba(255,255,255,.2); padding-bottom: 6px; }
  .play { display:inline-block; margin: 14px 0 6px; background: linear-gradient(180deg,#4aa8e0,#2f7fc0);
          padding: 12px 26px; border-radius: 12px; font-weight:700; font-size:16px; }
  .topnav { margin: 10px 0 4px; }
  .topnav a { display:inline-block; margin:0 10px 8px 0; background: rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.16);
              padding: 9px 18px; border-radius: 10px; font-size:13px; font-weight:600; }
  .topnav a:hover { background: rgba(255,255,255,.14); }
  .grid { display:grid; grid-template-columns: repeat(auto-fill,minmax(200px,1fr)); gap:12px; margin-top:10px; }
  .jc { background: rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.14); border-radius:14px;
        padding:14px; transition:.15s; }
  .jc:hover { transform:translateY(-2px); background:rgba(255,255,255,.1); }
  .jcover { font-size:34px; margin-bottom:6px; }
  .jname { font-weight:700; font-size:14px; line-height:1.25; }
  .jsub { font-size:11px; opacity:.7; margin-top:4px; }
  .list { columns: 3; column-gap: 22px; font-size:13px; line-height:1.7; opacity:.92; }
  .list a:hover { opacity:1; color:#9fe0ff; }
  .note { opacity:.6; font-size:12px; margin:12px 0 4px; }
  footer { margin-top:34px; opacity:.55; font-size:12px; border-top:1px solid rgba(255,255,255,.15); padding-top:12px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>🧊 Ледяной Пресс-Центр
    <small>газета «Ледяная Вечерка» · 100 статей-анализов · 50 номеров будущего · 12 журналов · 240 страниц · 120 обложек</small>
  </h1>
  <a class="play" href="index.html">🎮 Играть в «Ледяных человечков»</a>
  <div class="topnav">
    <a href="kiosk.html">🗞 Газетный киоск — 120 обложек</a>
    <a href="wiki-ice.html">📖 Энциклопедия Льда — движок, герои, инженерка, Бабай</a>
    <a href="heroes.html">🎭 Досье героев — 120 шаржей</a>
    <a href="fun.html">🎪 Забавный уголок</a>
  </div>

  <h2>📰 Журналы (PDF · по 10 выпусков)</h2>
  <div class="grid">@@CARDS@@</div>

  <h2>📄 50 статей-анализов</h2>
  <div class="list">
@@ARTS@@
  </div>

  <h2>🔮 50 статей о будущем («Ледяная Вечерка», номера 001–036)</h2>
  <div class="list">
@@FUTS@@
  </div>

  <h2>🗓 Архив будущего · каталог по месяцам (журналы/YYYY-MM)</h2>
  <p class="note">Первые полосы расставлены по месяцам: январь 2026 → сентябрь 2027. Когда месяцы пройдут,
  эти номера станут историей, которую вспомнят все.</p>

  <footer>Игра «Ледяные человечки» · движок из-под капота: лёд 0.7+0.06·люди/с, шторм ×2.5 на 10с (50–70с),
  заряд −3 маны → +2.5%, сеть +6 рыбы (0.4с), рождение ≥25 рыбы (−15), предел 12, счёт = время×10 + люди×50.
  <br>Репозиторий: github.com/pop31-ai/ice</footer>
</div>
</body>
</html>
"""

links_art = "\n".join('<a href="%s">%s</a>' % (rel(os.path.join("articles", os.path.basename(a))), os.path.basename(a)) for a in arts)
links_fut = "\n".join('<a href="%s">%s</a>' % (rel(os.path.join("articles/future", os.path.basename(a))), os.path.basename(a)) for a in futs)

open(os.path.join(BASE, "press-center.html"), "w", encoding="utf-8").write(
    html.replace("@@CARDS@@", cards).replace("@@ARTS@@", links_art).replace("@@FUTS@@", links_fut))
print("press-center.html written,", len(pdfs), "pdfs")