# -*- coding: utf-8 -*-
"""Генератор wiki-ice.html — «Энциклопедия Льда»: всё про игру —
движок, серии, герои, 100 статей, рецепты и реклама сковородок."""
import os, glob, re, html

import gen_pdf_journals as g
from gen_journal_catalog import THEMES, HEROES

BASE = os.path.dirname(__file__)

PANSK = [
    ("Заметка", "Ледяная сковорода выдерживает −40°… +900°. Один шеф-повар оставил её на балконе в Снежнинске — утром на ней идеально поджарился омлет из сосульки."),
    ("Реклама", "СКОВОРОДА «ШТОРМ»: жарь под ураганом! Крышка из льда №1, ручка из мороза. Только в лавке у Маяка, 3-я полка."),
    ("Рецепт", "Омлет по-ледянски: 3 яйца шахтёра, 2 щепотки рыбы-стражника, лёд с крыши барака №7. Жарить на сковороде-«Айсберг» 4 минуты с зарядом +2.5% маны."),
    ("Заметка", "Дед-ледяник сказал молодому: «Сытый тот, у кого сковорода греется реже, чем каждые 6 секунд». Записали слова на корке льда."),
    ("Реклама", "СКОВОРОДА «БАЛАНС»: три ручки, одна доза голода. Подари шахтёру — прирост продуктивности +0.06 человека в секунду от радости."),
    ("Рецепт", "Рыба под сетью: поймай 25 хвостов, дай сковороде «Племя» схватить корочку. Каждые 6 секунд — по свежей порции, минус 15 рыбин, плюс 10 счёта."),
    ("Заметка", "Старый капитан гладил свою сковороду как судовой журнал. «Это моя вторая карта, — говорил он, — север — на сковороде, юг — в тесте»."),
    ("Реклама", "СКОВОРОДА «АЙСБЕРГ»: девяносто процентов под водой, десять — на огне. Для тех, кто видит больше, чем витрина."),
    ("Рецепт", "Манный остров: молоко, лёд, манка без манки. Секрет — прожарить на сковороде «Манна» при пункте баланса 12 из 12. Сервируется с графиком."),
    ("Заметка", "В редакции «Вечного льда» сковорода — корпоративный символ: на ней главред жарит черновики неподписавших колонок."),
    ("Реклама", "СКОВОРОДА «ГЛЯНЕЦ»: позолота по краям, трещины по фактуре. Выпуск лимитированный — 10 штук, как выпусков в серии."),
    ("Рецепт", "Северная волна на сковороде: замеси тесто восходящим потоком, жарь на «Волне» ровно 10 минут — по минуте на номер журнала."),
]
PAN_ITEMS = PANSK  # по одному на серию; у 1..10 берём свои + добавляем для 11-12


def excerpt(path):
    txt = open(path, encoding="utf-8").read()
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    body = [l for l in lines if len(l) > 8]
    if not body:
        return "(пусто)"
    return body[0][:140]


def read_articles(paths):
    out = []
    for p in sorted(paths):
        t = excerpt(p)
        base = os.path.basename(p).replace(".txt", "")
        out.append('<li><b>%s</b> — %s…</li>' % (html.escape(base), html.escape(t)))
    return out


present_pdfs = set(os.path.basename(p) for p in glob.glob(os.path.join(BASE, "journals_pdf", "*.pdf")))


def serie_card(jno):
    name, slug, slogan = g.JOURNALS[jno]
    glossy = jno >= 11
    pdf = "journal-%02d-%s-01-10%s.pdf" % (jno, slug, "-glossy" if glossy else "")
    cv = "covers/j%02d-cover.png" % jno
    themes = " · ".join(THEMES[jno])
    heroes = " · ".join(HEROES[jno])
    pan_type, pan_text = PAN_ITEMS[jno - 1]
    have = os.path.exists(os.path.join(BASE, "journals_pdf", pdf))
    pdf_link = ('<a href="journals_pdf/%s">PDF</a>' % pdf) if have else "PDF — скоро"
    return ('<div class="sercard">'
            '<div class="serhead"><img src="%s" width="120"><div>'
            '<h3>%s</h3><div class="devis">%s</div></div></div>'
            '<div class="meta">10 номеров · %s · обложка 120 шт</div>'
            '<p class="lbl">ТЕМЫ:</p><div class="chips">%s</div>'
            '<p class="lbl">СУДЬБЫ ГЕРОЕВ:</p><div class="chips">%s</div>'
            '<div class="pan"><span class="ptag">%s</span> 🥘 %s</div>'
            '<div class="links">%s · <a href="kiosk.html#ser%d">киоск</a> · <a href="%s">обложка</a></div>'
            '</div>'
            % (cv, name, slogan, "глянец" if glossy else "обычный", themes, heroes,
               pan_type, pan_text, pdf_link, jno, cv))


articles_now = read_articles(glob.glob(os.path.join(BASE, "articles", "*.txt")))
articles_future = read_articles(f for f in glob.glob(os.path.join(BASE, "articles", "future", "*.txt"))
                                if "README" not in os.path.basename(f))

html_page = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Энциклопедия Льда · всё про «Ледяных человечков»</title>
<style>
  body { margin:0; font-family:'Segoe UI',system-ui,sans-serif; color:#eaf6ff;
         background:radial-gradient(1200px 700px at 80% -10%, #2b5d8a, #0d1b2a 60%, #071220);
         padding:26px; }
  .wrap { max-width: 1120px; margin:0 auto; }
  h1 { font-size:30px; letter-spacing:1px; }
  h1 small { display:block; font-size:13px; opacity:.7; font-weight:400; }
  h2 { margin:50px 0 14px; font-size:24px; border-bottom:1px solid rgba(255,255,255,.2); padding-bottom:8px; }
  a { color:inherit; }
  .top a { display:inline-block; margin:6px 12px 6px 0; background:linear-gradient(180deg,#4aa8e0,#2f7fc0);
           padding:10px 20px; border-radius:10px; font-weight:700; font-size:14px; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(500px,1fr)); gap:20px; }
  .sercard { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12); border-radius:16px; padding:18px; }
  .serhead { display:flex; gap:16px; align-items:center; }
  .serhead h3 { margin:0; font-size:19px; }
  .devis { opacity:.7; font-size:12px; }
  .meta { font-size:12px; opacity:.7; margin:12px 0 4px; }
  .lbl { font-size:11px; letter-spacing:2px; opacity:.6; margin:10px 0 4px; }
  .chips { display:flex; flex-wrap:wrap; gap:5px; }
  .chips span { background:rgba(74,168,224,.18); border-radius:20px; padding:3px 10px; font-size:11px; }
  .pan { margin-top:12px; background:rgba(255,190,80,.08); border-left:3px solid #ffbe50; padding:8px 12px; font-size:13px; border-radius:6px; }
  .ptag { font-weight:700; color:#ffbe50; margin-right:6px; }
  .links { margin-top:10px; font-size:12px; opacity:.85; }
  .links a { color:#9fe0ff; margin-right:10px; }
  ul.cols { columns:2; column-gap:40px; font-size:13px; }
  ul.cols li { margin-bottom:8px; break-inside:avoid; opacity:.9; }
  .block { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1); border-radius:16px; padding:18px; }
  .nums { display:flex; flex-wrap:wrap; gap:12px; }
  .num { background:rgba(74,168,224,.15); border-radius:12px; padding:12px 16px; min-width:150px; }
  .num b { font-size:22px; color:#9fe0ff; }
  .num .n1 { font-size:12px; opacity:.8; }
  footer { margin-top:40px; opacity:.6; font-size:12px; border-top:1px solid rgba(255,255,255,.15); padding-top:12px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>📖 Энциклопедия Льда 🧊<small>всё, что известно про «Ледяных человечков»: от формул таяния до рецептов на сковороде</small></h1>
  <div class="top">
    <a href="index.html">🎮 Игра</a>
    <a href="press-center.html">📰 Пресс-Центр</a>
    <a href="kiosk.html">🗞 Газетный киоск</a>
    <a href="heroes.html">🎭 Досье героев</a>
    <a href="fun.html">🎪 Забавный уголок</a>
    <a href="epochs.html">📅 Лента эпох</a>
    <a href="polyart.html">✨ Полиарт-φ</a>
    <a href="README.md">💾 README</a>
  </div>

  <h2>🚀 Что это такое</h2>
  <div class="block">
    <p><b>«Ледяные человечки»</b> — браузерная idling-игра про ледяной лагерь, который тает вместе с вашими решениями.
    Один файл, без сервера: сохраняете вкладку открытой — лагерь живёт, закрываете — история застывает, и про неё пишут журналы.</p>
    <p>Вокруг игры построен живой пресс-центр: <b>100 статей</b>, <b>12 серий журналов</b> по <b>120 выпусков</b>,
    <b>120 обложек</b>, рецепты и реклама «Ледяных сковород». Своевременный факт: выпущенные номера никогда не меняют дат —
    с выходом календаря вперёд старые номера становятся хроникой будущего.</p>
  </div>

  <h2>⚙️ Движок (по показаниям техпаспорта)</h2>
  <div class="section"></div>
  <div class="block nums">
    <div class="num"><b>0.7 + 0.06·люди</b><div class="n1">льдинок тает в секунду</div></div>
    <div class="num"><b>×2.5 на 10 с</b><div class="n1">шторм при 50–70 с</div></div>
    <div class="num"><b>−3 маны</b><div class="n1">заряд → +2.5% льда</div></div>
    <div class="num"><b>+6 рыбы</b><div class="n1">сеть, кулдаун 0.4 с</div></div>
    <div class="num"><b>каждые 6 с</b><div class="n1">рождение: рыба ≥ 25, −15</div></div>
    <div class="num"><b>3 с без пищи</b><div class="n1">голод людей</div></div>
    <div class="num"><b>12</b><div class="n1">предел населения</div></div>
    <div class="num"><b>время×10 + люди×50</b><div class="n1">счёт</div></div>
  </div>

  <h2>🗞 12 серий журналов</h2>
  <div class="grid">@@SERIES@@</div>

  <h2>📜 50 статей — анализ игры</h2>
  <div class="block"><ul class="cols">@@ART_NOW@@</ul></div>

  <h2>🔮 50 статей — прогнозы из будущего</h2>
  <div class="block"><ul class="cols">@@ART_FUT@@</ul></div>

  <footer>
    Игра «Ледяные человечки» · github.com/pop31-ai/ice · «Сковорода — это тоже судьба».
    Все даты в журналах фиксированы: 2026–2027. После прохождения они остаются историей.
  </footer>
</div>
</body>
</html>
"""

out = html_page
out = out.replace("@@SERIES@@", "".join(serie_card(j) for j in range(1, 13)))
out = out.replace("@@ART_NOW@@", "\n".join(articles_now))
out = out.replace("@@ART_FUT@@", "\n".join(articles_future))
open(os.path.join(BASE, "wiki-ice.html"), "w", encoding="utf-8").write(out)
print("wiki-ice.html written; articles:", len(articles_now), "+", len(articles_future))