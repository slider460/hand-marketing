// Учёт просмотра страницы океанариума для Hand Marketing: время по разделам, прокрутка, клики по интерактивам.
// Данные уходят только на наш сервер (?track=1).
(function () {
  var sid = Math.random().toString(36).slice(2, 12) + Date.now().toString(36).slice(-4);
  var t0 = Date.now(), events = [], dwell = {}, order = [], active = 0, maxScroll = 0, lastInput = Date.now(), dirty = true, sent = false;
  function cap(s) { s = (s || '').replace(/\s+/g, ' ').trim(); return s.charAt(0).toUpperCase() + s.slice(1); }
  var keys = {};
  function ev(k, d) { events.push({ k: k, d: d, at: Date.now() - t0 }); keys[k] = 1; dirty = true; }

  // Разделы с понятными названиями (по надписи над заголовком)
  var secs = [].slice.call(document.querySelectorAll('section, .final')).map(function (el) {
    var name = 'Первый экран';
    if (!el.classList.contains('hero')) {
      var eb = el.querySelector('.kick');
      if (eb) { var c = eb.cloneNode(true); var b = c.querySelector('em'); if (b) b.remove(); name = cap(c.textContent.toLowerCase()); }
      else name = el.id || 'Раздел';
    }
    if (order.indexOf(name) < 0) order.push(name);
    return { el: el, name: name };
  });
  function current() {
    var y = innerHeight * 0.45, best = null;
    secs.forEach(function (s) { var r = s.el.getBoundingClientRect(); if (r.top <= y && r.bottom >= y) best = s; });
    return best;
  }
  ['scroll', 'mousemove', 'touchstart', 'keydown', 'click', 'wheel'].forEach(function (t) {
    addEventListener(t, function () { lastInput = Date.now(); }, { passive: true });
  });
  // Раз в секунду: вкладка видна и человек не отошёл больше чем на минуту, копим время раздела
  setInterval(function () {
    if (document.visibilityState !== 'visible' || Date.now() - lastInput > 60000) return;
    active++; var s = current(); if (s) dwell[s.name] = (dwell[s.name] || 0) + 1;
    var h = document.documentElement.scrollHeight - innerHeight;
    var p = h > 0 ? Math.round(scrollY / h * 100) : 100; if (p > maxScroll) maxScroll = p;
    dirty = true;
  }, 1000);

  function send(final) {
    if (!dirty && !final) return;
    var body = JSON.stringify({ sid: sid, final: final ? 1 : 0, events: events.splice(0), dwell: dwell, order: order, active: active, scroll: maxScroll, keys: Object.keys(keys),
      env: sent ? null : { sw: screen.width, sh: screen.height, vw: innerWidth, vh: innerHeight, dpr: devicePixelRatio, touch: navigator.maxTouchPoints || 0,
        lang: navigator.language, tz: (Intl.DateTimeFormat().resolvedOptions().timeZone || ''), ref: document.referrer ? document.referrer.slice(0, 200) : '' } });
    sent = true; dirty = false;
    try {
      if (navigator.sendBeacon) navigator.sendBeacon('?track=1', new Blob([body], { type: 'application/json' }));
      else fetch('?track=1', { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'application/json' } });
    } catch (e) {}
  }
  ev('open', 'открыл страницу' + (location.hash ? ' (' + location.hash + ')' : ''));
  setTimeout(function () { send(false); }, 1500);
  setInterval(function () { send(false); }, 15000);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') { ev('hide', 'свернул или закрыл страницу'); send(true); }
    else ev('show', 'вернулся на страницу');
  });
  addEventListener('pagehide', function () { send(true); });
  addEventListener('beforeprint', function () { ev('print', 'печатает страницу'); });

  var once = {};
  function first(key, k, d) { if (once[key]) return; once[key] = 1; ev(k, d); }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a, button, .chap li, .idea'); if (!a) return;
    var txt = cap((a.getAttribute('aria-label') || a.textContent || '').replace(/\s+/g, ' ').slice(0, 80));
    var href = (a.getAttribute && a.getAttribute('href')) || '';
    if (a.classList.contains('pdf-btn')) return ev('pdf', 'нажал «Скачать PDF»');
    if (a.id === 'release') return ev('fish', 'раскрасил и отпустил рыбу');
    if (a.closest('#ftabs')) return first('floor' + txt, 'floor', 'демо пола: сцена «' + txt.replace(/^\d+\s*/, '') + '»');
    if (a.closest('#vtabs')) return ev('variant', 'схема: ' + txt.replace(/^[АБ]\s*/, ''));
    if (a.closest('#ledtabs')) return first('led' + txt, 'led', 'LED-фасад: вкладка «' + txt + '»');
    if (a.closest('.chap')) return first('chap' + txt.slice(0, 10), 'chapter', 'погружение: глава ' + txt.slice(0, 30));
    if (a.closest('#pg') || a.closest('#fbtn')) return first('masc' + txt, 'mascot', 'маскот: ' + txt);
    if (a.closest('.layers')) return first('lay' + txt, 'layer', 'схема: слой «' + txt.slice(0, 20) + '»');
    if (a.closest('.qa')) return first('q' + a.closest('.qrow').dataset.q, 'qa', 'параметры экрана: ответил на пункт ' + a.closest('.qrow').dataset.q);
    if (a.classList.contains('idea')) return first('idea' + txt.slice(0, 20), 'idea', 'отметил для расчёта: ' + txt.slice(0, 50));
    if (a.closest('#calc') && a.tagName === 'BUTTON') return ev('calc', 'нажал «Отправить выбор на расчёт»');
    if (a.closest('.top nav')) return ev('nav', 'меню: ' + txt);
    if (/^tel:/.test(href)) return ev('contact', 'нажал телефон');
    if (/^mailto:/.test(href)) return ev('contact', 'нажал почту');
    if (/t\.me|wa\.me/.test(href)) return ev('contact', 'нажал Telegram');
    if (/^https?:/.test(href)) { var h = a.querySelector('b'); return ev('link', 'открыл кейс: ' + cap(h ? h.textContent : txt) + ' → ' + href.replace('https://hand-marketing.ru', '')); }
    if (/^#/.test(href)) return ev('anchor', 'перешёл к разделу: ' + txt);
  }, true);
  document.addEventListener('copy', function () {
    var s = String(getSelection() || '').trim(); if (s) ev('copy', 'скопировал текст: «' + s.slice(0, 120) + (s.length > 120 ? '…' : '') + '»');
  });
})();
