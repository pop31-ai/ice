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
from matplotlib.colors import to_rgb, to_hex

from ice_lore import PANS, BABAIS, EXTRA, ENGINEERING as ENGCALC, GOLD

W, H = A4

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
    11: ("ЛЕДЯНОЙ ГЛЯНЕЦ", "ledyanoy-glyanets", "мода севера: шапки, цвет маны и стиль выживания; глянец из-под капота"),
    12: ("СЕВЕРНАЯ ВОЛНА", "severnaya-volna", "светская хроника льда: балы, тренды, шепоты шторма и звёзды деревни"),
    13: ("ЗОЛОТОЙ ЖУРНАЛ", "zolotoy-zhurnal", "золотая серия Вечерки: премии года, события месяцев и саги лагеря; 2027-10…2028-07"),
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
    11: ("#e8dcc8", "#fffdf5", "#D4AF37", "#3a2e1e", "#8a6d3b", "#241a0e", "#FBF3DF"),
    12: ("#f0d9e8", "#fff5fb", "#E8A0BF", "#7b2d5e", "#c26a9c", "#3a1030", "#FDEBF4"),
    13: ("#f2e6c8", "#fffbe6", "#FFD700", "#6b4e10", "#c9a227", "#241a0e", "#FFF3C4"),
}

MISTER_FUTURE = [
    "лед, который читал о будущем, начинает помнить начало",
    "завтра придёт без приглашения и оставит записку",
    "вода, идущая назад, знает, где спрятан трон",
    "тишина аккумулирует крики тех, кто не достучался",
    "под листом прошлого издание перечитывает автор",
    "что написано лунным светом, читается только в шторм",
    "зимы приходят ради того, чтобы имя дожило",
    "кольцо сомкнётся там, где безымянный оставил след",
]

# шифр из статей (будущих номеров Вечерки) как «вода» журналов
EPIGRAPH_SRC = {
    11: ("articles/01-shedevr.txt", "articles/future/001-epoha-odnogo-fayla.txt"),
    12: ("articles/02-odna-stranitsa.txt", "articles/future/002-pikseli-govoryat.txt"),
}


def epigraph(jno):
    """Тайный эпиграф номера, выжатый из статей (cp1251), + шифрованный намёк."""
    srcs = EPIGRAPH_SRC.get(jno)
    quote = "молчание льда так и не разрешили напечатать"
    if srcs:
        for f in srcs:
            p = os.path.join(BASE, f)
            if os.path.exists(p):
                try:
                    lines = open(p, encoding="cp1251").read().splitlines()
                except UnicodeDecodeError:
                    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
                body = " . ".join(l.strip() for l in lines[2:] if len(l.strip()) > 8)
                sents = [s.strip() for s in body.split(".") if len(s.strip()) > 35]
                if sents:
                    quote = max(sents, key=len)
                    break
    rnd = np.random.default_rng(jno * 11)
    hint = MISTER_FUTURE[(jno + 3) % len(MISTER_FUTURE)]
    return quote, hint


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
        ("ГЛАВНОЕ СОБЫТИЕ.", "main_event"),
    ]:
        for ln in txt.splitlines():
            if ln.strip().startswith(label):
                d[key] = ln.strip()[len(label):].strip()
                break
    d["events"] = []
    for ln in txt.splitlines():
        s = ln.strip()
        if s.startswith("СОБЫТИЕ."):
            ev = s[len("СОБЫТИЕ."):].strip()
            if ev:
                d["events"].append(ev)
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


def simulate(jno, issue):
    """Симулятор партии, точно повторяющий движок index.html (dt=0.01с)."""
    profiles = ["пассивная", "умеренная", "активная"]
    pname = profiles[(jno + issue) % 3]
    rnd = np.random.default_rng(jno * 31 + issue)
    T, dt = 190.0, 0.01
    n = int(T / dt)
    ice = np.zeros(n); mana = np.zeros(n); fish = np.zeros(n); pop = np.zeros(n)
    storm_arr = np.zeros(n)
    I, M, F, P = 100.0, 100.0, 40.0, 4
    stormT = 55.0; storm_on = False; sleft = 0.0
    fish_cd = 0.0; birth = 0.0; starve = 0.0
    frost_b = fish_b = 0.0
    rates = {"пассивная": (0.0, 0.0), "умеренная": (0.95, 0.9), "активная": (1.8, 1.5)}
    r_ice, r_fish = rates[pname]
    last_minmana = {"пассивная": 99, "умеренная": 26, "активная": 14}[pname]
    length = 0.0
    for i in range(n):
        t = i * dt
        melt = 0.7 + 0.06 * P
        if storm_on:
            melt *= 2.5
        I = max(0.0, I - melt * dt)
        M = min(100.0, M + 8 * dt)
        F = max(0.0, min(250.0, F + (P * 0.6 - P * 0.9) * dt))
        fish_cd = max(0.0, fish_cd - dt)
        # клики по льду: каждые −3 маны → +2.5% льда
        if r_ice > 0 and M > last_minmana:
            frost_b += r_ice * dt
            while frost_b >= 1 and M >= 3:
                frost_b -= 1; M -= 3; I = min(100.0, I + 2.5)
        # клики по воде: +6 рыбы каждые 0.4с (без затрат маны)
        if P < 12 and F < 90 and fish_cd <= 0:
            fish_b += r_fish * dt
            while fish_b >= 1:
                fish_b -= 1; fish_cd = 0.4; F = min(250.0, F + 6)
        else:
            fish_b = max(0.0, fish_b - dt)
        # рождение: рыба ≥ 25 → каждые 6с +1 человек, −15 рыбы
        if P < 12 and F >= 25:
            birth += dt
            if birth >= 6:
                birth = 0.0; P += 1; F = max(0.0, F - 15)
        else:
            birth = 0.0
        # голод: рыба = 0 → через 3с минус человек, потом каждые 2с
        if F <= 0:
            starve += dt
            if starve >= 3:
                starve = 2.0; P -= 1
                if P <= 0:
                    break
        else:
            starve = 0.0
        # шторм: каждые 50–70с на 10с таяние ×2.5
        stormT -= dt
        if stormT <= 0 and not storm_on:
            storm_on = True; sleft = 10.0; stormT = 50 + rnd.uniform(0, 20)
        if storm_on:
            sleft -= dt
            storm_on = sleft > 0
        ice[i] = I; mana[i] = M; fish[i] = F; pop[i] = P
        storm_arr[i] = 1 if storm_on else 0
        if I <= 0:
            break
        length = t
    return pname, length, ice, mana, fish, pop, storm_arr, dt


def chart(jno, issue):
    """График «из-под капота»: реальная симуляция партии по коду index.html."""
    sky1, sky2, sunc, accent, mid, dark, chip = PAL[jno]
    pname, length, ice, mana, fish, pop, storm, dt = simulate(jno, issue)
    t = np.arange(len(ice)) * dt
    w, h = 560, 48
    fig = plt.figure(figsize=(w / 96, h / 96), dpi=96)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.03, 0.12, 0.94, 0.76])
    ax.plot(t, ice, color=mid, lw=2.2, label="лёд")
    ax.plot(t, mana, color=accent, lw=1.5, alpha=0.85, label="мана")
    ax.plot(t, fish / 2.5, color=dark, lw=1.4, alpha=0.8, ls=":", label="рыба/2.5")
    on = storm > 0
    ax.fill_between(t, 0, 100, where=on, step="post", color=dark, alpha=0.16)
    # отметки штормов «воду»
    edges = np.diff(np.concatenate(([0], storm.astype(int), [0])))
    starts = np.where(edges == 1)[0] * dt
    ends = np.where(edges == -1)[0] * dt
    for s0, e0 in zip(starts, ends):
        ax.text((s0 + e0) / 2, 90, "ШТОРМ ×2.5", ha="center", fontsize=6, color=dark,
                fontname="DejaVu Sans", fontweight="bold")
    # рождения — отметка-звезда
    births = np.where(np.diff(pop) > 0)[0] * dt
    for b0 in births:
        ax.annotate("★ род", (b0, ice[int(b0 / dt)]), textcoords="offset points",
                    xytext=(-10, 5), fontsize=5.5, color=accent,
                    fontname="DejaVu Sans")
    # «вода» в графике: волны до горизонта
    xw = np.linspace(0, length if length else 60, 200)
    ax.fill_between(xw, 0, 12 + 8 * np.sin(xw * 0.4 + jno),
                    color=plt.matplotlib.colors.to_rgb(mid) + (0.25,), zorder=3)
    ax.set_ylim(-2, 104)
    ax.set_yticks([])
    ax.set_xticks([0, length / 2 if length else 30, length if length else 60])
    ax.set_xticklabels(["0с", "%ds" % round(length / 2), "%ds" % round(length)])
    ax.tick_params(labelsize=6)
    ax.set_title("симуляция кода index.html · профиль «%s» · племя в живых до %ds" %
                 (pname, round(length)), fontsize=7, color=dark, fontname="DejaVu Sans", loc="left")
    ax.legend(loc="upper right", fontsize=5.5, frameon=False, ncol=3)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_facecolor((1, 1, 1, 0))
    path = os.path.join(IMG, "chart-%02d-%02d.png" % (jno, issue))
    fig.savefig(path, dpi=96); plt.close(fig)
    return path


PHRASES = [
    "Клик — моя мана!", "Я спас этот лёд!", "Берегите шапки!",
    "Шторм? Где шторм?!", "Рыба — моя!", "Лёд помнит меня!",
    "Герой выходит из бури!", "Рекорд уже мой!",
    "Древняя формула у меня!", "Судьба льда — в моих руках!",
]


def caricature(jno, issue, hero):
    """Шарж героя номера: огромная голова, крошечное тело, шапка-помпон."""
    sky1, sky2, sunc, accent, mid, dark, chip = PAL[jno]
    rng = np.random.default_rng(jno * 1000 + issue)
    w, h = 220, 240
    fig = plt.figure(figsize=(w / 96, h / 96), dpi=96)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    for i in range(h):
        t = i / h
        col = tuple(t * np.array(plt.matplotlib.colors.to_rgb(sky2)) +
                    (1 - t) * np.array(plt.matplotlib.colors.to_rgb(sky1)))
        ax.add_patch(plt.Rectangle((0, i), w, 1, color=col))
    # снег
    ax.add_patch(plt.Rectangle((0, 0), w, h * 0.08, color=(0.97, 0.98, 1)))
    cx, cy = w / 2, h * 0.60
    skin = (1.0, 0.93, 0.87)
    # тело-полушубок (крошечное)
    ax.add_patch(plt.Rectangle((cx - 16, 4), 32, 26, color=accent, edgecolor=dark, lw=2, zorder=3))
    ax.add_patch(plt.Circle((cx - 16, 18), 5, color=mid)); ax.add_patch(plt.Circle((cx + 16, 18), 5, color=mid))
    ax.add_patch(plt.Circle((cx, 26), 9, color=skin, zorder=4))
    # огромная голова
    rx, ry = 52 + rng.uniform(-6, 8), 40 + rng.uniform(-5, 6)
    ax.add_patch(plt.matplotlib.patches.Ellipse((cx, cy), rx, ry, facecolor=skin,
                                                edgecolor=dark, lw=2, zorder=5))
    # уши
    for s in (-1, 1):
        ax.add_patch(plt.Circle((cx + s * rx * 0.62, cy - 8), 12, color=skin,
                                edgecolor=dark, lw=1.5, zorder=5))
    # гигантский нос
    ax.add_patch(plt.matplotlib.patches.Ellipse((cx, cy - 2), 20, 30, facecolor=(0.99, 0.85, 0.75),
                                                edgecolor=dark, lw=1.5, zorder=6))
    # глаза
    for s in (-1, 1):
        ax.add_patch(plt.Circle((cx + s * 16, cy + 12), 8, color="white", zorder=6))
        ax.add_patch(plt.Circle((cx + s * 16, cy + 12), 4, color=dark, zorder=7))
    ax.add_patch(plt.Circle((cx + 6, cy + 12), 7, color="white", zorder=6))
    ax.add_patch(plt.Circle((cx + 6, cy + 12), 3.5, color=dark, zorder=7))
    # брови
    for s in (-1, 1):
        ax.plot([cx + s * 25, cx + s * 8], [cy + 27, cy + 25], color=dark, lw=2.5, zorder=7)
    # румянец
    for s in (-1, 1):
        ax.add_patch(plt.Circle((cx + s * 26, cy - 12), 6, color=(1, 0.7, 0.7), alpha=0.55, zorder=5))
    # шапка с помпоном
    cols = [sunc, mid, accent]
    hc = cols[(issue + jno) % 3]
    ax.add_patch(plt.matplotlib.patches.Ellipse((cx, cy + ry * 0.52), rx * 0.9, 16,
                                                facecolor=hc, edgecolor=dark, lw=2, zorder=8))
    ax.add_patch(plt.Rectangle((cx - rx * 0.4, cy + ry * 0.46), rx * 0.8, 18, facecolor=hc,
                               edgecolor=dark, lw=2, zorder=8))
    ax.add_patch(plt.Circle((cx, cy + ry * 0.46 + 22), 9, color=mid if issue % 2 else sunc, zorder=9))
    # пузырь речи
    bx, by, bww, bhh = cx - rx * 1.55, cy + ry * 0.75, 150, 34
    ax.add_patch(plt.Rectangle((bx, by), bww, bhh, facecolor="white", edgecolor=dark,
                               lw=1.5, alpha=0.92, zorder=9))
    ax.plot([bx + 26, bx + 8], [by, by - 8], color=dark, lw=1.2, zorder=9)
    phrase = PHRASES[(jno + issue * 3) % len(PHRASES)]
    ax.text(bx + bww / 2, by + bhh / 2 - 4, phrase, ha="center", va="center",
            fontsize=10, color=dark, fontname="DejaVu Sans", zorder=10)
    # звезда-слава
    ax.text(cx + rx * 0.5, cy + ry * 0.8, "★", fontsize=16, color=sunc, ha="center", zorder=8)
    path = os.path.join(IMG, "caric-%02d-%02d.png" % (jno, issue))
    fig.savefig(path, dpi=96); plt.close(fig)
    return path


def _panel(jno, wpx, hpx):
    sky1, sky2, sunc, accent, mid, dark, chip = PAL[jno]
    fig = plt.figure(figsize=(wpx / 96, hpx / 96), dpi=96)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, wpx); ax.set_ylim(0, hpx); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), wpx, hpx, color=sky2))
    return fig, ax, (sky1, sky2, sunc, accent, mid, dark, chip)


def gauge(jno, issue):
    """Датчики ресурсов: полукруг-стрелка для льда + три шкалы мана/рыба/люди."""
    fig, ax, p = _panel(jno, 378, 162)
    sky1, sky2, sunc, accent, mid, dark, chip = p
    rng = np.random.default_rng(jno * 50 + issue)
    ice = min(88, max(30, 60 - issue * 2.2 + rng.uniform(-8, 10)))
    mana = min(100, max(25, 70 + rng.uniform(-14, 10)))
    fish = min(90, max(20, 55 + rng.uniform(-12, 12)))
    pop = min(12, max(1, round(1 + issue * 1.1 + rng.uniform(-1, 1))))
    cx, cy, r = 88, 78, 46
    th = np.linspace(np.pi, 0, 100)
    col = plt.matplotlib.colors.to_rgb(mid)
    ax.fill(cx + r * np.cos(th), cy + r * np.sin(th), color=(0.93, 0.95, 0.97), zorder=2)
    th2 = np.linspace(np.pi, 0, 100)
    ax.plot(cx + r * np.cos(th2), cy + r * np.sin(th2), color=col, lw=3, zorder=3)
    ang = np.pi * (1 - ice / 100)
    ax.plot([cx, cx + r * 0.78 * np.cos(ang)], [cy, cy + r * 0.78 * np.sin(ang)],
            color=accent, lw=5, zorder=4)
    ax.add_patch(plt.Circle((cx, cy), 7, color=dark, zorder=5))
    ax.text(cx, cy + r * 1.25, "ЛЁД %d%%" % round(ice), ha="center", fontsize=16,
            color=dark, fontname="DejaVu Sans", fontweight="bold", zorder=6)
    for i, (label, val, color) in enumerate([
            ("МАНА", mana, mid), ("РЫБА", fish, accent), ("ЛЮДИ", pop * 8.3, dark)]):
        bx = 196 + i * 68
        fh = min(72, val * 0.8 if i < 2 else pop * 6.6)
        ax.add_patch(plt.Rectangle((bx, 30), 36, max(4, fh), color=color, alpha=0.85, zorder=3))
        ax.text(bx + 6, 116, str(round(val if i < 2 else pop)), fontsize=13, color=dark,
                fontname="DejaVu Sans", fontweight="bold")
        ax.text(bx - 4, 18, label, fontsize=10, color=dark, fontname="DejaVu Sans")
    ax.text(189, 152, "ДАТЧИКИ ПЛЕМЕНИ", ha="center", fontsize=11, color="#FFFFFF",
            fontname="DejaVu Sans", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc=(0.35, 0.55, 0.78, 0.95), ec="none"))
    path = os.path.join(IMG, "gauge-%02d-%02d.png" % (jno, issue))
    fig.savefig(path, dpi=96); plt.close(fig)
    return path


def stormradar(jno, issue):
    """Круговой «секундомер» шторма: дуга бури 22–36с, стрелка текущего положения."""
    fig, ax, p = _panel(jno, 378, 162)
    sky1, sky2, sunc, accent, mid, dark, chip = p
    rng = np.random.default_rng(jno * 7 + issue)
    cx, cy, r = 88, 80, 48
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, color=dark, lw=2.5, zorder=3))
    for s in range(60):
        a = np.pi / 2 - 2 * np.pi * s / 60
        big = 22 <= s <= 36
        x1, y1 = cx + 0.86 * r * np.cos(a), cy + 0.86 * r * np.sin(a)
        x2, y2 = cx + (0.97 if big else 0.93) * r * np.cos(a), cy + (0.97 if big else 0.93) * r * np.sin(a)
        ax.plot([x1, x2], [y1, y2], color=(accent if big else dark), lw=(2.4 if big else 1.1), zorder=4)
    thb = np.linspace(np.pi / 2 - 2 * np.pi * 22 / 60, np.pi / 2 - 2 * np.pi * 36 / 60, 60)
    ax.fill(cx + 0.9 * r * np.cos(thb), cy + 0.9 * r * np.sin(thb),
            color=plt.matplotlib.colors.to_rgb(accent) + (0.18,), zorder=2)
    cur = (issue * 7 + int(rng.integers(0, 20))) % 60
    ac = np.pi / 2 - 2 * np.pi * cur / 60
    ax.plot([cx, cx + r * 0.8 * np.cos(ac)], [cy, cy + r * 0.8 * np.sin(ac)], color=sunc, lw=4, zorder=5)
    ax.add_patch(plt.Circle((cx, cy), 6, color=dark, zorder=6))
    to_storm = (22 - cur) % 60
    ax.text(cx, cy + r + 26, "ШТОРМ-РАДАР", ha="center", fontsize=11, color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.25", fc=(0.35, 0.55, 0.78, 0.95), ec="none"),
            fontname="DejaVu Sans", fontweight="bold")
    ax.text(cx + r + 46, cy + 26, "секунда:\n%d" % cur, ha="center", fontsize=13, color=dark,
            fontname="DejaVu Sans", fontweight="bold")
    ax.text(cx + r + 46, cy - 24, "до бури:\n~%dс" % to_storm, ha="center", fontsize=13, color=accent,
            fontname="DejaVu Sans", fontweight="bold")
    ax.text(362, 14, "", fontsize=1, color="none")
    path = os.path.join(IMG, "radar-%02d-%02d.png" % (jno, issue))
    fig.savefig(path, dpi=96); plt.close(fig)
    return path


def popgrowth(jno, issue):
    """Рост племени по выпускам: столбцы 1–10, текущий подсвечен."""
    fig, ax, p = _panel(jno, 378, 162)
    sky1, sky2, sunc, accent, mid, dark, chip = p
    rng = np.random.default_rng(jno * 3 + issue)
    vals = [min(12, max(1, round(1 + (i - 1) * 1.15 + rng.uniform(-0.8, 0.8)))) for i in range(1, 11)]
    for i, v in enumerate(vals):
        x = 40 + i * 32
        col = accent if i + 1 == issue else dark
        ax.add_patch(plt.Rectangle((x, 28), 22, v * 9.2, color=col, alpha=(1 if i + 1 == issue else 0.45), zorder=3))
        if i + 1 == issue:
            ax.text(x + 11, 130, "★", ha="center", fontsize=14, color=accent, zorder=5)
        ax.text(x + 11, 16, str(i + 1), ha="center", fontsize=9, color=dark, fontname="DejaVu Sans")
    ax.text(189, 152, "РОСТ ПЛЕМЕНИ", ha="center", fontsize=11, color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.25", fc=(0.35, 0.55, 0.78, 0.95), ec="none"),
            fontname="DejaVu Sans", fontweight="bold")
    path = os.path.join(IMG, "pop-%02d-%02d.png" % (jno, issue))
    fig.savefig(path, dpi=96); plt.close(fig)
    return path


def scoredonut(jno, issue):
    """Кольцо рекорда: доля времени и людей в счёте партии."""
    fig, ax, p = _panel(jno, 378, 162)
    sky1, sky2, sunc, accent, mid, dark, chip = p
    rng = np.random.default_rng(jno * 9 + issue)
    t_sec = 300 + issue * 40 + rng.uniform(-40, 60)
    pop = 1 + issue * 1.1
    a_t = t_sec * 10
    a_p = pop * 50
    cx, cy, r = 110, 80, 46
    tot = a_t + a_p
    f_t, f_p = a_t / tot, a_p / tot
    theta = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi * f_t, 80)
    ax.fill(cx + r * np.cos(theta), cy + r * np.sin(theta), color=mid, zorder=3)
    theta2 = np.linspace(np.pi / 2 - 2 * np.pi * f_t, np.pi / 2 - 2 * np.pi, 80)
    ax.fill(cx + r * np.cos(theta2), cy + r * np.sin(theta2), color=accent, zorder=3)
    ax.add_patch(plt.Circle((cx, cy), r * 0.62, color=sky2, zorder=4))
    ax.text(cx, cy, "%d" % round(tot), ha="center", va="center", fontsize=20, color=dark,
            fontname="DejaVu Sans", fontweight="bold", zorder=5)
    ax.plot([cx + r + 40, cx + r + 56], [cy + 20, cy + 20], color=mid, lw=4)
    ax.text(cx + r + 62, cy + 20, "ВРЕМЯ %.0f%%" % (f_t * 100), va="center", fontsize=10,
            color=dark, fontname="DejaVu Sans", fontweight="bold")
    ax.plot([cx + r + 40, cx + r + 56], [cy - 18, cy - 18], color=accent, lw=4)
    ax.text(cx + r + 62, cy - 18, "ЛЮДИ %.0f%%" % (f_p * 100), va="center", fontsize=10,
            color=dark, fontname="DejaVu Sans", fontweight="bold")
    ax.text(189, 152, "МАШИНА РЕКОРДА", ha="center", fontsize=11, color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.25", fc=(0.35, 0.55, 0.78, 0.95), ec="none"),
            fontname="DejaVu Sans", fontweight="bold")
    path = os.path.join(IMG, "score-%02d-%02d.png" % (jno, issue))
    fig.savefig(path, dpi=96); plt.close(fig)
    return path


def gold_timeline(jno, issue):
    """Лента Золотого года (2027-10 … 2028-07): 10 выпусков, текущий подсвечен звездой."""
    from gen_journal_catalog import GOLD_ISSUES
    fig, ax, p = _panel(jno, 700, 170)
    sky1, sky2, sun, accent, mid, dark, chip = p
    w, h = 700, 170
    months = ["окт.", "ноя.", "дек.", "янв.", "фев.", "март", "апр.", "май", "июнь", "июль"]
    xs = np.linspace(w * 0.06, w * 0.94, 10)
    ax.add_patch(plt.Rectangle((w * 0.02, h * 0.64), w * 0.96, 9, color=mid, alpha=0.45, zorder=2))
    for i, (x, mo) in enumerate(zip(xs, months)):
        cur = (i + 1) == issue
        ax.add_patch(plt.Circle((x, h * 0.685), (18 if cur else 10),
                                color=sun if cur else mid, zorder=4 + int(cur)))
        ax.text(x, h * 0.52, str(i + 1), ha="center", fontsize=(13 if cur else 9),
                color=dark, fontweight="bold", fontname="DejaVu Sans", zorder=6)
        ax.text(x, h * 0.38, "%s %d" % (mo, 2027 + (i >= 3)), ha="center", fontsize=7.5,
                color=dark, fontname="DejaVu Sans")
        head, _ = GOLD_ISSUES[i]
        ax.text(x, h * 0.22, head[:26] + ("…" if len(head) > 26 else ""), ha="center",
                fontsize=6, color=chip, fontname="DejaVu Sans")
        if cur:
            ax.text(x, h * 0.88, "★", ha="center", fontsize=24, color=sun, zorder=6)
    ax.text(w * 0.03, h * 0.965, "ЗОЛОТОЙ ГОД · лента выпусков октябрь 2027 → июль 2028",
            fontsize=9, color="#FFFFFF", fontweight="bold", fontname="DejaVu Sans",
            bbox=dict(boxstyle="round,pad=0.25", fc=(0.55, 0.45, 0.15, 0.95), ec="none"))
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    path = os.path.join(IMG, "gold-tl-%02d.png" % issue)
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


def draw_section(c, label, text, y, pal, font="DejaVu-Bold", lfont="DejaVu", lsize=7.6, tsize=8.3, lw=500, lx=34):
    dark = pal[5]
    c.setFont(font, lsize)
    c.setFillColor(pal[3])
    c.drawString(lx, y, label)
    y -= lsize + 3.5
    c.setFont(lfont, tsize)
    c.setFillColor(dark)
    line_h = tsize + 2.8
    for ln in wrap(text, lfont, tsize, lw):
        c.drawString(lx, y - 2, ln)
        y -= line_h
    return y - 2


TECHPASSPORT = ("СТАРТ ЛЁД 100/МАНА 100/РЫБА 40/ЛЮДИ 4 · ТАЯНИЕ 0.7+0.06·ЛЮДИ/с · ШТОРМ ×2.5 на 10с "
                "(каждые 50–70с) · МАНА +8/с · ЗАРЯД −3 маны → +2.5% льда · СЕТЬ +6 рыбы (0.4с) · "
                "УБЫЛЬ РЫБЫ −0.3·ЛЮДИ/с · РОЖДЕНИЕ: РЫБА ≥25 (каждые 6с, −15) · ГОЛОД 3с · ПРЕДЕЛ 12 · "
                "СЧЁТ = ВРЕМЯ×10 + ЛЮДИ×50")


def draw_techpass(c, y, pal):
    dark = pal[5]
    c.setFillColor(dark)
    c.roundRect(30, y, W - 60, 20, 5, fill=1, stroke=0)
    c.setFont("DejaVu", 6.8)
    c.setFillColor("#FFFFFF")
    c.drawCentredString(W / 2, y + 6, TECHPASSPORT)


def draw_hero_section(c, label, text, y, pal, car_p):
    dark = pal[5]
    c.setFont("DejaVu-Bold", 7.6)
    c.setFillColor(pal[3])
    c.drawString(34, y, label)
    y -= 10
    im_w, im_h = 118, 128
    x_im = W - 30 - im_w
    c.setFillColor("white")
    c.roundRect(x_im, y - im_h, im_w, im_h, 8, fill=1, stroke=0)
    c.drawImage(car_p, x_im + 3, y - im_h + 3, im_w - 6, im_h - 6)
    c.setFont("DejaVu-Obl", 6.5)
    c.setFillColor(pal[5])
    c.drawCentredString(x_im + im_w / 2, y - im_h - 9, "шарж номера · серийный герой")
    c.setFont("DejaVu", 8.3)
    c.setFillColor(dark)
    lw = x_im - 34 - 16
    for ln in wrap(text, "DejaVu", 8.3, lw):
        c.drawString(34, y - 2, ln)
        y -= 11.1
    c.setFont("DejaVu-Bold", 6.6)
    c.setFillColor(pal[3])
    c.drawString(34, y - 2, "арку продолжит следующий выпуск ★")
    return y - 16


def _one(text, n):
    text = " ".join(text.split())
    return text[:n].rsplit(" ", 1)[0] + "…" if len(text) > n else text


def _mix(c1, c2, t):
    a, b = to_rgb(c1), to_rgb(c2)
    return to_hex([(1 - t) * x + t * y for x, y in zip(a, b)])


def _card(c, x, y, w, h, title, body, tcol, bcol, border, glass=False, fill=None):
    """Рубриковая карточка: подложка, заголовок-плашка, обёрнутый текст."""
    if glass:
        c.setFillColor("#17101f"); c.setStrokeColor(border)
    else:
        c.setFillColor(fill if fill else "#FFFFFF"); c.setStrokeColor(border)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    c.setFillColor(tcol)
    c.roundRect(x + 3, y + h - 18, w - 6, 15, 5, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 7); c.setFillColor("#FFFFFF")
    c.drawCentredString(x + w / 2, y + h - 14.5, title)
    c.setFont("DejaVu", 8.4); c.setFillColor(bcol)
    yy = y + h - 32
    for ln in wrap(body, "DejaVu", 8.4, w - 22):
        if yy < y + 8:
            break
        c.drawString(x + 11, yy, ln)
        yy -= 12.2


def rubric_page(c, jno, iss, issue, quote, hint, glass=False):
    """Вторая страница номера — лист рубрик: ПРОГНОЗ-инженерка, СКОВОРОДНИК, БАБАЙ, КАНЦЕЛЯРИЯ."""
    name, slug, slogan = JOURNALS[jno]
    sky1, sky2, sun, accent, mid, dark, chip = PAL[jno]
    if glass:
        base, bar, ink, frame_col = "#0f0b16", sun, sky2, sun
    else:
        base, bar, ink, frame_col = sky2, accent, dark, mid
    c.setFillColor(base); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(frame_col); c.setLineWidth(1.2); c.rect(16, 16, W - 32, H - 32, fill=0, stroke=1)
    # хедер
    c.setFillColor(bar)
    c.roundRect(30, H - 68, W - 60, 40, 8, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 13); c.setFillColor("#FFFFFF")
    c.drawCentredString(W / 2, H - 49, "«%s» · ЛИСТ РУБРИК" % name)
    c.setFont("DejaVu-Obl", 8); c.setFillColor(ink)
    c.drawCentredString(W / 2, H - 74, "№ %02d/10 · %s · вторая страница номера — как в настоящих газетах"
                     % (issue, iss.get("date", "")))
    # рубрики — плотная сетка 2x2 на всю высоту страницы
    eng_title, eng_body = ENGCALC[(issue - 1) % len(ENGCALC)]
    pan_kind, pan_text = PANS[(jno + issue) % len(PANS)]
    babai = BABAIS[(jno * 3 + issue) % len(BABAIS)]
    extra = EXTRA[(jno + issue * 2) % len(EXTRA)]
    blue, gold = mid, accent
    top1, gap, rowh = H - 150, 16, 210
    xl, xr, cw = 34, 310, 262
    if glass:
        f1 = f2 = None
    else:
        f1 = _mix(base, accent, 0.10)
        f2 = _mix(base, mid, 0.10)
    _card(c, xl, top1 - rowh, cw, rowh, "ПРОГНОЗ · ИНЖЕНЕРНЫЕ ВЫКЛАДКИ",
          "Расчёт — " + eng_title + ". " + eng_body +
          " Цифры проверены редакцией и съедены в виде омлета по-ледянски. "
          "Любой показатель можно пересчитать: калькулятор прилагается к чаю.",
          blue, ink, frame_col, glass, fill=f1)
    _card(c, xr, top1 - rowh, cw, rowh, "СКОВОРОДНИК · %s" % pan_kind,
          pan_text + " На полях зарисовка: сковорода — тоже судьба. "
          "Инструкция к ней: жарить с уважением к льду, переворачивать на закате, "
          "мыть талой водой и не давать Бабаю.",
          gold, ink, frame_col, glass, fill=f2)
    bot = top1 - gap - rowh
    _card(c, xl, bot, cw, rowh, "БАБАЙ · НАБЛЮДЕНИЯ",
          babai + " Записано дежурным по лагерю, подписано неразборчиво, "
          "перечитано вслух при свече изо льда. Свидетелей было трое: все считают иначе. "
          "В архив сдан оригинал, в киоск — иллюстрация.",
          gold, ink, frame_col, glass, fill=f2)
    _card(c, xr, bot, cw, rowh, "КАНЦЕЛЯРИЯ · ПРОЧЕЕ",
          extra + " Учётная строка: «" + _one(iss.get("refl", ""), 96) + "». "
          "Второй экземпляр сдан в архив Вечерки; третий — засушен между страницами 120-го номера.",
          blue, ink, frame_col, glass, fill=f1)
    # широкая нижняя полоса с тайной строкой
    c.setFillColor(bar)
    c.roundRect(30, 226, W - 60, 46, 8, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 8); c.setFillColor("#FFFFFF")
    c.drawCentredString(W / 2, 258, "★ ПАМЯТЬ НОМЕРА ★")
    c.setFont("DejaVu-Obl", 8.5); c.setFillColor("#FFFFFF")
    c.drawCentredString(W / 2, 240, "……" + hint + "……")
    # техпаспорт
    draw_techpass(c, 176, tuple(PAL[jno]))
    c.setFont("DejaVu-Obl", 7.5); c.setFillColor(ink)
    c.drawCentredString(W / 2, 146, "серия «%s» · № %02d/10 · лист 2/2 · иллюстрации — полиарт" % (name, issue))
    # орнамент внизу + подвал
    c.setFillColor(frame_col)
    c.roundRect(34, 60, W - 68, 30, 5, fill=1, stroke=0)
    c.setFont("DejaVu", 6.6); c.setFillColor("#FFFFFF")
    c.drawCentredString(W / 2, 74, "© Ледяная Вечерка · все выпуски живут по своим датам · сковородка печатается по понедельникам")


def build_pdf(jno, issues):
    """Смелая афиша номера: большая обложка, чипы-сводки, крупный график. Минимум текста."""
    name, slug, slogan = JOURNALS[jno]
    if jno >= 13:
        return build_golden_pdf(jno, issues)
    if jno >= 11:
        return build_glossy_pdf(jno, issues)
    sky1, sky2, sun, accent, mid, dark, chip = PAL[jno]
    path = os.path.join(OUT, "journal-%02d-%s-01-10.pdf" % (jno, slug))
    c = rlcanvas.Canvas(path, pagesize=A4)
    for idx, iss in enumerate(issues):
        issue = idx + 1
        chart_p = chart(jno, issue)
        cover_p = os.path.join(BASE, "covers", "j%02d-issue-%02d.png" % (jno, issue))
        if not os.path.exists(cover_p):
            cover_p = banner(jno)
        quote, hint = epigraph(jno)
        # фон: двусоставный цвет
        c.setFillColor(sky2); c.rect(0, H / 2, W, H / 2, fill=1, stroke=0)
        c.setFillColor(sky1); c.rect(0, 0, W, H / 2, fill=1, stroke=0)
        # лёгкий орнамент-снег
        import random
        rnd = random.Random(jno * 100 + issue)
        c.setFillColor("#FFFFFF")
        for _ in range(40):
            c.circle(rnd.randint(20, int(W) - 20), rnd.randint(30, int(H) - 90), 1.2 + rnd.random() * 1.2, fill=1, stroke=0)
        # мастхэд (полоса с названием и слоганом)
        c.setFillColor(accent)
        c.roundRect(30, H - 84, W - 60, 56, 8, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 16); c.setFillColor("#FFFFFF")
        c.drawCentredString(W / 2, H - 52, "«%s»" % name)
        c.setFont("DejaVu-Obl", 8.5); c.setFillColor(sky2)
        c.drawCentredString(W / 2, H - 70, slogan)
        # дата — плашка под мастхэдом
        c.setFillColor(mid)
        c.roundRect(30, H - 134, W - 60, 20, 5, fill=1, stroke=0)
        c.setFont("DejaVu", 9); c.setFillColor("#FFFFFF")
        c.drawCentredString(W / 2, H - 128, iss.get("date", "") + " · № %02d/10" % issue)
        # заголовок-плакат (без наложения на дату и обложку)
        c.setFillColor(dark)
        c.roundRect(30, 668, W - 60, 36, 7, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 15); c.setFillColor(sky2)
        c.drawString(46, 679, "№ %02d · " % issue)
        c.drawString(122, 679, _one(iss.get("title", ""), 40))
        # ОБЛОЖКА — главный герой страницы
        c.setFillColor("white")
        c.roundRect(66, 296, W - 132, 404, 12, fill=1, stroke=0)
        c.drawImage(cover_p, 70, 300, W - 140, 396, preserveAspectRatio=True, anchor="c")
        # чипы-сводки (море в одну строку)
        takes = [
            ("СКАЗ", _one(iss.get("refl", ""), 72)),
            ("ПРОГНОЗ", _one(iss.get("forecast", ""), 72)),
            ("ПРИЁМ", _one(iss.get("tip", ""), 72)),
            ("ПАРАЛЛЕЛЬ", _one(iss.get("other", ""), 72)),
            ("КОНКУРС", _one(iss.get("contest", ""), 72)),
        ]
        for i, (lab, txt) in enumerate(takes):
            bx = 30 + i * 108
            c.setFillColor("white")
            c.roundRect(bx, 216, 102, 76, 7, fill=1, stroke=0)
            c.setFillColor(accent)
            c.roundRect(bx, 282, 102, 14, 5, fill=1, stroke=0)
            c.setFont("DejaVu-Bold", 6.5); c.setFillColor("#FFFFFF")
            c.drawCentredString(bx + 51, 287, "◆ " + lab)
            c.setFillColor(dark)
            c.setFont("DejaVu", 7)
            for j, ln in enumerate(wrap(txt, "DejaVu", 7, 94)[:3]):
                c.drawString(bx + 5, 272 - j * 9, ln)
        # крупный график симуляции
        c.setFillColor("white")
        c.roundRect(30, 96, W - 60, 112, 8, fill=1, stroke=0)
        c.drawImage(chart_p, 36, 100, W - 72, 104)
        # тайная строка
        c.setFont("DejaVu-Obl", 7.5); c.setFillColor(dark)
        c.drawCentredString(W / 2, 84, "…%s…" % hint)
        # техпаспорт
        draw_techpass(c, 56, tuple(PAL[jno]))
        # подвал
        c.setFillColor(accent)
        c.roundRect(30, 28, W - 60, 22, 5, fill=1, stroke=0)
        c.setFont("DejaVu", 7); c.setFillColor("#FFFFFF")
        c.drawCentredString(W / 2, 34, "серия «%s» · книга «%s» · герой: %s …" %
                            (name, quote[:60], _one(iss.get("hero", ""), 90)))
        c.showPage()
        rubric_page(c, jno, iss, issue, quote, hint, glass=False)
        c.showPage()
    c.save()
    return path


def build_glossy_pdf(jno, issues):
    """Глянцевый журнал «в стиле мода»: тёмная мистика, золото, крупные цитаты из статей."""
    name, slug, slogan = JOURNALS[jno]
    sky1, sky2, sun, accent, mid, dark, chip = PAL[jno]
    path = os.path.join(OUT, "journal-%02d-%s-01-10-glossy.pdf" % (jno, slug))
    c = rlcanvas.Canvas(path, pagesize=A4)
    d0, d1 = "#0d0a12", "#1c1427"
    for idx, iss in enumerate(issues):
        issue = idx + 1
        car_p = caricature(jno, issue, iss.get("hero", ""))
        quote, hint = epigraph(jno)
        # тёмный фон
        c.setFillColor(d0); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(d1); c.rect(0, H / 2, W, H / 2, fill=1, stroke=0)
        # золотая рамка
        c.setStrokeColor(sun); c.setLineWidth(1.4); c.rect(14, 14, W - 28, H - 28, fill=0, stroke=1)
        c.setStrokeColor(sun); c.setLineWidth(0.5); c.rect(19, 19, W - 38, H - 38, fill=0, stroke=1)
        # мастхэд
        c.setFillColor(sun)
        c.roundRect(30, H - 72, W - 60, 36, 6, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 15); c.setFillColor(d0)
        c.drawCentredString(W / 2, H - 62, "«%s»" % name)
        c.setFont("DejaVu-Obl", 9); c.setFillColor(sky2)
        c.drawCentredString(W / 2, H - 80, slogan + " · глянец Севера")
        # дата
        c.setFillColor(accent)
        c.roundRect(30, H - 102, W - 60, 22, 5, fill=1, stroke=0)
        c.setFont("DejaVu", 9); c.setFillColor(sky2)
        c.drawCentredString(W / 2, H - 96, "№ %02d/10 · %s · из будущего, которое станет историей" % (issue, iss.get("date", "")))
        # шарж-витрина слева
        c.drawImage(car_p, 40, 480, 260, 300)
        c.setFont("DejaVu-Obl", 8.5); c.setFillColor(sun)
        c.drawCentredString(170, 468, "герой номера · из статей будущего")
        # заголовок номера справа
        c.setFillColor(sky2)
        c.setFont("DejaVu-Bold", 20)
        for j, ln in enumerate(wrap(iss.get("title", ""), "DejaVu-Bold", 20, W - 370)):
            c.drawString(W - 340, H - 210 - j * 26, ln)
        # эпиграф из статей — «вода»
        c.setFillColor(sky1)
        c.setFont("DejaVu-Obl", 10.5)
        qy = H - 300
        for ln in wrap(quote, "DejaVu-Obl", 10.5, W - 370):
            c.drawString(W - 340, qy, ln)
            qy -= 15
        # секции в две колонки
        sect_lines = [
            ("размышление", iss.get("refl", "")),
            ("прогноз", iss.get("forecast", "")),
            ("приём", iss.get("tip", "")),
            ("параллель", iss.get("other", "")),
            ("конкурс", iss.get("contest", "")),
            ("судьбы", iss.get("hero", "")),
        ]
        cols = [(40, 280), (W - 330, 250)]
        col_y = {"left": 430, "right": 430}
        for i, (lab, txt) in enumerate(sect_lines):
            cx, lw = cols[i % 2]
            yy = col_y["left" if i % 2 == 0 else "right"]
            c.setFillColor(sun)
            c.setFont("DejaVu-Bold", 8)
            c.drawString(cx, yy, "◊ " + lab.upper())
            c.setStrokeColor(sun); c.setLineWidth(0.6)
            c.line(cx - 4, yy - 4, cx + lw + 4, yy - 4)
            yy -= 13
            c.setFillColor(sky1)
            c.setFont("DejaVu", 7.6)
            for ln in wrap(txt, "DejaVu", 7.6, lw):
                c.drawString(cx, yy, ln)
                yy -= 10.5
            col_y["left" if i % 2 == 0 else "right"] = yy - 14
        # тайная строка
        c.setFillColor(sky2)
        c.setFont("DejaVu-Obl", 9)
        c.drawCentredString(W / 2, 210, "……" + hint + "……")
        # техпаспорт
        draw_techpass(c, 168, tuple(PAL[jno]))
        # подвал
        c.setFillColor(sun)
        c.roundRect(30, 40, W - 60, 24, 5, fill=1, stroke=0)
        c.setFont("DejaVu", 7); c.setFillColor(d0)
        c.drawCentredString(W / 2, 49, TECHPASSPORT[:180])
        c.setFont("DejaVu-Obl", 7); c.setFillColor(sky1)
        c.drawCentredString(W / 2, 30, "глянцевый журнал о будущем игры «Ледяные человечки» · всё по статьям «Ледяной Вечерки»")
        c.showPage()
        rubric_page(c, jno, iss, issue, quote, hint, glass=True)
        c.showPage()
    c.save()
    return path


def build_golden_pdf(jno, issues):
    """ЗОЛОТОЙ ЖУРНАЛ: по 3 листа на номер — афиша, события, закулисье."""
    name, slug, slogan = JOURNALS[jno]
    sky1, sky2, sun, accent, mid, dark, chip = PAL[jno]
    path = os.path.join(OUT, "journal-%02d-%s-01-10-golden.pdf" % (jno, slug))
    c = rlcanvas.Canvas(path, pagesize=A4)
    d0, d1 = "#241a0e", "#3a2e1e"
    for idx, iss in enumerate(issues):
        issue = idx + 1
        gd = GOLD.get(issue, {})
        quote, hint = epigraph(jno)
        car_p = caricature(jno, issue, iss.get("hero", ""))
        cover_p = os.path.join(BASE, "covers", "j%02d-issue-%02d.png" % (jno, issue))
        if not os.path.exists(cover_p):
            cover_p = banner(jno)
        events = iss.get("events") or [""] * 6
        # ─────────────── ЛИСТ 1 · АФИША ───────────────
        c.setFillColor(d0); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(d1); c.rect(0, H / 2, W, H / 2, fill=1, stroke=0)
        c.setStrokeColor(sun); c.setLineWidth(1.6); c.rect(12, 12, W - 24, H - 24, fill=0, stroke=1)
        c.setStrokeColor(sun); c.setLineWidth(0.6); c.rect(18, 18, W - 36, H - 36, fill=0, stroke=1)
        import random
        rnd = random.Random(jno * 100 + issue)
        c.setFillColor(sun)
        for _ in range(26):
            c.circle(rnd.randint(30, int(W) - 30), rnd.randint(30, int(H) - 30), 1.0 + rnd.random(), fill=1, stroke=0)
        # мастхэд
        c.setFillColor(sun)
        c.roundRect(30, H - 78, W - 60, 40, 7, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 17); c.setFillColor(d0)
        c.drawCentredString(W / 2, H - 68, "«%s»" % name)
        c.setFont("DejaVu-Obl", 9); c.setFillColor(sky2)
        c.drawCentredString(W / 2, H - 86, slogan)
        # дата
        c.setFillColor(accent)
        c.roundRect(30, H - 124, W - 60, 26, 5, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 10); c.setFillColor(sky2)
        c.drawCentredString(W / 2, H - 116, "№ %02d/10 · %s · золотой выпуск года" % (issue, iss.get("date", "")))
        # тема — плакат
        c.setFillColor(dark)
        c.roundRect(30, H - 170, W - 60, 34, 7, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 15); c.setFillColor(sky2)
        c.drawString(48, H - 160, _one(iss.get("title", ""), 46))
        # обложка слева
        c.setFillColor("white")
        c.roundRect(40, 268, 268, 360, 10, fill=1, stroke=0)
        c.drawImage(cover_p, 44, 272, 260, 352, preserveAspectRatio=True, anchor="c")
        c.setFillColor(sun)
        c.setFont("DejaVu-Bold", 8)
        c.drawCentredString(174, 258, "обложка серии «%s» · полиарт-φ" % name)
        # главное событие справа
        xr0, xr1 = 326, W - 34
        cw = xr1 - xr0
        c.setFillColor(sun)
        c.roundRect(xr0, 638, cw, 30, 6, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 10); c.setFillColor(d0)
        c.drawCentredString((xr0 + xr1) / 2, 648, "★ ГЛАВНОЕ СОБЫТИЕ ★")
        yy = 622
        me = iss.get("main_event", "")
        c.setFont("DejaVu-Bold", 9.5); c.setFillColor(sky1)
        for ln in wrap(me, "DejaVu-Bold", 9.5, cw - 14):
            c.drawString(xr0 + 7, yy, ln); yy -= 13.5
        yy -= 12
        c.setStrokeColor(sun); c.setLineWidth(0.6); c.line(xr0, yy, xr1, yy); yy -= 8
        # события месяца — нумерованный список
        for k, ev in enumerate(events[:6]):
            if not ev:
                continue
            c.setFont("DejaVu-Bold", 9); c.setFillColor(sun)
            c.drawString(xr0, yy, "◆ %d" % (k + 1))
            c.setFont("DejaVu", 8.4); c.setFillColor(sky2)
            for j, ln in enumerate(wrap(ev, "DejaVu", 8.4, cw - 44)):
                if j == 0:
                    yy2 = yy
                else:
                    yy2 = yy - j * 11.5
                c.drawString(xr0 + 44, yy2, ln)
            rows = max(1, len(wrap(ev, "DejaVu", 8.4, cw - 44)))
            yy -= rows * 11.5 + 7
            if yy < 300:
                break
        c.setFont("DejaVu-Obl", 8); c.setFillColor(sky2)
        c.drawCentredString((xr0 + xr1) / 2, 282, "шесть происшествий месяца — все произошли ровно в эти даты")
        # график симуляции
        chart_p = chart(jno, issue)
        c.setFillColor("white")
        c.roundRect(30, 106, W - 60, 92, 8, fill=1, stroke=0)
        c.drawImage(chart_p, 36, 110, W - 72, 84)
        c.setFont("DejaVu-Obl", 7.5); c.setFillColor(sun)
        c.drawCentredString(W / 2, 94, "...%s..." % hint)
        draw_techpass(c, 62, tuple(PAL[jno]))
        c.setFillColor(sun)
        c.roundRect(30, 30, W - 60, 24, 5, fill=1, stroke=0)
        c.setFont("DejaVu", 7); c.setFillColor(d0)
        c.drawCentredString(W / 2, 38, "серия «%s» · номер %02d/10 · герой: %s …" %
                            (name, issue, _one(iss.get("hero", ""), 88)))
        c.showPage()

        # ─────────────── ЛИСТ 2 · СОБЫТИЯ ───────────────
        c.setFillColor(sky2); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setStrokeColor(sun); c.setLineWidth(1.2); c.rect(16, 16, W - 32, H - 32, fill=0, stroke=1)
        c.setFillColor(sun)
        c.roundRect(30, H - 68, W - 60, 40, 8, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 13); c.setFillColor(d0)
        c.drawCentredString(W / 2, H - 49, "«%s» · ЛИСТ СОБЫТИЙ" % name)
        c.setFont("DejaVu", 8); c.setFillColor(dark)
        c.drawCentredString(W / 2, H - 74, "№ %02d/10 · %s · лента Золотого года" % (issue, iss.get("date", "")))
        # лента-график
        tl_p = gold_timeline(jno, issue)
        c.setFillColor("white")
        c.roundRect(30, H - 270, W - 60, 150, 8, fill=1, stroke=0)
        c.drawImage(tl_p, 40, H - 266, W - 80, 142)
        # карточки событий 2×3 (между лентой и памятным блоком — без наложений)
        top1, gap, rowh = 444, 8, 112
        xl, xr, cw2 = 34, 320, 250
        f1 = _mix(sky2, sun, 0.10)
        f2 = _mix(sky2, mid, 0.10)
        for k in range(6):
            ev = events[k] if k < len(events) else ""
            col_i, row_i = k % 2, k // 2
            x = xl if col_i == 0 else xr
            y = top1 - row_i * (rowh + gap)
            if y < 160:
                continue
            _card(c, x, y, cw2, rowh, "СОБЫТИЕ %d" % (k + 1), ev,
                  tcol=dark, bcol=dark, border=sun, glass=False, fill=(f1 if col_i == 0 else f2))
        # память номера
        c.setFillColor(sun)
        c.roundRect(30, 150, W - 60, 44, 8, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 8); c.setFillColor(d0)
        c.drawCentredString(W / 2, 174, "★ ПАМЯТЬ ЗОЛОТОГО НОМЕРА ★")
        c.setFont("DejaVu-Obl", 8.5); c.setFillColor(d0)
        c.drawCentredString(W / 2, 158, "……%s……" % hint)
        draw_techpass(c, 116, tuple(PAL[jno]))
        c.setFont("DejaVu-Obl", 8); c.setFillColor(dark)
        c.drawCentredString(W / 2, 96, "серия «%s» · № %02d/10 · лист 2/3 · события месяца стали историей"
                         % (name, issue))
        c.setStrokeColor(sun); c.setLineWidth(0.6)
        c.roundRect(34, 60, W - 68, 28, 5, fill=1, stroke=0)
        c.setFont("DejaVu", 6.8); c.setFillColor(d0)
        c.drawCentredString(W / 2, 71, "© Ледяная Вечерка · события живут по своим датам · следующее происшествие — в течение 50–70 секунд")
        c.showPage()

        # ─────────────── ЛИСТ 3 · ЗАКУЛИСЬЕ ───────────────
        c.setFillColor(sky2); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setStrokeColor(sun); c.setLineWidth(1.2); c.rect(16, 16, W - 32, H - 32, fill=0, stroke=1)
        c.setFillColor(dark)
        c.roundRect(30, H - 68, W - 60, 40, 8, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 13); c.setFillColor(sun)
        c.drawCentredString(W / 2, H - 49, "«%s» · ЗАКУЛИСЬЕ ЗОЛОТОГО НОМЕРА" % name)
        c.setFont("DejaVu", 8); c.setFillColor(dark)
        c.drawCentredString(W / 2, H - 74, "№ %02d/10 · %s · что осталось за афишей" % (issue, iss.get("date", "")))
        # премия номера
        pri = gd.get("prize", "Золотая премия номера")
        c.setFillColor(sun)
        c.roundRect(30, H - 160, W - 60, 34, 7, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 12); c.setFillColor(d0)
        c.drawCentredString(W / 2, H - 150, "🏆 ПРЕМИЯ НОМЕРА · %s 🏆" % pri)
        # интервью
        it = gd.get("interview")
        x0 = 34
        cw3 = W - 68
        f1p = _mix(sky2, sun, 0.10)
        f2p = _mix(sky2, mid, 0.10)
        _card(c, 30, H - 330, cw3, 168, "ИНТЕРВЬЮ · %s" % (it[0] if it else "беседа"), "",
              tcol=dark, bcol=dark, border=sun, glass=False, fill=f1p)
        yi = H - 196
        c.setFont("DejaVu-Bold", 8.2); c.setFillColor(dark)
        for ln in wrap("— " + it[1], "DejaVu-Bold", 8.2, cw3 - 24):
            if yi < H - 318:
                break
            c.drawString(x0 + 12, yi, ln); yi -= 11.8
        yi -= 5
        c.setFont("DejaVu-Obl", 8.2); c.setFillColor(mid)
        for ln in wrap("«" + it[2] + "»", "DejaVu-Obl", 8.2, cw3 - 24):
            if yi < H - 318:
                break
            c.drawString(x0 + 12, yi, ln); yi -= 11.8
        # рецепт золотой сковороды
        _card(c, 30, H - 500, cw3, 168, "ЗОЛОТАЯ СКОВОРОДА · рецепт", "", tcol=dark, bcol=dark,
              border=sun, glass=False, fill=f2p)
        yr = H - 372
        c.setFont("DejaVu", 8.2); c.setFillColor(dark)
        for ln in wrap(gd.get("recipe", "…"), "DejaVu", 8.2, cw3 - 24):
            if yr < H - 490:
                break
            c.drawString(x0 + 12, yr, ln); yr -= 11.8
        # пятёрка года
        rating = gd.get("rating", [])
        c.setFillColor("white")
        c.roundRect(30, H - 640, cw3 - 190, 110, 8, fill=1, stroke=0)
        c.setFillColor(sun)
        c.roundRect(30, H - 640, cw3 - 190, 22, 6, fill=1, stroke=0)
        c.setFont("DejaVu-Bold", 8.5); c.setFillColor(d0)
        c.drawCentredString(30 + (cw3 - 190) / 2, H - 632, "★ ПЯТЁРКА ЗОЛОТОГО ГОДА ★")
        rr = H - 556
        c.setFont("DejaVu-Obl", 7.8); c.setFillColor(dark)
        for line in rating[:5]:
            if rr < H - 636:
                break
            c.drawCentredString(30 + (cw3 - 190) / 2, rr, line); rr -= 15.5
        # шарж героя справа
        c.setFillColor("white")
        c.roundRect(W - 196, H - 640, 166, 110, 8, fill=1, stroke=0)
        c.drawImage(car_p, W - 191, H - 634, 156, 98, preserveAspectRatio=True, anchor="c")
        c.setFont("DejaVu-Obl", 7); c.setFillColor(dark)
        c.drawCentredString(W - 113, H - 650, "герой номера")
        # письмо редактора
        c.setFont("DejaVu-Obl", 8); c.setFillColor(dark)
        c.drawCentredString(W / 2, H - 668, "Письмо редактора: «Золотой год — это год, который читает сам себя».")
        draw_techpass(c, H - 700, tuple(PAL[jno]))
        c.setFont("DejaVu-Obl", 8); c.setFillColor(dark)
        c.drawCentredString(W / 2, H - 712, "серия «%s» · № %02d/10 · лист 3/3 · закулисье печатается после афиши и событий"
                         % (name, issue))
        c.setFillColor(sun)
        c.roundRect(34, 40, W - 68, 26, 5, fill=1, stroke=0)
        c.setFillColor(sun)
        c.setFont("DejaVu", 6.8); c.setFillColor(d0)
        c.drawCentredString(W / 2, 50, "© Ледяная Вечерка · премия, рецепт и пятёрка года — только в Золотом журнале")
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