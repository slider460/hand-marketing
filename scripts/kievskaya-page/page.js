(function () {
  var list = [].slice.call(document.querySelectorAll('.pos'));
  var flt = document.querySelector('.flt');
  var ex = flt.querySelector('.ex');

  // Фильтр «Все / Берем / Не оказываем»
  flt.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    if (b.dataset.x) {
      var open = b.dataset.x === '1';
      list.forEach(function (p) { if (p.tagName === 'DETAILS' && !p.classList.contains('hide')) p.open = open; });
      b.dataset.x = open ? '0' : '1';
      b.textContent = open ? 'Свернуть все' : 'Раскрыть все';
      return;
    }
    [].forEach.call(flt.querySelectorAll('[data-f]'), function (x) { x.classList.toggle('on', x === b); });
    var f = b.dataset.f;
    list.forEach(function (p) { p.classList.toggle('hide', f !== 'all' && p.dataset.s !== f); });
  });

  // Переход по якорю #p01…#p31: раскрыть строку, снять фильтр, если строка скрыта
  function openHash() {
    var id = location.hash.slice(1); if (!/^p\d\d$/.test(id)) return;
    var p = document.getElementById(id); if (!p) return;
    if (p.classList.contains('hide')) flt.querySelector('[data-f="all"]').click();
    if (p.tagName === 'DETAILS') p.open = true;
    setTimeout(function () { p.scrollIntoView({ block: 'start' }); }, 30);
  }
  addEventListener('hashchange', openHash);
  openHash();

  // Раскрытая строка получает адрес, чтобы ссылку на позицию можно было переслать
  list.forEach(function (p) {
    if (p.tagName !== 'DETAILS') return;
    p.addEventListener('toggle', function () {
      if (p.open && history.replaceState) history.replaceState(null, '', '#' + p.id);
    });
  });

  addEventListener('beforeprint', function () { list.forEach(function (p) { if (p.tagName === 'DETAILS') p.open = true; }); });
  if (ex) ex.dataset.x = '1';
})();

// Цели Метрики: скачал КП в Excel, нажал контакт
(function () {
  function goal(g) { if (window.ym) try { ym(71125393, 'reachGoal', g); } catch (e) { } }
  [].forEach.call(document.querySelectorAll('.xlsx-btn'), function (a) { a.addEventListener('click', function () { goal('kievskaya_xlsx'); }); });
  [].forEach.call(document.querySelectorAll('a[href^="tel:"], a[href^="mailto:"], a[href*="t.me/"]'), function (a) { a.addEventListener('click', function () { goal('kievskaya_contact'); }); });
})();
