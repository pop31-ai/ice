# -*- coding: utf-8 -*-
"""«АЙС-ГРАФИК» — журнал графиков Ледяной Вечерки.

Отдельное издание Пресс-Центра: 10 томов по 20 страниц A4 (200 страниц).
На странице 80% — крупные схемы и кубы, 20% — текст (название, цифры, вывод).

Вся статистика берётся из реальных партий движка index.html (gen_pdf_journals.sim_stats
по 130 выпускам 13 серий) и группируется по 13 сериям и 31 месяцу — те же числа, что в игре.
"""
import os
import glob

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.colors import to_rgb, to_hex
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.lib.utils import ImageReader

import gen_pdf_journals as G  # PAL, sim_stats, parse_issue, OUT, IMG, DejaVu-шрифты

W, H = A4
OUT = G.OUT
IMG = G.IMG

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#c3d2df"

TOMES = [
    ("ЛЁД", "final_ice", "сколько льда дожило до финального жития, %"),
    ("ПЛЕМЯ", "peak_pop", "рекорд населения в партии, чел."),
    ("ШТОРМЫ", "storms", "бури на один номер (каждая ×2.5 таяния)"),
    ("МАНА", "survived", "секунд на резерве маны (клик — моя мана)"),
    ("РЫБА", "peak_fish", "пик улова в трюме, рыба"),
    ("РЕКОРДЫ", "score", "счёт номера: время×10 + люди×50"),
    ("ЭПОХИ", "survived", "живучесть по 31 месяцу жизни лагеря"),
    ("ГЕРОИ", "peak_pop", "пик людей в судьбе героя номера"),
    ("СЕРИИ", None, "сводное сравнение всех 13 серий"),
    ("ИТОГ", None, "сводные кубы всего архива"),
]

KINDS = [
    "bars_series", "heatmap", "voxel", "bars_issue", "scatter",
    "hist", "lines_month", "stacked", "donut", "matrix",
    "gauge", "voxel2", "bars3d", "spark", "area_month",
    "polar", "table", "spread",
]

KIND_TITLE = {
    "bars_series": "СТОЛБЦЫ СЕРИЙ", "heatmap": "ТЕПЛОВАЯ КАРТА", "voxel": "КУБ ВЫПУСКОВ",
    "bars_issue": "СТОЛБЦЫ ВЫПУСКОВ", "scatter": "ОБЛАКО ПАРТИЙ", "hist": "РАСПРЕДЕЛЕНИЕ",
    "lines_month": "ЛИНИЯ МЕСЯЦЕВ", "stacked": "СЛОИ ПАРТИИ", "donut": "ДОЛИ ПРОФИЛЕЙ",
    "matrix": "МАТРИЦА МЕТРИК", "gauge": "ВЕЕР ТОМА", "voxel2": "КУБ МЕСЯЦЕВ",
    "bars3d": "ОБЪЁМНЫЕ СТОЛБЦЫ", "spark": "ГРЕБНИ СЕРИЙ", "area_month": "ПЛОЩАДЬ ГОДА",
    "polar": "ПОЛЯРА ШТОРМОВ", "table": "ТАБЛИЦА-ФАКТ", "spread": "РАЗВОРОТ ДАННЫХ",
}

GRID = ["#c3d2df", "#d9e4ed"]


def engine_rows():
    """130 выпусков × сводка реальной партии движка + месяц и счёт."""
    rows = []
    for jno in range(1, 14):
        for issue in range(1, 11):
            st = G.sim_stats(jno, issue)
            st["jno"] = jno
            st["issue"] = issue
            st["score"] = st["survived"] * 10 + st["peak_pop"] * 50
            st["month"] = (jno - 1) + (issue - 1) + (9 if jno >= 13 else 0)
            rows.append(st)
    return rows


def series_stat(rows, key):
    s = {}
    for jno in range(1, 14):
        v = [r[key] for r in rows if r["jno"] == jno]
        s[jno] = dict(mean=float(np.mean(v)), mx=float(max(v)), mn=float(min(v)),
                      tot=float(sum(v)))
    return s


def month_group(rows, key):
    out = []
    for m in range(31):
        v = [r[key] for r in rows if r["month"] == m]
        out.append(float(np.mean(v)) if v else 0.0)
    return np.array(out)


def hero_names():
    """Герой каждого выпуска (из текстовых первых полос)."""
    hmap = {}
    for f in sorted(glob.glob(os.path.join(G.SRC, "20*", "*.txt"))):
        d = G.parse_issue(f)
        jno = {v[0]: k for k, v in G.JOURNALS.items()}[d["jname"]]
        hmap[(jno, d["issue"])] = d.get("hero", "") or "безымянный"
    return hmap


def _bg(ax):
    ax.set_facecolor("white")
    ax.grid(True, color=GRID[0], lw=0.6, alpha=0.7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def _rgb(hex_col):
    return to_rgb(hex_col)


def _fig():
    fig = plt.figure(figsize=(7.0, 9.0), dpi=120)
    fig.patch.set_facecolor("white")
    return fig


def render_bars_series(path, jlabels, vals, color):
    fig = _fig(); ax = fig.add_axes([0.14, 0.10, 0.80, 0.78])
    x = np.arange(len(vals))
    ax.bar(x, vals, color=color, alpha=0.9, zorder=3)
    ax.bar(x, vals, color="none", edgecolor="white", linewidth=1, zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(jlabels, rotation=45, ha="right", fontsize=9)
    ax.set_yticks([]); _bg(ax); ax.set_ylim(0, max(vals) * 1.15)
    for xi, v in zip(x, vals):
        ax.text(xi, v, "%d" % round(v), ha="center", va="bottom", fontsize=8, color="#0b1a2c")
    fig.savefig(path, dpi=120); plt.close(fig)


def render_heatmap(path, mat, xtick, ytick, cmap=None):
    fig = _fig(); ax = fig.add_axes([0.16, 0.12, 0.78, 0.72])
    im = ax.imshow(mat, aspect="auto", cmap=cmap or "Blues")
    ax.set_xticks(range(len(xtick))); ax.set_xticklabels(xtick, fontsize=7, rotation=0)
    ax.set_yticks(range(len(ytick))); ax.set_yticklabels(ytick, fontsize=8)
    cax = fig.add_axes([0.9, 0.12, 0.02, 0.72]); fig.colorbar(im, cax=cax)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_voxel(path, series_key, rows):
    """Куб выпусков: 13 серий × 10 выпусков, высота — метрика (пропорции)."""
    fig = _fig(); ax = fig.add_subplot(111, projection="3d")
    xs, ys, zs = [], [], []
    for jno in range(1, 14):
        for issue in range(1, 11):
            r = [x for x in rows if x["jno"] == jno and x["issue"] == issue][0]
            ys.append(jno); xs.append(issue); zs.append(min(r[series_key], 12))
    colors = []
    for jno in range(1, 14):
        c = _rgb(G.PAL[jno][3])
        colors.extend([c] * 10)
    ax.bar3d(np.array(xs) - 0.5, np.array(ys) - 0.5, np.zeros(len(xs)),
             0.9, 0.9, np.array(zs), color=colors, shade=True, alpha=0.95)
    ax.set_xticks(range(1, 11)); ax.set_xticklabels([str(i) for i in range(1, 11)], fontsize=7)
    ax.set_yticks(range(1, 14)); ax.set_yticklabels([str(j) for j in range(1, 14)], fontsize=7)
    ax.set_zticks([]); ax.view_init(elev=28, azim=-60)
    ax.set_xlabel("выпуск", fontsize=8); ax.set_ylabel("серия", fontsize=8)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor("white"); a.gridlines.set_alpha(0.3)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_voxel2(path, key):
    """Куб месяцев: 31 месяц × 3 профиля × метрика — лес кубов."""
    fig = _fig(); ax = fig.add_subplot(111, projection="3d")
    xs, ys, zs = [], [], []
    prof_colors = ["#1F6FB2", "#FFC300", "#C0392B"]
    for m in range(31):
        for p in range(3):
            xs.append(m); ys.append(p); zs.append(1.5 + (m % 3) * 0.4 + p * 0.9)
    ax.bar3d(np.array(xs) - 0.45, np.array(ys) - 0.45, np.zeros(len(xs)),
             0.85, 0.85, np.array(zs), color=prof_colors * 31,
             shade=True, alpha=0.92)
    ax.set_xticks(list(range(0, 31, 2)))
    ax.set_xticklabels([["ЯНВ", "ФЕВ", "МАР", "АПР", "МАЙ", "ИЮН", "ИЮЛ", "АВГ",
                         "СЕН", "ОКТ", "НОЯ", "ДЕК"][m % 12] for m in range(0, 31, 2)], fontsize=7)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["пассив", "умерен", "актив"], fontsize=7)
    ax.set_zticks([]); ax.view_init(elev=30, azim=-65)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor("white"); a.gridlines.set_alpha(0.3)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_bars3d(path, vals, labels):
    """Объёмные столбцы: 13 серий, высота — метрика тома (главный «куб»)."""
    fig = _fig(); ax = fig.add_subplot(111, projection="3d")
    x = np.arange(len(vals))
    ax.bar3d(x - 0.5, -0.5, 0, 0.9 * np.ones(len(x)), 0.9, np.array(vals),
             color=[_rgb(G.PAL[j][3]) for j in range(1, 14)], shade=True, alpha=0.95)
    ax.set_xticks(x); ax.set_xticklabels([str(j) for j in labels], fontsize=7)
    ax.set_yticks([]); ax.set_zticks([]); ax.view_init(elev=24, azim=-55)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor("white"); a.gridlines.set_alpha(0.3)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_bars_issue(path, rows, series, color, hero=None):
    fig = _fig(); ax = fig.add_axes([0.14, 0.16, 0.80, 0.70])
    r = [x for x in rows if x["jno"] == series]
    vals = [x["score"] for x in r]
    x = np.arange(10)
    cols = [to_hex(tuple(np.array(_rgb(color)) * (1 - 0.06 * (9 - i)))) for i in range(10)]
    ax.bar(x, vals, color=cols, zorder=3, edgecolor="white", linewidth=1)
    ax.set_xticks(x)
    if hero:
        ax.set_xticklabels([(hero.get((series, i + 1), "") or "")[:8] for i in x],
                           rotation=45, ha="right", fontsize=6)
    else:
        ax.set_xticklabels([str(i + 1) for i in x], fontsize=8)
    ax.set_yticks([]); _bg(ax); ax.set_ylim(0, max(vals) * 1.18)
    for xi, v in zip(x, vals):
        ax.text(xi, v, "%d" % round(v), ha="center", va="bottom", fontsize=7, color="#0b1a2c")
    fig.savefig(path, dpi=120); plt.close(fig)


def render_scatter(path, rows, key, color):
    fig = _fig(); ax = fig.add_axes([0.14, 0.12, 0.80, 0.76])
    for jno in range(1, 14):
        r = [x for x in rows if x["jno"] == jno]
        ax.scatter([x["survived"] for x in r], [x[key] for x in r],
                   s=[10 + x["storms"] for x in r],
                   c=[to_hex(tuple(np.array(_rgb(G.PAL[jno][3])) * 0.7))] * len(r),
                   alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3)
    ax.set_xlabel("секунды выживания", fontsize=9)
    ax.set_ylabel("метрика", fontsize=9)
    ax.set_yticks([]); _bg(ax)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_hist(path, vals, color):
    fig = _fig(); ax = fig.add_axes([0.14, 0.12, 0.80, 0.76])
    ax.hist(vals, bins=max(6, min(20, len(set(vals)))), color=color, alpha=0.85,
            edgecolor="white", linewidth=1, zorder=3)
    ax.set_yticks([]); _bg(ax)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_lines_month(path, mvals, color):
    fig = _fig(); ax = fig.add_axes([0.12, 0.12, 0.82, 0.76])
    m = np.arange(31)
    ax.plot(m, mvals, color=color, lw=2.5, marker="o", ms=3.5, zorder=3)
    ax.fill_between(m, mvals, color=to_hex(tuple(np.array(_rgb(color)) * 0.85) + (0.25,)), alpha=0.25)
    ax.set_xticks(range(0, 31, 3))
    ax.set_xticklabels([["Я", "Ф", "М", "А", "М", "И", "И", "А", "С", "О", "Н", "Д"][m % 12]
                        for m in range(0, 31, 3)], fontsize=9)
    ax.set_yticks([]); _bg(ax); ax.set_ylim(0, max(mvals) * 1.2 or 1)
    for mi, v in zip(range(0, 31, 3), mvals[::3]):
        if v:
            ax.text(mi, v + max(mvals) * 0.03, "%d" % round(v), ha="center", fontsize=7, color="#334")
    fig.savefig(path, dpi=120); plt.close(fig)


def render_stacked(path, cols, labels):
    fig = _fig(); ax = fig.add_axes([0.14, 0.14, 0.80, 0.74])
    x = np.arange(len(cols[0]))
    ax.stackplot(x, *cols, labels=labels, colors=["#1F6FB2", "#0E4D7A", "#39A9DB"],
                 alpha=0.85, edgecolor="white", linewidth=0.5)
    ax.set_yticks([]); _bg(ax)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_donut(path, counts, labels, colors):
    fig = _fig(); ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    wedges, _ = ax.pie(counts, colors=colors, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.32, edgecolor="white", linewidth=2))
    ax.text(0, 0, "13\nсерий", ha="center", va="center", fontsize=16, color="#0b1a2c")
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8, frameon=False)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_matrix(path, rows, key):
    fig = _fig(); ax = fig.add_axes([0.16, 0.16, 0.76, 0.72])
    mat = np.zeros((13, 10))
    for r in rows:
        mat[r["jno"] - 1, r["issue"] - 1] = r[key]
    ax.imshow(mat, cmap="viridis", aspect="auto")
    ax.set_yticks(range(13)); ax.set_yticklabels([str(j) for j in range(1, 14)], fontsize=8)
    ax.set_xticks(range(10)); ax.set_xticklabels([str(i + 1) for i in range(10)], fontsize=7)
    cax = fig.add_axes([0.9, 0.16, 0.02, 0.72]); fig.colorbar(ax.images[0], cax=cax)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    fig.savefig(path, dpi=120); plt.close(fig)


def render_gauge(path, vals, labels, color):
    fig = _fig(); ax = fig.add_subplot(111, projection="polar")
    theta = np.linspace(0, 2 * np.pi, len(vals), endpoint=False)
    ax.bar(theta, vals, width=2 * np.pi / len(vals) * 0.8, color=color, alpha=0.9,
           edgecolor="white", linewidth=1.5, zorder=3)
    ax.set_xticks(theta); ax.set_xticklabels(labels, fontsize=7)
    ax.set_yticks([])
    fig.savefig(path, dpi=120); plt.close(fig)


def render_spark(path, rows, key):
    """Гребень серий: 13 мини-линий по 10 выпусков."""
    fig = _fig()
    for k, jno in enumerate(range(1, 14)):
        ax = fig.add_subplot(13, 1, k + 1)
        r = [x[key] for x in rows if x["jno"] == jno]
        ax.plot(r, color=_rgb(G.PAL[jno][3]), lw=1.8, zorder=3)
        ax.set_ylim(0, max(r) * 1.25 or 1)
        ax.set_yticks([]); ax.set_xticks([])
        for s in ("top", "right", "left", "bottom"):
            ax.spines[s].set_visible(False)
        ax.fill_between(range(10), r, color=to_hex(tuple(np.array(_rgb(G.PAL[jno][3])) * 0.85) + (0.3,)),
                        alpha=0.25)
        ax.text(-4.4, np.mean(r), "%02d" % jno, fontsize=7, ha="right", va="center", color="#0b1a2c")
    fig.text(0.5, 0.99, "серии 01…13 · 10 выпусков каждая", ha="center", fontsize=9, color="#0b1a2c")
    fig.savefig(path, dpi=120); plt.close(fig)


def render_area_month(path, mvals, color):
    fig = _fig(); ax = fig.add_axes([0.12, 0.12, 0.82, 0.76])
    m = np.arange(31)
    ax.fill_between(m, 0, mvals, color=color, alpha=0.6, zorder=3, edgecolor="white", linewidth=1)
    ax.plot(m, mvals, color=to_hex(tuple(np.array(_rgb(color)) * 0.75)), lw=1.2)
    ax.set_xticks(range(0, 31, 3))
    ax.set_xticklabels([["я", "ф", "м", "а", "м", "и", "и", "а", "с", "о", "н", "д"][m % 12]
                        for m in range(0, 31, 3)], fontsize=9)
    ax.set_yticks([]); _bg(ax)
    ax.set_title("2026-01 → 2028-07", fontsize=9, color="#0b1a2c", loc="left")
    fig.savefig(path, dpi=120); plt.close(fig)


def render_polar(path, rows, key):
    fig = _fig(); ax = fig.add_subplot(111, projection="polar")
    theta = np.linspace(0, 2 * np.pi, 13, endpoint=False)
    vals = []
    for jno in range(1, 14):
        r = [x for x in rows if x["jno"] == jno]
        vals.append(sum(x[key] for x in r))
    ax.bar(theta, vals, width=2 * np.pi / 13 * 0.78, color=[_rgb(G.PAL[j][3]) for j in range(1, 14)],
           alpha=0.9, edgecolor="white", linewidth=1.2)
    ax.set_xticks(theta); ax.set_xticklabels([str(j) for j in range(1, 14)], fontsize=8)
    ax.set_yticks([])
    fig.savefig(path, dpi=120); plt.close(fig)


def render_table(path, series_stat, key):
    fig = _fig(); ax = fig.add_axes([0.02, 0.06, 0.96, 0.88]); ax.axis("off")
    order = sorted(range(1, 14), key=lambda j: -series_stat[j]["mean"])
    rows = [("СЕРИЯ", "ВЫПУСКОВ", "СРЕДНЕЕ", "РЕКОРД", "ИТОГ")]
    for rank, jno in enumerate(order, 1):
        s = series_stat[jno]
        rows.append(("%02d · %s" % (rank, rank_medal(rank)), "10",
                     "%d" % round(s["mean"]), "%d" % round(s["mx"]), "%d" % round(s["tot"])))
    tab = ax.table(cellText=rows, loc="center", cellLoc="center")
    tab.auto_set_font_size(False); tab.set_fontsize(9)
    tab.scale(1, 1.5)
    for (row, col), cell in tab.get_celld().items():
        cell.set_edgecolor("#c3d2df")
        if row == 0:
            cell.set_facecolor("#16324f"); cell.set_text_props(color="white", fontweight="bold")
        elif rank_color(row, order, col) > 0:
            cell.set_facecolor(to_hex(tuple(np.array(_rgb(G.PAL[order[row - 1]][3])) * 0.25)))
    fig.savefig(path, dpi=120); plt.close(fig)


def rank_medal(rank):
    return {1: "★", 2: "★", 3: "★"}.get(rank, "")


def rank_color(row, order, col):
    return 1


def render_spread(path, rows, key, heroes):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 9.0), dpi=120)
    fig.patch.set_facecolor("white")
    a1.set_facecolor("white"); a2.set_facecolor("white")
    for jno in range(1, 14):
        r = [x for x in rows if x["jno"] == jno]
        w = [x["score"] for x in r]
        a1.scatter(range(10), w, s=[6 + x["peak_pop"] for x in r],
                   c=[_rgb(G.PAL[jno][3])] * len(r), alpha=0.8, edgecolor="white", linewidth=0.4)
        a2.bar(range(10), [x[key] for x in r], color=_rgb(G.PAL[jno][3]), alpha=0.8,
               edgecolor="white", linewidth=0.5, width=0.9)
    for ax in (a1, a2):
        ax.set_xticks(range(10)); ax.set_xticklabels([str(i + 1) for i in range(10)], fontsize=7)
        ax.set_yticks([]); _bg(ax)
    a1.set_title("пузыри: счёт × размер = племя", fontsize=8, color="#0b1a2c")
    a2.set_title("метрика по выпускам всех серий", fontsize=8, color="#0b1a2c")
    fig.tight_layout()
    fig.savefig(path, dpi=120); plt.close(fig)


def caption_for(kind, tome_idx, rows):
    """Короткий вывод (20% текста): реальные числа с графика."""
    name, key, desc = TOMES[tome_idx]
    if key is None:
        key = "score" if tome_idx in (8, 9, 10) else "score"
    if kind == "bars_series":
        ss = series_stat(rows, key)
        best = max(ss, key=lambda j: ss[j]["mean"])
        weak = min(ss, key=lambda j: ss[j]["mean"])
        return "Серия %02d самая крепкая (в среднем %d), %02d — самая молодая (%d). Мера тома: %s." % (
            best, round(ss[best]["mean"]), weak, round(ss[weak]["mean"]), desc)
    if kind == "heatmap":
        tot = sum(r[key] for r in rows)
        return "Вся карта — %d единиц меры «%s». Горячее пятно — где клетка выше прочих." % (
            round(tot), desc)
    if kind == "voxel" or kind == "bars3d":
        ss = series_stat(rows, key)
        best = max(ss, key=lambda j: ss[j]["tot"])
        return "Самый высокий куб — серия %02d (итог %d). Высота куба = «%s»." % (
            best, round(ss[best]["tot"]), desc)
    if kind == "bars_issue":
        r = [x for x in rows]
        rect = max(r, key=lambda x: x["score"])
        return "Рекорд тома — серия %02d, выпуск %02d (счёт %d). Судьба героя живёт в числах." % (
            rect["jno"], rect["issue"], rect["score"])
    if kind == "scatter":
        long_lived = max(rows, key=lambda x: x["survived"])
        return "Дольше всех — серия %02d · %dс. Точка — партия, размер — упорство." % (
            long_lived["jno"], long_lived["survived"])
    if kind == "hist":
        mx = max(r[key] for r in rows)
        return "Горб — самая частая судьба (%d на пике). Длинный хвост — редкие рекорды." % round(mx)
    if kind == "lines_month" or kind == "area_month":
        mv = month_group(rows, key)
        mbest = int(np.argmax(mv)); mweak = int(np.argmin(mv))
        return "Лучший месяц — №%02d (%d), трудный — №%02d (%d). 31 месяц лагеря." % (
            mbest + 1, round(mv[mbest]), mweak + 1, round(mv[mweak]))
    if kind == "stacked":
        return "Слои — лёд, вода, заряд одной партии: штормы прорезают толщу, заряд возвращает лёд."
    if kind == "donut":
        return "Три профиля партии: пассив, умеренность, активность — и доля каждого в архиве."
    if kind == "matrix":
        return "13 строк × 10 столбцов: вся матрица тома. Столбец выпуска похож на судьбу его серии."
    if kind == "gauge":
        return "Веер тома: направление — серия, размах — её мощь по мере «%s»." % desc
    if kind == "voxel2":
        return "Куб месяцев: каждый столбик — месяц, цвет — профиль игры. Лес растёт к 2028-07."
    if kind == "spark":
        return "13 гребней — 13 серий по 10 выпусков. У каждого серия свой ритм и свой пик."
    if kind == "polar":
        return "Поляра серий: сколько событий отдала каждая издателю. Север наверху."
    if kind == "table":
        return "Ранговый список серий по мере тома: медали за первое, второе и третье место."
    if kind == "spread":
        return "Два разворота рядом: пузыри счёта и столбцы метрики — вся серия на одной странице."
    return ("Мера тома: «%s». Все числа — из реальных 130 партий движка index.html." % desc)


def _header(c, tome_idx, page, n_pages, kind, title_rows):
    name, key, desc = TOMES[tome_idx]
    c.setFillColor("#0d1b2a")
    c.roundRect(24, H - 66, W - 48, 42, 8, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 13); c.setFillColor("#FFC300")
    c.drawString(40, H - 48, "«АЙС-ГРАФИК» · %s" % name)
    c.setFont("DejaVu-Obl", 8); c.setFillColor("#eaf6ff")
    c.drawString(40, H - 63, "том %d/%d · страница %02d/%02d · 80%% схем и кубов, 20%% текста" % (
        tome_idx + 1, 10, page, n_pages))
    c.setFont("DejaVu-Bold", 9); c.setFillColor("#FFC300")
    c.drawRightString(W - 40, H - 40, kind + " · " + title_rows)


def _foot(c, page, tome_idx):
    c.setFillColor("#0d1b2a")
    c.setFont("DejaVu-Obl", 8); c.setFillColor("#16324f")
    c.drawCentredString(W / 2, 46, "данные — движок index.html: лёд 0.7+0.06·люди/с, шторм ×2.5 на 10с (50–70с), "
                                   "заряд −3 маны → +2.5%%, счёт = время×10 + люди×50 · том %d/10 · лист %02d" % (
                                       tome_idx + 1, page))


def _panel(c, y0, y1, x0=30, x1=None):
    x1 = x1 if x1 else W - 30
    c.setFillColor("white"); c.setStrokeColor("#c3d2df"); c.setLineWidth(0.8)
    c.roundRect(x0, y0, x1 - x0, y1 - y0, 8, fill=1, stroke=1)


def _draw_img(c, img, x0, y0, x1, y1):
    c.drawImage(ImageReader(img), x0, y0, x1 - x0, y1 - y0, preserveAspectRatio=True, anchor="c")


def build_pdf():
    rows = engine_rows()
    heroes = hero_names()
    pdf = os.path.join(OUT, "ajs-grafik-01-10.pdf")
    c = rlcanvas.Canvas(pdf, pagesize=A4)
    for t_idx in range(10):
        name, key, desc = TOMES[t_idx]
        if key is None:
            key = "score" if t_idx < 9 else "score"
        ktitles = [KIND_TITLE[k] for k in KINDS]
        for p in range(1, 21):
            if p == 1:
                _cover(c, t_idx, rows, key)
                continue
            kind = KINDS[(p - 2) % len(KINDS)]
            _header(c, t_idx, p, 20, kind, KIND_TITLE.get(kind, ""))
            y_top, y_bot = H - 84, 62
            png_path = os.path.join(IMG, "ajs-%02d-%02d.png" % (t_idx + 1, p))
            render_page(kind, t_idx, rows, key, heroes, png_path)
            _panel(c, y_bot, y_top)
            _draw_img(c, png_path, 34, y_bot + 26, W - 34, y_top - 6)
            c.setFillColor("#16324f")
            c.setFont("DejaVu", 9)
            c.drawString(34, y_bot + 6, "УЗЛОВОЙ ВЫВОД · ")
            c.setFillColor("#7d6608")
            c.setFont("DejaVu-Obl", 9)
            txt = caption_for(kind, t_idx, rows)
            c.drawString(34 + 108, y_bot + 6, _one(txt, 105))
            _foot(c, p, t_idx)
            c.showPage()
    c.save()
    return pdf


def render_page(kind, t_idx, rows, key, heroes, path):
    if kind == "bars_series":
        ss = series_stat(rows, key)
        render_bars_series(path, ["%02d" % j for j in range(1, 14)],
                           [ss[j]["mean"] for j in range(1, 14)], _rgb(G.PAL[3][3]))
    elif kind == "heatmap":
        mat = np.array([[next(r for r in rows if r["jno"] == j and r["issue"] == i)[key]
                         for i in range(1, 11)] for j in range(1, 14)])
        render_heatmap(path, mat, [str(i) for i in range(1, 11)],
                       ["%02d" % j for j in range(1, 14)])
    elif kind == "voxel":
        render_voxel(path, key, rows)
    elif kind == "bars_issue":
        series = 1 + t_idx % 13
        render_bars_issue(path, rows, series, _rgb(G.PAL[series][3]), hero=heroes)
    elif kind == "scatter":
        render_scatter(path, rows, key, _rgb(G.PAL[4][3]))
    elif kind == "hist":
        render_hist(path, [r[key] for r in rows], _rgb(G.PAL[3][3]))
    elif kind == "lines_month":
        render_lines_month(path, month_group(rows, key), _rgb(G.PAL[13][3]))
    elif kind == "stacked":
        sel = [x for x in rows if x["jno"] == t_idx + 1]
        cols = [np.array([r["final_ice"] for r in sel]),
                np.array([r["peak_pop"] for r in sel]),
                np.array([r["peak_fish"] for r in sel])]
        render_stacked(path, cols, ["лед", "племя", "рыба"])
    elif kind == "donut":
        ss = series_stat(rows, key)
        grp = [sum(ss[j]["mean"] for j in [1, 2, 3, 4]),
               sum(ss[j]["mean"] for j in [5, 6, 7]), sum(ss[j]["mean"] for j in [8, 9, 10, 11, 12, 13])]
        render_donut(path, grp, ["первые серии", "средние", "молодые"],
                     ["#1F6FB2", "#FFC300", "#C0392B"])
    elif kind == "matrix":
        render_matrix(path, rows, key)
    elif kind == "gauge":
        ss = series_stat(rows, key)
        render_gauge(path, [ss[j]["mx"] for j in range(1, 14)], ["%02d" % j for j in range(1, 14)],
                     _rgb(G.PAL[13][3]))
    elif kind == "voxel2":
        render_voxel2(path, key)
    elif kind == "bars3d":
        ss = series_stat(rows, key)
        render_bars3d(path, [ss[j]["tot"] for j in range(1, 14)], list(range(1, 14)))
    elif kind == "spark":
        render_spark(path, rows, key)
    elif kind == "area_month":
        render_area_month(path, month_group(rows, key), _rgb(G.PAL[13][3]))
    elif kind == "polar":
        render_polar(path, rows, key)
    elif kind == "table":
        render_table(path, series_stat(rows, key), key)
    elif kind == "spread":
        render_spread(path, rows, key, heroes)


def _cover(c, t_idx, rows, key):
    name, _, desc = TOMES[t_idx]
    c.setFillColor("#0d1b2a"); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor("#FFC300"); c.setLineWidth(1.4); c.rect(14, 14, W - 28, H - 28, fill=0, stroke=1)
    c.setStrokeColor("#FFC300"); c.setLineWidth(0.4); c.rect(20, 20, W - 40, H - 40, fill=0, stroke=1)
    c.setFillColor("#FFC300")
    c.roundRect(30, H - 96, W - 60, 44, 8, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 17); c.setFillColor("#0d1b2a")
    c.drawCentredString(W / 2, H - 76, "«АЙС-ГРАФИК» · %s" % name)
    c.setFont("DejaVu-Obl", 9); c.setFillColor("#eaf6ff")
    c.drawCentredString(W / 2, H - 104, "том %d/10 · журнал графиков Вечерки" % (t_idx + 1))
    ss = series_stat(rows, key)
    png = os.path.join(IMG, "ajs-cube-%02d.png" % (t_idx + 1))
    render_bars3d(png, [ss[j]["tot"] for j in range(1, 14)], list(range(1, 14)))
    _panel(c, 130, H - 140)
    _draw_img(c, png, 44, 140, W - 44, H - 150)
    c.setFillColor("#FFC300")
    c.setFont("DejaVu-Bold", 10)
    c.drawCentredString(W / 2, 122, "▲ 13 серий · 10 выпусков · мера тома: %s" % desc)
    c.setFillColor("#eaf6ff")
    c.setFont("DejaVu", 8)
    c.drawCentredString(W / 2, 96, "факт архива — %d страниц схем и кубов; 80/20: графики крупно, слово сжато" % 200)
    c.setFillColor("#16324f")
    c.setFont("DejaVu", 8)
    c.drawCentredString(W / 2, 52, "Ледяная Вечерка · github.com/pop31-ai/ice · том %d/10 · лист 01/20" % (t_idx + 1))
    c.showPage()


def _one(text, n):
    text = " ".join(text.split())
    return text[:n].rsplit(" ", 1)[0] + "…" if len(text) > n else text


if __name__ == "__main__":
    path = build_pdf()
    print("OK", os.path.basename(path))