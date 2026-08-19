# -*- coding: utf-8 -*-
"""Считает пропорции и тональность каждого кадра и раскладывает галерею как композицию:
чередует вертикальные и горизонтальные, светлые и тёмные, держит колонки равными по высоте."""
import io, json, os
from PIL import Image, ImageStat

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES = os.path.join(ROOT, "images")
CATEGORIES = ["lovestory", "family", "personal"]


def measure(path):
    """Возвращает размеры, тон, контраст и «крупность плана».
    Крупность считаем по доле пикселей телесного тона: на портрете крупным планом
    кожи в кадре много, на общем — мало."""
    with Image.open(path) as im:
        rgb = im.convert("RGB")
        w, h = rgb.size
        small = rgb.resize((80, 80))
        grey = small.convert("L")
        lum = ImageStat.Stat(grey).mean[0]
        contrast = ImageStat.Stat(grey).stddev[0]

        skin = 0
        px = small.load()
        for y in range(80):
            for x in range(80):
                r, g, b = px[x, y]
                mx, mn = max(r, g, b), min(r, g, b)
                if r > 95 and g > 40 and b > 20 and mx - mn > 15 and r > g > b and abs(r - g) > 12:
                    skin += 1
        skin_ratio = skin / 6400.0
    return w, h, round(lum, 1), round(contrast, 1), round(skin_ratio, 3)


def main():
    manifest = json.load(io.open(os.path.join(IMAGES, "manifest.json"), encoding="utf-8"))
    for cat in CATEGORIES:
        items = manifest.get(cat, [])
        for item in items:
            path = os.path.join(IMAGES, cat, item["id"] + "-full.webp")
            w, h, lum, contrast, skin = measure(path)
            item["w"], item["h"] = w, h
            item["r"] = round(h / w, 3)      # >1 вертикальный, <1 горизонтальный
            item["lum"] = lum
            item["con"] = contrast
            item["skin"] = skin              # чем больше, тем крупнее план
        manifest[cat] = arrange(items)
        tone = "".join("O" if i["lum"] > 150 else ("o" if i["lum"] > 90 else ".") for i in manifest[cat])
        plan = "".join("K" if i["skin"] > 0.18 else ("s" if i["skin"] > 0.07 else "-") for i in manifest[cat])
        print(f"{cat}: {len(items)} кадров")
        print(f"  тон  {tone}   (O светлый, o средний, . тёмный)")
        print(f"  план {plan}   (K крупный, s средний, - общий)")
    json.dump(manifest, io.open(os.path.join(IMAGES, "manifest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


def arrange(items):
    """Собирает ритм: соседние кадры должны различаться по тону (светлый/тёмный),
    по крупности плана (портрет/общий) и по форме (вертикальный/горизонтальный).
    Считается разница с двумя предыдущими кадрами — так ритм держится на всей ленте,
    а не только между парами."""
    if not items:
        return items

    pool = list(items)
    # начинаем с самого выразительного кадра — он открывает галерею
    pool.sort(key=lambda i: -(i["con"] + i["skin"] * 60))
    result = [pool.pop(0)]

    while pool:
        prev = result[-1]
        prev2 = result[-2] if len(result) > 1 else None
        best, best_score = None, None
        for cand in pool:
            tone = abs(cand["lum"] - prev["lum"]) / 255.0
            plan = abs(cand["skin"] - prev["skin"]) * 3
            shape = min(abs(cand["r"] - prev["r"]), 0.6)
            score = tone * 1.0 + plan * 1.0 + shape * 0.8
            if prev2:  # мягкий штраф за повтор через один
                score -= (1 - abs(cand["lum"] - prev2["lum"]) / 255.0) * 0.25
            if best_score is None or score > best_score:
                best, best_score = cand, score
        pool.remove(best)
        result.append(best)
    return result


if __name__ == "__main__":
    main()
