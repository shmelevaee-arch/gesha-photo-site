# -*- coding: utf-8 -*-
"""Собирает html-страницы из общего каркаса: шапка «имя · раздел» + бургер, светлая тема."""
import io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NAME = "Евгения Досаева"
INSTA = "https://www.instagram.com/gesha__ph/"
V = "5"  # версия ассетов, чтобы браузер не держал старый CSS

NAV = io.open(os.path.join(ROOT, "_tools", "nav_snippet.html"), encoding="utf-8").read().strip()

HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
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
  <p class="meta">Съёмки в Москве и с выездом</p>
  <p class="meta"><a href="{insta}" target="_blank" rel="noopener">Instagram — @gesha__ph</a></p>
</footer>

<script src="assets/js/nav.js?v={v}"></script>
{extra}
</body>
</html>
'''


def head(title, desc, section):
    return HEAD.format(title=title, desc=desc, section=section, name=NAME, nav=NAV, v=V)


def foot(extra=""):
    return FOOT.format(insta=INSTA, v=V, extra=extra)


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
      <p class="lead">Съёмка начинается с разговора: обсуждаем задачу, место и образы, чтобы в кадре вы были собой, а не позировали на камеру.</p>

      <section class="block">
        <h3 class="block__title">Съёмки</h3>
        <div class="row">
          <span class="row__name">Индивидуальная портретная<span class="row__note">студия, улица, кафе или другое место по договорённости</span></span>
          <span class="row__value">10 000 ₽</span>
        </div>
        <div class="row">
          <span class="row__name">Парная или семейная<span class="row__note">локация по договорённости</span></span>
          <span class="row__value">12 000 ₽</span>
        </div>
      </section>

      <section class="block">
        <h3 class="block__title">Что входит</h3>
        <ul class="plain">
          <li>консультация перед съёмкой</li>
          <li>помощь с подбором образа</li>
          <li>работа с позированием во время съёмки</li>
          <li>1,5 часа съёмки</li>
          <li>50+ фотографий в цветокоррекции</li>
          <li>10 фотографий в детальной ретуши</li>
          <li>готовность материала до 14 дней</li>
        </ul>
      </section>

      <section class="block">
        <h3 class="block__title">Оплачивается отдельно</h3>
        <div class="row"><span class="row__name">Аренда студии</span><span class="row__value">по тарифу студии</span></div>
        <div class="row"><span class="row__name">Услуги визажиста</span><span class="row__value">по тарифу мастера</span></div>
        <div class="row"><span class="row__name">Дополнительный час съёмки</span><span class="row__value">5 000 ₽</span></div>
      </section>

      <section class="block">
        <h3 class="block__title">Как записаться</h3>
        <p class="lead">Напишите в директ желаемую дату и задачу съёмки — отвечу и подберу время.</p>
        <a class="cta" href="{insta}" target="_blank" rel="noopener">Написать в Instagram</a>
      </section>
    </div>
  </div>
</main>
'''.format(insta=INSTA)

content_page("prices", "Цены",
             "Стоимость съёмок: индивидуальная портретная — 10 000 ₽, парная или семейная — 12 000 ₽. Москва.",
             PRICES)

ABOUT = '''<main class="page">
  <div class="content split">
    <div class="split__media">
      <img src="images/personal/03-grid.webp" alt="Портрет с индивидуальной съёмки" loading="eager" decoding="async">
    </div>

    <div>
      <div class="page__head"><h2 class="page__title">О себе</h2></div>
      <p class="lead">Меня зовут Евгения, я снимаю людей в Москве — портреты, пары и семьи.</p>
      <p class="lead">Мне важно, чтобы на фотографиях человек был похож на себя, а не на удачную позу. Поэтому съёмка всегда начинается с разговора: обсуждаем, для чего вам эти кадры, где вам будет комфортно и какие образы стоит взять с собой. На самой съёмке я подсказываю, как встать и куда смотреть, — от вас не требуется опыта перед камерой.</p>

      <section class="block">
        <h3 class="block__title">Как проходит съёмка</h3>
        <div class="row"><span class="row__name">Созвон или переписка</span><span class="row__value">до съёмки</span></div>
        <div class="row"><span class="row__name">Сама съёмка</span><span class="row__value">1,5 часа</span></div>
        <div class="row"><span class="row__name">Отбор и цветокоррекция</span><span class="row__value">50+ кадров</span></div>
        <div class="row"><span class="row__name">Детальная ретушь</span><span class="row__value">10 кадров</span></div>
        <div class="row"><span class="row__name">Готовность материала</span><span class="row__value">до 14 дней</span></div>
      </section>

      <section class="block">
        <h3 class="block__title">Что снимаю</h3>
        <ul class="plain">
          <li>индивидуальные портретные съёмки</li>
          <li>лавстори и парные съёмки</li>
          <li>семейные и детские съёмки</li>
        </ul>
        <a class="cta" href="prices.html">Посмотреть цены</a>
      </section>
    </div>
  </div>
</main>
'''

CONTACTS = '''<main class="page">
  <div class="content split">
    <div class="split__media">
      <img src="images/lovestory/05-grid.webp" alt="Кадр с парной съёмки" loading="eager" decoding="async">
    </div>

    <div>
      <div class="page__head"><h2 class="page__title">Контакты</h2></div>
      <p class="lead">Чтобы записаться, напишите в директ желаемую дату и задачу съёмки — отвечу и подберу время.</p>

      <section class="block">
        <h3 class="block__title">Связаться</h3>
        <div class="row"><span class="row__name">Instagram</span><span class="row__value"><a href="{insta}" target="_blank" rel="noopener">@gesha__ph</a></span></div>
        <div class="row"><span class="row__name">Город</span><span class="row__value">Москва</span></div>
        <div class="row"><span class="row__name">Выезд</span><span class="row__value">по договорённости</span></div>
      </section>

      <section class="block">
        <h3 class="block__title">Съёмки</h3>
        <ul class="plain">
          <li>индивидуальные портретные</li>
          <li>парные и лавстори</li>
          <li>семейные и детские</li>
        </ul>
        <a class="cta" href="{insta}" target="_blank" rel="noopener">Написать в директ</a>
      </section>
    </div>
  </div>
</main>
'''.format(insta=INSTA)

content_page("about", "О себе",
             "Фотограф Евгения Досаева: как проходит съёмка, подход к работе, что вы получаете в результате. Москва.",
             ABOUT)
content_page("contacts", "Контакты",
             "Записаться на съёмку к фотографу Евгении Досаевой: напишите в Instagram-директ дату и задачу съёмки. Москва.",
             CONTACTS)
