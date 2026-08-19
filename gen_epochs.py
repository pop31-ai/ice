# -*- coding: utf-8 -*-
"""Генератор epochs.html — «Лента эпох»: все 20 месяцев 2026-01…2027-09,
выпуски по датам жизни, обложки, герои, первые полосы. Когда месяц проходит —
выпуск становится историей."""
import os, glob, urllib.parse

import gen_pdf_journals as g
from gen_journal_catalog import THEMES, HEROES

BASE = os.path.dirname(__file__)
SRC = os.path.join(BASE, "journals")

MONTHS = ["январь", "февраль", "март", "апрель", "май", "июнь",
          "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]


def q(p):
    return urllib.parse.quote(p.replace("\\", "/"))


# журнал по имени
JNAME2JNO = {v[0]: k for k, v in g.JOURNALS.items()}

month_blocks = []
mdirs = sorted(glob.glob(os.path.join(SRC, "20*")))
for d in mdirs:
    mname = os.path.basename(d)
    files = sorted(glob.glob(os.path.join(d, "*.txt")))
    if not files:
        continue
    mq = mname + " @ " + ["история уже живёт в архиве", "месяц ещё впереди"][0]
    yy, mm = int(mname[:4]), int(mname[5:7])
    label = "%s %d" % (MONTHS[mm - 1], yy)
    cards = []
    for f in files:
        iss = g.parse_issue(f)
        jno = JNAME2JNO.get(iss.get("jname"))
        if not jno:
            continue
        issue = int(iss.get("issue", 0))
        name, slug, slogan = g.JOURNALS[jno]
        glossy = jno >= 11
        suf = "-glossy" if glossy else ""
        pdf = "journals_pdf/journal-%02d-%s-01-10%s.pdf" % (jno, slug, suf)
        cov = "covers/j%02d-issue-%02d.png" % (jno, issue)
        txt = f.replace("\\", "/")
        hero = HEROES[jno][issue - 1]
        theme = THEMES[jno][issue - 1]
        cards.append(
            '<div class="ep">'
            '<a href="%s#page=%d"><img src="%s" width="130"></a>'
            '<div class="eh">%s · № %02d/10</div>'
            '<div class="et">%s</div>'
            '<div class="ec">Тема: %s<br>Судьба: %s</div>'
            '<div class="el"><a href="%s">PDF</a> · <a href="%s">текст</a></div>'
            '</div>'
            % (q(pdf), issue * 2 - 1, q(cov), name, issue,
               iss.get("title", ""), theme, hero, q(pdf), q(txt)))
    month_blocks.append(
        '<div class="mo"><h2>%s</h2><p class="mt">когда этот месяц пройдёт — '
        'следующие читаются как история, а эти помнят начало</p>'
        '<div class="row">%s</div></div>'
        % (label, "".join(cards)))

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Лента эпох · Ледяной Пресс-Центр · 2026–2027</title>
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
  .mo { margin:38px 0; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12);
        border-radius:18px; padding:20px; }
  .mo h2 { margin:0; font-size:24px; color:#9fe0ff; }
  .mt { opacity:.6; font-size:12.5px; margin:6px 0 16px; }
  .row { display:flex; flex-wrap:wrap; gap:16px; justify-content:center; }
  .ep { text-align:center; width:150px; }
  .ep img { border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,.5); transition:.15s; }
  .ep img:hover { transform:translateY(-3px) scale(1.03); }
  .eh { font-size:11.5px; font-weight:700; margin-top:6px; }
  .et { font-size:10.5px; opacity:.85; line-height:1.25; }
  .ec { font-size:9.5px; opacity:.6; margin-top:4px; line-height:1.3; }
  .el { font-size:10px; opacity:.7; margin-top:3px; }
  .el a { color:#9fe0ff; margin:0 5px; }
  footer { margin-top:40px; opacity:.6; font-size:12px; border-top:1px solid rgba(255,255,255,.15); padding-top:12px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>📅 Лента эпох 🧊<small>21 месяц жизни лагеря: январь 2026 → сентябрь 2027. Каждый выпуск опубликован ровно в своём месяце — и когда месяц пройдёт, он останется историей, которую вспомнят все.</small></h1>
  <div class="top">
    <a href="index.html">🎮 Игра</a>
    <a href="press-center.html">📰 Пресс-Центр</a>
    <a href="kiosk.html">🗞 Киоск</a>
    <a href="wiki-ice.html">📖 Энциклопедия</a>
    <a href="heroes.html">🎭 Досье героев</a>
    <a href="fun.html">🎪 Забавный уголок</a>
  </div>
  @@MONTHS@@
  <footer>Игра «Ледяные человечки» · github.com/pop31-ai/ice · «Эпохи не тают — они становятся историей».</footer>
</div>
</body>
</html>
"""

open(os.path.join(BASE, "epochs.html"), "w", encoding="utf-8").write(
    html.replace("@@MONTHS@@", "".join(month_blocks)))
print("epochs.html written; months:", len(month_blocks))