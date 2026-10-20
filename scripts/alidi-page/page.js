(function () {
  // Архив прежней страницы: раскрывается кнопкой «Посмотреть»
  var arch = document.getElementById('archive'), archBtn = document.getElementById('arch-btn');
  function openArch(scroll) {
    arch.hidden = false; archBtn.setAttribute('aria-expanded', 'true'); archBtn.textContent = 'Свернуть';
    var v = arch.querySelector('.hero-bg'); if (v && v.paused) { var pp = v.play(); if (pp && pp.catch) pp.catch(function () {}); }
    if (scroll) arch.scrollIntoView({ behavior: 'smooth' });
  }
  archBtn.addEventListener('click', function () {
    if (arch.hidden) openArch(true);
    else { arch.hidden = true; archBtn.setAttribute('aria-expanded', 'false'); archBtn.textContent = 'Посмотреть'; }
  });
  document.querySelectorAll('a[href="#archive-open"]').forEach(function (l) { l.addEventListener('click', function () { openArch(false); }); });

  // Счётчик до юбилея и шкала: сегодня → старт съёмок → сдача → 26.08.2027
  var DAY = 864e5, now = new Date(); now.setHours(0, 0, 0, 0);
  var end = new Date(2027, 7, 26), days = Math.max(0, Math.round((end - now) / DAY));
  document.getElementById('days').textContent = days;
  var span = end - now;
  document.querySelectorAll('.mk[data-d]').forEach(function (m) {
    var p = m.dataset.d.split('-'), d = new Date(+p[0], +p[1] - 1, +p[2]);
    m.style.setProperty('--p', Math.min(100, Math.max(0, (d - now) / span * 100)).toFixed(1) + '%');
  });

  // Фоновая нарезка: запускаем сами (Safari в энергосбережении игнорирует autoplay),
  // при отказе пробуем снова на первом движении, прокрутке или касании
  var bg = document.querySelector('.hero-bg');
  if (bg && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    bg.muted = true; bg.defaultMuted = true; bg.setAttribute('muted', '');
    var kick = function () { if (bg.paused) { var p = bg.play(); if (p && p.catch) p.catch(function () {}); } };
    kick();
    bg.addEventListener('canplay', kick);
    ['pointermove', 'scroll', 'touchstart', 'keydown', 'click'].forEach(function (t) {
      addEventListener(t, kick, { passive: true });
    });
    document.addEventListener('visibilitychange', function () { if (!document.hidden) kick(); });
  }

  // Карта площадок рисуется, когда доходит до экрана
  var geo = document.querySelector('.geo');
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en, ob) { if (en[0].isIntersecting) { geo.classList.add('in'); ob.disconnect(); } }, { threshold: .35 }).observe(geo);
  } else geo.classList.add('in');

  // «Что уже снимали»: строка слева → кадры и кейс справа
  var rows = document.querySelectorAll('.m-row'), panes = document.querySelectorAll('.m-pane');
  rows.forEach(function (r) {
    function go() {
      rows.forEach(function (x) { x.classList.toggle('on', x === r); x.setAttribute('aria-selected', x === r); });
      panes.forEach(function (p) { p.classList.toggle('on', p.dataset.i === r.dataset.i); });
    }
    r.addEventListener('click', go);
    r.addEventListener('mouseenter', function () { if (matchMedia('(hover:hover)').matches) go(); });
  });

  // Ролики: обложка → плеер на месте, шоурил в окне
  document.querySelectorAll('.vid').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.vid video').forEach(function (v) { v.pause(); });
      var v = document.createElement('video');
      v.src = b.dataset.video; v.controls = true; v.autoplay = true; v.playsInline = true; v.preload = 'auto';
      var box = document.createElement('div');
      box.className = 'vid'; box.appendChild(v);
      b.replaceWith(box);
      v.play().catch(function () {});
    });
  });
  var modal = document.getElementById('modal'), mv = modal.querySelector('.mv');
  function closeModal() { mv.innerHTML = ''; modal.hidden = true; document.body.style.overflow = ''; }
  document.querySelectorAll('.vid-inline').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.vid video').forEach(function (v) { v.pause(); });
      mv.innerHTML = '<video controls autoplay playsinline src="' + b.dataset.video + '"></video>';
      modal.hidden = false; document.body.style.overflow = 'hidden';
    });
  });
  modal.addEventListener('click', function (ev) { if (ev.target === modal || ev.target.classList.contains('x')) closeModal(); });
  addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && !modal.hidden) closeModal(); });

  // Фильтр «Все остальные проекты»
  var tabs = document.querySelectorAll('.tabs button'), cards = document.querySelectorAll('.card');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (x) { x.classList.toggle('on', x === t); });
      cards.forEach(function (c) { c.classList.toggle('hide', t.dataset.f !== '*' && c.dataset.k !== t.dataset.f); });
    });
  });
})();

// «Как снимаем»: портреты и главы запускают ролик с нужной секунды; один ролик играет за раз
(function () {
  document.querySelectorAll('.tp, .pc').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = document.getElementById(b.dataset.p), t = parseFloat(b.dataset.t);
      document.querySelectorAll('.how video').forEach(function (x) { if (x !== v) x.pause(); });
      var go = function () { v.currentTime = t; var pp = v.play(); if (pp && pp.catch) pp.catch(function () {}); };
      if (v.readyState >= 1) go(); else { v.preload = 'auto'; v.addEventListener('loadedmetadata', go, { once: true }); v.load(); }
      b.parentNode.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
    });
  });
  document.querySelectorAll('.how video').forEach(function (v) {
    v.addEventListener('play', function () { document.querySelectorAll('.how video').forEach(function (x) { if (x !== v) x.pause(); }); });
  });
})();

// Карты: немые петли играют только на экране
(function () {
  var vs = document.querySelectorAll('.mp-v');
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (en) {
    en.forEach(function (x) {
      var v = x.target;
      if (x.isIntersecting) { if (!v.src) v.src = v.dataset.src; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      else v.pause();
    });
  }, { threshold: .35 });
  vs.forEach(function (v) { v.muted = true; io.observe(v); });
})();

// Драфт-бюджет: подсказки «?», «Раскрыть всё», переход к разделу из сводки
(function () {
  var bud = document.getElementById('budget');
  if (!bud) return;
  var tips = bud.querySelectorAll('.tip');
  function place(w) {
    // на телефоне подсказка снизу экрана (CSS), на широком держим её в пределах окна
    var b = w.querySelector('.tip-b');
    b.style.marginLeft = ''; b.style.removeProperty('--ax'); w.classList.remove('below');
    if (innerWidth <= 640) return;
    if (getComputedStyle(b).display === 'none') return;
    var r = b.getBoundingClientRect(), shift = 0;
    if (r.left < 12) shift = 12 - r.left; else if (r.right > innerWidth - 12) shift = innerWidth - 12 - r.right;
    if (shift) { b.style.marginLeft = (-150 + shift) + 'px'; b.style.setProperty('--ax', (150 - shift) + 'px'); }
    if (r.top < 70) w.classList.add('below');
  }
  function closeAll(except) {
    tips.forEach(function (t) { if (t !== except) t.setAttribute('aria-expanded', 'false'); });
  }
  tips.forEach(function (t) {
    var w = t.parentNode;
    w.addEventListener('mouseenter', function () { requestAnimationFrame(function () { place(w); }); });
    t.addEventListener('focus', function () { requestAnimationFrame(function () { place(w); }); });
    t.addEventListener('click', function (ev) {
      ev.preventDefault(); ev.stopPropagation();
      var open = t.getAttribute('aria-expanded') !== 'true';
      closeAll(t); t.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) place(w);
    });
  });
  document.addEventListener('click', function (ev) { if (!ev.target.closest('.tip-w')) closeAll(); });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') closeAll(); });
  addEventListener('scroll', function () { if (innerWidth > 640) closeAll(); }, { passive: true });

  var all = bud.querySelector('.bs-all');
  var secs = bud.querySelectorAll('.bs, .cy');
  if (all) all.addEventListener('click', function () {
    var open = all.getAttribute('aria-pressed') !== 'true';
    secs.forEach(function (d) { d.open = open; });
    all.setAttribute('aria-pressed', open ? 'true' : 'false');
    all.textContent = open ? 'Свернуть всё' : 'Раскрыть всё';
  });
  bud.querySelectorAll('.bud-secs a').forEach(function (a) {
    a.addEventListener('click', function () { var d = document.querySelector(a.getAttribute('href')); if (d) d.open = true; });
  });
  addEventListener('beforeprint', function () { secs.forEach(function (d) { d.open = true; }); });
})();
