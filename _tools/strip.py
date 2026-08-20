# -*- coding: utf-8 -*-
"""Подбирает пять кадров для ленты на главной и переписывает блок .strip в index.html.

Правила отбора: каждый раздел представлен, кадры максимально разные по тону
и крупности плана, предпочтение выразительным (высокий контраст)."""
import io, json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TITLES = {"lovestory": ("Кадр из съёмки лавстори", "lovestory.html"),
          "family": ("Кадр из семейной съёмки", "family.html"),
          "personal": ("Кадр из индивидуальной съёмки", "personal.html")}
COUNT = 8


def distance(a, b):
    return abs(a["lum"] - b["lum"]) / 255.0 + abs(a.get("skin", 0) - b.get("skin", 0)) * 3


def main():
    manifest = json.load(io.open(os.path.join(ROOT, "images", "manifest.json"), encoding="utf-8"))
    pool = []
    for cat, items in manifest.items():
        for item in items:
            pool.append(dict(item, cat=cat))

    chosen = []
    # по одному лучшему кадру из каждого раздела — чтобы лента показывала всё портфолио
    for cat in TITLES:
        best = max((p for p in pool if p["cat"] == cat),
                   key=lambda p: p["con"] + p.get("skin", 0) * 40)
        chosen.append(best)
        pool.remove(best)

    # добираем самыми непохожими на уже выбранные
    while len(chosen) < COUNT:
        best = max(pool, key=lambda p: min(distance(p, c) for c in chosen) + p["con"] / 100)
        chosen.append(best)
        pool.remove(best)

    # раскладываем так, чтобы соседние кадры контрастировали
    order = [chosen.pop(0)]
    while chosen:
        nxt = max(chosen, key=lambda p: distance(p, order[-1]))
        chosen.remove(nxt)
        order.append(nxt)

    lines = []
    for n, item in enumerate(order):
        alt, href = TITLES[item["cat"]]
        loading = "eager" if n < 4 else "lazy"
        # пропорция задаётся контейнеру заранее — место под кадр зарезервировано,
        # поэтому лента не прыгает, пока подгружаются снимки
        lines.append(
            '    <a href="{href}" style="aspect-ratio: {w} / {h}">'
            '<img src="images/{cat}/{id}-grid.webp" alt="{alt}" width="{w}" height="{h}" '
            'loading="{loading}" decoding="async"></a>'.format(
                href=href, cat=item["cat"], id=item["id"], alt=alt,
                loading=loading, w=item["w"], h=item["h"]))

    p = os.path.join(ROOT, "index.html")
    html = io.open(p, encoding="utf-8", newline="").read()
    block = '  <div class="strip">\n' + "\n".join(lines) + "\n  </div>"
    html = re.sub(r'  <div class="strip">.*?</div>', block, html, flags=re.S)
    io.open(p, "w", encoding="utf-8", newline="\n").write(html)

    for item in order:
        print("{cat}/{id}  тон {lum:>5}  контраст {con:>5}  план {skin}".format(**item))


if __name__ == "__main__":
    main()
