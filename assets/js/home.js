// Меняет фоновое фото при наведении на пункт меню.
// Картинки создаются один раз и переиспользуются, чтобы не дёргать сеть на каждый ховер.
(function () {
  var bg = document.getElementById('bg');
  var rows = document.querySelectorAll('.menu__row');
  if (!bg || !rows.length) return;

  var layers = {};

  rows.forEach(function (row) {
    var src = row.dataset.bg;
    if (!src || layers[src]) return;
    var img = new Image();
    img.src = src;
    img.alt = '';
    img.decoding = 'async';
    bg.appendChild(img);
    layers[src] = img;
  });

  function show(src) {
    Object.keys(layers).forEach(function (key) {
      layers[key].classList.toggle('is-active', key === src);
    });
  }

  function clear() {
    Object.keys(layers).forEach(function (key) {
      layers[key].classList.remove('is-active');
    });
  }

  rows.forEach(function (row) {
    row.addEventListener('mouseenter', function () { show(row.dataset.bg); });
    row.addEventListener('focus', function () { show(row.dataset.bg); });
    row.addEventListener('mouseleave', clear);
    row.addEventListener('blur', clear);
  });
})();
