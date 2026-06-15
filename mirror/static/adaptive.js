/* Адаптация секционных блоков для планшетов и мобильных.
   На ширинах 480/640 часть текстовых элементов накладывается друг на друга.
   Скрипт находит пересекающиеся элементы и вставляет вертикальное
   пространство: всё ниже точки разрыва сдвигается, фоны растягиваются. */
/* Запрет автозапуска роликов.
   Снимает атрибут autoplay со всех <video>, ставит preload="none" и ставит
   на паузу любой ролик, запущенный не по действию пользователя (в т.ч.
   в попапах, добавляемых в DOM динамически). */
(function () {
  'use strict'
  var userInteracted = false
  ;['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) {
    window.addEventListener(ev, function () { userInteracted = true }, { capture: true, passive: true })
  })

  function disarm(v) {
    if (!v || v.__noAutoplay) return
    v.__noAutoplay = true
    v.autoplay = false
    v.removeAttribute('autoplay')
    if (!v.getAttribute('preload')) v.preload = 'none'
    // если ролик попытается стартовать сам (скрипт/браузер) — гасим
    v.addEventListener('play', function () {
      if (!userInteracted) {
        v.pause()
        try { v.currentTime = 0 } catch (e) {}
      }
    })
  }

  function scan() {
    var vids = document.getElementsByTagName('video')
    for (var i = 0; i < vids.length; i++) disarm(vids[i])
  }

  // Полная остановка ролика: пауза + сброс на начало (звук не должен играть в фоне)
  function stopVideo(v) {
    try { v.pause() } catch (e) {}
    try { v.currentTime = 0 } catch (e) {}
  }
  function stopInside(el) {
    if (!el) return
    var vids = el.getElementsByTagName ? el.getElementsByTagName('video') : []
    for (var i = 0; i < vids.length; i++) stopVideo(vids[i])
    // iframe-плееры (YouTube/Vimeo) — перезагрузить src, чтобы выгрузить
    var ifr = el.getElementsByTagName ? el.getElementsByTagName('iframe') : []
    for (var j = 0; j < ifr.length; j++) {
      var f = ifr[j]
      if (/youtube|vimeo|rutube|vk\.com|kinescope/.test(f.src || '')) f.src = f.src
    }
  }

  function isHidden(p) {
    if (p.classList && p.classList.contains('t-popup_show')) return false
    var st = p.getAttribute && p.getAttribute('style')
    if (st && /display\s*:\s*block/.test(st)) return false
    return true
  }

  // Следим за всеми попапами: как только попап скрывается — гасим в нём видео
  function watchPopups() {
    var popups = document.querySelectorAll('.t-popup, .t-popupcontainer, [data-tooltip-hook]')
    for (var i = 0; i < popups.length; i++) {
      var p = popups[i]
      if (p.__videoWatched) continue
      p.__videoWatched = true
      new MutationObserver(function () {
        var self = this.__el
        if (isHidden(self)) stopInside(self)
      }.bind({ __el: p })).observe(p, { attributes: true, attributeFilter: ['class', 'style'] })
    }
  }

  function scanAll() { scan(); watchPopups() }

  // Закрытие по Esc и по клику на кнопку/оверлей — гасим все видео в открытых попапах
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.keyCode === 27) {
      document.querySelectorAll('.t-popup').forEach(function (p) { setTimeout(function () { stopInside(p) }, 50) })
    }
  })
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('.t-popup__close, .t-popup__close-wrapper, .t-popup__bg')) {
      var p = e.target.closest('.t-popup')
      setTimeout(function () { stopInside(p) }, 50)
    }
  }, true)

  scanAll()
  document.addEventListener('DOMContentLoaded', scanAll)
  new MutationObserver(scanAll).observe(document.documentElement, { childList: true, subtree: true })
})()

(function () {
  'use strict'
  var GAP = 18
  var FIXED = new WeakSet()

  function rect(e) {
    return e.getBoundingClientRect()
  }

  // сдвиг вниз с учётом привязки элемента (top или bottom)
  function shiftDown(e, dy) {
    if (e.style.bottom && !e.style.top) {
      e.style.bottom = (parseFloat(e.style.bottom) || 0) - dy + 'px'
    } else {
      e.style.top = (parseFloat(e.style.top) || 0) + dy + 'px'
    }
  }

  // вставить dy пикселей пустоты на уровне y (в координатах viewport)
  function insertSpace(els, y, dy) {
    els.forEach(function (e) {
      var r = rect(e)
      if (r.top >= y - 2) {
        e.style.top = (parseFloat(e.style.top) || 0) + dy + 'px'
      } else if (r.bottom > y + 2) {
        var h = parseFloat(e.style.height)
        if (!isNaN(h)) e.style.height = h + dy + 'px'
      }
    })
  }

  function fixArtboard(ab) {
    if (window.innerWidth >= 960) return
    var els = [].slice.call(ab.querySelectorAll('.tn-elem')).filter(function (e) {
      var r = rect(e)
      return r.height > 0 && r.width > 0
    })
    var texts = els
      .filter(function (e) {
        return e.getAttribute('data-elem-type') === 'text'
      })
      .sort(function (a, b) {
        return rect(a).top - rect(b).top
      })
    var totalShift = 0
    for (var i = 1; i < texts.length; i++) {
      var cur = rect(texts[i])
      var need = 0
      for (var j = 0; j < i; j++) {
        var prev = rect(texts[j])
        var xOverlap = Math.min(cur.right, prev.right) - Math.max(cur.left, prev.left)
        var minW = Math.min(cur.width, prev.width)
        if (xOverlap > minW * 0.2 && cur.top < prev.bottom - 4 && cur.bottom > prev.top + 4) {
          need = Math.max(need, prev.bottom + GAP - cur.top)
        }
      }
      if (need > 1) {
        var curEl = texts[i]
        var curBottom = cur.bottom
        // сдвинуть сам элемент
        shiftDown(curEl, need)
        // и всё, что лежало ниже его нижней границы; фоны поперёк — растянуть
        els.forEach(function (e) {
          if (e === curEl) return
          var r = rect(e)
          if (r.top >= curBottom - 2) {
            shiftDown(e, need)
          } else if (r.top < cur.top - 2 && r.bottom > curBottom + 2) {
            var tp = e.getAttribute('data-elem-type')
            if (tp === 'shape' || tp === 'image') {
              var h = parseFloat(e.style.height)
              if (!isNaN(h)) e.style.height = h + need + 'px'
            }
          }
        })
        totalShift += need
      }
    }
    if (totalShift > 0) {
      var h = parseFloat(ab.style.height) || rect(ab).height
      ab.style.height = h + totalShift + 'px'
      var wrap = ab.closest('.t396')
      if (wrap) wrap.style.height = ab.style.height
    }
  }

  var fixing = false
  function run() {
    if (fixing) return
    fixing = true
    try {
      [].slice.call(document.querySelectorAll('.t396__artboard')).forEach(fixArtboard)
    } finally {
      fixing = false
    }
  }

  var timers = []
  function schedule() {
    timers.forEach(clearTimeout)
    timers = [400, 1000, 2200].map(function (ms) {
      return setTimeout(run, ms)
    })
  }

  window.addEventListener('load', function () {
    setTimeout(run, 600)
    setTimeout(run, 1500)
  })
  window.addEventListener('resize', schedule)
  window.addEventListener('orientationchange', schedule)
})()
