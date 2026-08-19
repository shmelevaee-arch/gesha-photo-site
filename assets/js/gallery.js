// Собирает сетку галереи из images/manifest.json и открывает лайтбокс по клику.
// Манифест хранит размеры кадров — по ним задаём aspect-ratio, чтобы сетка не прыгала при загрузке.
(function () {
  var root = document.querySelector('[data-category]');
  if (!root) return;

  var category = root.dataset.category;
  var grid = root.querySelector('.gallery');
  var items = [];

  fetch('images/manifest.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      items = data[category] || [];
      render();
    })
    .catch(function (e) { console.error('Не удалось загрузить manifest.json', e); });

  // Ряды одинаковой высоты: каждый ряд заполняет ширину целиком, поэтому низ сетки
  // всегда ровный, а кадры сохраняют пропорции (ничего не обрезается).
  function targetHeight() {
    var w = window.innerWidth;
    if (w <= 560) return 260;
    if (w <= 900) return 320;
    if (w < 1400) return 380;
    return Math.min(560, Math.round(w * 0.26));
  }

  function gapPx() {
    var g = getComputedStyle(grid).gap;
    var n = parseFloat(g);
    return isNaN(n) ? 16 : n;
  }

  function maxPerRow() {
    var w = window.innerWidth;
    if (w <= 560) return 2;
    if (w <= 900) return 3;
    if (w < 1500) return 4;
    return 5;
  }

  // Разбиение на ряды методом динамического программирования (как в justified-галереях):
  // перебираем все допустимые разбиения с сохранением порядка кадров и выбираем то,
  // где высоты рядов меньше всего отклоняются от целевой — тогда ритм ровный,
  // а каждый ряд заполняет ширину целиком.
  function splitRows(list, total, gap) {
    var perRow = maxPerRow();
    var n = list.length;
    var ratios = list.map(function (it) { return it.w / it.h; });

    // целевую высоту считаем от самих кадров: сколько рядов получится при желаемом
    // масштабе, столько и делим — иначе ряды выходят разной высоты
    var sumRatio = ratios.reduce(function (a, b) { return a + b; }, 0);
    var base = targetHeight();
    var rowsCount = Math.max(Math.ceil(n / perRow), Math.round(sumRatio * base / total), 1);
    var target = total / (sumRatio / rowsCount);

    var cost = new Array(n + 1).fill(Infinity);
    var from = new Array(n + 1).fill(0);
    cost[0] = 0;

    for (var i = 0; i < n; i++) {
      if (cost[i] === Infinity) continue;
      var sum = 0;
      for (var k = 0; k < perRow && i + k < n; k++) {
        sum += ratios[i + k];
        var count = k + 1;
        var h = (total - gap * (count - 1)) / sum;
        var end = i + count;
        // штраф за отклонение высоты ряда от целевой; последний ряд судим мягче
        var penalty = Math.pow(h - target, 2);
        if (end === n) penalty *= 0.4;
        if (h > target * 2 || h < target * 0.45) penalty *= 6;
        if (cost[i] + penalty < cost[end]) {
          cost[end] = cost[i] + penalty;
          from[end] = i;
        }
      }
    }

    var bounds = [];
    for (var pos = n; pos > 0; pos = from[pos]) bounds.unshift([from[pos], pos]);

    return bounds.map(function (b) {
      var chunk = list.slice(b[0], b[1]);
      return {
        items: chunk,
        ratio: chunk.reduce(function (acc, it) { return acc + it.w / it.h; }, 0)
      };
    });
  }

  function render() {
    grid.innerHTML = '';
    var gap = gapPx();
    var total = grid.clientWidth || grid.getBoundingClientRect().width;
    var rows = splitRows(items, total, gap);
    var index = 0;

    // Высота ряда задаётся самими кадрами: ничего не обрезаем и не растягиваем.
    rows.forEach(function (r) {
      var free = total - gap * (r.items.length - 1);
      var h = free / r.ratio;

      var rowEl = document.createElement('div');
      rowEl.className = 'gallery__row';
      grid.appendChild(rowEl);

      var used = 0;

      r.items.forEach(function (item, k2) {
        var a = document.createElement('a');
        a.className = 'gallery__item';
        a.href = 'images/' + category + '/' + item.id + '-full.webp';
        a.dataset.index = index;
        var wpx = (k2 === r.items.length - 1) ? Math.round(free - used) : Math.floor(h * (item.w / item.h));
        used += wpx;
        a.style.width = wpx + 'px';
        a.style.height = Math.round(h) + 'px';

        var img = document.createElement('img');
        img.src = 'images/' + category + '/' + item.id + '-grid.webp';
        img.alt = (root.dataset.alt || 'Фото') + ' — кадр ' + (index + 1);
        img.loading = index < 8 ? 'eager' : 'lazy';
        img.decoding = 'async';

        a.appendChild(img);
        rowEl.appendChild(a);
        index++;
      });
    });

    renderedWidth = window.innerWidth;
  }

  var renderedWidth = 0;
  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      if (items.length && Math.abs(window.innerWidth - renderedWidth) > 40) render();
    }, 150);
  });

  // ---------- лайтбокс ----------
  var box = document.getElementById('lightbox');
  var boxImg = box.querySelector('img');
  var counter = box.querySelector('.lightbox__counter');
  var current = 0;

  function open(index) {
    current = index;
    show();
    box.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    box.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  function show() {
    var item = items[current];
    boxImg.src = 'images/' + category + '/' + item.id + '-full.webp';
    boxImg.alt = 'Фото ' + (current + 1) + ' из ' + items.length;
    counter.textContent = (current + 1) + ' / ' + items.length;
  }

  function step(delta) {
    current = (current + delta + items.length) % items.length;
    show();
  }

  grid.addEventListener('click', function (e) {
    var link = e.target.closest('.gallery__item');
    if (!link) return;
    e.preventDefault();
    open(Number(link.dataset.index));
  });

  box.addEventListener('click', function (e) {
    if (e.target === box || e.target.closest('.lightbox__close')) return close();
    if (e.target.closest('.lightbox__prev')) return step(-1);
    if (e.target.closest('.lightbox__next')) return step(1);
  });

  document.addEventListener('keydown', function (e) {
    if (!box.classList.contains('is-open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'ArrowRight') step(1);
  });

  // свайп на телефоне
  var startX = null;
  box.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
    startX = null;
  }, { passive: true });
})();
