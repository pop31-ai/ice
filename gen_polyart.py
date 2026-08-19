# -*- coding: utf-8 -*-
"""Генератор polyart.html — «Полиарт-φ галерея»: все 120 обложек в стиле
полиномиального искусства и золотого сечения + манифест и поводы для PR."""
import os, urllib.parse

import gen_pdf_journals as g
from gen_kiosk import issue_date

BASE = os.path.dirname(__file__)
COVERS = os.path.join(BASE, "covers")

MANIFEST = [
    "1. У каждой обложки — своя кривая. Полином степени 3 задаёт слои неба — ни одна из 120 не повторяет ни одну другую.",
    "2. Золотое сечение правит композицией: φ-сечения расставляют заголовки, спираль — ритм, а читатель — порядок.",
    "3. Кристаллы нарисованы полиномиальными дугами: шесть лепестков, каждый — квадратичная кривая Безье, повёрнутая на 60°.",
    "4. Палитра серии — это характер издания: холодный свет Площади, огонь Шторма, золото Глянца. Цвет — мнение, а не украшение.",
    "5. Алгоритм — это автор: каждый тираж уникален, как снежинка, но подписан одной редакцией.",
    "6. Полиарт-φ — это привет математике: игра про таяние иллюстрирована формулами, а не «картинками ради картинок».",
    "7. Стиль порождает контент: о покрытии, кривых и кристаллах можно писать статьи, делать посты и мерчадайзинг.",
    "8. Технологичность — тема PR: 120 обложек сгенерированы кодом за минуты, но выглядят как ручная графика.",
    "9. Идентичность серий: глаза, шапки и сковородки остаются, а небо меняется — читатель узнаёт издание мгновенно.",
    "10. Всё связано: обложка, PDF, статьи, энциклопедия и игра живут в одном репозитории — это издательство, а не набор файлов.",
    "11. Этика эстетики: прекрасное без затрат, искусство без гуру — годный повод рассказать о репозитории.",
    "12. Каждая обложка — маленькая история, которая станет большой, когда её месяц пройдёт.",
]

blocks = []
for jno in range(1, 13):
    name, slug, slogan = g.JOURNALS[jno]
    thumbs = []
    for issue in range(1, 11):
        cov = "covers/j%02d-issue-%02d.png" % (jno, issue)
        date = issue_date(jno, issue)
        thumbs.append(
            '<div class="iss"><img src="%s" width="124"><div class="ino">%s · №%02d/10</div>'
            '<div class="it">%s</div></div>'
            % (cov, name, issue, date))
    blocks.append(
        '<div class="ser"><h2>%s <small>серия из 10 полиарт-обложек</small></h2>'
        '<p class="devis">%s</p><div class="row">%s</div></div>'
        % (name, slogan, "".join(thumbs)))

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Полиарт-φ · Ледяной Пресс-Центр</title>
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
  .manifest { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12); border-radius:16px;
              padding:20px 24px; margin:28px 0; }
  .manifest .mrow { margin:9px 0; font-size:14px; line-height:1.5; opacity:.94; }
  .manifest .mrow b { color:#9fe0ff; }
  .ser { margin:40px 0; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12);
         border-radius:18px; padding:20px; }
  .ser h2 { margin:0; font-size:22px; }
  .ser h2 small { font-size:12px; opacity:.6; font-weight:400; }
  .devis { opacity:.75; font-size:13px; margin:6px 0 14px; }
  .row { display:flex; flex-wrap:wrap; gap:14px; justify-content:center; }
  .iss { text-align:center; width:124px; }
  .iss img { border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,.5); }
  .ino { font-size:11px; margin-top:6px; opacity:.85; }
  .it { font-size:10px; opacity:.6; }
  footer { margin-top:36px; opacity:.6; font-size:12px; border-top:1px solid rgba(255,255,255,.15); padding-top:12px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>✨ Полиарт-φ 🧊<small>120 обложек в стиле полиномиального искусства и золотого сечения — метод, а не шаблон</small></h1>
  <div class="top">
    <a href="index.html">🎮 Игра</a>
    <a href="press-center.html">📰 Пресс-Центр</a>
    <a href="kiosk.html">🗞 Киоск</a>
    <a href="wiki-ice.html">📖 Энциклопедия</a>
    <a href="heroes.html">🎭 Досье героев</a>
    <a href="fun.html">🎪 Забавный уголок</a>
    <a href="epochs.html">📅 Лента эпох</a>
    <a href="situations.html">🖼 Ситуации</a>
  </div>

  <div class="manifest">
    <h2 style="margin-top:0">Манифест стиля</h2>
    @@MANIFEST@@
  </div>

  @@SERIES@@
  <footer>Игра «Ледяные человечки» · github.com/pop31-ai/ice · «Красота — это полином, у которого есть характер».</footer>
</div>
</body>
</html>
"""

out = html
rows = "\n".join('<div class="mrow"><b>%s</b></div>' % m for m in MANIFEST)
out = out.replace("@@MANIFEST@@", rows).replace("@@SERIES@@", "".join(blocks))
open(os.path.join(BASE, "polyart.html"), "w", encoding="utf-8").write(out)
print("polyart.html written; covers:", 120)