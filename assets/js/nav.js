// Бургер: открывает список разделов поверх страницы, закрывается по Escape и по клику по пункту.
(function () {
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('navmenu');
  if (!burger || !menu) return;

  function toggle(open) {
    burger.classList.toggle('is-open', open);
    menu.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
  }

  burger.addEventListener('click', function () {
    toggle(!menu.classList.contains('is-open'));
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) toggle(false);
  });
})();
