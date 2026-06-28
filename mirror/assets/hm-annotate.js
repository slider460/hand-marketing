/* Адаптивные RoughNotation-аннотации для Самара-кейсов.
   Считывает цвета/типы из исходной React-разметки, заменяет её своими аннотациями
   и ПЕРЕРИСОВЫВАЕТ их при resize/смене устройства (React этого не делал — отсюда «съезд»). */
(function () {
  function typeFor(c) {
    c = (c || '').toLowerCase();
    if (/fde68a|fbbf24|fcd34d|fef08a|fde047|yellow/.test(c)) return 'highlight';
    if (/a7f3d0|10b981|34d399|6ee7b7|22c55e|green/.test(c)) return 'box';
    return 'underline';
  }
  function spans() {
    return Array.prototype.slice.call(
      document.querySelectorAll('.relative.inline-block.bg-transparent')
    );
  }
  var CFG = null;
  function derive() {
    var a = document.querySelectorAll('.rough-annotation');
    if (!a.length) return false;
    CFG = Array.prototype.map.call(a, function (s) {
      var el = s.querySelector('[stroke]');
      var c = el ? el.getAttribute('stroke') : '#3b82f6';
      return { color: c, type: typeFor(c) };
    });
    return true;
  }
  function clear() {
    Array.prototype.forEach.call(
      document.querySelectorAll('.rough-annotation'),
      function (s) { s.remove(); }
    );
  }
  function draw() {
    if (!CFG || !window.RoughNotation) return;
    clear();
    var sp = spans();
    if (!sp.length) return;
    var list = sp.map(function (el, i) {
      var cf = CFG[i] || CFG[CFG.length - 1];
      var o = { type: cf.type, color: cf.color, multiline: true, iterations: 2, animationDuration: 600 };
      if (cf.type === 'underline') { o.strokeWidth = 2; o.padding = 2; }
      else if (cf.type === 'box') { o.strokeWidth = 2; o.padding = 4; }
      else if (cf.type === 'highlight') { o.iterations = 2; }
      return window.RoughNotation.annotate(el, o);
    });
    var g = window.RoughNotation.annotationGroup(list);
    g.show();
    // пометить наши SVG, чтобы CSS их показал (React-аннотации остаются скрыты)
    requestAnimationFrame(function () {
      Array.prototype.forEach.call(
        document.querySelectorAll('.rough-annotation'),
        function (s) { s.classList.add('hm-ann'); }
      );
    });
  }
  var done = false, tries = 0;
  var iv = setInterval(function () {
    if (done) return;
    if (derive()) {
      done = true; clearInterval(iv);
      draw();
      var t;
      window.addEventListener('resize', function () {
        clearTimeout(t); t = setTimeout(draw, 250);
      }, { passive: true });
      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(function () { setTimeout(draw, 120); });
      }
    } else if (++tries > 50) { clearInterval(iv); }
  }, 150);
})();
