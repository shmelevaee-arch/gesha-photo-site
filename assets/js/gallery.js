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

  function render() {
    var frag = document.createDocumentFragment();
    items.forEach(function (item, i) {
      var a = document.createElement('a');
      a.className = 'gallery__item';
      a.href = 'images/' + category + '/' + item.id + '-full.webp';
      a.dataset.index = i;

      var img = document.createElement('img');
      img.src = 'images/' + category + '/' + item.id + '-grid.webp';
      img.alt = root.dataset.alt ? root.dataset.alt + ' — кадр ' + (i + 1) : 'Фото ' + (i + 1);
      img.loading = i < 4 ? 'eager' : 'lazy';
      img.decoding = 'async';
      img.width = item.w;
      img.height = item.h;
      img.style.aspectRatio = item.w + ' / ' + item.h;

      a.appendChild(img);
      frag.appendChild(a);
    });
    grid.appendChild(frag);
  }

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
