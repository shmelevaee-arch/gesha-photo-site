// Фон главной: первый кадр показан всегда, при наведении на пункт меняется на кадр раздела.
(function () {
  var bg = document.getElementById('bg');
  var rows = document.querySelectorAll('[data-bg]');
  if (!bg || !rows.length) return;

  var layers = {};
  var defaultSrc = rows[0].dataset.bg;

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

  show(defaultSrc);

  rows.forEach(function (row) {
    row.addEventListener('mouseenter', function () { show(row.dataset.bg); });
    row.addEventListener('focus', function () { show(row.dataset.bg); });
    row.addEventListener('mouseleave', function () { show(defaultSrc); });
    row.addEventListener('blur', function () { show(defaultSrc); });
  });
})();
