# -*- coding: utf-8 -*-
"""Технический аудит сайта: коды ответа, мета, заголовки, alt, ссылки, вес страниц."""
import io, re, sys, urllib.error, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://www.geshaph.ru"
PAGES = ["/", "/lovestory.html", "/family.html", "/personal.html", "/prices.html", "/about.html"]


def get(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "audit"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read() if method == "GET" else b""
            return r.status, body.decode("utf-8", "replace"), dict(r.headers), r.url
    except urllib.error.HTTPError as e:
        return e.code, "", {}, url
    except Exception as e:
        return 0, str(e), {}, url


def main():
    problems, info = [], []

    # robots и sitemap
    for f in ("robots.txt", "sitemap.xml"):
        code, body, _, _ = get(BASE + "/" + f)
        info.append("%s: %s" % (f, code))
        if code != 200:
            problems.append("%s недоступен (код %s)" % (f, code))

    # 404
    code, _, _, _ = get(BASE + "/takoy-stranicy-net-123")
    info.append("несуществующая страница: код %s" % code)
    if code != 404:
        problems.append("несуществующий адрес отдаёт %s вместо 404" % code)

    for page in PAGES:
        url = BASE + page
        code, html, headers, final = get(url)
        name = page or "/"
        if code != 200:
            problems.append("%s: код %s" % (name, code))
            continue

        title = re.search(r"<title>(.*?)</title>", html, re.S)
        desc = re.search(r'name="description" content="(.*?)"', html)
        canon = re.search(r'rel="canonical" href="(.*?)"', html)
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)
        schema = "application/ld+json" in html or "itemscope" in html
        imgs = re.findall(r"<img[^>]*>", html)
        no_alt = [i for i in imgs if 'alt="' not in i]
        empty_alt = [i for i in imgs if 'alt=""' in i]
        lang = re.search(r'<html lang="(.*?)"', html)
        viewport = 'name="viewport"' in html
        weight = len(html.encode("utf-8")) / 1024

        info.append("%s: %.0f КБ, h1=%d, h2=%d, img=%d (без alt %d)" %
                    (name, weight, len(h1), len(h2), len(imgs), len(no_alt)))

        if not title: problems.append("%s: нет title" % name)
        elif len(re.sub("<.*?>", "", title.group(1)).strip()) > 65:
            problems.append("%s: title длиннее 65 знаков" % name)
        if not desc: problems.append("%s: нет description" % name)
        if not canon: problems.append("%s: нет canonical" % name)
        if len(h1) == 0: problems.append("%s: нет H1" % name)
        if len(h1) > 1: problems.append("%s: несколько H1 (%d)" % (name, len(h1)))
        if not schema: problems.append("%s: нет микроразметки Schema.org" % name)
        if no_alt: problems.append("%s: %d картинок без alt" % (name, len(no_alt)))
        if not lang: problems.append("%s: не указан язык страницы" % name)
        if not viewport: problems.append("%s: нет viewport (мобильная адаптация)" % name)

    print("--- ФАКТЫ ---")
    for i in info: print(" ", i)
    print("--- ПРОБЛЕМЫ (%d) ---" % len(problems))
    for p in problems: print(" !", p)


main()
