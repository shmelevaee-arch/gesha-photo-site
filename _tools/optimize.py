# -*- coding: utf-8 -*-
"""Готовит веб-версии фото: из _raw/<категория>/*.jpg делает images/<категория>/NN-{grid,full}.webp
и пишет images/manifest.json с размерами (нужны, чтобы сетка не прыгала при загрузке)."""
import json, os
from PIL import Image, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "_raw")
OUT = os.path.join(ROOT, "images")

CATEGORIES = ["lovestory", "family", "personal"]
GRID_W = 1100   # превью в сетке
FULL_W = 2000   # версия для лайтбокса
QUALITY_GRID = 78
QUALITY_FULL = 82


def resize(img, target_w):
    if img.width <= target_w:
        return img.copy()
    h = round(img.height * target_w / img.width)
    return img.resize((target_w, h), Image.LANCZOS)


def main():
    manifest = {}
    for cat in CATEGORIES:
        src_dir = os.path.join(RAW, cat)
        dst_dir = os.path.join(OUT, cat)
        if not os.path.isdir(src_dir):
            print(f"пропуск {cat}: нет папки")
            continue
        os.makedirs(dst_dir, exist_ok=True)
        files = sorted(f for f in os.listdir(src_dir) if f.lower().endswith((".jpg", ".jpeg", ".png")))
        items = []
        for n, name in enumerate(files, 1):
            with Image.open(os.path.join(src_dir, name)) as im:
                im = ImageOps.exif_transpose(im).convert("RGB")
                stem = f"{n:02d}"
                grid = resize(im, GRID_W)
                grid.save(os.path.join(dst_dir, f"{stem}-grid.webp"), "WEBP", quality=QUALITY_GRID, method=6)
                full = resize(im, FULL_W)
                full.save(os.path.join(dst_dir, f"{stem}-full.webp"), "WEBP", quality=QUALITY_FULL, method=6)
                items.append({"id": stem, "w": full.width, "h": full.height})
                print(f"{cat}/{stem}: {im.width}x{im.height} -> grid {grid.width}, full {full.width}", flush=True)
        manifest[cat] = items
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print(f"Готово. images/ весит {total/1024/1024:.1f} МБ")


if __name__ == "__main__":
    main()
