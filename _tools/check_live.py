# -*- coding: utf-8 -*-
"""Проверяет опубликованный сайт: страницы, внутренние ссылки, картинки, мета-теги."""
import json, re, sys, urllib.error, urllib.request

BASE = "https://shmelevaee-arch.github.io/gesha-photo-site/"
PAGES = ["", "lovestory.html", "family.html", "personal.html", "prices.html"]


def get(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "site-check"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace") if method == "GET" else ""
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, str(e)


def main():
    problems = []
    checked = set()

    for page in PAGES:
        url = BASE + page
        status, html = get(url)
        name = page or "index.html"
        if status != 200:
            problems.append(f"{name}: код {status}")
            continue

        title = re.search(r"<title>(.*?)</title>", html)
        desc = re.search(r'name="description" content="(.*?)"', html)
        lang = re.search(r'<html lang="(.*?)"', html)
        print(f"[{status}] {name}")
        print(f"      title: {title.group(1) if title else 'НЕТ'}")
        if not desc:
            problems.append(f"{name}: нет meta description")
        if not lang or lang.group(1) != "ru":
            problems.append(f"{name}: не указан lang=ru")
        if "favicon" not in html:
            problems.append(f"{name}: нет иконки сайта (favicon)")

        # внутренние ссылки и ресурсы
        refs = set(re.findall(r'(?:href|src)="(?!https?:|mailto:|#)([^"]+)"', html))
        for ref in sorted(refs):
            target = BASE + ref.split("?")[0]
            if target in checked:
                continue
            checked.add(target)
            code, _ = get(target, "HEAD")
            if code != 200:
                problems.append(f"{name}: битая ссылка {ref} -> {code}")

        # внешние ссылки
        for ext in sorted(set(re.findall(r'href="(https?://[^"]+)"', html))):
            if ext in checked:
                continue
            checked.add(ext)
            code, _ = get(ext, "HEAD")
            if code >= 400:
                problems.append(f"{name}: внешняя ссылка {ext} -> {code}")

    # все картинки из манифеста
    status, raw = get(BASE + "images/manifest.json")
    manifest = json.loads(raw)
    total = 0
    for cat, items in manifest.items():
        for item in items:
            for kind in ("grid", "full"):
                total += 1
                code, _ = get(f"{BASE}images/{cat}/{item['id']}-{kind}.webp", "HEAD")
                if code != 200:
                    problems.append(f"картинка {cat}/{item['id']}-{kind}.webp -> {code}")
    print(f"\nпроверено картинок: {total}")

    print("\n--- ИТОГ ---")
    if problems:
        for p in problems:
            print("!", p)
    else:
        print("проблем не найдено")
    return 1 if problems else 0


sys.exit(main())
