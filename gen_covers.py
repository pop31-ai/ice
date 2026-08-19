# -*- coding: utf-8 -*-
"""Обложки всех выпусков: журнал определённой серии = 10 номеров (1–10).
Output: covers/jNN-issue-MM.png (120 шт.) + covers/jNN-cover.png (= номер 01)."""
import os
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from matplotlib import font_manager as _fm

import gen_pdf_journals as g
from gen_journal_catalog import THEMES, HEROES

BASE = os.path.dirname(__file__)
COVERS = os.path.join(BASE, "covers")
os.makedirs(COVERS, exist_ok=True)

_TTF = os.path.join(os.path.dirname(_fm.__file__), "mpl-data", "fonts", "ttf")
F = lambda s: ImageFont.truetype(os.path.join(_TTF, "DejaVuSans.ttf"), s)
FB = lambda s: ImageFont.truetype(os.path.join(_TTF, "DejaVuSans-Bold.ttf"), s)

MONTHS = ["январь", "февраль", "март", "апрель", "май", "июнь",
          "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]


def issue_date(jno, issue):
    idx = (jno - 1) + (issue - 1)
    return "%s %d" % (MONTHS[idx % 12].capitalize(), 2026 + idx // 12)


def make_cover(jno, issue):
    name, slug, slogan = g.JOURNALS[jno]
    sky1, sky2, sunc, accent, mid, dark, chip = g.PAL[jno]
    quote, hint = g.epigraph(jno)
    title = THEMES[jno][issue - 1]
    hero = HEROES[jno][issue - 1]
    W, H = 600, 840
    c1 = np.array(Image.new("RGB", (1, 1), sky1).getpixel((0, 0)))
    c2 = np.array(Image.new("RGB", (1, 1), sky2).getpixel((0, 0)))
    if jno >= 11:
        c1, c2 = np.array([13, 10, 18]), np.array([28, 20, 39])
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        t = y / H
        col = tuple((c1 * (1 - t) + c2 * t).astype(int))
        for x in range(W):
            px[x, y] = col
    d = ImageDraw.Draw(im)

    b = Image.open(g.banner(jno)).convert("RGB")
    bw = W - 40
    bh = int(b.height * bw / b.width)
    im.paste(b.resize((bw, bh)), (20, 24))

    d.rectangle([10, 10, W - 10, H - 10], outline=sunc if jno >= 11 else accent, width=2)
    d.rectangle([16, 16, W - 16, H - 16], outline=sunc if jno >= 11 else accent, width=1)

    my = 60 + bh
    d.rounded_rectangle([30, my, W - 30, my + 70], radius=12, fill=accent if jno < 11 else sunc)
    tname = FB(30)
    tw = d.textlength(name, font=tname)
    d.text(((W - tw) / 2, my + 10), name, font=tname, fill="#0d0a12" if jno >= 11 else "#ffffff")
    d.text((34, my + 54), "  " + slogan[:56] + "…", font=F(12), fill=sunc if jno < 11 else "#1a1030")

    d.text((36, my + 86), "№ %02d/10 · %s" % (issue, issue_date(jno, issue)),
           font=FB(15), fill=chip if jno < 11 else sunc)

    yt = my + 148
    d.text((36, yt), "ТЕМА НОМЕРА:", font=F(12), fill=sunc if jno < 11 else "#e8a0bf")
    for k, ln in enumerate(g.wrap(title, "DejaVu-Bold", 24, W - 80)):
        d.text((36, yt + 22 + k * 32), ln, font=FB(24), fill=sky2 if jno < 11 else "#fffdf5")

    car = Image.open(g.caricature(jno, issue, hero)).convert("RGB")
    cw = int((W - 120) * 0.62)
    chh = int(car.height * cw / car.width)
    car = car.resize((cw, chh))
    cy = H - chh - 148
    im.paste(car, (int((W - cw) / 2) - 60, cy))
    d.rounded_rectangle([int((W - cw) / 2) - 62, cy - 4, int((W - cw) / 2) + cw + 2, cy + chh + 4],
                        radius=8, outline=sunc if jno >= 11 else mid, width=2)
    d.text((36, cy + chh - 72), "герой номера", font=F(14), fill=sunc if jno < 11 else "#e8a0bf")

    yq = cy + chh + 10
    d.rounded_rectangle([30, yq, W - 30, yq + 60], radius=10, outline=sunc if jno >= 11 else mid, width=1)
    d.multiline_text((46, yq + 10), "«" + (quote[:90] + "…»"), font=F(12), fill=chip if jno < 11 else "#fffdf5")

    d.text((30, H - 52), "ИЗ-ПОД КАПОТА · 0.7+0.06·люди/с · шторм ×2.5", font=FB(12),
           fill=accent if jno < 11 else sunc)
    d.text((30, H - 34), "серия «%s» · номер %02d/10 · путь героя: %s" % (name, issue, hero[:44]),
           font=F(10), fill=chip if jno < 11 else "#b8a2c8")

    out = os.path.join(COVERS, "j%02d-issue-%02d.png" % (jno, issue))
    im.save(out)
    return out


if __name__ == "__main__":
    n = 0
    for j in range(1, 13):
        for i in range(1, 11):
            make_cover(j, i)
            n += 1
        import shutil
        shutil.copy(os.path.join(COVERS, "j%02d-issue-01.png" % j),
                    os.path.join(COVERS, "j%02d-cover.png" % j))
    print("covers:", n)