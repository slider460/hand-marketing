/* Страница для океанариума. Без библиотек: море на канвасе, глубиномер, демо пола, раскраска рыбы, маскот, LED-фасад */
(function () {
  'use strict';
  var D = window.OC || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DPR = Math.min(window.devicePixelRatio || 1, 1.5);
  var mobile = window.innerWidth < 760;

  /* ---------- форма рыбы: те же контуры, что в бланке раскраски ---------- */
  var FP = {
    tail: new Path2D('M-27,0 L-54,-22 C-47,-8 -47,8 -54,22 Z'),
    fin1: new Path2D('M-8,-19 C0,-38 18,-36 24,-17 Z'),
    fin2: new Path2D('M-6,17 C0,30 12,30 17,16 Z'),
    body: new Path2D('M-32,0 C-22,-24 22,-28 44,-4 C48,0 48,2 44,6 C22,28 -22,24 -32,0 Z'),
    stripe: new Path2D('M2,-23 C12,-10 12,10 2,23 L-8,21 C1,9 1,-9 -8,-21 Z')
  };
  function drawFish(ctx, x, y, ang, s, col, glow, wig) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s * (Math.abs(ang) > Math.PI / 2 ? -1 : 1));
    if (glow) { ctx.shadowColor = col.body; ctx.shadowBlur = 18 / s; }
    ctx.save(); ctx.rotate(Math.sin(wig || 0) * .12); ctx.fillStyle = col.tail; ctx.fill(FP.tail); ctx.restore();
    ctx.fillStyle = col.fin; ctx.fill(FP.fin1); ctx.fill(FP.fin2);
    ctx.fillStyle = col.body; ctx.fill(FP.body);
    ctx.shadowBlur = 0;
    ctx.fillStyle = col.stripe; ctx.fill(FP.stripe);
    if (col.line) { ctx.strokeStyle = col.line; ctx.lineWidth = 3; ctx.stroke(FP.body); }
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(31, -5, 5.5, 0, 7); ctx.fill();
    ctx.fillStyle = '#10202a'; ctx.beginPath(); ctx.arc(32.5, -5, 2.6, 0, 7); ctx.fill();
    ctx.restore();
  }

  /* ---------- указатель (общий для фонового моря) ---------- */
  var ptr = { x: -999, y: -999, t: 0 };
  function setPtr(x, y) { ptr.x = x; ptr.y = y; ptr.t = performance.now(); }
  window.addEventListener('pointermove', function (ev) { setPtr(ev.clientX, ev.clientY); }, { passive: true });
  window.addEventListener('touchmove', function (ev) { var t = ev.touches[0]; if (t) setPtr(t.clientX, t.clientY); }, { passive: true });

  /* ---------- глубина по скроллу ---------- */
  var secs = $$('section[data-depth]');
  var depth = 0;
  var STOPS = [[0, [14, 92, 138]], [30, [9, 66, 102]], [1000, [6, 34, 58]], [4000, [3, 15, 28]], [11000, [1, 4, 9]]];
  var TRACK = [[0, 0], [30, 25], [1000, 50], [4000, 75], [11000, 100]];
  function pw(arr, v, f) {
    for (var i = 1; i < arr.length; i++) if (v <= arr[i][0]) { var a = arr[i - 1], b = arr[i], k = (v - a[0]) / (b[0] - a[0]); return f(a[1], b[1], k); }
    return arr[arr.length - 1][1];
  }
  var lerp = function (a, b, k) { return a + (b - a) * k; };
  var lerpC = function (a, b, k) { return [lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k)]; };
  var bg = $('#bg'), gv = $('#gv'), gl = $('#gl'), gi = $('#gi'), rays = $('.rays');
  function zoneName(d) { return d < 30 ? 'поверхность' : d < 1000 ? 'риф' : d < 4000 ? 'сумерки' : d < 11000 ? 'бездна' : 'дно впадины'; }
  function onScroll() {
    var mid = window.innerHeight * .5, d = 0;
    for (var i = 0; i < secs.length; i++) {
      var r = secs[i].getBoundingClientRect();
      if (r.top <= mid && r.bottom > mid) {
        var a = +secs[i].dataset.depth, b = secs[i + 1] ? +secs[i + 1].dataset.depth : a;
        d = lerp(a, b, Math.min(1, Math.max(0, (mid - r.top) / r.height)));
        break;
      }
      if (r.top > mid) { d = +secs[i].dataset.depth; break; }
      d = +secs[i].dataset.depth;
    }
    depth = d;
    var c = pw(STOPS, d, lerpC);
    bg.style.backgroundColor = 'rgb(' + c.map(Math.round).join(',') + ')';
    rays.style.setProperty('--rays', Math.max(0, 1 - d / 900).toFixed(2));
    gv.textContent = Math.round(d).toLocaleString('ru-RU');
    gl.textContent = zoneName(d);
    gi.style.top = pw(TRACK, d, lerp) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- фоновое море: косяк рыб + морской снег ---------- */
  var sea = $('#sea'), sx = sea.getContext('2d'), W = 0, H = 0;
  function sizeSea() { W = window.innerWidth; H = window.innerHeight; sea.width = W * DPR; sea.height = H * DPR; sx.setTransform(DPR, 0, 0, DPR, 0, 0); }
  sizeSea(); window.addEventListener('resize', sizeSea);
  var SILVER = { body: '#cfe3ee', fin: '#9fc0d2', tail: '#9fc0d2', stripe: '#b6d2e0' };
  var GLOWS = [
    { body: '#3fd0e8', fin: '#1d8fa6', tail: '#1d8fa6', stripe: '#9ff0ff' },
    { body: '#c9ec3a', fin: '#7fa012', tail: '#7fa012', stripe: '#efffb0' },
    { body: '#e64bd0', fin: '#9b2a8f', tail: '#9b2a8f', stripe: '#ffc2f4' }
  ];
  var fish = [], snow = [];
  var N = reduce ? 0 : (mobile ? 14 : 24);
  for (var i = 0; i < N; i++) fish.push({ x: Math.random() * W, y: H * (.25 + Math.random() * .5), vx: 1 + Math.random(), vy: (Math.random() - .5), s: .2 + Math.random() * .12, g: GLOWS[i % 3], w: Math.random() * 6 });
  for (i = 0; i < (mobile ? 40 : 80); i++) snow.push({ x: Math.random(), y: Math.random(), r: .4 + Math.random() * 1.6, v: .00005 + Math.random() * .00015 });
  var mine = [];
  function addMine(col, x, y, silent) {
    var f = { x: x, y: y, vx: 2, vy: -1, s: mobile ? .42 : .55, col: col, mine: true, w: 0 };
    fish.push(f); mine.push(f);
    if (mine.length > 12) { var old = mine.shift(); fish.splice(fish.indexOf(old), 1); }
    if (!silent) saveMine();
  }
  function saveMine() {
    try { localStorage.setItem('oc-fish', JSON.stringify({ d: new Date().toDateString(), f: mine.map(function (m) { return m.col; }) })); } catch (e) { }
  }
  try {
    var saved = JSON.parse(localStorage.getItem('oc-fish') || 'null');
    if (saved && saved.d === new Date().toDateString()) saved.f.forEach(function (c) { addMine(c, Math.random() * W, H * .5, true); });
  } catch (e) { }

  var lastScroll = window.scrollY;
  function seaStep(t) {
    sx.clearRect(0, 0, W, H);
    var deep = depth > 1400, dy = window.scrollY - lastScroll; lastScroll = window.scrollY;
    // морской снег сдвигается вместе со скроллом, как будто опускаемся
    sx.fillStyle = deep ? 'rgba(170,240,255,.55)' : 'rgba(220,245,255,.35)';
    for (var i = 0; i < snow.length; i++) {
      var p = snow[i]; p.y = (p.y - p.v * 16 - dy / H * .35 + 1) % 1; p.x = (p.x + Math.sin(t / 3000 + i) * .00008 + 1) % 1;
      sx.beginPath(); sx.arc(p.x * W, p.y * H, p.r, 0, 7); sx.fill();
    }
    // у поверхности за заголовком проходит кашалот
    if (depth < 700 && !reduce) {
      sx.globalAlpha = .3 * (1 - depth / 700);
      var span = W + 1600 * Math.max(.6, W / 1440);
      whale(sx, (t / 26) % span - 700 * Math.max(.6, W / 1440), H * .62, Math.max(.6, W / 1440) * 1.5, false);
      sx.globalAlpha = 1;
    }
    var near = performance.now() - ptr.t < 2500;
    for (i = 0; i < fish.length; i++) {
      var f = fish[i], cx = 0, cy = 0, ax = 0, ay = 0, sx2 = 0, sy2 = 0, n = 0;
      for (var j = 0; j < fish.length; j++) {
        if (i === j) continue;
        var o = fish[j], ddx = o.x - f.x, ddy = o.y - f.y, d2 = ddx * ddx + ddy * ddy;
        if (d2 < 22000) { cx += o.x; cy += o.y; ax += o.vx; ay += o.vy; n++; if (d2 < 900) { sx2 -= ddx; sy2 -= ddy; } }
      }
      if (n) { f.vx += ((cx / n - f.x) * .0006 + (ax / n - f.vx) * .04); f.vy += ((cy / n - f.y) * .0006 + (ay / n - f.vy) * .04); }
      f.vx += sx2 * .004; f.vy += sy2 * .004;
      if (near) {
        var px = f.x - ptr.x, py = f.y - ptr.y, pd = Math.sqrt(px * px + py * py);
        if (pd < 150) { f.vx += px / pd * 1.1; f.vy += py / pd * 1.1; }
      }
      // держимся середины экрана по вертикали
      f.vy += (H * .5 - f.y) * .00006;
      var sp = Math.sqrt(f.vx * f.vx + f.vy * f.vy), max = f.mine ? 2.2 : 3, min = 1;
      if (sp > max) { f.vx *= max / sp; f.vy *= max / sp; } else if (sp < min) { f.vx *= min / sp; f.vy *= min / sp; }
      f.x += f.vx; f.y += f.vy; f.w += .25 * sp;
      if (f.x > W + 60) f.x = -60; if (f.x < -60) f.x = W + 60;
      if (f.y > H + 60) f.y = -60; if (f.y < -60) f.y = H + 60;
      var col = f.col || (deep ? f.g : SILVER);
      sx.globalAlpha = f.mine ? 1 : (deep ? .42 : .38);
      drawFish(sx, f.x, f.y, Math.atan2(f.vy, f.vx), f.s, col, false, f.w);
    }
    sx.globalAlpha = 1;
  }

  /* ---------- окно в зал: пять глав ---------- */
  var dive = $('#dive'), dcv = dive.querySelector('canvas'), dx = dcv.getContext('2d'), dW = 0, dH = 0;
  function sizeDive() { var r = dive.getBoundingClientRect(); dW = r.width; dH = r.height; dcv.width = dW * DPR; dcv.height = dH * DPR; dx.setTransform(DPR, 0, 0, DPR, 0, 0); }
  sizeDive(); window.addEventListener('resize', sizeDive);
  var CH = D.chapters || [], chap = 0, shown = 0, chapT = 0;
  var dm = $('#dm'), dc = $('#dc');
  var lis = $$('#chap li');
  function setChap(i) {
    chap = i; chapT = performance.now();
    lis.forEach(function (l, k) { l.classList.toggle('on', k === i); });
    dc.textContent = CH[i] ? CH[i][1] + ': ' + CH[i][2] : '';
  }
  lis.forEach(function (l, k) { l.addEventListener('click', function () { setChap(k); }); });
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) setChap(+en.target.dataset.i); }); }, { rootMargin: '-48% 0px -48% 0px' });
    lis.forEach(function (l) { cio.observe(l); });
  }
  setChap(0);
  var reef = []; for (i = 0; i < 46; i++) reef.push({ a: Math.random() * 6.3, r: .12 + Math.random() * .16, s: .006 + Math.random() * .006, y: Math.random() });
  var bubbles = []; for (i = 0; i < 26; i++) bubbles.push({ x: Math.random(), y: Math.random(), r: 1 + Math.random() * 3, v: .001 + Math.random() * .002 });
  var glowDots = []; for (i = 0; i < 70; i++) glowDots.push({ x: Math.random(), y: Math.random(), p: Math.random() * 6, c: ['#3fd0e8', '#c9ec3a', '#e64bd0'][i % 3] });
  var DBG = [['#2aa3d8', '#0b4a72'], ['#139080', '#06364a'], ['#0b2340', '#030b17'], ['#03070d', '#000'], ['#020306', '#000']];
  function penguin(ctx, x, y, a, s) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s);
    ctx.fillStyle = '#10161b'; ctx.beginPath(); ctx.ellipse(0, 0, 34, 13, 0, 0, 7); ctx.fill();
    ctx.fillStyle = '#eef3f5'; ctx.beginPath(); ctx.ellipse(4, 5, 24, 7, 0, 0, 7); ctx.fill();
    ctx.fillStyle = '#10161b'; ctx.beginPath(); ctx.ellipse(-2, 9, 14, 4, .5, 0, 7); ctx.fill();
    ctx.fillStyle = '#ff9a2e'; ctx.beginPath(); ctx.moveTo(33, -3); ctx.lineTo(42, 0); ctx.lineTo(33, 2); ctx.fill();
    ctx.restore();
  }
  function shark(ctx, x, y, s, dir) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s); ctx.fillStyle = 'rgba(8,40,52,.85)';
    ctx.beginPath(); ctx.moveTo(60, 0); ctx.quadraticCurveTo(20, -18, -40, -4); ctx.lineTo(-70, -22); ctx.lineTo(-62, 0); ctx.lineTo(-70, 20); ctx.lineTo(-40, 4); ctx.quadraticCurveTo(20, 16, 60, 0); ctx.fill();
    ctx.beginPath(); ctx.moveTo(5, -12); ctx.lineTo(-8, -36); ctx.lineTo(-18, -9); ctx.fill();
    ctx.beginPath(); ctx.moveTo(10, 8); ctx.lineTo(-6, 26); ctx.lineTo(-10, 7); ctx.fill();
    ctx.restore();
  }
  function manta(ctx, x, y, s, t, col) { // скат сверху: широкие крылья машут, хвост-хлыст
    var f = Math.sin(t) * 9;
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col || 'rgba(10,46,58,.9)';
    ctx.beginPath(); ctx.moveTo(34, 0);
    ctx.bezierCurveTo(30, -18, 8, -40 - f, -8, -62 - f); ctx.bezierCurveTo(-14, -40, -24, -14, -30, -4);
    ctx.lineTo(-30, 4); ctx.bezierCurveTo(-24, 14, -14, 40, -8, 62 + f); ctx.bezierCurveTo(8, 40 + f, 30, 18, 34, 0); ctx.fill();
    ctx.strokeStyle = ctx.fillStyle; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(-28, 0); ctx.quadraticCurveTo(-56, Math.sin(t * 1.3) * 6, -84, 0); ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.18)'; ctx.beginPath(); ctx.arc(14, -9, 3, 0, 7); ctx.arc(14, 9, 3, 0, 7); ctx.fill();
    ctx.restore();
  }
  function whale(ctx, x, y, s, eyeGlow, col0) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    ctx.fillStyle = col0 || 'rgba(30,44,62,.95)';
    ctx.beginPath(); ctx.moveTo(200, -40); ctx.bezierCurveTo(230, -42, 236, 30, 200, 44); ctx.bezierCurveTo(80, 60, -80, 40, -190, 8);
    ctx.lineTo(-250, -30); ctx.lineTo(-236, 2); ctx.lineTo(-260, 34); ctx.lineTo(-190, 14); ctx.bezierCurveTo(-80, -50, 80, -44, 200, -40); ctx.fill();
    ctx.fillStyle = 'rgba(20,30,44,.95)'; ctx.beginPath(); ctx.moveTo(60, 30); ctx.lineTo(20, 74); ctx.lineTo(10, 34); ctx.fill();
    ctx.fillStyle = eyeGlow ? '#ffd27a' : '#c9d6e0'; ctx.shadowColor = '#ffd27a'; ctx.shadowBlur = eyeGlow ? 16 : 6;
    ctx.beginPath(); ctx.arc(150, 6, 5, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
    ctx.restore();
  }
  var diveTrail = [];
  dive.addEventListener('pointermove', function (ev) { var r = dive.getBoundingClientRect(); diveTrail.push({ x: ev.clientX - r.left, y: ev.clientY - r.top, a: 1 }); });
  var diveVisible = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { diveVisible = es[0].isIntersecting; }).observe(dive);
  function diveStep(t) {
    if (!diveVisible) return;
    var target = CH[chap] ? CH[chap][0] : 0;
    shown += (target - shown) * .06; if (Math.abs(target - shown) < 1) shown = target;
    dm.textContent = Math.round(shown).toLocaleString('ru-RU');
    var g = dx.createLinearGradient(0, 0, 0, dH), c = DBG[chap];
    g.addColorStop(0, c[0]); g.addColorStop(1, c[1]); dx.fillStyle = g; dx.fillRect(0, 0, dW, dH);
    var k = (t - chapT) / 1000;
    if (chap === 0) {
      for (var i = 0; i < 7; i++) {
        var x = (i / 7) * dW + Math.sin(t / 2000 + i) * 30;
        dx.fillStyle = 'rgba(220,250,255,' + (.06 + .04 * Math.sin(t / 700 + i)) + ')';
        dx.beginPath(); dx.moveTo(x, 0); dx.lineTo(x + 50, 0); dx.lineTo(x - 80, dH); dx.lineTo(x - 150, dH); dx.fill();
      }
      for (i = 0; i < 3; i++) { var pp = ((k * .12 + i * .33) % 1); penguin(dx, dW * (1.1 - pp * 1.3), dH * (.1 + pp * .8) + i * 18, .55, dW / 700 * (1 - i * .15)); }
    } else if (chap === 1) {
      dx.fillStyle = '#0a2a30'; dx.beginPath(); dx.moveTo(0, dH);
      for (i = 0; i <= 12; i++) dx.lineTo(i / 12 * dW, dH * .86 - Math.abs(Math.sin(i * 1.7)) * dH * .1); dx.lineTo(dW, dH); dx.fill();
      reef.forEach(function (p) { p.a += p.s; drawFish(dx, dW * .55 + Math.cos(p.a) * dW * p.r * 1.3, dH * .42 + Math.sin(p.a) * dH * p.r, p.a + Math.PI / 2, dW / 2600, { body: '#ffd23f', fin: '#ff9a2e', tail: '#ff9a2e', stripe: '#fff' }, false, p.a * 8); });
      shark(dx, ((k * 40) % (dW + 300)) - 150, dH * .25, dW / 900, 1);
      shark(dx, dW + 150 - ((k * 28 + 400) % (dW + 300)), dH * .7, dW / 1200, -1);
      manta(dx, ((k * 22 + 200) % (dW + 300)) - 150, dH * .58, dW / 1500, t / 400);
    } else if (chap === 2) {
      var wx = -dW * .15 + ((k * 34) % (dW * 1.9));
      whale(dx, wx, dH * .5, dW / 560, true, 'rgba(62,88,118,.95)');
    } else if (chap === 3) {
      glowDots.forEach(function (p) {
        var a = .3 + .7 * Math.abs(Math.sin(t / 900 + p.p));
        dx.fillStyle = p.c; dx.globalAlpha = a; dx.shadowColor = p.c; dx.shadowBlur = 10;
        dx.beginPath(); dx.arc(p.x * dW + Math.sin(t / 3000 + p.p) * 10, ((p.y - t / 90000) % 1 + 1) % 1 * dH, 1.6, 0, 7); dx.fill();
      });
      dx.shadowBlur = 0; dx.globalAlpha = 1;
      // «следы посетителей»: курсор по окну
      if (performance.now() - ptr.t > 1500 && diveTrail.length < 2) diveTrail.push({ x: dW * (.5 + .35 * Math.sin(t / 1300)), y: dH * (.6 + .2 * Math.sin(t / 900)), a: 1 });
      diveTrail.forEach(function (p) { p.a -= .012; dx.globalAlpha = Math.max(0, p.a); dx.fillStyle = '#9ff0ff'; dx.shadowColor = '#3fd0e8'; dx.shadowBlur = 16; dx.beginPath(); dx.arc(p.x, p.y, 4 + (1 - p.a) * 10, 0, 7); dx.fill(); });
      diveTrail = diveTrail.filter(function (p) { return p.a > 0; }); dx.globalAlpha = 1; dx.shadowBlur = 0;
    } else {
      dx.fillStyle = 'rgba(200,220,240,.3)';
      for (i = 0; i < 30; i++) { dx.beginPath(); dx.arc((i * 97) % dW, ((i * 53 + t / 60) % dH), .8, 0, 7); dx.fill(); }
      var wx2 = Math.min(dW * .55, -dW * .3 + k * 90);
      whale(dx, wx2, dH * .55, dW / 560, true, 'rgba(40,56,76,.95)');
    }
    // пузыри
    if (chap < 2) bubbles.forEach(function (b) { b.y -= b.v; if (b.y < 0) { b.y = 1; b.x = Math.random(); } dx.strokeStyle = 'rgba(255,255,255,.4)'; dx.beginPath(); dx.arc(b.x * dW, b.y * dH, b.r, 0, 7); dx.stroke(); });
  }

  /* ---------- интерактивный пол ---------- */
  var floor = $('#floor'), fcv = floor.querySelector('canvas'), fx = fcv.getContext('2d'), fW = 0, fH = 0;
  function sizeFloor() { var r = floor.getBoundingClientRect(); fW = r.width; fH = r.height; fcv.width = fW * DPR; fcv.height = fH * DPR; fx.setTransform(DPR, 0, 0, DPR, 0, 0); }
  sizeFloor(); window.addEventListener('resize', function () { sizeFloor(); initMode(); });
  var mode = 'plankton', feet = { x: -999, y: -999, t: 0, real: false }, lastStep = null;
  var trail = [], school = [], raysF = [], trash = [], grass = [], cleaned = 0, cleanDone = 0;
  var fhint = $('#fhint'), fstat = $('#fstat');
  function floorPtr(ev) {
    var r = floor.getBoundingClientRect();
    feet.x = ev.clientX - r.left; feet.y = ev.clientY - r.top; feet.t = performance.now(); feet.real = true;
    fhint.style.opacity = 0;
  }
  floor.addEventListener('pointermove', floorPtr);
  floor.addEventListener('pointerdown', floorPtr);
  floor.addEventListener('pointerleave', function () { feet.real = false; feet.t = 0; });
  function initMode() {
    trail = []; raysF = []; school = []; trash = []; grass = []; cleaned = 0; cleanDone = 0; fstat.textContent = '';
    if (mode === 'school') for (var i = 0; i < (mobile ? 70 : 130); i++) school.push({ x: Math.random() * fW, y: Math.random() * fH, vx: Math.random() - .5, vy: Math.random() - .5, w: Math.random() * 6 });
    if (mode === 'clean') {
      for (i = 0; i < 16; i++) trash.push({ x: fW * (.06 + Math.random() * .88), y: fH * (.1 + Math.random() * .8), k: i % 3, a: Math.random() * 6, life: 1, vx: (Math.random() - .5) * .2 });
      fstat.textContent = 'мусора на дне: 16';
    }
  }
  $$('#ftabs button').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('#ftabs button').forEach(function (x) { x.classList.toggle('on', x === b); });
      mode = b.dataset.m; $$('#fdesc p').forEach(function (p) { p.hidden = p.dataset.m !== mode; });
      initMode();
    });
  });
  initMode();
  function ghost(t) { // если никто не трогает пол, по нему гуляет «посетитель»
    return { x: fW * (.5 + .38 * Math.sin(t / 2300)), y: fH * (.5 + .32 * Math.sin(t / 1700 + 1)) };
  }
  var floorVisible = false;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { floorVisible = es[0].isIntersecting; }).observe(floor); else floorVisible = true;
  var ripples = null;
  function floorStep(t) {
    if (!floorVisible) return;
    var real = feet.real && performance.now() - feet.t < 3000;
    var p = real ? feet : ghost(t);
    var moved = lastStep ? Math.hypot(p.x - lastStep.x, p.y - lastStep.y) : 0;
    if (mode === 'plankton' || mode === 'school') { fx.fillStyle = '#021320'; fx.fillRect(0, 0, fW, fH); }
    else { // песок
      var gsand = fx.createRadialGradient(fW / 2, fH / 2, 10, fW / 2, fH / 2, fW * .7);
      if (mode === 'clean') { var live = trash.length ? cleaned / trash.length : 0; gsand.addColorStop(0, 'rgb(' + Math.round(70 + 40 * live) + ',' + Math.round(66 + 34 * live) + ',' + Math.round(58 + 6 * live) + ')'); gsand.addColorStop(1, '#1c1d1c'); }
      else { gsand.addColorStop(0, '#6e5e44'); gsand.addColorStop(1, '#241f17'); }
      fx.fillStyle = gsand; fx.fillRect(0, 0, fW, fH);
      fx.strokeStyle = 'rgba(255,240,210,.06)'; fx.lineWidth = 2;
      for (var r = 0; r < 14; r++) { fx.beginPath(); for (var xx = 0; xx <= fW; xx += 20) fx.lineTo(xx, r * fH / 13 + Math.sin(xx / 60 + r) * 6); fx.stroke(); }
      // каустика
      fx.fillStyle = 'rgba(180,230,255,.035)';
      for (r = 0; r < 9; r++) { fx.beginPath(); fx.arc((r * 173 + t / 40) % fW, (r * 97 + Math.sin(t / 1500 + r) * 30 + fH) % fH, 60, 0, 7); fx.fill(); }
    }
    if (mode === 'plankton') {
      if (moved > 3) { for (var k = 0; k < 3; k++) trail.push({ x: p.x + (Math.random() - .5) * 18, y: p.y + (Math.random() - .5) * 18, a: 1, r: 2 + Math.random() * 3, c: Math.random() < .7 ? '#7ff3ff' : '#c9ec3a' }); }
      fx.globalCompositeOperation = 'lighter';
      trail.forEach(function (q) { q.a -= .006; fx.globalAlpha = Math.max(0, q.a); fx.fillStyle = q.c; fx.shadowColor = q.c; fx.shadowBlur = 14; fx.beginPath(); fx.arc(q.x, q.y, q.r * (1.6 - q.a * .6), 0, 7); fx.fill(); });
      fx.globalCompositeOperation = 'source-over'; fx.globalAlpha = 1; fx.shadowBlur = 0;
      trail = trail.filter(function (q) { return q.a > 0; }); if (trail.length > 1600) trail.splice(0, trail.length - 1600);
    } else if (mode === 'school') {
      var still = real ? performance.now() - feet.t > 700 : false;
      school.forEach(function (f, i) {
        var cx = 0, cy = 0, n = 0;
        for (var j = i % 4; j < school.length; j += 4) { var o = school[j], d2 = (o.x - f.x) * (o.x - f.x) + (o.y - f.y) * (o.y - f.y); if (d2 < 4000 && d2 > 0) { cx += o.vx; cy += o.vy; n++; if (d2 < 220) { f.vx -= (o.x - f.x) * .02; f.vy -= (o.y - f.y) * .02; } } }
        if (n) { f.vx += (cx / n - f.vx) * .06; f.vy += (cy / n - f.vy) * .06; }
        f.vx += Math.cos(t / 3000) * .02; f.vy += Math.sin(t / 2500) * .02;
        var dx2 = f.x - p.x, dy2 = f.y - p.y, d = Math.hypot(dx2, dy2), R = still ? 34 : 95;
        if (d < R) { f.vx += dx2 / d * 1.4; f.vy += dy2 / d * 1.4; }
        var sp = Math.hypot(f.vx, f.vy); if (sp > 3.2) { f.vx *= 3.2 / sp; f.vy *= 3.2 / sp; } if (sp < .8) { f.vx *= .8 / sp; f.vy *= .8 / sp; }
        f.x = (f.x + f.vx + fW) % fW; f.y = (f.y + f.vy + fH) % fH; f.w += .3;
        drawFish(fx, f.x, f.y, Math.atan2(f.vy, f.vx), mobile ? .13 : .16, { body: '#bfe6f5', fin: '#6fb3cf', tail: '#6fb3cf', stripe: '#3fd0e8' }, false, f.w);
      });
    } else if (mode === 'rays') {
      if (moved > 110 || !lastStep) { if (lastStep) raysF.push({ x: p.x, y: p.y, s: 0, age: 0, dir: p.x < fW / 2 ? -1 : 1, vy: (Math.random() - .5) * .6 }); lastStep = { x: p.x, y: p.y }; }
      raysF.forEach(function (q) {
        q.age++; q.s = Math.min(1, q.s + .03);
        if (q.age < 30) { fx.fillStyle = 'rgba(220,200,160,' + (.35 * (1 - q.age / 30)) + ')'; fx.beginPath(); fx.arc(q.x, q.y, 20 + q.age * 1.6, 0, 7); fx.fill(); }
        else { q.x += q.dir * Math.min(3.2, (q.age - 30) * .08); q.y += q.vy; }
        fx.save(); fx.translate(q.x, q.y); fx.rotate(q.dir < 0 ? Math.PI : 0);
        fx.fillStyle = 'rgba(0,0,0,.22)'; fx.beginPath(); fx.ellipse(-4, 14, 30 * q.s, 44 * q.s, 0, 0, 7); fx.fill();
        manta(fx, 0, 0, (mobile ? .6 : .85) * q.s, t / 260 + q.age / 10, 'rgba(96,112,120,.97)');
        fx.restore();
      });
      raysF = raysF.filter(function (q) { return q.x > -120 && q.x < fW + 120; });
      if (raysF.length > 26) raysF.shift();
    } else if (mode === 'clean') {
      grass.forEach(function (g) {
        g.h = Math.min(g.H, g.h + .5);
        for (var b = 0; b < 7; b++) { var bx = g.x + (b - 3) * 6; fx.strokeStyle = b % 2 ? '#5fae3a' : '#86cc4a'; fx.lineWidth = 3; fx.beginPath(); fx.moveTo(bx, g.y); fx.quadraticCurveTo(bx + Math.sin(t / 700 + b) * 8, g.y - g.h / 2, bx + Math.sin(t / 600 + b + g.x) * 12, g.y - g.h); fx.stroke(); }
      });
      trash.forEach(function (q) {
        if (q.life <= 0) return;
        q.x += q.vx; q.a += .004;
        if (q.life === 1 && Math.hypot(q.x - p.x, q.y - p.y) < 48) { q.life = .99; }
        if (q.life < 1) { q.life -= .05; if (q.life <= 0) { cleaned++; grass.push({ x: q.x, y: q.y + 14, h: 0, H: 26 + Math.random() * 20 }); fstat.textContent = cleaned < trash.length ? 'мусора на дне: ' + (trash.length - cleaned) : 'дно чистое'; } }
        fx.save(); fx.globalAlpha = Math.max(0, q.life); fx.translate(q.x, q.y); fx.rotate(q.a);
        if (q.k === 0) { fx.fillStyle = 'rgba(160,210,220,.75)'; fx.fillRect(-16, -6, 28, 12); fx.fillRect(12, -3, 7, 6); fx.fillStyle = '#d33'; fx.fillRect(18, -3, 3, 6); }
        else if (q.k === 1) { fx.fillStyle = 'rgba(235,235,230,.7)'; fx.beginPath(); fx.moveTo(-14, -12); fx.quadraticCurveTo(0, -20, 14, -12); fx.lineTo(18, 14); fx.quadraticCurveTo(0, 20, -18, 14); fx.fill(); }
        else { fx.strokeStyle = 'rgba(255,170,90,.8)'; fx.lineWidth = 1.5; for (var g2 = -14; g2 <= 14; g2 += 7) { fx.beginPath(); fx.moveTo(g2, -14); fx.lineTo(g2 + 6, 14); fx.stroke(); fx.beginPath(); fx.moveTo(-14, g2); fx.lineTo(14, g2 + 4); fx.stroke(); } }
        fx.restore();
      });
      if (trash.length && cleaned === trash.length) {
        cleanDone++;
        var q2 = cleanDone * 2.2;
        for (var m = 0; m < 3; m++) manta(fx, -120 + q2 - m * 150, fH * (.3 + m * .2), mobile ? .6 : .8, t / 300 + m, 'rgba(58,72,80,.95)');
        if (-120 + q2 - 300 > fW + 100) initMode();
      }
    }
    if (mode !== 'rays') lastStep = { x: p.x, y: p.y };
    // «нога» посетителя
    fx.strokeStyle = real ? 'rgba(201,236,58,.85)' : 'rgba(255,255,255,.35)'; fx.lineWidth = 2;
    fx.beginPath(); fx.arc(p.x, p.y, 14, 0, 7); fx.stroke();
    if (!real) { fx.fillStyle = 'rgba(255,255,255,.5)'; fx.font = '12px "IBM Plex Mono", monospace'; fx.fillText('посетитель', p.x + 18, p.y + 4); }
  }

  /* ---------- варианты и слои схем ---------- */
  $$('#vtabs button').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('#vtabs button').forEach(function (x) { x.classList.toggle('on', x === b); });
      $$('#variants .var').forEach(function (v) { v.hidden = v.dataset.var !== b.dataset.var; });
      $$('#variants .cmp').forEach(function (c) { c.dataset.on = b.dataset.var; });
    });
  });
  $$('#variants .var').forEach(function (v) {
    var lyrs = $$('.lyr', v);
    $$('.layers button', v).forEach(function (b) {
      b.addEventListener('click', function () {
        var off = b.classList.toggle('off');
        lyrs.forEach(function (g) { if (g.dataset.l === b.dataset.l) g.classList.toggle('hide', off); });
      });
      b.addEventListener('mouseenter', function () { lyrs.forEach(function (g) { g.style.opacity = g.dataset.l === b.dataset.l || g.classList.contains('hide') ? '' : .25; }); });
      b.addEventListener('mouseleave', function () { lyrs.forEach(function (g) { g.style.opacity = ''; }); });
    });
  });

  /* ---------- раскраска рыбы ---------- */
  var cur = '#ff9a2e', parts = { body: '#ffffff', fin: '#ffffff', tail: '#ffffff', stripe: '#ffffff' };
  $$('#pal button').forEach(function (b) {
    b.addEventListener('click', function () { cur = b.dataset.c; $$('#pal button').forEach(function (x) { x.classList.toggle('on', x === b); }); });
  });
  var sheet = $('.sheet svg');
  $$('[data-part]', sheet).forEach(function (el) {
    el.addEventListener('click', function () {
      var k = el.dataset.part; parts[k] = cur;
      $$('[data-part="' + k + '"]', sheet).forEach(function (x) { x.setAttribute('fill', cur); });
    });
  });
  var rel = $('#release'), relMsg = $('#released');
  rel.addEventListener('click', function () {
    var painted = Object.keys(parts).some(function (k) { return parts[k] !== '#ffffff'; });
    if (!painted) { relMsg.textContent = 'Сначала раскрасьте хотя бы одну часть рыбы'; return; }
    var r = sheet.getBoundingClientRect();
    addMine({ body: parts.body, fin: parts.fin, tail: parts.tail, stripe: parts.stripe, line: '#1c2b33' }, r.left + r.width / 2, r.top + r.height / 2);
    relMsg.textContent = 'Ваша рыба плывёт по странице. Рыб в косяке: ' + mine.length + '. Она останется здесь до конца дня';
    sheet.style.transition = 'transform .5s, opacity .5s'; sheet.style.transform = 'translateX(60px)'; sheet.style.opacity = '0';
    setTimeout(function () {
      Object.keys(parts).forEach(function (k) { parts[k] = '#ffffff'; });
      $$('[data-part]', sheet).forEach(function (x) { x.setAttribute('fill', '#fff'); });
      sheet.style.transform = ''; sheet.style.opacity = '';
    }, 600);
  });

  /* ---------- маскот: касания ---------- */
  var FACES = D.faces || {};
  function face(k, txt) {
    $$('#face img').forEach(function (im) { im.classList.toggle('on', im.dataset.f === k); });
    var f = FACES[k]; if (!f) return;
    $('#fs').textContent = f[1]; $('#ft').textContent = txt || f[2];
  }
  var beakT = 0, beakTimer = null;
  $$('#pg .hs').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('#pg .hs').forEach(function (x) { x.classList.toggle('on', x === b); });
      var h = b.dataset.h;
      if (h === 'flip') face('laugh', 'Тронули ласту: смеётся');
      else if (h === 'belly') face('laugh', 'Тронули живот: икает и смеётся');
      else {
        var now = performance.now();
        clearTimeout(beakTimer);
        if (now - beakT < 450) { face('wink', 'Двойное касание клюва: замирает и подмигивает, на маске обратный отсчёт 5 секунд'); beakT = 0; }
        else { beakT = now; beakTimer = setTimeout(function () { face('wow', 'Тронули клюв: удивляется'); }, 300); }
      }
    });
  });
  $$('#fbtn button').forEach(function (b) { b.addEventListener('click', function () { face(b.dataset.f); }); });

  /* ---------- маскот: разрез ---------- */
  function part(i) {
    $$('#parts li').forEach(function (l) { l.classList.toggle('on', +l.dataset.p === i); });
    $$('#anat .pt').forEach(function (l) { l.classList.toggle('on', +l.dataset.p === i); });
  }
  $$('#parts li').forEach(function (l) { l.addEventListener('mouseenter', function () { part(+l.dataset.p); }); l.addEventListener('click', function () { part(+l.dataset.p); }); });
  $$('#anat .pt').forEach(function (l) { l.addEventListener('mouseenter', function () { part(+l.dataset.p); }); l.addEventListener('click', function () { part(+l.dataset.p); }); });

  /* ---------- маскот: день ---------- */
  var DAY = D.day || [], drange = $('#drange'), dayTouched = false;
  function setDay(i) {
    $$('#day img').forEach(function (im) { im.classList.toggle('on', +im.dataset.d === i); });
    var d = DAY[i]; if (!d) return;
    $('#dtm').textContent = d[0];
    var ds = $('#dds'); ds.style.setProperty('--c', 'var(' + d[3] + ')');
    ds.innerHTML = '<b>' + d[1] + '</b><span>' + d[2] + '</span>';
    drange.value = i;
  }
  drange.addEventListener('input', function () { dayTouched = true; setDay(+drange.value); });
  var dayVisible = false;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { dayVisible = es[0].isIntersecting; }, { threshold: .5 }).observe($('#day'));
  setInterval(function () { if (dayVisible && !dayTouched && !reduce) setDay((+drange.value + 1) % DAY.length); }, 3800);

  /* ---------- LED: вкладки и рыбы между экранами ---------- */
  var ledBox = $('#led-svg');
  $$('#ledtabs button').forEach(function (b) {
    b.addEventListener('click', function () { $$('#ledtabs button').forEach(function (x) { x.classList.toggle('on', x === b); }); ledBox.dataset.v = b.dataset.v; });
  });
  var NS = 'http://www.w3.org/2000/svg', lf = $('#ledfish'), ledF = [];
  var LCOL = [['#ff9a2e', '#ffd23f'], ['#3fd0e8', '#bff6ff'], ['#e64bd0', '#ffc2f4'], ['#c9ec3a', '#f2ffc0'], ['#ffd23f', '#ff9a2e']];
  var SHAPE = [['tail', 'M-27,0 L-54,-22 C-47,-8 -47,8 -54,22 Z'], ['fin', 'M-8,-19 C0,-38 18,-36 24,-17 Z'], ['fin', 'M-6,17 C0,30 12,30 17,16 Z'],
    ['body', 'M-32,0 C-22,-24 22,-28 44,-4 C48,0 48,2 44,6 C22,28 -22,24 -32,0 Z'], ['stripe', 'M2,-23 C12,-10 12,10 2,23 L-8,21 C1,9 1,-9 -8,-21 Z']];
  for (i = 0; i < 6; i++) {
    var g = document.createElementNS(NS, 'g'), c2 = LCOL[i % LCOL.length];
    SHAPE.forEach(function (s) { var pth = document.createElementNS(NS, 'path'); pth.setAttribute('d', s[1]); pth.setAttribute('fill', s[0] === 'body' ? c2[0] : s[0] === 'stripe' ? '#fff' : c2[1]); g.appendChild(pth); });
    var eye = document.createElementNS(NS, 'circle'); eye.setAttribute('cx', 32); eye.setAttribute('cy', -5); eye.setAttribute('r', 4); eye.setAttribute('fill', '#0b1a22'); g.appendChild(eye);
    lf.appendChild(g);
    ledF.push({ g: g, x: -2000 - i * 2700, y: 5300 + (i % 3) * 900, s: 11 + (i % 3) * 3, v: 26 + (i % 4) * 7, ph: i });
  }
  // кольцо из рыб в арке, как в знаке океанариума
  var ring = $('#ledring'), ringF = [];
  if (ring) for (i = 0; i < 11; i++) {
    var rg = document.createElementNS(NS, 'g'), rc = i % 3 ? ['#ffffff', '#cfe6f5'] : ['#3fd0e8', '#9ff0ff'];
    SHAPE.forEach(function (s) { var pth = document.createElementNS(NS, 'path'); pth.setAttribute('d', s[1]); pth.setAttribute('fill', s[0] === 'body' ? rc[0] : s[0] === 'stripe' ? '#0b3a5a' : rc[1]); rg.appendChild(pth); });
    ring.appendChild(rg); ringF.push(rg);
  }
  var ledVisible = false;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { ledVisible = es[0].isIntersecting; }).observe(ledBox); else ledVisible = true;
  function ledStep(t) {
    if (!ledVisible) return;
    var ra = t / 9000;
    ringF.forEach(function (g, k) {
      var a = ra + k / ringF.length * Math.PI * 2, R = 820 + Math.sin(t / 1400 + k) * 30;
      g.setAttribute('transform', 'translate(' + (Math.cos(a) * R).toFixed(0) + ' ' + (Math.sin(a) * R).toFixed(0) + ') rotate(' + ((a + Math.PI / 2) * 180 / Math.PI).toFixed(1) + ') scale(4.6)');
    });
    ledF.forEach(function (f) {
      f.x += f.v; if (f.x > 17800) f.x = -1800 - Math.random() * 3000;
      var y = f.y + Math.sin(t / 900 + f.ph) * 160;
      f.g.setAttribute('transform', 'translate(' + f.x.toFixed(0) + ' ' + y.toFixed(0) + ') scale(' + f.s + ')');
    });
  }

  /* ---------- параметры экранов: верно / иначе ---------- */
  var qrows = $$('.qrow'), qcount = $('#qcount');
  function qAnswers() {
    return qrows.map(function (r) {
      var a = r.dataset.a; if (!a) return null;
      var inp = r.querySelector('input');
      return r.dataset.q + (a === 'ok' ? ' верно' : ' иначе: ' + (inp.value.trim() || 'без пояснения'));
    }).filter(Boolean);
  }
  function qUpdate() { if (qcount) qcount.textContent = qAnswers().length; sumUpdate(); }
  qrows.forEach(function (r) {
    var inp = r.querySelector('input');
    $$('button', r).forEach(function (b) {
      b.addEventListener('click', function () {
        var same = r.dataset.a === b.dataset.a;
        r.dataset.a = same ? '' : b.dataset.a;
        $$('button', r).forEach(function (x) { x.classList.toggle('on', !same && x === b); });
        inp.hidden = r.dataset.a !== 'no';
        if (!inp.hidden) inp.focus();
        qUpdate();
      });
    });
    inp.addEventListener('input', qUpdate);
  });

  /* ---------- выбор идей и отправка на расчёт ---------- */
  var ideas = $$('.idea input[type="checkbox"]'), csum = $('#csum');
  function picked() { return ideas.filter(function (x) { return x.checked; }).map(function (x) { return x.dataset.label; }); }
  function sumUpdate() {
    if (!csum) return;
    var p = picked(), q = qAnswers().length;
    csum.textContent = (p.length ? 'Идей в расчёте: ' + p.length : 'Идеи пока не выбраны') + ' · параметров экранов подтверждено: ' + q + ' из ' + qrows.length;
  }
  ideas.forEach(function (x) { x.addEventListener('change', sumUpdate); });
  sumUpdate();
  var calc = $('#calc');
  // черновик выбора хранится в браузере, чтобы не потерять ответы при перезагрузке
  var DKEY = 'oc-calc-v1';
  function saveDraft() {
    if (!calc) return;
    var d = { ideas: ideas.filter(function (x) { return x.checked; }).map(function (x) { return x.value; }), q: {}, f: {} };
    qrows.forEach(function (r) { if (r.dataset.a) d.q[r.dataset.q] = [r.dataset.a, r.querySelector('input').value]; });
    var sp = $('input[name="supply"]:checked'); d.supply = sp ? sp.value : '';
    ['name', 'contact', 'comment'].forEach(function (k) { d.f[k] = calc.elements[k].value; });
    try { localStorage.setItem(DKEY, JSON.stringify(d)); } catch (e) { }
  }
  function loadDraft() {
    var d; try { d = JSON.parse(localStorage.getItem(DKEY) || 'null'); } catch (e) { }
    if (!d || !calc) return;
    ideas.forEach(function (x) { x.checked = d.ideas.indexOf(x.value) >= 0; });
    qrows.forEach(function (r) {
      var v = d.q[r.dataset.q]; if (!v) return;
      r.dataset.a = v[0]; var inp = r.querySelector('input'); inp.value = v[1] || ''; inp.hidden = v[0] !== 'no';
      $$('button', r).forEach(function (b) { b.classList.toggle('on', b.dataset.a === v[0]); });
    });
    $$('input[name="supply"]').forEach(function (x) { x.checked = x.value === d.supply; });
    ['name', 'contact', 'comment'].forEach(function (k) { if (d.f[k]) calc.elements[k].value = d.f[k]; });
    qUpdate();
  }
  loadDraft();
  document.addEventListener('change', saveDraft);
  document.addEventListener('input', function (ev) { if (ev.target.closest && ev.target.closest('#calc, .qrow')) saveDraft(); });
  qrows.forEach(function (r) { $$('button', r).forEach(function (b) { b.addEventListener('click', saveDraft); }); });

  function groupPicked(g) {
    return ideas.filter(function (x) { return x.checked && x.closest('.ig').dataset.g === g; }).map(function (x) { return x.dataset.label; }).join('; ');
  }
  function summaryText() {
    var f = calc.elements, sp = $('input[name="supply"]:checked');
    return ['Океанариум: выбор для расчёта', 'Имя: ' + f['name'].value.trim(), 'Контакт: ' + f['contact'].value.trim(),
      'Идеи: ' + (picked().join('; ') || 'не выбраны'), 'Где заказывать: ' + (sp ? sp.dataset.label : 'не выбрано'),
      'Параметры экранов: ' + (qAnswers().join('; ') || 'по нашему предложению'), 'Комментарий: ' + f['comment'].value.trim()].join('\n');
  }
  function fail(msg) {
    var err = $('#cerr');
    var mail = 'mailto:info@hand-marketing.ru?subject=' + encodeURIComponent('Океанариум: выбор для расчёта') + '&body=' + encodeURIComponent(summaryText());
    err.innerHTML = msg + ' Ваш выбор сохранён. <a href="' + mail + '">Отправить письмом</a> · <a href="#" id="ccopy">Скопировать выбор</a> · <a href="https://t.me/narodetskii" target="_blank" rel="noopener">Telegram</a>';
    err.hidden = false;
    $('#ccopy').addEventListener('click', function (e) {
      e.preventDefault();
      var t = summaryText();
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { e.target.textContent = 'Скопировано'; }, function () { window.prompt('Скопируйте текст', t); });
    });
  }
  if (calc) calc.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var f = calc.elements, err = $('#cerr'), contact = f['contact'].value.trim();
    err.hidden = true;
    if (contact.replace(/\D/g, '').length < 6 && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact)) {
      err.textContent = 'Укажите телефон или e-mail, чтобы мы прислали расчёт'; err.hidden = false; f['contact'].focus(); return;
    }
    if (!picked().length) { err.textContent = 'Отметьте хотя бы одну идею для расчёта'; err.hidden = false; return; }
    // обработчик заявок берёт до 20 полей по 500 символов: ответы режем по три пункта на поле
    var qa = qAnswers(), body = {
      form: 'for-oceanarium', company: 'Океанариум', name: f['name'].value.trim(), contact: contact, comment: f['comment'].value.trim(),
      ideas_wow: groupPicked('wow'), ideas_modules: groupPicked('mod'), ideas_mascot: groupPicked('mascot'), ideas_led: groupPicked('led'),
      supply: ($('input[name="supply"]:checked') || {}).value || '',
      led_answers: qa.length ? 'подтверждено ' + qa.length + ' из ' + qrows.length : 'не отмечены, считать по нашему предложению',
      website: f['website'].value
    };
    for (var k = 0; k < qa.length; k += 3) body['led_' + (k / 3 + 1)] = qa.slice(k, k + 3).join('; ');
    var btn = calc.querySelector('button'); btn.disabled = true; btn.textContent = 'Отправляем...';
    var ctl = window.AbortController ? new AbortController() : null, tm = setTimeout(function () { if (ctl) ctl.abort(); }, 20000);
    fetch('/api/lead.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { return r.json().catch(function () { return { status: r.status }; }).then(function (d) { d.status = r.status; return d; }); })
      .then(function (d) {
        clearTimeout(tm);
        if (d && (d.ok || d.success)) {
          calc.hidden = true; $('#cok').hidden = false;
          try { localStorage.removeItem(DKEY); } catch (e) { }
          if (window.ym) try { ym(71125393, 'reachGoal', 'oceanarium_calc'); } catch (e) { }
          return;
        }
        btn.disabled = false; btn.textContent = 'Отправить выбор на расчёт';
        fail(d.status === 429 ? 'Слишком частая отправка, подождите 10 секунд и нажмите ещё раз.' : 'Не получилось отправить.');
      })
      .catch(function () { clearTimeout(tm); btn.disabled = false; btn.textContent = 'Отправить выбор на расчёт'; fail('Не получилось отправить: нет связи с сервером.'); });
  });

  // цели Метрики: скачивание PDF (отправка выбора отмечается в обработчике формы)
  $$('.pdf-btn').forEach(function (a) { a.addEventListener('click', function () { if (window.ym) try { ym(71125393, 'reachGoal', 'oceanarium_pdf'); } catch (e) { } }); });

  /* ---------- появление и график ---------- */
  if ('IntersectionObserver' in window) {
    var rio = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); rio.unobserve(en.target); } }); }, { threshold: .12 });
    $$('.rv, #gantt').forEach(function (el) { rio.observe(el); });
  } else $$('.rv, #gantt').forEach(function (el) { el.classList.add('in'); });

  /* ---------- общий цикл ---------- */
  function loop(t) {
    if (!document.hidden) {
      seaStep(t); diveStep(t); floorStep(t); ledStep(t);
    }
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
