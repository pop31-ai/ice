# -*- coding: utf-8 -*-
"""Генератор kiosk.html — «Газетный киоск»: все 120 обложек по 12 сериям (10 номеров)."""
import os, glob, urllib.parse

import gen_pdf_journals as g
from gen_journal_catalog import THEMES, HEROES
from ice_lore import PANS, BABAIS

BASE = os.path.dirname(__file__)
COVERS = os.path.join(BASE, "covers")

MONTHS = ["январь", "февраль", "март", "апрель", "май", "июнь",
          "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]


def issue_date(jno, issue):
    idx = (jno - 1) + (issue - 1)
    return "%s %d" % (MONTHS[idx % 12].capitalize(), 2026 + idx // 12)


def txt_path(jno, slug, issue):
    idx = (jno - 1) + (issue - 1)
    mdir = "%d-%02d" % (2026 + idx // 12, idx % 12 + 1)
    return os.path.join("journals", mdir, "journal-%02d-%s-issue-%02d.txt" % (jno, slug, issue))


def pdf_path(jno, slug, glossy):
    suf = "-glossy" if glossy else ""
    return os.path.join("journals_pdf", "journal-%02d-%s-01-10%s.pdf" % (jno, slug, suf))


def q(p):
    return urllib.parse.quote(p.replace("\\", "/"))


series_blocks = []
for jno in range(1, 13):
    name, slug, slogan = g.JOURNALS[jno]
    glossy = jno >= 11
    thumbs = []
    for issue in range(1, 11):
        date = issue_date(jno, issue)
        cov = os.path.join(COVERS, "j%02d-issue-%02d.png" % (jno, issue))
        pdf = pdf_path(jno, slug, glossy)
        txt = txt_path(jno, slug, issue)
        thumbs.append(
            '<div class="iss"><a href="%s#page=%d" title="%s · № %02d/10 — открыть PDF (лист 1-2: афиша, лист 2-2: рубрики)">'
            '<img src="%s" width="150"></a>'
            '<div class="ino">№%02d/%02d · %s</div>'
            '<div class="it"><a href="%s">PDF</a> · <a href="%s">текст</a> · '
            '<a href="%s">обложка</a></div></div>'
            % (q(pdf), issue * 2 - 1, name, issue, q(cov), issue, issue, date, q(pdf), q(txt), q(cov)))
    pan_kind, pan_text = PANS[(jno + 2) % len(PANS)]
    babai = BABAIS[(jno * 5) % len(BABAIS)]
    series_blocks.append(
        '<div class="ser"><h2>%s <small>серия из 10 номеров</small></h2>'
        '<p class="devis">%s</p><div class="row">%s</div>'
        '<div class="note"><span class="ntag">%s · ЗАРИСОВКА 🥘</span> %s</div>'
        '<div class="note"><span class="ntag">БАБАЙ · НАБЛЮДЕНИЕ 👻</span> %s</div>'
        '<div class="gal"><a href="%s">📥 скачать весь архив: PDF 10 выпусков · 20 страниц</a>'
        ' · <a href="covers/">папка обложек</a>'
        ' · <a href="journals/">каталог по месяцам</a></div></div>'
        % (name, slogan, "".join(thumbs), pan_kind, pan_text, babai, q(pdf_path(jno, slug, glossy))))

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Газетный киоск · Ледяной Пресс-Центр · 120 обложек</title>
<style>
  body { margin:0; font-family:'Segoe UI',system-ui,sans-serif; color:#eaf6ff;
         background:radial-gradient(1200px 700px at 20% -10%, #2b5d8a, #0d1b2a 60%, #071220);
         padding: 26px; }
  a { color: inherit; }
  .wrap { max-width: 1180px; margin: 0 auto; }
  h1 { font-size: 32px; letter-spacing:1px; }
  h1 small { display:block; font-size:14px; opacity:.7; font-weight:400; }
  .top a { display:inline-block; margin:6px 12px 6px 0; background:linear-gradient(180deg,#4aa8e0,#2f7fc0);
           padding:10px 20px; border-radius:10px; font-weight:700; font-size:14px; }
  .ser { margin: 42px 0; background: rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12);
         border-radius:18px; padding: 20px; }
  .ser h2 { margin:0; font-size:22px; }
  .ser h2 small { font-size:12px; opacity:.6; font-weight:400; }
  .devis { opacity:.75; font-size:13px; margin:6px 0 14px; }
  .row { display:flex; flex-wrap:wrap; gap:16px; justify-content:center; }
  .iss { text-align:center; width:150px; }
  .iss img { border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,.5); transition:.15s; }
  .iss img:hover { transform:translateY(-4px) scale(1.03); }
  .ino { font-size:11px; margin-top:6px; opacity:.85; }
  .it { font-size:10px; opacity:.6; }
  .gal { margin-top:16px; font-size:13px; opacity:.9; }
  .gal a { color:#9fe0ff; }
  .note { margin-top:10px; background:rgba(255,190,80,.1); border-left:3px solid #ffbe50;
          padding:8px 12px; font-size:13px; border-radius:6px; }
  .note .ntag { font-weight:700; color:#ffbe50; margin-right:8px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>🗞 Газетный киоск 🧊<small>12 серий журналов по 10 номеров — 120 обложек, 240 тщательных листов (афиша + лист рубрик каждый). Открой номер — и он станет историей в следующем году.</small></h1>
  <div class="top">
    <a href="index.html">🎮 Игра</a>
    <a href="press-center.html">📰 Пресс-Центр</a>
    <a href="wiki-ice.html">📖 Энциклопедия Льда</a>
    <a href="heroes.html">🎭 Досье героев</a>
    <a href="fun.html">🎪 Забавный уголок</a>
    <a href="README.md">💾 README</a>
  </div>
  @@SERIES@@
  <footer style="margin-top:40px; opacity:.6; font-size:12px; border-top:1px solid rgba(255,255,255,.15); padding-top:12px;">
    Игра «Ледяные человечки» · github.com/pop31-ai/ice · новости из будущего, которые станут прошлым
  </footer>
</div>
</body>
</html>
"""

open(os.path.join(BASE, "kiosk.html"), "w", encoding="utf-8").write(
    html.replace("@@SERIES@@", "".join(series_blocks)))
print("kiosk.html written:", len(series_blocks), "series")