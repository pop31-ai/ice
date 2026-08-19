# -*- coding: utf-8 -*-
"""
Свёрстка «Ледяного Пресс-Центра»: 10 цветных PDF-журналов,
по 10 выпусков (первых полос) в каждом. Контент берётся из
journals/YYYY-MM/*.txt. Иллюстрации — matplotlib, шрифты —
DejaVu (из поставки matplotlib), страницы — reportlab canvas.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from matplotlib import font_manager as _fm

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = os.path.dirname(__file__)
SRC = os.path.join(BASE, "journals")
OUT = os.path.join(BASE, "journals_pdf")
IMG = os.path.join(OUT, "_img")
os.makedirs(OUT, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

_TTF = os.path.join(os.path.dirname(_fm.__file__), "mpl-data", "fonts", "ttf")
pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(_TTF, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(_TTF, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Obl", os.path.join(_TTF, "DejaVuSans-Oblique.ttf")))

JOURNALS = {
    1: ("ЛЕДЯНАЯ ПЛОЩАДЬ", "ledyanaya-ploshchad", "металописье деревни у общего айсберга; хроника дней племени"),
    2: ("ШАПКА И КЛИК", "shapka-i-klik", "приёмы, стратегии и тактики выживания; школа клика"),
    3: ("БАЛАНС-ВЕСТНИК", "balans-vestnik", "числа правят льдом; моделирование и алгоритмы"),
    4: ("ШТОРМ-ТАЙМС", "shtorm-tayms", "хроника бурь и отважных сердец; драматургия непогоды"),
    5: ("ПЛЕМЯ-КУРЬЕР", "plemya-kurer", "жизни и судьбы человечков; сериалы, судьбы, продолжения"),
    6: ("АЙСБЕРГ-FUTURE", "aysberg-future", "прогнозы эпох и планы веков; футурология игры"),
    7: ("МАНА-ГАЗЕТКА", "mana-gazetka", "технологии льда: от клика до кванта; код и схемы"),
    8: ("РЕКОРД-ПРЕСС", "rekord-press", "турниры, рекорды и победы; конкурсы и лиги"),
    9: ("ВЕЧНЫЙ ЛЁД", "vechnyy-led", "притчи и размышления о вечном; философия"),
    10: ("ГАЛАКТИКА АЙСБЕРГ", "galaktika-aysberg", "ледяные миры планеты и звёзд; космос будущего"),
}

PAL = {
    1: ("#bfe8ff", "#fff6e0", "#FFC300", "#1F6FB2", "#39A9DB", "#0E4D7A", "#EAF6FF"),
    2: ("#ffe3d1", "#fff9f2", "#FF6B4A", "#C0392B", "#E74C3C", "#7B241C", "#FDEBD0"),
    3: ("#d3f5e8", "#eefbf5", "#2ECC71", "#148F77", "#1ABC9C", "#0B5345", "#E8F8F5"),
    4: ("#cfd8ff", "#f3e8ff", "#8E44AD", "#5B2C6F", "#7D3C98", "#331A4D", "#F4ECF7"),
    5: ("#ffe9c2", "#fffaf0", "#F39C12", "#B9770E", "#E67E22", "#7E5109", "#FEF9E7"),
    6: ("#f3c9ff", "#fff0fb", "#E91E8C", "#A62CB8", "#D63384", "#4A0E5C", "#FDE7F5"),
    7: ("#c9f0ff", "#eefbff", "#00BCD4", "#00838F", "#00ACC1", "#004D5C", "#E0F7FA"),
    8: ("#ffe9c2", "#fff8ec", "#F1C40F", "#D4AC0D", "#F39C12", "#7D6608", "#FEF9E7"),
    9: ("#d6e4f0", "#f2f6fb", "#AAB7C4", "#566573", "#7F8C8D", "#2E4053", "#EBF5FB"),
    10: ("#b6c2ff", "#f0e9ff", "#F5B7B1", "#4A235A", "#6C3483", "#1A0F2E", "#E8DAEF"),
}


def parse_issue(path):
    txt = open(path, encoding="utf-8").read()
    d = {}
    for label, key in [
        ("ЗАГОЛОВОК:", "title"),
        ("РАЗМЫШЛЕНИЕ.", "refl"),
        ("ПРОГНОЗ НА МЕСЯЦ.", "forecast"),
        ("ПРИЁМ И СТРАТЕГИЯ.", "tip"),
        ("ПАРАЛЛЕЛЬ С ДРУГИМИ ИГРАМИ.", "other"),
        ("КОНКУРС НОМЕРА.", "contest"),
        ("СУДЬБЫ ГЕРОЕВ.", "hero"),
    ]:
        for ln in txt.splitlines():
            if ln.strip().startswith(label):
                d[key] = ln.strip()[len(label):].strip()
                break
    head = txt.splitlines()[0:3]
    import re
    m = re.search(r"ВЫПУСК (\d+)/10", txt)
    d["issue"] = int(m.group(1)) if m else 0
    m = re.search(r"(\d{4}) года", txt)
    d["year"] = m.group(1) if m else ""
    m = re.search(r"ЖУРНАЛ «([^»]+)»", txt)
    d["jname"] = m.group(1) if m else ""
    for ln in txt.splitlines()[:3]:
        s = ln.strip()
        if s and not s.startswith("="):
            d["date"] = s
            break
    return d


def banner(jno):
    sky1, sky2, sun, accent, mid, dark, chip = PAL[jno]
    w, h = 560, 215
    fig = plt.figure(figsize=(w / 96, h / 96), dpi=96)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    for i in range(h):
        t = i / h
        col = tuple(t * np.array(plt.matplotlib.colors.to_rgb(sky2)) +
                    (1 - t) * np.array(plt.matplotlib.colors.to_rgb(sky1)))
        ax.add_patch(plt.Rectangle((0, i), w, 1, color=col))
    cx = w * (0.72 + 0.12 * np.sin(jno))
    sun = plt.matplotlib.colors.to_rgb(sun)
    ax.add_patch(plt.Circle((cx, h * 0.80), h * 0.16, color=sun))
    # лёд
    ice = plt.matplotlib.colors.to_rgb(accent)
    ice_l = plt.matplotlib.colors.to_rgb(mid)
    pts = [(0, h * 0.34), (w * 0.16, h * 0.46), (w * 0.30, h * 0.40), (w * 0.42, h * 0.68),
           (w * 0.52, h * 0.42), (w * 0.64, h * 0.5), (w * 0.78, h * 0.38), (w, h * 0.42),
           (w, h * 0.10), (0, h * 0.10)]
    ax.fill([p[0] for p in pts], [p[1] for p in pts], color=ice, edgecolor=ice_l, linewidth=2, zorder=3)
    # отражение и вода
    ax.add_patch(plt.Rectangle((0, 2), w, h * 0.09, color=ice_l, alpha=0.35, zorder=4))
    # куски льда
    for k, x in enumerate(np.linspace(w * 0.04, w * 0.94, 5 + jno)):
        a = h * 0.11 + (h * 0.05) * np.sin(k * jno)
        ax.add_patch(plt.Rectangle((x, a), w * 0.05, h * 0.045, color=ice_l,
                                   alpha=0.6, angle=15, zorder=5))
    # человечки с шапками
    rng = np.random.default_rng(jno)
    for k in range(6):
        x = w * (0.10 + 0.16 * k + 0.02 * np.random.default_rng(jno * 10 + k).uniform())
        y = h * 0.36 + 4
        col = plt.matplotlib.colors.to_rgb(dark if k % 2 else mid)
        ax.add_patch(plt.Circle((x, y + 6), 4.4, facecolor=(0.96, 0.93, 0.9), zorder=6))
        ax.add_patch(plt.Polygon([(x - 4.6, y + 9), (x + 4.6, y + 9), (x, y + 15)],
                                 color=col, zorder=7))
    # звёзды
    for k in range(8):
        xs, ys = rng.uniform(0, w), rng.uniform(h * 0.86, h * 0.99)
        ax.plot(xs, ys, marker="o", markersize=1 + (k % 2), color=(0.2, 0.3, 0.45), alpha=0.5)
    path = os.path.join(IMG, "banner-%02d.png" % jno)
    fig.savefig(path, dpi=96); plt.close(fig)
    return path


def chart(jno, issue):
    sky1, sky2, sun, accent, mid, dark, chip = PAL[jno]
    rng = np.random.default_rng(jno * 100 + issue)
    t = np.arange(0, 62)
    storm0, storm1 = 22, 36
    base = 95 - issue * 2.4 + rng.uniform(-3, 3)
    ice = base - 0.22 * t
    ice[storm0:storm1] -= (t[storm0:storm1] - storm0) * 1.1
    mana = np.clip(40 + 5 * t - 90 * ((t > storm0) & (t < storm1)), 5, 400)
    fish = np.clip(30 + 3 * np.sin(t / 3) + (t > 45) * 18, 0, 80)
    w, h = 560, 48
    fig = plt.figure(figsize=(w / 96, h / 96), dpi=96)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.03, 0.12, 0.94, 0.76])
    ax.plot(t, ice, color=mid, lw=2.2, label="лёд")
    ax.plot(t, mana / 4, color=accent, lw=1.6, alpha=0.85, label="мана/4")
    ax.plot(t, fish, color=dark, lw=1.6, alpha=0.8, ls=":", label="рыба")
    ax.axvspan(storm0, storm1, color=dark, alpha=0.12)
    ax.set_ylim(0, max(ice.max() + 8, 105))
    ax.set_yticks([]); ax.set_xticks([storm0, storm1, 60]); ax.set_xticklabels(["шторм—", "—буря", "60с"])
    ax.tick_params(labelsize=6)
    ax.legend(loc="upper right", fontsize=5, frameon=False)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_facecolor((1, 1, 1, 0))
    path = os.path.join(IMG, "chart-%02d-%02d.png" % (jno, issue))
    fig.savefig(path, dpi=96); plt.close(fig)
    return path


def wrap(text, font, size, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_section(c, label, text, y, pal, font="DejaVu-Bold", lfont="DejaVu", lsize=8.5, tsize=9.2, lw=500, lx=34):
    dark = pal[5]
    c.setFont(font, lsize)
    c.setFillColor(pal[3])
    c.drawString(lx, y, label)
    y -= lsize + 4
    c.setFont(lfont, tsize)
    c.setFillColor(dark)
    line_h = tsize + 3.4
    for ln in wrap(text, lfont, tsize, lw):
        c.drawString(lx, y - 2, ln)
        y -= line_h
    return y - 2


def build_pdf(jno, issues):
    name, slug, slogan = JOURNALS[jno]
    sky1, sky2, sun, accent, mid, dark, chip = PAL[jno]
    path = os.path.join(OUT, "journal-%02d-%s-01-10.pdf" % (jno, slug))
    c = rlcanvas.Canvas(path, pagesize=A4)
    W, H = A4
    banner_p = banner(jno)
    for idx, iss in enumerate(issues):
        issue = idx + 1
        chart_p = chart(jno, issue)
        # фон
        c.setFillColor("#FFFFFF"); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(sky1); c.rect(0, 0, W, H, fill=1, stroke=0)
        # шапка журнала
        c.roundRect(30, H - 64, W - 60, 34, 6, fill=1, stroke=0)
        c.setFillColor(accent)
        c.roundRect(30, H - 64, W - 60, 34, 6, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 13.5)
        c.setFillColor("#FFFFFF")
        c.drawCentredString(W / 2, H - 55, "ЖУРНАЛ «%s» · %02d/10 · ЛЕДЯНОЙ ПРЕСС-ЦЕНТР" % (name, issue))
        c.setFont("DejaVu-Obl", 8)
        c.setFillColor(sky2)
        c.drawCentredString(W / 2, H - 69, slogan)
        # дата-полоса
        c.roundRect(30, H - 94, W - 60, 22, 5, fill=1, stroke=0)
        c.setFillColor(mid)
        c.setFont("DejaVu", 9.5)
        c.setFillColor("#FFFFFF")
        c.drawCentredString(W / 2, H - 88, iss.get("date", "") + "  ·  ПЕРВАЯ ПОЛОСА ·  из архива будущего — "
                            "история, которую все вспомнят завтра")
        # картинка
        im_h = 205
        c.drawImage(banner_p, 30, H - 94 - im_h - 6, W - 60, im_h, preserveAspectRatio=True)
        # заголовок
        top = H - 94 - im_h - 6 - 34
        c.setFillColor(dark)
        c.roundRect(30, top, W - 60, 30, 5, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 13)
        c.setFillColor("#FFFFFF")
        c.drawString(44, top + 8, "№ %02d  ·  " % issue)
        c.drawString(110, top + 8, iss.get("title", ""))
        # график прогноза
        gy = top - 6 - 46
        c.setFillColor("white")
        c.roundRect(30, gy, W - 60, 46, 5, fill=1, stroke=0)
        c.drawImage(chart_p, 34, gy + 3, W - 68, 40)
        # секции
        y = gy - 8
        for label, key, fill in [
            ("РАЗМЫШЛЕНИЕ", "refl", sky1),
            ("ПРОГНОЗ НА МЕСЯЦ", "forecast", sky1),
            ("ПРИЁМ И СТРАТЕГИЯ", "tip", sky1),
            ("ПАРАЛЛЕЛЬ С ДРУГИМИ ИГРАМИ", "other", sky1),
            ("КОНКУРС НОМЕРА", "contest", sky1),
            ("СУДЬБЫ ГЕРОЕВ", "hero", sky1),
        ]:
            if fill:
                c.setFillColor(sky2)
                c.roundRect(30, y - 26, W - 60, 2, 2, fill=0, stroke=0)
            y = draw_section(c, label + ".  ", iss.get(key, ""), y, tuple(PAL[jno]))
            y -= 6
        # кластфер «продолжение»
        c.setFillColor(sky2)
        c.roundRect(30, y - 34, W - 60, 26, 5, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 10)
        c.setFillColor(dark)
        c.drawCentredString(W / 2, y - 24, "Продолжение серии — в следующем месяце · Лёд помнит всё (архив будущего станет историей)")
        # подвал
        c.setFillColor(accent)
        c.roundRect(30, 40, W - 60, 26, 5, fill=1, stroke=0)
        c.setFont("DejaVu", 8)
        c.setFillColor("#FFFFFF")
        c.drawCentredString(W / 2, 50, "ЛЁД 100% · ТАЯНИЕ 0.7%/с · МАНА +8/с · ЗАРЯД −3 за +2.5% · СЕТЬ +6 рыбы · "
                        "РОЖДЕНИЕ при рыбе ≥25 · ПРЕДЕЛ 12 чел. · ШТОРМ 10с ×2.5 · СЧЁТ = время×10 + люди×50")
        c.setFont("DejaVu-Obl", 7.5)
        c.setFillColor(dark)
        c.drawCentredString(W / 2, 28, "Игра «Ледяные человечки» · журнал «%s» · всё по статьям «Ледяной Вечерки»" % name)
        c.showPage()
    c.save()
    return path


def main():
    files = sorted(glob.glob(os.path.join(SRC, "20*", "*.txt")))
    by_journal = {}
    for f in files:
        d = parse_issue(f)
        jno = {v[0]: k for k, v in JOURNALS.items()}[d["jname"]]
        by_journal.setdefault(jno, []).append((d["issue"], f))
    out = []
    for jno in sorted(by_journal):
        ffs = sorted(by_journal[jno])
        issues = [parse_issue(f) for _, f in ffs]
        out.append(build_pdf(jno, issues))
        print("OK", os.path.basename(out[-1]))
    print("PDF files:", len(out))


if __name__ == "__main__":
    main()