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

  function columnCount() {
    if (window.innerWidth <= 560) return 2;
    if (window.innerWidth < 1200) return 3;
    return 4;  // как в шаблоне-прототипе: четыре колонки на десктопе
  }

  // Раскладываем кадры по колонкам: каждый следующий уходит в самую короткую колонку,
  // чтобы низ галереи получался ровным независимо от пропорций фото.
  function render() {
    var cols = columnCount();
    grid.innerHTML = '';
    var heights = [];
    var nodes = [];

    for (var c = 0; c < cols; c++) {
      var col = document.createElement('div');
      col.className = 'gallery__col';
      grid.appendChild(col);
      nodes.push(col);
      heights.push(0);
    }

    items.forEach(function (item, i) {
      // кадры идут по кругу — так ритм из манифеста (тон, крупность плана, форма)
      // читается по горизонтали; в короткую колонку уходим, только если она заметно отстала
      var target = i % cols;
      var shortest = heights.indexOf(Math.min.apply(null, heights));
      if (heights[target] - heights[shortest] > 0.9) target = shortest;

      var a = document.createElement('a');
      a.className = 'gallery__item';
      a.href = 'images/' + category + '/' + item.id + '-full.webp';
      a.dataset.index = i;

      var img = document.createElement('img');
      img.src = 'images/' + category + '/' + item.id + '-grid.webp';
      img.alt = (root.dataset.alt || 'Фото') + ' — кадр ' + (i + 1);
      img.loading = i < cols * 2 ? 'eager' : 'lazy';
      img.decoding = 'async';
      img.width = item.w;
      img.height = item.h;

      a.appendChild(img);
      nodes[target].appendChild(a);
      heights[target] += item.h / item.w;
    });

    levelOut(nodes, heights);
    renderedCols = cols;
  }

  // Доводит низ колонок: пробует перенести один из последних кадров самой длинной
  // колонки в самую короткую и оставляет тот перенос, который сильнее сокращает разрыв.
  // Кадры при этом не обрезаются и не масштабируются — меняется только их порядок.
  function levelOut(nodes, heights) {
    for (var pass = 0; pass < 30; pass++) {
      var max = heights.indexOf(Math.max.apply(null, heights));
      var min = heights.indexOf(Math.min.apply(null, heights));
      if (max === min) return;
      var diff = heights[max] - heights[min];
      var kids = nodes[max].children;
      if (kids.length < 2) return;

      var bestNode = null, bestDiff = diff, bestH = 0;
      for (var k = Math.max(0, kids.length - 3); k < kids.length; k++) {
        var img = kids[k].querySelector('img');
        var itemH = img.height / img.width;
        var after = Math.abs((heights[max] - itemH) - (heights[min] + itemH));
        if (after < bestDiff) { bestDiff = after; bestNode = kids[k]; bestH = itemH; }
      }
      if (!bestNode) return;

      nodes[min].appendChild(bestNode);
      heights[max] -= bestH;
      heights[min] += bestH;
    }
  }

  var renderedCols = 0;
  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      if (items.length && columnCount() !== renderedCols) render();
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
