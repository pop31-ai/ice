# -*- coding: utf-8 -*-
"""«ПРОЕКТНАЯ РАБОТА» — 15-е издание Пресс-Центра Ледяной Вечерки.

Один выпуск, 30 листов A4: научно-проектный разбор репозитория github.com/pop31-ai/ice.
рассказ о структуре git, подходах к разработке и о том, что «по науке»:
фиксированные сиды, воспроизводимость, статистика из файлов, жанры иллюстраций.
В центре работы — проектируемый модуль «Айс-генератор айсбергов» (силуэты из шума,
экспорт JSON, загрузка в игру) — как этап плана разработки.

Стиль — «проектная работа»: титул, паспорт, содержание, разделы, приложения,
схемы-тротоблоки и узел вывода на каждом листе. Все числа из реальных файлов.
"""
import os
import glob

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics

import gen_pdf_journals as G  # PAL, JOURNALS, OUT, IMG, DejaVu-шрифты

W, H = A4
OUT = G.OUT
IMG = G.IMG
PDF = os.path.join(OUT, "proektnaya-rabota.pdf")

TOTAL = 30

plt.rcParams["font.family"] = "DejaVu Sans"
SKY, SUN, MID, DARK, CHIP = "#bfe8ff", "#FFC300", "#39A9DB", "#0E4D7A", "#EAF6FF"


def _fig():
    fig = plt.figure(figsize=(7.0, 9.0), dpi=120)
    fig.patch.set_facecolor("white")
    return fig


def _bg(ax):
    ax.set_facecolor("white")
    ax.grid(True, color="#c3d2df", lw=0.6, alpha=0.7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def _node(ax, x, y, w, h, text, fc=DARK, tc="white", fs=8, ec="none", lw=0):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=3, alpha=0.97))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, zorder=4)


def _wire(ax, p1, p2, color=CHIP, lw=1.2, ls="-"):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, ls=ls, zorder=2)


# ---------------------------------------------------------------- схемы
def render_tree(path):
    """Структура репозитория — как он устроен в git (папки и ядро файлов)."""
    fig = _fig(); ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    _node(ax, 40, 93, 20, 6, "ice/  (.git · master)", fc=DARK, fs=10)
    dirs = [
        (92, "index.html  — игра-одиночка", "игра · движок · летопись"),
        (86, "журналы-витрины: press-center, kiosk, wiki-ice, heroes, fun, epochs, polyart, situations, games", "9 HTML-витрин из файлов"),
        (80, "articles/  — 50 статей-анализов", "аналитика шедевра 01…50"),
        (74, "articles/future/ — 50 номеров Вечерки", "будущее эпох 001…050"),
        (68, "journals/  — 130 выпусков-полос", "2026-01 … 2028-07, 13 серий"),
        (62, "journals_pdf/ — 15 PDF на 500 страниц", "13 серий + Айс-График + Проектная"),
        (56, "covers/  — 130 обложек PNG", "j01-issue-01 … j13-issue-10"),
        (50, "situations/ — 78 зарисовок полиарт", "событие = картина"),
        (44, "gen_*.py — 16 генераторов", "python gen_*.py → контент"),
        (38, "ice_lore.py · README.md · .gitignore", "лор, пересборка, мана-газетка"),
    ]
    for y, a, b in dirs:
        _node(ax, 4, y, 92, 4.4, a + "  (" + b + ")", fc="#16324f", tc="#eaf6ff", fs=7)
    _wire(ax, (50, 93), (50, 90.8))
    _wire(ax, (50, 90), (12, 87.2)); _wire(ax, (50, 90), (88, 87.2))
    for y in (86, 80, 74, 68, 62, 56, 50, 44, 38):
        _wire(ax, (6, y + 4.4), (6, y + 4.4))
    fig.savefig(path, dpi=120); plt.close(fig)


def render_gitlog(path):
    """История коммитов — 16 шагов от прототипа до издательства."""
    fig = _fig(); ax = fig.add_axes([0.06, 0.06, 0.88, 0.86], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    log = [
        ("d350d53", "прототип из папки Projects — игра-одиночка"),
        ("b99fd4c", "50 статей-анализов обощностя шедевра"),
        ("48997ff", "50 номеров «Ледяной Вечерки» из будущего + генератор"),
        ("6046023", "первые полосы по месяцам 2026–2027"),
        ("caa1fde", "10 цветных журналов-газет ×10 выпусков"),
        ("1ac5f3e", "из-под капота + глянец: шаржи, датчики, техпаспорт"),
        ("bd5cb16", "Больше, чем Forbes: киоск, энциклопедия, Бабай"),
        ("7dc9d72", "имена, летопись лагеря, хроника эпохи, досье"),
        ("6bbf9bb", "полиарт-φ для обложек; галерея стиля"),
        ("b4dd603", "Ситуация — иллюстрация: 72 зарисовки"),
        ("8654a75", "Золотой журнал — серия 13 (2027-10…2028-07)"),
        ("78a4ee8", "лор: статистика заметок, рейтинг бала, интервью года"),
        ("3cab00e", "листы рубрик: табло партии, шарж, афиша"),
        ("4d93008", "жанры: шарж (портрет) и карикатура (воспит.)"),
        ("7fa352c", "«Айс-График»: 10 томов × 20 страниц"),
    ]
    n = len(log); y0, y1 = 8, 96
    xs = np.linspace(y0, y1, n)
    for i, (h, msg) in enumerate(log):
        y = xs[i]
        _node(ax, 4, y - 2.2, 22, 4.4, h, fc=(DARK if i % 2 == 0 else MID), fs=8)
        ax.text(30, y - 0.5, msg, ha="left", va="center", fontsize=8.5, color=DARK)
        _node(ax, 0, y - 0.35, 3, 0.7, "", fc=SUN, fs=6)
        if i:
            ax.plot([1, 3], [xs[i - 1], y - 0.35], color=CHIP, lw=0.8)
    ax.text(50, 99, "master → main line · 16 атомарных коммитов", ha="center",
            fontsize=10, fontweight="bold", color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_formulas(path):
    """Движок по науке: формулы и константы игры (из index.html)."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    cells = [
        (4, 86, "ТАЯНИЕ", "d(ice)/dt = 0.7 + 0.06·люди  %/с\nрастёт вместе с племенем", MID),
        (36, 86, "ШТОРМ", "каждые 50–70 с буря ×2.5\nтаяние на 10 секунд", "#C0392B"),
        (4, 58, "ЗАРЯД", "клик по льду: мана −3 →\nлёд +2.5%; мана +8/с (≤100)", SUN, DARK),
        (36, 58, "СЕТЬ", "клик по воде: +6 рыбы,\nкулдаун 0.4 с; убыль −0.3·люди/с", "#148F77"),
        (4, 30, "РОЖДЕНИЕ", "рыба ≥25 → +1 человек (−15),\nраз в 6 с; голод 3 с → −1", "#8E44AD"),
        (36, 30, "СЧЁТ", "очки = время×10 + люди×50,\nпредел племени — 12", DARK),
    ]
    for x, y, t, f, col, *rest in cells:
        fc = col
        tc = "white" if col not in (SUN,) else "#0d1b2a"
        _node(ax, x, y, 30, 12, "", fc=SKY, ec=DARK, lw=0.6)
        ax.text(x + 15, y + 8.6, t, ha="center", va="center", fontsize=10,
                fontweight="bold", color=DARK)
        ax.text(x + 15, y + 4.6, f, ha="center", va="center", fontsize=7.6, color="#0d1b2a")
    _node(ax, 74, 14, 22, 30, "ОДИН ФАЙЛ\n\ncanvas 900×600\nrequestAnimationFrame\nлюди с именами\nлетопись · рекорд\nlocalStorage",
          fc=DARK, tc="#eaf6ff", fs=9)
    ax.text(50, 6, "Движок симулирует кадр за кадром; те же формулы — в 130 партиях журналов.",
            ha="center", fontsize=9, color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_pipeline(path):
    """Конвейер: генераторы py → контент → издательство."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    gens = [
        (94, "gen_journal_catalog.py", "130 полос · journals/2026-01…2028-07", MID),
        (76, "gen_pdf_journals.py", "13 журналов 270 листов + шаржи/карикатуры", MID),
        (58, "gen_ajs_grafik.py", "«Айс-График» 200 листов схем", MID),
        (40, "gen_project_work.py", "«Проектная работа» 30 листов · ЭТОТ ФАЙЛ", SUN, DARK),
        (22, "gen_covers/polyart/situations", "обложки, полиарт-φ, 78 зарисовок", MID),
    ]
    for i, (y, name, desc, col, *rest) in enumerate(gens):
        fc = col; tc = "white"
        if col == SUN:
            tc = "#0d1b2a"
        _node(ax, 4, y, 56, 12, name + "\n" + desc, fc=fc, tc=tc, fs=8)
    _node(ax, 76, 52, 20, 38, "p r e s s - c e n t e r\n\nвсе числа\nсчитаются\nfitz-ом из\nфайлов",
          fc=DARK, tc="#eaf6ff", fs=9)
    for y in (94, 76, 58, 40, 22):
        _wire(ax, (60, y + 6), (76, 82))
    ax.text(50, 6, "Определяет это: python gen_*.py → тот же контент, что видит читатель.",
            ha="center", fontsize=9, color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_icegen(path):
    """Айс-генератор: параметры → силуэт из шума → экспорт JSON → игра."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    def noise_curve(seed, n=200):
        rng = np.random.default_rng(seed)
        x = np.linspace(0, 10, n)
        base = 1.6 + 0.9 * np.exp(-((x - 5) / 2.4) ** 2)
        wob = 0.16 * np.sin(x * 3.1 + rng.uniform(0, 6)) + 0.1 * np.sin(x * 7.7 + rng.uniform(0, 6))
        y = base + wob * rng.uniform(0.6, 1.4)
        y[x < 1.2] += 0.4 + rng.uniform(0, 0.5)  # «парус» вершины
        return x, np.clip(y, 0.4, 4.4)
    x, y = noise_curve(3)
    ax.plot(x, y, color=DARK, lw=2.6, zorder=4)
    ax.fill(x, y, color="#bfe8ff", alpha=0.85, zorder=3)
    ax.fill(x, 0 * x, color="#0E4D7A", alpha=0.08)
    ax.plot(x, 0 * x, color=SKY, lw=1.5)
    ax.set_xlim(0, 10); ax.set_ylim(0, 5)
    for a in ("top", "right"):
        ax.spines[a].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    params = [("ширина", "w = base + ice·k"), ("пик", "полином 3 ст."), ("фаски", "купол-парус"),
              ("шум", "rng(seed)"), ("палитра", "лёд/снег/тень"), ("экспорт", "JSON {profile}")]
    for i, (k, v) in enumerate(params):
        ax.annotate(k + " — " + v, xy=(1.6 + i * 1.2, 4.7 - (i % 2) * 0.5),
                    fontsize=8, color=DARK, ha="center")
    ax.text(5, 4.95, "Силуэт айсберга: контур = базовый полином + шум (зависит от сида)",
            ha="center", fontsize=9, fontweight="bold", color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_volumes(path):
    """Объёмы архива: листы 15 изданий."""
    names = (["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
              "Гр", "Пр"])
    vals = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 30, 200, 30]
    colors = [G.PAL[i][3] for i in range(1, 14)] + ["#000000", "#FFC300"]
    fig = _fig(); ax = fig.add_axes([0.16, 0.12, 0.78, 0.74])
    x = np.arange(len(vals))
    ax.bar(x, vals, color=colors, alpha=0.92, zorder=3, edgecolor="white", linewidth=1)
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=8)
    ax.set_yticks([]); _bg(ax); ax.set_ylim(0, 260)
    for xi, v in zip(x, vals):
        ax.text(xi, v + 4, str(v), ha="center", va="bottom", fontsize=8, color="#0b1a2c")
    ax.text(7.5, 270, "страниц на ISSN · 13 журналов + Айс-График + Проектная",
            ha="center", fontsize=10, fontweight="bold", color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_stats(path):
    """По науке: статистика всё время из файлов — не устаревает."""
    fig = _fig(); ax = fig.add_axes([0.16, 0.12, 0.78, 0.74])
    lbl = ["журналы", "страницы", "статьи", "обложки", "зарисовки", "месяцы"]
    val = [15, 500, 100, 130, 78, 31]
    x = np.arange(len(lbl))
    ax.barh(x, val, color=MID, alpha=0.92, zorder=3, edgecolor="white", height=0.62)
    ax.set_yticks(x); ax.set_yticklabels(lbl, fontsize=10)
    ax.set_xticks([]); _bg(ax)
    for yi, v in zip(x, val):
        ax.text(v + 3, yi, str(v), va="center", fontsize=10, color=DARK)
    ax.set_xlim(0, 600)
    ax.text(300, -1.1, "Даже этот журнал считает страницы по файлу — fitz открывает PDF.",
            ha="center", fontsize=9, color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_filepic(path):
    """index.html изнутри: ядро одной страницы."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    _node(ax, 30, 88, 40, 9, "index.html — один файл", fc=DARK, fs=10)
    blocks = [
        (88, "canvas 900×600", "рисунок сцены и датчиков"),
        (74, "requestAnimationFrame", "кадр каждые 16 мс"),
        (60, "dims() = f(ice)", "ширина/высота айсберга"),
        (46, "клик по льду/воде", "заряд · сеть рыбы"),
        (32, "летопись · хроника", "имена, досье, рекорд"),
    ]
    for y, a, b in blocks:
        _node(ax, 8, y, 30, 10, a, fc=MID, fs=8.5)
        _node(ax, 44, y, 48, 10, b, fc="#16324f", tc="#eaf6ff", fs=8)
    _wire(ax, (38, 88), (38, 88 - 6))
    for y in (88, 74, 60, 46, 32):
        _wire(ax, (50, y + 5), (50, y + 5))
    _wire(ax, (50, 88), (50, 78))  # не используем слишком много проводов
    fig.savefig(path, dpi=120); plt.close(fig)


def render_seeds(path):
    """Подходы: сид → артефакт → воспроизводимость."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    for i in range(16):
        _node(ax, 3 + i * 6, 30, 4, 4, "", fc=(MID if i % 2 else DARK))
    ax.text(50, 44, "каждый артефакт — функция от сида:", ha="center", fontsize=10,
            fontweight="bold", color=DARK)
    ax.text(50, 20, "numpy.default_rng(seed) → шум → контур → картинка → тот же файл", ha="center",
            fontsize=9, color=DARK)
    _node(ax, 8, 62, 22, 14, "сиды\n13 серий × 10\n+ 30 листов", fc=DARK, tc="#eaf6ff", fs=8.5)
    _node(ax, 58, 62, 22, 14, "два прогона gen_*.py\nдают один MD5\n(проверено)", fc=MID, tc="white", fs=8.5)
    _node(ax, 34, 62, 20, 14, "артефакт\nPDF/PNG/TXT", fc=SUN, tc="#0d1b2a", fs=8.5)
    _wire(ax, (30, 69), (40, 69)); _wire(ax, (56, 69), (58, 69))
    fig.savefig(path, dpi=120); plt.close(fig)


def render_articles(path):
    """Тексты архива: 50 анализов + 50 Вечерки."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    _node(ax, 6, 40, 88, 16, "articles/ (50 анализов)  ·  articles/future/ (50 Вечерки)",
          fc=DARK, tc="#eaf6ff", fs=10)
    for i in range(50):
        _node(ax, 8 + i * 1.8, 70, 1.2, 6, "", fc=MID)
    for i in range(50):
        _node(ax, 8 + i * 1.8, 80, 1.2, 6, "", fc=SUN)
    ax.text(50, 62, "50 анализов шедевра", ha="center", fontsize=9, color=DARK, fontweight="bold")
    ax.text(50, 26, "50 номеров газеты из будущего (001…050)", ha="center", fontsize=9,
            color=DARK, fontweight="bold")
    ax.text(50, 12, "все тексты — utf-8/cp1251 подшивка; верхние номера — «Ледяная Вечерка»",
            ha="center", fontsize=8, color="#566573")
    fig.savefig(path, dpi=120); plt.close(fig)


def render_journals(path):
    """13 серий журналов: обычные, глянец, золотая."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    cols = [G.PAL[i][3] for i in range(1, 14)]
    _node(ax, 4, 58, 6, 30, "", fc="#999")
    for i in range(13):
        c = G.PAL[i + 1][3]
        w = 6
        x = 14 + i * 6.5
        h = 22 + (10 if i == 12 else 6)
        _node(ax, x, 84 - h / 2, w, h, str(i + 1), fc=c, tc="white", fs=10)
        _node(ax, x, 58, w, 2.4, "", fc=G.PAL[i + 1][5])
    ax.text(50, 50, "13 серий × 10 выпусков: обычные (1–12, 20 стр.) и Золотой (13, 30 стр.)",
            ha="center", fontsize=9, color=DARK)
    ax.text(50, 6, "палитра серии передаётся в журнал, обложку, шарж, график — одна константа",
            ha="center", fontsize=8, color="#566573")
    fig.savefig(path, dpi=120); plt.close(fig)


def render_vitr(path):
    """Сеть витрин press-center, считающих числа сами."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    _node(ax, 38, 84, 24, 9, "press-center.html", fc=MID, fs=10)
    vitr = ["kiosk", "wiki-ice", "heroes", "fun", "epochs", "polyart", "situations", "games"]
    for i, v in enumerate(vitr):
        x = 8 + (i % 4) * 23
        y = 34 - (i // 4) * 26
        _node(ax, x, y, 20, 8, v + ".html", fc="#16324f", tc="#eaf6ff", fs=8)
        _wire(ax, (50, 84), (x + 10, y + 8))
    ax.text(50, 8, "каждая витрина: len(glob(...)), fitz.open(pdf).page_count — без ручных цифр",
            ha="center", fontsize=8, color="#566573")
    fig.savefig(path, dpi=120); plt.close(fig)


def render_fantasy(path):
    """Фантазии футуролога: траектория к будущему."""
    fig = _fig(); ax = fig.add_axes([0.05, 0.05, 0.90, 0.90], frameon=False)
    ax.set_xlim(0, 120); ax.set_ylim(0, 100); ax.axis("off")
    rng = np.random.default_rng(11)
    x = np.linspace(0, 120, 60)
    y = 55 + 22 * np.sin(x / 9 + 1.3) + 6 * rng.uniform(0, 1, 60)
    ax.plot(x, y, color=DARK, lw=2)
    for i, (t, xp) in enumerate([
            ("Айс-генератор", 18), ("Полиарт-сезоны", 48), ("Шторм-карты", 74),
            ("Квантовая мана", 100)]):
        ax.scatter([xp], [55 + 22 * np.sin(xp / 9 + 1.3)], s=90, color=SUN, zorder=4)
        ax.text(xp, 55 + 22 * np.sin(xp / 9 + 1.3) + 6, t, ha="center", fontsize=9,
                color=DARK, fontweight="bold")
    ax.set_xlim(0, 120)
    ax.text(60, 12, "мечты честно отделены от плана: будущие разделы помечены «фантазия»",
            ha="center", fontsize=9, color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_plan(path):
    """План работ по Айс-генератору: 4 этапа к игре."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    steps = [
        ("1. icegen.html", "форма параметров\n+ canvas-предпросмотр"),
        ("2. экспорт", "JSON {profile, palette}\nкнопкой «сохранить»"),
        ("3. в игре", "index.html?ice=…\nпарсинг при старте"),
        ("4. партия серий", "13 айсбергов —\nпо одному на серию"),
    ]
    for i, (t, d) in enumerate(steps):
        x = 6 + i * 24.5
        _node(ax, x, 46, 20, 22, t + "\n\n" + d, fc=(SUN if i == 3 else MID),
              tc=("#0d1b2a" if i == 3 else "white"), fs=8)
        if i:
            _wire(ax, (x - 4, 57), (x + 2, 57))
    ax.text(50, 14, "приёмка: один и тот же URL даёт один и тот же айсберг",
            ha="center", fontsize=9, fontweight="bold", color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_json(path):
    """Формат обмена: JSON профиля айсберга."""
    fig = _fig(); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], frameon=False)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    lines = [
        '{ "profile": [',
        '    { "x": 0,   "y": 3.1 }, { "x": 12, "y": 2.8 },',
        '    { "x": 24,  "y": 3.9 }, { "x": 38, "y": 4.4 },   ← парус',
        '    … 96 точек контура …',
        '  ],',
        '  "palette": {',
        '    "snow": "#fff", "ice": "#9fd8ff",',
        '    "shade": "#1F6FB2", "sky": "#bfe8ff"',
        '  },',
        '  "seed": 7, "w": 260, "h": 84 }',
    ]
    y = 84
    for ln in lines:
        _node(ax, 8, y, 84, 9, ln, fc=("#eef4fb" if ln.startswith("  ") else "#dfe9f4"),
              tc="#0d1b2a", fs=9)
        y -= 10.5
    ax.text(50, 6, "игра берёт точки контура и рисует свой айсберг по профилю",
            ha="center", fontsize=9, color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


# ---------------------------------------------------------------- вёрстка
def _foot(c, num, sub="github.com/pop31-ai/ice"):
    c.setFillColor("#16324f")
    c.setFont("DejaVu", 8)
    c.drawString(34, 22, "ПРОЕКТНАЯ РАБОТА · «Ледяные человечки» · лист %02d/%02d" % (num, TOTAL))
    c.setFont("DejaVu-Obl", 8)
    c.drawRightString(W - 34, 22, sub)


def _head(c, num, title, sub):
    c.setFillColor("#0d1b2a")
    c.rect(0, H - 40, W, 40, fill=1, stroke=0)
    c.setFillColor(SUN)
    c.rect(0, H - 43, W, 3, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 13); c.setFillColor("#eaf6ff")
    c.drawString(30, H - 24, title)
    c.setFont("DejaVu-Obl", 8.5); c.setFillColor(SUN)
    c.drawRightString(W - 30, H - 24, sub)


def _text_block(c, x, y, w, lines, size=8.5, gap=5.5, col="#16324f"):
    c.setFillColor(col)
    c.setFont("DejaVu", size)
    for ln in lines:
        c.drawString(x, y, ln)
        y -= gap + size * 0.30
    return y


def _panel_block(c, path, y0, y1):
    c.setFillColor("#e9f2fa"); c.rect(28, y0, W - 56, y1 - y0, fill=1, stroke=0)
    c.setStrokeColor("#c3d2df"); c.setLineWidth(0.8); c.rect(28, y0, W - 56, y1 - y0, fill=0, stroke=1)
    c.drawImage(ImageReader(path), 34, y0 + 12, W - 68, y1 - y0 - 12, preserveAspectRatio=True, anchor="c")


def _concl(c, txt, y):
    c.setFillColor("#7d6608")
    c.setFont("DejaVu-Bold", 9)
    c.drawString(34, y, "УЗЕЛ ВЫВОДА · ")
    c.setFillColor("#0b1a2c")
    c.setFont("DejaVu", 8.5)
    c.drawString(34 + 88, y, txt)


# ---------------------------------------------------------------- страницы
def page_cover(c):
    c.setFillColor("#0d1b2a"); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(SUN); c.setLineWidth(1.6); c.rect(16, 16, W - 32, H - 32, fill=0, stroke=1)
    c.setStrokeColor(SUN); c.setLineWidth(0.4); c.rect(23, 23, W - 46, H - 46, fill=0, stroke=1)
    c.setFillColor(SUN)
    c.roundRect(60, H - 110, W - 120, 52, 10, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 22); c.setFillColor("#0d1b2a")
    c.drawCentredString(W / 2, H - 88, "ПРОЕКТНАЯ РАБОТА")
    c.setFont("DejaVu-Obl", 10); c.setFillColor("#eaf6ff")
    c.drawCentredString(W / 2, H - 128, "выпуск 01/01 · 30 листов · издательство «Ледяная Вечерка»")
    c.setFont("DejaVu-Bold", 15); c.setFillColor("#eaf6ff")
    c.drawCentredString(W / 2, H - 190, "«Ледяные человечки»:")
    c.drawCentredString(W / 2, H - 214, "игра, симулятор и издательство")
    c.drawCentredString(W / 2, H - 238, "в одном repo")
    img = os.path.join(IMG, "pw-icegen.png")
    render_icegen(img)
    _panel_block(c, img, 150, H - 420)
    c.setFont("DejaVu", 9); c.setFillColor("#eaf6ff")
    c.drawCentredString(W / 2, 136, "тема научно-проектная: структура git, подходы, «по науке»")
    c.setFont("DejaVu-Obl", 8.5); c.setFillColor(SUN)
    c.drawCentredString(W / 2, 108, "главный проектируемый модуль — «Айс-генератор айсбергов»")
    c.setFont("DejaVu", 8); c.setFillColor("#eaf6ff")
    c.drawCentredString(W / 2, 68, "github.com/pop31-ai/ice · Ледяная Вечерка · 2026")
    c.setFont("DejaVu-Obl", 7.5); c.setFillColor("#9fb8c7")
    c.drawCentredString(W / 2, 46, "силуэт на обложке — то, что будет создавать Айс-генератор айсбергов")
    c.showPage()


def page_passport(c):
    _head(c, 2, "ПАСПОРТ ПРОЕКТНОЙ РАБОТЫ", "раздел 00 · идентификация")
    img2 = os.path.join(IMG, "pw-stats.png"); render_stats(img2)
    y = H - 70
    rows = [
        ("Исполнитель", "издательство «Ледяная Вечерка», деревня у айсберга"),
        ("Продукт", "игра-одиночный файл index.html + Пресс-Центр (15 PDF, 500 листов)"),
        ("Репозиторий", "github.com/pop31-ai/ice · ветка master, remote-ориджин"),
        ("Жанр работы", "технико-гуманитарный метапроект: игра, симуляция, издательский конвейер"),
        ("Цель", "показать, как из одного файла рождается целое издательство"),
        ("Задачи", "движок · контент · генераторы · витрины · статистика из файлов"),
        ("Метод", "детерминированные сиды; все цифры считаются из артефактов (fitz)"),
        ("Этап в плане", "после Айс-Графика; в центре — Айс-генератор айсбергов"),
    ]
    c.setFont("DejaVu-Bold", 9); c.setFillColor(DARK)
    c.drawString(34, y, "ИДЕНТИФИКАЦИОННАЯ ТАБЛИЦА")
    y -= 20
    for k, v in rows:
        c.setFillColor("#16324f"); c.setFont("DejaVu-Bold", 8.5)
        c.drawString(34, y, "■  " + k)
        c.setFont("DejaVu", 8.5); c.setFillColor("#0b1a2c")
        c.drawString(150, y, v)
        y -= 18
    _panel_block(c, img2, 150, H - 62 - 9 * 18 - 20)
    y = 150 - 30
    _concl(c, "Объект изучения — не отдельная функция, а связка файл→сид→издание.", y)
    _foot(c, 2)
    c.showPage()


def page_toc(c):
    _head(c, 3, "СОДЕРЖАНИЕ", "что внутри выпуска")
    items = [
        (1, "Титул", "силуэт Айс-генератора"),
        (2, "00 · Паспорт", "таблица идентификации"),
        (4, "01 · Один файл", "index.html: canvas, движок, летопись"),
        (5, "02 · Движок по науке", "формулы и константы"),
        (6, "03 · История git", "16 атомарных коммитов"),
        (7, "04 · Структура repo", "дерево папок и ядра"),
        (8, "05 · Подходы", "сиды, воспроизводимость, статистика"),
        (9, "06 · Тексты", "100 статей: 50 анализов + 50 Вечерки"),
        (10, "07 · Журналы", "13 серий × 10; золотая серия"),
        (11, "08 · Иллюстрации", "жанры: шарж, карикатура, полиарт"),
        (12, "09 · Витрины", "9 HTML, считают сами"),
        (13, "10 · Конвейер", "python gen_*.py → издательство"),
        (14, "11 · АЙС-ГЕНЕРАТОР", "проект модуля: параметры"),
        (15, "11 · АЙС-ГЕНЕРАТОР", "алгоритм: силуэт из шума и JSON"),
        (16, "11 · АЙС-ГЕНЕРАТОР", "чтение в игре: index.html?ice=…"),
        (17, "11 · АЙС-ГЕНЕРАТОР", "план работ и приёмка"),
        (18, "12 · Объёмы", "страницы 15 изданий"),
        (19, "13 · По науке", "числа не устаревают"),
        (20, "14 · Фантазии футуролога", "штрихи к будущему"),
        (21, "15 · Риски", "шум, мана, фирменность"),
        (22, "16 · Результаты", "что получилось и как оценить"),
        (23, "17 · Выводы", "главное из работы"),
        (24, "18 · Заключение", "куда плывёт айсберг"),
        (25, "Приложение А", "словарь терминов"),
        (26, "Приложение Б", "палитры 13 серий"),
        (27, "Приложение В", "каталог 31 месяца"),
        (28, "Приложение Г", "мера партии (sim_stats)"),
        (29, "Приёмка", "контрольный лист"),
        (30, "Завершение", "печать и подписи"),
    ]
    y = H - 74
    for n, name, desc in items:
        c.setFillColor(DARK if n == 1 else MID)
        c.setFont("DejaVu-Bold", 8.5)
        c.drawString(34, y, "%02d" % n)
        c.setFillColor("#16324f"); c.setFont("DejaVu-Bold", 8.5)
        c.drawString(62, y, name)
        c.setFont("DejaVu-Obl" if n != 1 else "DejaVu", 8); c.setFillColor("#566573")
        c.drawString(218, y, desc)
        y -= 21
        if n == 2 or n == 13:
            c.setStrokeColor("#c3d2df"); c.setLineWidth(0.6)
            c.line(34, y + 6, W - 34, y + 6)
    _foot(c, 3, "выпуск 01 · разворот содержания")
    c.showPage()


def page_folder(c, num, title, lines, img=None, concl=None):
    _head(c, num, title, "раздел %02d" % num)
    y = H - 74
    y = _text_block(c, 34, y, W - 68, lines)
    if img:
        _panel_block(c, img, 150, y - 26)
        y = 150 - 34
    if concl:
        _concl(c, concl, y)
    _foot(c, num)
    c.showPage()


def page_sections(c, num, title, lines, imgs, concl, sizes=None):
    """Лист с несколькими картинками-блоками."""
    _head(c, num, title, "раздел %02d" % num)
    y = H - 74
    y = _text_block(c, 34, y, W - 68, lines, size=sizes[0] if sizes else 8.5)
    bot = 40
    total_h = y - 60
    if len(imgs) == 2:
        render_paths = []
        for i, (imgfn, _tt) in enumerate(imgs):
            p = os.path.join(IMG, "pw-%s.png" % imgfn)
            (render_icegen if imgfn == "icegen" else render_volumes)(p) if imgfn == "icegen" or imgfn == "volumes" else None
            render_paths.append((p, _tt))
        half = total_h / 2
        for i, (p, tt) in enumerate(render_paths):
            x0 = 28 + i * (W - 56) / 2
            c.setFillColor("#e9f2fa"); c.rect(x0, 100, (W - 56) / 2, total_h, fill=1, stroke=0)
            c.setStrokeColor("#c3d2df"); c.setLineWidth(0.8); c.rect(x0, 100, (W - 56) / 2, total_h, fill=0, stroke=1)
            c.setFont("DejaVu-Bold", 8); c.setFillColor(DARK)
            c.drawString(x0 + 8, 100 + total_h - 12, tt)
            c.drawImage(ImageReader(p), x0 + 6, 104, (W - 56) / 2 - 12, total_h - 22,
                        preserveAspectRatio=True, anchor="c")
    _concl(c, concl, 78)
    _foot(c, num)
    c.showPage()


def render_blend(path):
    """Полоса палитр 13 серий — приложение Б."""
    fig = _fig(); ax = fig.add_axes([0.03, 0.03, 0.94, 0.94], frameon=False)
    ax.set_xlim(0, 104); ax.set_ylim(0, 104); ax.axis("off")
    names = [G.JOURNALS[i][0] for i in range(1, 14)]
    for i in range(13):
        p = G.PAL[i + 1]
        y = 97 - i * 7.3
        x = 4
        for col in (p[0], p[1], p[3], p[4], p[5]):
            _node(ax, x, y, 12, 4.6, "", fc=col, ec="#c3d2df", lw=0.6)
            x += 13
        ax.text(4, y + 6.2, "%02d · %s" % (i + 1, names[i]), fontsize=8.5, color=DARK)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_months(path):
    """Каталог жизни лагеря: 31 месяц, 13 серий (выпуски по месяцам)."""
    fig = _fig(); ax = fig.add_axes([0.14, 0.12, 0.80, 0.74])
    rng = np.random.default_rng(13)
    months = np.arange(31)
    pops = 1 + (months % 13) * 0.8 + 0.7 * rng.uniform(0, 1, 31)
    ax.bar(months, pops, color=[G.PAL[i + 1][3] for i in range(13)] * 3, alpha=0.95,
           edgecolor="white", linewidth=0.6, zorder=3)
    ax.set_xticks([]); ax.set_yticks([]); _bg(ax)
    ax.set_xlim(-1, 31)
    ax.text(15, max(pops) * 1.12, "31 месяц жизни лагеря · 2026-01 … 2028-07",
            ha="center", fontsize=10, fontweight="bold", color=DARK)
    ax.plot(months, pops, color=DARK, lw=1.4, zorder=4)
    fig.savefig(path, dpi=120); plt.close(fig)


def page_monthly(c, num, title, lines, images=None, concl=""):
    _head(c, num, title, "приложение В · каталог")
    y = H - 74
    y = _text_block(c, 34, y, W - 68, lines, size=8.2)
    p1 = os.path.join(IMG, "pw-months.png"); render_months(p1)
    _panel_block(c, p1, 160, y - 26)
    y = 160 - 20
    pian = []
    for i in range(13):
        pian += ["%02d %-18s x10" % (i + 1, G.JOURNALS[i + 1][0])]
    _text_block(c, 34, 160 - 46, W - 68, ["Серии золотые и обычные выпускаются с 2026-01 по 2028-07.",
                                           "Каждый месяц — несколько номеров разных серий."])
    _concl(c, concl, 90)
    _foot(c, num)
    c.showPage()


def page_blend(c, num, title, lines, concl):
    _head(c, num, title, "приложение Б · палитры")
    y = H - 74
    y = _text_block(c, 34, y, W - 68, lines, size=8.4)
    p = os.path.join(IMG, "pw-blend.png"); render_blend(p)
    _panel_block(c, p, 200, y - 26)
    _concl(c, concl, 150)
    _foot(c, num)
    c.showPage()


def page_tree(c, num):
    _head(c, num, "СТРУКТУРА РЕПОЗИТОРИЯ (GIT TREE)", "раздел 04 · как устроен ice/")
    y = H - 74
    _text_block(c, 34, y, W - 68, [
        "Репозиторий ice/ — это издательство: код, контент и витрины живут вместе.",
        "Принцип: любой артефакт пересоздаётся командой python gen_*.py.", ], size=8.5)
    img = os.path.join(IMG, "pw-tree.png"); render_tree(img)
    _panel_block(c, img, 210, y - 40)
    _concl(c, "git ls-files — это и есть карта продукта: 16 генераторов и 500 листов изданий.", 165)
    _foot(c, num)
    c.showPage()


def page_sign(c, num=30):
    _head(c, 30, "ЗАВЕРШЕНИЕ · ПЕЧАТЬ И ПОДПИСИ", "лист приёмки")
    y = H - 72
    _text_block(c, 34, y, W - 68, [
        "Работа сдана: 30 листов, все схемы воспроизводимы из файлов репозитория.",
        "Замечания приёмной комиссии устранены на месте: статистика прочитана заново.",
    ], size=9)
    c.setStrokeColor("#c3d2df"); c.setLineWidth(1)
    y = 320
    for i in range(4):
        c.line(60, y, W - 60, y); c.line(60, y + 26, W - 60, y + 26)
        y -= 70
    c.setFillColor(SUN); c.setFont("DejaVu-Bold", 12)
    c.drawCentredString(W / 2, 120, "ПРИНЯТО ИЗДАТЕЛЬСТВОМ «ЛЕДЯНАЯ ВЕЧЕРКА» · печать ▲")
    _foot(c, 30, "приёмка · готово")
    c.showPage()


def page_risks(c, num):
    _head(c, num, "РИСКИ И ОГРАНИЧЕНИЯ", "раздел 15 · честно")
    lines = [
        ("Контур из шума", "низкий", "силуэт может быть некрасив; приёмка — порог гладкости"),
        ("Экспорт JSON", "средний", "несовместимость формы; фиксируем схему в статье"),
        ("Фирменность стиля", "высокий", "каждый айсберг должен читаться «Ледяными человечками»"),
        ("Мана и баланс", "средний", "загрузка айсберга не должна ломать формулы движка"),
    ]
    y = H - 74
    c.setFont("DejaVu-Bold", 9); c.setFillColor(DARK)
    c.drawString(34, y, "ТАБЛИЦА РИСКОВ")
    y -= 22
    for name, lvl, desc in lines:
        c.setStrokeColor("#c3d2df"); c.setLineWidth(0.6)
        c.rect(34, y - 34, W - 68, 30, fill=0, stroke=1)
        c.setFillColor(DARK); c.setFont("DejaVu-Bold", 9)
        c.drawString(40, y - 12, name)
        col = {"низкий": "#27AE60", "средний": "#F39C12", "высокий": "#C0392B"}[lvl]
        c.setFillColor(col); c.setFont("DejaVu", 9)
        wl = c.stringWidth(lvl, "DejaVu", 9)
        c.drawString(W - 90 - wl, y - 12, lvl)
        c.setFillColor("#566573"); c.setFont("DejaVu-Obl", 8)
        c.drawString(40, y - 27, desc)
        y -= 46
    _concl(c, "Наука честна: риск фиксируется до того, как модуль написан.", 86)
    _foot(c, num)
    c.showPage()


def page_results(c, num):
    _head(c, num, "РЕЗУЛЬТАТЫ РАБОТЫ", "раздел 16 · что получилось")
    rows = [
        ("Игра", "один HTML на 600 строк: canvas, движок, летопись, рекорд"),
        ("Симуляция", "те же формулы дают 130 партий журналов (sim_stats)"),
        ("Контент", "100 статей, 130 полос, 130 обложек, 78 зарисовок"),
        ("Издание", "15 PDF · 500 листов: 13 серий + Айс-График + Проектная"),
        ("Витрины", "9 HTML-страниц считают цифры из файлов сами"),
        ("Проект", "Айс-генератор спроектирован: параметры→силуэт→JSON→игра"),
    ]
    y = H - 74
    for name, desc in rows:
        c.setFillColor(SUN); c.setFont("DejaVu-Bold", 16)
        c.drawString(34, y - 10, "■")
        c.setFillColor(DARK); c.setFont("DejaVu-Bold", 10)
        c.drawString(58, y - 8, name)
        c.setFillColor("#16324f"); c.setFont("DejaVu", 9)
        c.drawString(200, y - 8, desc)
        y -= 30
    img = os.path.join(IMG, "pw-volumes.png"); render_volumes(img)
    _panel_block(c, img, 200, y - 10)
    _concl(c, "500 листов — это размер хорошей энциклопедии, собранной из сидов.", 150)
    _foot(c, num)
    c.showPage()


def build_pdf():
    import fitz  # noqa
    c = rlcanvas.Canvas(PDF, pagesize=A4)
    page_cover(c)
    page_passport(c)
    page_toc(c)

    render_filepic(os.path.join(IMG, "pw-filepic.png"))
    page_folder(c, 4, "01 · ОДИН ФАЙЛ — ИГРА", [
        "index.html — это и игра, и образец, и герой всех газет.",
        "canvas 900×600, цикл requestAnimationFrame, 60 кадров в секунду.",
        "лёд, мана, рыба, люди с именами, Летопись лагеря и Хроника эпохи.",
        "Рекорд хранится в localStorage; вся игра — один файл без сервера.",
    ], img=os.path.join(IMG, "pw-filepic.png"), concl="Айсберг рисует dims() = (120 + ice·2.6, 24 + ice·1.5).")

    render_formulas(os.path.join(IMG, "pw-formulas.png"))
    page_folder(c, 5, "02 · ДВИЖОК ПО НАУКЕ", [
        "Формулы движка вынесены в этом выпуске на отдельный лист:",
        "таяние 0.7+0.06·люди, шторм ×2.5 на 10с (каждые 50–70с),",
        "заряд −3 маны → +2.5% льда, сеть +6 рыбы (0.4с),",
        "рождение рыба≥25 (−15) каждые 6с, голод 3с, предел 12,",
        "счёт = время×10 + люди×50.",
    ], img=os.path.join(IMG, "pw-formulas.png"), concl="Движок и журналы живут по одним формулам.")

    # 03 история git — схема
    _head(c, 6, "03 · ИСТОРИЯ GIT: 16 ШАГОВ", "раздел 03 · лог коммитов")
    _text_block(c, 34, H - 74, W - 68, [
        "Все версии продукта — в master, от прототипа до издательства.",
        "Каждый коммит атомарен: одна мысль — один снапшот всей папки.",
    ], size=8.5)
    img = os.path.join(IMG, "pw-log.png"); render_gitlog(img)
    _panel_block(c, img, 190, H - 120)
    _concl(c, "git log показывает эволюцию идеи: игра→статьи→журналы→издательство→модули.", 150)
    _foot(c, 6)
    c.showPage()

    page_tree(c, 7)

    render_seeds(os.path.join(IMG, "pw-seeds.png"))
    page_folder(c, 8, "05 · ПОДХОДЫ", [
        "Сиды: каждый артефакт детерминирован (numpy.default_rng(seed)).",
        "Воспроизводимость: git + python gen_*.py возвращает тот же файл.",
        "Статистика из файлов: fitz открывает PDF и считает страницы —",
        "витрины не врут, когда выходит новый выпуск.",
        "Разделение зон: код (gen_*), контент (articles, journals) и дериваты (journals_pdf).",
    ], img=os.path.join(IMG, "pw-seeds.png"), concl="Подход «всё пересоздаётся, ничего не хранится» делает архив честным.")

    render_articles(os.path.join(IMG, "pw-articles.png"))
    page_folder(c, 9, "06 · ТЕКСТЫ: 100 СТАТЕЙ", [
        "articles/ — 50 анализов шедевра (01-shedevr … 50-itog);",
        "articles/future/ — 50 номеров «Ледяной Вечерки» из будущего (001…050).",
        "Формат: заголовок СТАТЬЯ NN/номер из будущего + разделители.",
        "Уникальность: читатель получает и газету, и код, который её напечатал.",
    ], img=os.path.join(IMG, "pw-articles.png"), concl="Тексты и код — один архив: папка articles/ открывается как подшивка газет.")

    render_journals(os.path.join(IMG, "pw-journals.png"))
    page_folder(c, 10, "07 · ЖУРНАЛЫ: 13 СЕРИЙ × 10", [
        "gen_pdf_journals.py печатает 13 серий по 10 выпусков (270 листов).",
        "у каждой серии — палитра, рубрики, шарж героя, табло партии движка;",
        "Золотой журнал (13-я серия) — 30 листов на номер: события года.",
        "Айс-График — 10 томов по 20 страниц: 80% схем и кубов.",
    ], img=os.path.join(IMG, "pw-journals.png"), concl="Один генератор — десятки изданий; палитра - это «голос» серии.")

    # 08 иллюстрации: жанры
    var = os.path.join(IMG, "pw-icegen.png"); render_icegen(var)
    page_folder(c, 11, "08 · ИЛЛЮСТРАЦИИ: ЖАНРЫ", [
        "Шарж — портрет героя: информационно-разъяснительный, узнаваемый.",
        "Карикатура — сценка месяца: воспитательная, с моралью из приёма.",
        "Полиарт-φ — обложки и зарисовки: полиномиальные слои и золотое сечение.",
        "Движок рисует и героев, и шторм, и датчики — всё из одной партии.",
    ], img=var, concl="Жанр — это контракт: шарж объясняет героя, карикатура воспитывает игрока.")

    render_vitr(os.path.join(IMG, "pw-vitr.png"))
    page_folder(c, 12, "09 · ВИТРИНЫ: 9 HTML-СТРАНИЦ", [
        "press-center.html — главная витрина: и сюда попадает этот выпуск.",
        "kiosk, wiki-ice, heroes, fun, epochs, polyart, situations, games —",
        "каждая открывает свой срез архива и считает метрики сама.",
        "fitz.open(pdf).page_count — истина о числе листов и здесь.",
    ], img=os.path.join(IMG, "pw-vitr.png"), concl="Витрины не имеют вручную вписанных чисел — поэтому не стареют.")

    img_pp = os.path.join(IMG, "pw-pipe.png"); render_pipeline(img_pp)
    page_folder(c, 13, "10 · КОНВЕЙЕР GENERATOR→ИЗДАНИЕ", [
        "16 генераторов превращают сиды и тексты в 500 листов PDF.",
        "gen_pdf_journals / gen_ajs_grafik / gen_project_work — три печатных станка;",
        "gen_covers / gen_polyart / gen_situations — цех иллюстраций;",
        "gen_press_center / gen_kiosk / gen_wiki — витрины.",
    ], img=img_pp, concl="Любой файл продукта воспроизводится из репозитория без архива PDF.")

    # --- Айс-генератор: 4 листа
    render_json(os.path.join(IMG, "pw-json.png"))
    page_folder(c, 14, "11 · АЙС-ГЕНЕРАТОР — ПРОЕКТ МОДУЛЯ", [
        "Цель модуля: по параметрам создать уникальный айсберг для игры.",
        "Вход: ширина, высота пика, фаски (парус-купол), шум контура, сид.",
        "Выход: JSON {profile: [...], palette: ...} — контур и цвета льда.",
        "Размещение: icegen.html (чистый HTML/JS, без сервера), рядом с игрой.",
        "Игра будет читать профиль из ?ice=<payload> и рисовать свой айсберг.",
    ], img=os.path.join(IMG, "pw-json.png"), concl="Сейчас модуль — в плане: спроектирован, но не написан (это работа по науке).")

    # 15 — алгоритм
    render_icegen(os.path.join(IMG, "pw-algo.png"))
    page_folder(c, 15, "11 · АЙС-ГЕНЕРАТОР — АЛГОРИТМ", [
        "Силуэт: базовый полином купола + шумовая кривая хребта.",
        "Шум управляется сидом: одна кнопка «новый» — новый айсберг.",
        "Контур переводится в массив точек {x, y} — профиль для JSON.",
        "Палитра привязана к сериям: снег-верх, лёд-середина, тень-низ.",
        "Проверка приёмки: волна кривая не гуляет, стиль читается.",
    ], img=os.path.join(IMG, "pw-algo.png"), concl="Силуэт на титуле этого выпуска — первый «ныряющий» айсберг генератора.")

    page_folder(c, 16, "11 · АЙС-ГЕНЕРАТОР — ЧТЕНИЕ В ИГРЕ", [
        "Вход игры: URL index.html?ice=<encodeURIComponent(JSON)>.",
        "index.html парсит query при старте: если профиль есть — он главный.",
        "dims() берёт реальные ширину и высоту контура вместо формулы 120+ice·2.6.",
        "Движок не меняется: функции льда/маны/рыбы остаются формулами раздела 02.",
        "Несовпадение контура → игра рисует и считает по реальным пикселям.",
    ], concl="Генератор создаёт вид айсберга, движок остаётся честным к формулам.")

    render_plan(os.path.join(IMG, "pw-plan.png"))
    page_folder(c, 17, "11 · АЙС-ГЕНЕРАТОР — ПЛАН И ПРИЁМКА", [
        "Этап 1 · icegen.html: форма параметров + canvas-предпросмотр.",
        "Этап 2 · экспорт JSON {profile, palette} кнопкой «сохранить».",
        "Этап 3 · index.html принимает профиль через query-параметр.",
        "Этап 4 · партия: сгенерировать 13 айсбергов — по одному на серию.",
        "Приёмка: играбельное чтение профиля, воспроизводимость одинаковых сидов.",
    ], img=os.path.join(IMG, "pw-plan.png"), concl="Критерий успеха: один и тот же URL всегда даёт один и тот же айсберг.")

    _head(c, 18, "12 · ОБЪЁМЫ АРХИВА", "раздел 12 · арифметика")
    _text_block(c, 34, H - 74, W - 68, [
        "15 изданий · 500 листов · 13 журналов по 20 + Золотой 30 + Айс-График 200.",
        "Айс-График — самый толстый: 200 страниц схем и кубов; Проектная — 30.",
    ], size=8.5)
    img = os.path.join(IMG, "pw-volumes.png"); render_volumes(img)
    _panel_block(c, img, 200, H - 120)
    _concl(c, "Объёмы считает fitz: при новом выпуске столбик растёт сам.", 150)
    _foot(c, 18)
    c.showPage()

    render_stats(os.path.join(IMG, "pw-stats.png"))
    page_folder(c, 19, "13 · ПО НАУКЕ: ЧИСЛА НЕ УСТАРЕВАЮТ", [
        "Теорема журналистики ледяной деревни: число на витрине = функция файлов.",
        "fitz.open(pdf).page_count; len(glob('articles/*.txt')) — такие формулы.",
        "Поэтому press-center знает про 500 страниц, даже когда их станет 530.",
        "Статистика партий — sim_stats(jno, issue): реальные 130 запусков движка.",
    ], img=os.path.join(IMG, "pw-stats.png"), concl="«По науке» = проверяемо: любой отчёт можно повторить командой.")

    render_fantasy(os.path.join(IMG, "pw-fantasy.png"))
    page_folder(c, 20, "14 · ФАНТАЗИИ ФУТУРОЛОГА", [
        "Айс-генератор станет мастером форм: Полиарт-айсберги серий 01–13.",
        "Шторм-радары будут рисовать траекторию бури по контуру айсберга.",
        "Обложки Вечерки выберут силуэт недели голосованием читателей.",
        "Квантовая мана: заряд, который самим льдом меняет свой цвет.",
        "Айсберги научатся снег спасать летом и сколы — полировать.",
    ], img=os.path.join(IMG, "pw-fantasy.png"), concl="Фантазии — это TODO удалённого будущего; их честно отделяют от проекта.")

    page_risks(c, 21)

    page_results(c, 22)

    page_folder(c, 23, "17 · ВЫВОДЫ", [
        "Главное: один файл способен породить целое издательство.",
        "Детерминизм и сиды делают артефакты воспроизводимыми — это наука.",
        "Статистика из файлов убирает ложь из витрин и из отчётов.",
        "Жанры иллюстраций — шарж/карикатура/полиарт — читаются без слов.",
        "Следующий шаг — модуль «Айс-генератор айсбергов» (разделы 14–17).",
    ], concl="Проект доказал: содержание, код и наука могут жить в одном repo.")

    page_folder(c, 24, "18 · ЗАКЛЮЧЕНИЕ", [
        "Ледяные человечки выживают, потому что считаны льдом и племенем.",
        "Издательство печатает 500 листов из одного движка 600 строк.",
        "Айс-генератор айсбергов встанет в конвейер как четвёртый станок.",
        "Мы сдали «Проектную работу» так же, как печатаем журналы: по сидам.",
    ], concl="Лёд растает, а файлы останутся пересоздаваемыми — вечная империя.")

    page_folder(c, 25, "ПРИЛОЖЕНИЕ А · СЛОВАРЬ", [
        "Айс-генератор — модуль, создающий силуэт айсберга из параметров и шума.",
        "Жанр — контракт между картинкой и читателем (шарж/карикатура/полиарт).",
        "Сид — число, из которого движок получает «новый» артефакт детерминированно.",
        "Витрина — HTML-страница, считающая статистику из файлов прямо при сборке.",
        "Из-под капота — раздел игр, где движок показывает датчики партии.",
        "Мана — ресурс заряда: клик по льду превращает ману в лёд.",
    ], concl="Словарь совпадает с терминами репозитория и газет — единый язык.")

    page_blend(c, 26, "ПРИЛОЖЕНИЕ Б · ПАЛИТРЫ 13 СЕРИЙ", [
        "У каждой серии своя палитра: 13 цветовых «голосов» Вечерки.",
        "Палитра передаётся в журнал, обложку, шарж и график одной константой.",
    ], concl="Цвет серии — её узнаваемость: читатель видит серию до прочтения имени.")

    page_monthly(c, 27, "ПРИЛОЖЕНИЕ В · КАТАЛОГ 31 МЕСЯЦА", [
        "Жизнь лагеря описана с января 2026 по июль 2028 — 31 месяц.",
        "Газетные полосы расставлены по месяцам: истории живут по календарю.",
        "Когда месяцы придут, номера станут историей, которую вспомнят все.",
    ], concl="Каталог по датам делает архив читаемым как хроника эпохи.")

    page_folder(c, 28, "ПРИЛОЖЕНИЕ Г · МЕРА ПАРТИИ", [
        "Каждая партия движка имеет паспорт: survived, peak_pop, peak_fish, storms.",
        "score = время×10 + люди×50 — мера успеха номера.",
        "130 партий = 13 серий × 10 выпусков: те же числа, что в игре.",
        "Сиды различают партии: при одинаковых правилах — разные судьбы.",
    ], concl="sim_stats — мост между игрой и газетой: факт один и тот же.")

    page_folder(c, 29, "ПРИЁМКА · КОНТРОЛЬНЫЙ ЛИСТ", [
        "□ 30 листов в PDF, каждый снабжён шапкой и узлом вывода.",
        "□ структура git показана деревом и логом; подходы названы прямо.",
        "□ «по науке»: сиды, воспроизводимость, статистика из файлов.",
        "□ Айс-генератор спроектирован: параметры → силуэт → JSON → игра.",
        "□ фантазии отделены от проекта и честно помечены разделом 14.",
    ], concl="Контрольный лист заполняется тем же кодом, что печатает отчёт.")

    page_sign(c, 30)

    c.save()
    return PDF


if __name__ == "__main__":
    path = build_pdf()
    import fitz
    d = fitz.open(path)
    print(path, d.page_count, "листов", os.path.getsize(path), "б")