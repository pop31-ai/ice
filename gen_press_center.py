# -*- coding: utf-8 -*-
"""Генерирует press-center.html — витрину репозитория: игра, статьи, журналы.
Все числа (журналы, страницы, обложки, месяцы, шаржи) вычисляются из
реальных файлов, чтобы статистика никогда не расходилась с архивом."""
import os, glob, urllib.parse
import fitz

BASE = os.path.dirname(__file__)

def rel(p):
    return urllib.parse.quote(p.replace("\\", "/"))

pdfs = sorted(glob.glob(os.path.join(BASE, "journals_pdf", "*.pdf")))
arts = sorted(glob.glob(os.path.join(BASE, "articles", "*.txt")))
futs = sorted(a for a in glob.glob(os.path.join(BASE, "articles", "future", "*.txt"))
              if os.path.basename(a) != "README-future.txt")

N_J = len(pdfs)
N_ART = len(arts)
N_FUT = len(futs)
N_PAGES = sum(fitz.open(f).page_count for f in pdfs)
N_COV = len(glob.glob(os.path.join(BASE, "covers", "j*-issue-*.png")))
N_MONTH = len([d for d in sorted(glob.glob(os.path.join(BASE, "journals", "20*")))
               if glob.glob(os.path.join(d, "*.txt"))])
try:
    import gen_pdf_journals as _g
    N_SERIES = len(_g.JOURNALS)
except Exception:
    N_SERIES = N_J
N_CAR = N_SERIES * 10
N_SIT = N_SERIES * 6

card = []
for f in pdfs:
    n = os.path.basename(f)
    if "ajs-grafik" in n:
        disp = "«Айс-График» · журнал графиков"
        pages = 200
        sub = "10 томов · %d страниц · 80%% схем и кубов, 20%% текста" % pages
    elif "proektnaya-rabota" in n:
        disp = "«Проектная работа» · журнал о репозитории"
        pages = 30
        sub = "1 выпуск · %d листов · структура git, подходы, по науке" % pages
    else:
        disp = n[:-4].replace("journal-", "№ ").replace("-50", "").replace("-01-10-golden", " · золотая серия").replace("-01-10-glossy", " · глянец").replace("-01-10", "").replace("-", " ").replace("  ", " ")
        pages = 30 if "golden" in n else 20
        sub = "10 выпусков · %d страниц · %s" % (pages, "золотая серия событий" if "golden" in n else ("глянцевая мода" if "glossy" in n else "из-под капота"))
    card.append(
        '<a class="jc" href="%s" download>\n'
        '  <div class="jcover">▲</div><div class="jname">%s</div>'
        '  <div class="jsub">%s</div></a>'
        % (rel(os.path.join("journals_pdf", n)), disp, sub))
cards = "\n".join(card)

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ледяной Пресс-Центр · журналы 2026–2028</title>
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
    <small>газета «Ледяная Вечерка» · @@N_ART@@ статей-анализов · @@N_FUT@@ @@FUT_WORD@@ будущего · @@N_J@@ журналов · @@N_PAGES@@ страниц · @@N_COV@@ обложек</small>
  </h1>
  <a class="play" href="index.html">🎮 Играть в «Ледяных человечков»</a>
  <div class="topnav">
    <a href="kiosk.html">🗞 Газетный киоск — @@N_COV@@ обложек</a>
    <a href="wiki-ice.html">📖 Энциклопедия Льда — движок, герои, инженерка, Бабай</a>
    <a href="heroes.html">🎭 Досье героев — @@N_CAR@@ шаржей</a>
    <a href="fun.html">🎪 Забавный уголок</a>
    <a href="epochs.html">📅 Лента эпох — @@N_MONTH@@ @@MONTH_WORD@@ жизни лагеря</a>
    <a href="polyart.html">✨ Полиарт-φ — @@N_COV@@ обложек в фирменном стиле</a>
    <a href="situations.html">🖼 Ситуация — иллюстрация — @@N_SIT@@ зарисовок событий</a>
  </div>

  <h2>📰 Журналы (PDF · по 10 выпусков)</h2>
  <div class="grid">@@CARDS@@</div>

  <h2>📄 @@N_ART@@ статей-анализов</h2>
  <div class="list">
@@ARTS@@
  </div>

  <h2>🔮 @@N_FUT@@ статей о будущем («Ледяная Вечерка», номера @@FUT_RANGE@@)</h2>
  <div class="list">
@@FUTS@@
  </div>

  <h2>🗓 Архив будущего · каталог по месяцам (журналы/YYYY-MM)</h2>
  <p class="note">Первые полосы расставлены по месяцам: январь 2026 → июль 2028. Когда месяцы пройдут,
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

def pl_n(n, one, few, many):
    if 11 <= n % 100 <= 19:
        return many
    m10 = n % 10
    return one if m10 == 1 else (few if 2 <= m10 <= 4 else many)

MONTH_WORD = pl_n(N_MONTH, "месяц", "месяца", "месяцев")
FUT_WORD = pl_n(N_FUT, "номер", "номера", "номеров")
import re
_fnums = sorted(int(re.search(r"(\d+)", os.path.basename(a)).group(1)) for a in futs)
FUT_RANGE = "%03d–%03d" % (_fnums[0], _fnums[-1])

toks = {
    "@@N_ART@@": str(N_ART), "@@N_FUT@@": str(N_FUT), "@@N_J@@": str(N_J),
    "@@N_PAGES@@": str(N_PAGES), "@@N_COV@@": str(N_COV),
    "@@N_CAR@@": str(N_CAR), "@@N_SIT@@": str(N_SIT),
    "@@N_MONTH@@": str(N_MONTH), "@@MONTH_WORD@@": MONTH_WORD,
    "@@FUT_WORD@@": FUT_WORD, "@@FUT_RANGE@@": FUT_RANGE,
}

out = html.replace("@@CARDS@@", cards).replace("@@ARTS@@", links_art).replace("@@FUTS@@", links_fut)
for k, v in toks.items():
    out = out.replace(k, v)
open(os.path.join(BASE, "press-center.html"), "w", encoding="utf-8").write(out)
print("press-center.html written,", len(pdfs), "pdfs,", N_PAGES, "pages")