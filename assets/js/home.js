// Главная: при наведении на раздел рядом с курсором появляется кадр из этого раздела.
// Приём перенесён с сайта Чаплыгиной (блок «Почитать»): карточка плывёт за курсором
// с инерцией и лёгким наклоном. Отличие — фото показано целиком, без обрезки:
// у карточки меняется пропорция под каждый кадр, а сами кадры сменяются через проявление.
(() => {
  const menu = document.querySelector('.stack__menu');
  if (!menu || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const rows = [...menu.querySelectorAll('.stack__row[data-cover]')];
  if (!rows.length) return;

  const cover = document.createElement('div');
  cover.className = 'hover-cover';
  cover.setAttribute('aria-hidden', 'true');
  cover.innerHTML = '<div class="hover-cover__card">' +
    rows.map((r) => `<img src="${r.dataset.cover}" alt="" decoding="async">`).join('') + '</div>';
  document.body.appendChild(cover); // в body, а не в меню: у строк меню есть transform, fixed внутри него ломается
  const card = cover.querySelector('.hover-cover__card');
  const imgs = [...card.querySelectorAll('img')];

  // Названия разделов короткие, поэтому кадр не висит у самого курсора (закрыл бы соседние пункты),
  // а стоит справа от списка и плывёт за курсором только по вертикали.
  const anchorX = () => menu.getBoundingClientRect().right + 48;

  let x = 0, y = 0, tx = 0, ty = 0, active = false, raf = 0;
  const loop = () => {
    const dy = ty - y;
    x += (tx - x) * 0.14;
    y += dy * 0.14;
    const tilt = Math.max(-5, Math.min(5, dy * -0.04)); // лёгкий наклон по скорости движения
    cover.style.transform = `translate3d(${x}px, ${y}px, 0) rotate(${tilt}deg)`;
    raf = active || Math.abs(dy) > 0.5 ? requestAnimationFrame(loop) : 0;
  };
  const kick = () => { if (!raf) raf = requestAnimationFrame(loop); };

  menu.addEventListener('pointermove', (e) => { tx = anchorX(); ty = e.clientY; kick(); });
  rows.forEach((row, i) => row.addEventListener('pointerenter', (e) => {
    if (!active) { x = tx = anchorX(); y = ty = e.clientY; }
    active = true;
    card.style.aspectRatio = row.dataset.ratio;
    imgs.forEach((img, j) => img.classList.toggle('is-active', j === i));
    cover.classList.add('is-on');
    kick();
  }));
  menu.addEventListener('pointerleave', () => { active = false; cover.classList.remove('is-on'); });
})();
