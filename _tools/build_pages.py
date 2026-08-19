# -*- coding: utf-8 -*-
"""Собирает html-страницы из общего каркаса: шапка «имя · раздел» + бургер, светлая тема."""
import io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NAME = "Евгения Досаева"
INSTA = "https://www.instagram.com/gesha__ph/"
TG = "https://t.me/evgeshaa1707"
V = "43"  # версия ассетов, чтобы браузер не держал старый CSS

NAV = io.open(os.path.join(ROOT, "_tools", "nav_snippet.html"), encoding="utf-8").read().strip()

HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/base.css?v={v}">
<link rel="stylesheet" href="assets/css/page.css?v={v}">
</head>
<body>
<header class="topbar">
  <h1 class="topbar__title"><a href="index.html">{name}</a> <span>· {section}</span></h1>
  <button class="burger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="navmenu">
    <span></span><span></span><span></span>
  </button>
</header>

{nav}

'''

FOOT = '''
<footer class="foot">
  <p class="meta">Москва · студия и улица</p>
  <p class="meta"><a href="{insta}" target="_blank" rel="noopener">Instagram</a> &nbsp;·&nbsp; <a href="{tg}" target="_blank" rel="noopener">Telegram</a></p>
</footer>

<p class="disclaimer">Instagram принадлежит компании Meta, признанной экстремистской организацией и запрещённой на территории РФ.</p>

<script src="assets/js/nav.js?v={v}"></script>
{extra}
</body>
</html>
'''


def head(title, desc, section):
    return HEAD.format(title=title, desc=desc, section=section, name=NAME, nav=NAV, v=V)


def foot(extra=""):
    return FOOT.format(insta=INSTA, tg=TG, v=V, extra=extra)


def gallery_page(slug, section, desc):
    body = '''<main class="page" data-category="{slug}" data-alt="{section}">
  <div class="gallery"></div>
</main>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Просмотр фотографии">
  <button class="lightbox__close" type="button" aria-label="Закрыть">✕</button>
  <button class="lightbox__btn lightbox__prev" type="button" aria-label="Предыдущее фото">←</button>
  <img src="" alt="">
  <button class="lightbox__btn lightbox__next" type="button" aria-label="Следующее фото">→</button>
  <span class="lightbox__counter meta"></span>
</div>
'''.format(slug=slug, section=section)
    html = head("{} — {}, фотограф".format(section, NAME), desc, section) + body + foot(
        '<script src="assets/js/gallery.js?v={}"></script>'.format(V))
    io.open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8", newline="\n").write(html)
    print("собрал", slug + ".html")


gallery_page("lovestory", "Лавстори",
             "Съёмки для пар: лавстори в студии, на улице и в городе. Фотограф Евгения Досаева, Москва.")
gallery_page("family", "Семья",
             "Семейные и детские съёмки на природе и в студии. Фотограф Евгения Досаева, Москва.")
gallery_page("personal", "Персональные",
             "Индивидуальные портретные съёмки в студии и на улице. Фотограф Евгения Досаева, Москва.")


def content_page(slug, section, desc, body):
    html = head("{} — {}, фотограф".format(section, NAME), desc, section) + body + foot()
    io.open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8", newline="\n").write(html)
    print("собрал", slug + ".html")


PRICES = '''<main class="page">
  <div class="content split">
    <div class="split__media">
      <img src="images/personal/04-grid.webp" alt="Кадр с индивидуальной съёмки" loading="eager" decoding="async">
    </div>

    <div>
      <div class="page__head"><h2 class="page__title">Цены</h2></div>

      <section class="price">
        <h3 class="price__name">Индивидуальная портретная съёмка</h3>
        <p class="price__value">10 000 ₽</p>
        <p class="price__label">Что входит</p>
        <ul class="plain">
          <li>консультация перед съёмкой</li>
          <li>помощь с подбором образа</li>
          <li>работа с позированием во время съёмки</li>
          <li>1,5 часа съёмки</li>
          <li>50+ фотографий в цветокоррекции</li>
          <li>10 фотографий в детальной ретуши</li>
          <li>готовность материала до 14 дней</li>
        </ul>
        <div class="price__loc">
          <p class="price__label">Локация</p>
          <p class="plain-text">Студия, улица, кафе или другое место по договорённости.</p>
        </div>
      </section>

      <section class="price">
        <h3 class="price__name">Парная или семейная съёмка</h3>
        <p class="price__value">12 000 ₽</p>
        <p class="price__label">Что входит</p>
        <ul class="plain">
          <li>консультация перед съёмкой</li>
          <li>помощь с подбором образов</li>
          <li>работа с позированием во время съёмки</li>
          <li>1,5 часа съёмки</li>
          <li>50+ фото в цветокоррекции</li>
          <li>10 фото в детальной ретуши</li>
          <li>готовность до 14 дней</li>
        </ul>
        <div class="price__loc">
          <p class="price__label">Локация</p>
          <p class="plain-text">По договорённости.</p>
        </div>
      </section>

      <section class="price">
        <h3 class="price__name">Дополнительно</h3>
        <p class="price__label">При необходимости оплачивается отдельно</p>
        <ul class="plain">
          <li>аренда студии</li>
          <li>услуги визажиста</li>
          <li>дополнительный час съёмки — 5 000 ₽</li>
        </ul>
      </section>

      <section class="price">
        <h3 class="price__name">Записаться</h3>
        <p class="plain-text">Напишите в Telegram желаемую дату и задачу съёмки — отвечу и подберу время.</p>
        <a class="cta" href="{tg}" target="_blank" rel="noopener">Telegram — @evgeshaa1707</a>
      </section>
    </div>
  </div>
</main>
'''.format(insta=INSTA, tg=TG)

content_page("prices", "Цены",
             "Стоимость съёмок: индивидуальная портретная — 10 000 ₽, парная или семейная — 12 000 ₽. Москва.",
             PRICES)

