<?php
// Персональная страница для Самарского океанариума: WOW-зона, маскот, LED-экраны. Доступ по коду.
// Собирается scripts/ocean-page/build.py, руками не править.
// В файле только SHA-256 хеш кода. Аналитика визитов: _analytics.php, отчёт по ?stats=<ключ>.
define('HM_OCEAN', 1);
date_default_timezone_set('Europe/Moscow');
require __DIR__ . '/_analytics.php';

$ACCESS_HASH = 'd8d28567e28a71a911f09f578a8d1ba7ed5ad9aad9162e340d6a6b565ef149da';
$COOKIE_NAME = 'hm_oc_access';

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: private, no-store');

hm_vid();
if (isset($_GET['stats'])) { hm_stats_page($_GET['stats']); }

$authed = isset($_COOKIE[$COOKIE_NAME]) && hash_equals($ACCESS_HASH, $_COOKIE[$COOKIE_NAME]);

// Приём событий со страницы: только от вошедших
if (isset($_GET['track'])) {
    if (!$authed) { http_response_code(403); exit; }
    hm_track();
    exit;
}

$error = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = isset($_POST['code']) ? $_POST['code'] : '';
    $code = strtoupper(preg_replace('/\s+/', '', $input));
    if ($code !== '' && hash_equals($ACCESS_HASH, hash('sha256', $code))) {
        setcookie($COOKIE_NAME, $ACCESS_HASH, time() + 60 * 60 * 24 * 30, '/for/oceanarium/', '', hm_https(), true);
        $g = hm_geo(hm_ip());
        hm_event('login_ok', array('geo' => $g));
        hm_tg("🔓 <b>Океанариум открыл страницу</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where($g) . "\n" . date('d.m H:i'));
        header('Location: ./');
        exit;
    }
    // введённый текст не сохраняем: это может оказаться чужой пароль
    hm_event('login_fail', array('len' => function_exists('mb_strlen') ? mb_strlen($input) : strlen($input)));
    $error = true;
}

if (!$authed) {
    if ($_SERVER['REQUEST_METHOD'] === 'GET') hm_event('gate_view');
    $errHtml = $error ? '<p class="gate-error">Код не подошёл. Попробуйте ещё раз.</p>' : '';
    echo <<<GATE
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Доступ к странице · Океанариум × Hand Marketing</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/oswald-onest.css">
<link rel="stylesheet" href="/fonts/jost-intertight.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Inter Tight',system-ui,sans-serif; color:#eaf6ff; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:20px;
    background:radial-gradient(ellipse at 50% -10%, #1673a3 0%, #0a3d5e 30%, #04121e 70%); }
  .gate { width:100%; max-width:430px; padding:42px 34px 32px; border-radius:18px; background:rgba(4,20,34,.72); border:1px solid rgba(160,220,255,.16); backdrop-filter:blur(10px); }
  .logos { display:flex; align-items:center; gap:14px; margin-bottom:34px; font-family:'Oswald',sans-serif; font-size:14px; letter-spacing:.12em; text-transform:uppercase; color:#8fb3c9; }
  .logos img { height:28px; }
  h1 { font-family:'Oswald',sans-serif; font-weight:700; font-size:40px; line-height:1; margin-bottom:12px; }
  h1 span { color:#3fd0e8; }
  .sub { font-size:15px; color:#8fb3c9; margin-bottom:24px; }
  form { display:flex; flex-direction:column; gap:10px; }
  input { font-family:'Oswald',sans-serif; font-weight:500; font-size:20px; letter-spacing:.14em; text-align:center; text-transform:uppercase; color:#eaf6ff;
    padding:14px; border:1.5px solid rgba(160,220,255,.22); border-radius:10px; outline:none; background:rgba(255,255,255,.05); }
  input:focus { border-color:#3fd0e8; }
  button { font-family:'Inter Tight',sans-serif; font-weight:700; font-size:16px; color:#0e1d06; background:#c9ec3a; border:0; border-radius:10px; padding:16px; cursor:pointer; }
  button:hover { background:#d8f55c; }
  .gate-error { color:#ff6b78; font-size:13px; margin-top:4px; text-align:center; }
  .note { margin-top:24px; font-size:12px; color:#5b7d93; text-align:center; }
</style>
</head>
<body>
  <div class="gate">
    <div class="logos"><img src="hm-logo.svg" alt="Hand Marketing"><span>× океанариум</span></div>
    <h1>Глубина.<br><span>Материалы для вас</span></h1>
    <p class="sub">WOW-зона, маскот и LED-экраны на одной странице. Введите код доступа из письма</p>
    <form method="post" action="./" autocomplete="off">
      <input type="text" name="code" placeholder="код доступа" maxlength="30" autocapitalize="characters" spellcheck="false" autofocus required>
      <button type="submit">Погрузиться</button>
      {$errHtml}
    </form>
    <p class="note">Hand Marketing · доступ по личному приглашению</p>
  </div>
</body>
</html>
GATE;
    exit;
}
// PDF для печати: только после входа, прямой доступ к файлу закрыт в .htaccess
if (isset($_GET['pdf'])) {
    $f = __DIR__ . '/oceanarium.pdf';
    if (!is_file($f)) { http_response_code(404); exit; }
    hm_event('pdf_download');
    hm_tg("📄 <b>Океанариум скачал PDF</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where(hm_geo(hm_ip())) . "\n" . date('d.m H:i'));
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="Hand_Marketing_oceanarium.pdf"');
    header('Content-Length: ' . filesize($f));
    readfile($f);
    exit;
}
hm_event('page_view');
?>
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#04121e">
<title>Hand Marketing для Самарского океанариума: WOW-зона, маскот, LED-экраны</title>
<meta name="description" content="Иммерсивный зал «Глубина», ростовой маскот с живым лицом и техническое задание на LED-экраны входной группы.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/oswald-onest.css">
<link rel="stylesheet" href="/fonts/jost-intertight.css">
<link rel="stylesheet" href="/fonts/plex.css">
<style>
/* Страница для океанариума: погружение. Шрифты: Oswald (сжатый, как Proxima ExCn в наших презентациях) + Inter Tight, цифры глубины в IBM Plex Mono */
:root {
  --ink: #eaf6ff; --mut: #8fb3c9; --dim: #5b7d93;
  --line: rgba(160, 220, 255, .14); --card: rgba(8, 30, 48, .62); --card2: rgba(10, 40, 62, .78);
  --lime: #c9ec3a; --cyan: #3fd0e8; --mag: #e64bd0; --orange: #ff9a2e; --red: #ff4d5e; --teal: #2fb39a;
  --h: 'Oswald', 'Arial Narrow', sans-serif; --t: 'Inter Tight', system-ui, sans-serif; --m: 'IBM Plex Mono', ui-monospace, monospace;
  --wrap: 1180px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { font-family: var(--t); color: var(--ink); background: #04121e; font-size: 17px; line-height: 1.5; overflow-x: hidden; -webkit-font-smoothing: antialiased; }
img { display: block; max-width: 100%; }
a { color: inherit; }
button { font: inherit; color: inherit; cursor: pointer; }
.wrap { max-width: var(--wrap); margin: 0 auto; padding: 0 28px; position: relative; }

/* Фоновое море: цвет меняет скрипт по глубине, канвас с рыбами поверх цвета */
#bg { position: fixed; inset: 0; z-index: -2; background: #0b4a72; transition: background-color .25s linear; }
#sea { position: fixed; inset: 0; z-index: -1; width: 100%; height: 100%; pointer-events: none; }
.rays { position: fixed; inset: 0; z-index: -1; pointer-events: none; opacity: var(--rays, 1);
  background: repeating-linear-gradient(100deg, rgba(255,255,255,.0) 0 60px, rgba(190,235,255,.07) 60px 90px, rgba(255,255,255,0) 90px 170px);
  mask-image: linear-gradient(#000, transparent 70%); -webkit-mask-image: linear-gradient(#000, transparent 70%);
  animation: rays 14s ease-in-out infinite alternate; }
@keyframes rays { to { transform: translateX(-80px) skewX(-4deg); } }

/* Шапка */
.top { position: fixed; top: 0; left: 0; right: 0; z-index: 30; display: flex; align-items: center; gap: 18px; padding: 14px 28px;
  background: linear-gradient(rgba(3,14,24,.75), rgba(3,14,24,0)); }
.top img { height: 26px; }
.top .x { font-family: var(--h); font-size: 15px; letter-spacing: .06em; color: var(--mut); text-transform: uppercase; }
.top nav { margin-left: auto; display: flex; gap: 6px; }
.top nav a { text-decoration: none; font-size: 14px; font-weight: 600; padding: 8px 14px; border-radius: 30px; border: 1px solid var(--line); background: rgba(4,20,34,.5); backdrop-filter: blur(6px); }
.top nav a:hover { border-color: var(--cyan); color: var(--cyan); }

/* Глубиномер */
.gauge { position: fixed; right: 22px; top: 50%; transform: translateY(-50%); z-index: 25; width: 92px; text-align: right; pointer-events: none; }
.gauge .val { font-family: var(--m); font-weight: 500; font-size: 22px; line-height: 1; color: var(--lime); white-space: nowrap; }
.gauge .val small { font-size: 13px; color: var(--mut); margin-left: 3px; }
.gauge .lbl { font-family: var(--h); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--mut); margin-top: 6px; }
.gauge .tr { position: relative; height: 38vh; margin: 14px 0 0 auto; width: 2px; background: var(--line); }
.gauge .tr i { position: absolute; left: -4px; width: 10px; height: 10px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 14px var(--lime); top: 0; transform: translateY(-50%); }
.gauge .tr b { position: absolute; right: 12px; transform: translateY(-50%); font-family: var(--m); font-weight: 400; font-size: 10px; color: var(--dim); white-space: nowrap; }

/* Типографика */
section { position: relative; padding: 120px 0; }
.kick { font-family: var(--h); font-weight: 500; font-size: 14px; letter-spacing: .16em; text-transform: uppercase; color: var(--lime); margin-bottom: 18px; display: flex; gap: 12px; align-items: center; }
.kick em { font-style: normal; font-family: var(--m); color: var(--mut); letter-spacing: 0; font-size: 13px; }
h1, h2, h3 { font-family: var(--h); font-weight: 700; line-height: 1.02; letter-spacing: -.005em; }
h2 { font-size: clamp(38px, 5.4vw, 72px); max-width: 15ch; margin-bottom: 26px; }
h3 { font-size: 26px; line-height: 1.1; margin-bottom: 10px; }
.lead { font-size: 20px; color: #cfe6f5; max-width: 62ch; }
.sm { font-size: 14px; color: var(--mut); }
.note { font-size: 14px; color: var(--mut); max-width: 80ch; margin-top: 22px; }
.c-lime { color: var(--lime); } .c-cyan { color: var(--cyan); } .c-mag { color: var(--mag); } .c-orange { color: var(--orange); } .c-red { color: var(--red); } .c-teal { color: var(--teal); }

/* Хиро */
.hero { min-height: 100vh; display: flex; align-items: flex-end; padding: 140px 0 70px; }
.hero h1 { font-size: clamp(64px, 12vw, 176px); line-height: .9; letter-spacing: -.01em; margin-bottom: 26px; }
.hero h1 span { display: block; font-size: .38em; letter-spacing: .01em; color: var(--cyan); margin-top: 10px; }
.hero .lead { font-size: clamp(18px, 2vw, 23px); }
.trio { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 46px; }
.trio a { display: block; text-decoration: none; padding: 20px 22px 22px; border-radius: 14px; border: 1px solid var(--line); background: var(--card); backdrop-filter: blur(8px); transition: border-color .2s, transform .2s; }
.trio a:hover { transform: translateY(-3px); border-color: var(--cyan); }
.trio b { font-family: var(--h); font-weight: 600; font-size: 24px; display: block; margin: 6px 0 4px; }
.trio i { font-style: normal; font-family: var(--m); font-size: 12px; color: var(--lime); }
.trio span { font-size: 14px; color: var(--mut); }
.scrollhint { margin-top: 38px; font-size: 13px; color: var(--mut); display: flex; gap: 10px; align-items: center; }
.scrollhint:before { content: ''; width: 1px; height: 34px; background: linear-gradient(var(--lime), transparent); animation: drip 1.8s infinite; }
@keyframes drip { 0% { transform: scaleY(.2); transform-origin: top; } 60% { transform: scaleY(1); } 100% { opacity: 0; } }

/* Запрос построчно */
.req { display: grid; gap: 1px; background: var(--line); border-radius: 14px; overflow: hidden; border: 1px solid var(--line); }
.req div { display: grid; grid-template-columns: 40px 260px 1fr; gap: 16px; align-items: baseline; padding: 18px 22px; background: var(--card2); }
.req div i { font-style: normal; font-family: var(--m); font-size: 12px; color: var(--dim); }
.req div b { font-weight: 600; }
.req div span { color: #c3dbea; font-size: 16px; }
.req .plus { background: rgba(201,236,58,.08); }
.req .plus b { color: var(--lime); }

.nums { display: grid; grid-template-columns: repeat(3, 1fr); gap: 34px; margin: 40px 0 34px; }
.nums b { font-family: var(--h); font-weight: 700; font-size: clamp(44px, 5vw, 66px); line-height: 1; display: block; margin-bottom: 8px; }
.nums span { font-size: 15px; color: var(--mut); display: block; max-width: 30ch; }
.facts2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.facts2 p { padding: 16px 18px; border-radius: 12px; background: var(--card); border: 1px solid var(--line); font-size: 15px; color: #c3dbea; }

/* Погружение по главам */
.dive { display: grid; grid-template-columns: 1fr 1.15fr; gap: 50px; align-items: start; }
.dive .sticky { position: sticky; top: 100px; }
.chap { list-style: none; border-left: 2px solid var(--line); }
.chap li { position: relative; padding: 18px 0 18px 30px; cursor: pointer; opacity: .55; transition: opacity .25s; }
.chap li:before { content: ''; position: absolute; left: -7px; top: 26px; width: 12px; height: 12px; border-radius: 50%; background: #04121e; border: 2px solid var(--dim); transition: all .25s; }
.chap li.on { opacity: 1; }
.chap li.on:before { background: var(--c); border-color: var(--c); box-shadow: 0 0 16px var(--c); }
.chap .d { font-family: var(--m); font-weight: 500; font-size: 26px; color: var(--c); }
.chap .n { font-family: var(--h); font-size: 13px; letter-spacing: .16em; text-transform: uppercase; color: var(--mut); margin-left: 10px; }
.chap p { font-size: 16px; color: #c3dbea; margin-top: 4px; max-width: 46ch; }
.window { position: relative; aspect-ratio: 4 / 3.2; border-radius: 18px; overflow: hidden; border: 1px solid var(--line); background: #021019; }
.window canvas { position: absolute; inset: 0; width: 100%; height: 100%; }
.window .meter { position: absolute; left: 18px; top: 16px; font-family: var(--m); font-size: 34px; font-weight: 500; color: #fff; text-shadow: 0 0 20px rgba(0,0,0,.6); }
.window .meter small { font-size: 14px; color: var(--mut); margin-left: 4px; }
.window .cap { position: absolute; left: 18px; bottom: 14px; right: 18px; font-size: 13px; color: var(--mut); }
.link { margin-top: 26px; padding: 18px 20px; border-radius: 12px; background: rgba(63,208,232,.08); border: 1px solid rgba(63,208,232,.25); font-size: 15px; color: #cfe6f5; }
.link b { color: var(--cyan); }

/* Два режима */
.modes { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.mode { padding: 26px; border-radius: 16px; background: var(--card); border: 1px solid var(--line); }
.mode .k { font-family: var(--h); font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--lime); }
.mode h3 { margin: 8px 0 14px; font-size: 32px; }
.mode ul { list-style: none; }
.mode li { padding: 7px 0 7px 22px; position: relative; font-size: 15px; color: #c3dbea; border-top: 1px solid var(--line); }
.mode li:before { content: ''; position: absolute; left: 2px; top: 15px; width: 7px; height: 7px; border-radius: 50%; background: var(--cyan); }
.cycle { margin-top: 18px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.cycle div { padding: 20px 22px; border-radius: 14px; border: 1px solid var(--line); }
.cycle b { font-family: var(--h); font-size: 50px; line-height: 1; display: block; }
.cycle span { font-size: 14px; color: var(--mut); }

/* Интерактивный пол */
.floor { position: relative; border-radius: 20px; overflow: hidden; border: 1px solid var(--line); background: #03131d; touch-action: none; aspect-ratio: 16 / 8; cursor: none; }
.floor canvas { position: absolute; inset: 0; width: 100%; height: 100%; }
.floor .hint { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); font-family: var(--h); font-size: 20px; letter-spacing: .06em; text-transform: uppercase; color: rgba(255,255,255,.55); pointer-events: none; transition: opacity .5s; text-align: center; }
.floor .stat { position: absolute; right: 16px; top: 14px; font-family: var(--m); font-size: 13px; color: var(--mut); pointer-events: none; }
.tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 26px 0 16px; }
.tabs button { border: 1px solid var(--line); background: var(--card); border-radius: 30px; padding: 10px 18px; font-weight: 600; font-size: 15px; }
.tabs button i { font-style: normal; font-family: var(--m); font-size: 12px; color: var(--dim); margin-right: 8px; }
.tabs button.on { background: var(--lime); color: #071a0c; border-color: var(--lime); }
.tabs button.on i { color: #355000; }
.floor-desc { display: grid; grid-template-columns: 1.3fr 1fr; gap: 30px; margin-top: 22px; }
.floor-desc p { font-size: 16px; color: #c3dbea; }
.floor-desc .how { font-size: 14px; color: var(--mut); padding-left: 18px; border-left: 2px solid var(--line); }

/* Схема зала */
.plan { display: grid; grid-template-columns: 1.25fr 1fr; gap: 36px; align-items: start; }
.plan svg { width: 100%; height: auto; display: block; border-radius: 16px; background: rgba(2,14,22,.75); border: 1px solid var(--line); }
.layers { display: grid; gap: 8px; }
.layers button { display: grid; grid-template-columns: 96px 1fr; gap: 14px; align-items: baseline; text-align: left; padding: 14px 16px; border-radius: 12px; border: 1px solid var(--line); background: var(--card); transition: all .2s; }
.layers button b { font-family: var(--h); font-size: 20px; font-weight: 600; color: var(--c); }
.layers button span { font-size: 14px; color: #c3dbea; }
.layers button.off { opacity: .38; }
.layers button:hover { border-color: var(--c); }
.plan .lyr { transition: opacity .3s; }
.plan .lyr.hide { opacity: 0; }
.plan .why { margin-top: 14px; padding: 16px 18px; border-radius: 12px; background: var(--card2); font-size: 14px; color: #c3dbea; }

/* Таблица оборудования */
.eq { display: grid; gap: 8px; }
.eq div { display: grid; grid-template-columns: 70px 300px 1fr; gap: 18px; align-items: center; padding: 16px 22px; border-radius: 12px; background: var(--card); border: 1px solid var(--line); }
.eq b { font-family: var(--h); font-size: 40px; color: var(--lime); line-height: 1; }
.eq strong { font-weight: 600; }
.eq span { font-size: 15px; color: #c3dbea; }
.six { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 40px; }
.six div { padding: 22px; border-radius: 14px; background: var(--card); border: 1px solid var(--line); }
.six i { font-style: normal; font-family: var(--m); font-size: 13px; color: var(--c, var(--cyan)); }
.six b { display: block; font-family: var(--h); font-size: 22px; font-weight: 600; margin: 6px 0; }
.six p { font-size: 14px; color: #b7d0df; }

/* Модули */
.paint { display: grid; grid-template-columns: 1.1fr 1fr; gap: 40px; align-items: center; padding: 34px; border-radius: 22px; background: #f3efe6; color: #182630; }
.paint .kick { color: #4b7a00; }
.paint h2 { color: #0d1b24; }
.paint .lead { color: #33454f; }
.paint .steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 22px; }
.paint .steps div { font-size: 13px; color: #4a5b65; }
.paint .steps b { display: block; font-family: var(--h); font-size: 18px; color: #0d1b24; }
.paint .steps i { font-style: normal; font-family: var(--m); color: #b04a9e; font-size: 12px; }
.sheet { background: #fff; border-radius: 10px; padding: 18px; box-shadow: 0 20px 40px rgba(0,0,0,.18); transform: rotate(-1.5deg); }
.sheet .t { display: flex; justify-content: space-between; font-family: var(--h); font-size: 13px; letter-spacing: .12em; text-transform: uppercase; color: #8a969c; margin-bottom: 6px; }
.sheet svg { width: 100%; height: auto; display: block; }
.sheet svg [data-part] { cursor: pointer; transition: fill .15s; stroke: #1c2b33; stroke-width: 3; stroke-linejoin: round; }
.pal { display: flex; gap: 8px; flex-wrap: wrap; margin: 12px 0 14px; }
.pal button { width: 34px; height: 34px; border-radius: 50%; border: 3px solid #fff; box-shadow: 0 0 0 1px #c8ccce; }
.pal button.on { box-shadow: 0 0 0 3px #182630; }
.release { width: 100%; border: 0; border-radius: 10px; padding: 15px; background: #182630; color: #fff; font-weight: 700; font-size: 16px; }
.release:hover { background: #0b4a72; }
.release[disabled] { opacity: .5; cursor: default; }
.released { font-size: 13px; color: #4b7a00; margin-top: 8px; min-height: 20px; text-align: center; }

.mods { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-top: 18px; }
.mod { padding: 26px; border-radius: 16px; background: var(--card); border: 1px solid var(--line); }
.mod .k { font-family: var(--h); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--mut); }
.mod h3 { margin: 6px 0 10px; color: var(--c); font-size: 28px; }
.mod p { font-size: 15px; color: #c3dbea; }
.mod .term { font-family: var(--m); font-size: 12px; color: var(--lime); margin-top: 14px; }
.mod .flow { display: flex; gap: 6px; margin-top: 14px; flex-wrap: wrap; }
.mod .flow span { font-size: 12px; padding: 5px 10px; border-radius: 20px; background: rgba(255,255,255,.06); color: #cfe6f5; }

/* Маскот */
.masc-hero { position: relative; border-radius: 22px; overflow: hidden; min-height: 560px; display: flex; align-items: flex-end; }
.masc-hero img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 60% 30%; }
.masc-hero:after { content: ''; position: absolute; inset: 0; background: linear-gradient(transparent 35%, rgba(2,8,14,.92)); }
.masc-hero .in { position: relative; z-index: 2; padding: 38px; max-width: 760px; }
.masc-hero h2 { margin-bottom: 14px; }
.mnum { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 18px; }
.mnum div { padding: 20px; border-radius: 14px; background: var(--card); border: 1px solid var(--line); }
.mnum b { font-family: var(--h); font-size: 46px; line-height: 1; display: block; }
.mnum span { font-size: 14px; color: var(--mut); }

.play { display: grid; grid-template-columns: .9fr 1.1fr; gap: 34px; align-items: center; margin-top: 80px; }
.pg { position: relative; border-radius: 18px; overflow: hidden; background: #0a0a0c; }
.pg img { width: 100%; }
.pg .hs { position: absolute; transform: translate(-50%, -50%); width: 46px; height: 46px; border-radius: 50%; border: 2px solid #fff; background: rgba(201,236,58,.25); }
.pg .hs:before { content: ''; position: absolute; inset: -9px; border-radius: 50%; border: 2px solid rgba(201,236,58,.7); animation: ping 2s infinite; }
.pg .hs span { position: absolute; left: 50%; top: 100%; transform: translateX(-50%); margin-top: 6px; white-space: nowrap; font-size: 12px; font-weight: 600; background: rgba(0,0,0,.65); padding: 3px 8px; border-radius: 10px; }
.pg .hs:hover, .pg .hs.on { background: var(--lime); }
@keyframes ping { 0% { transform: scale(.8); opacity: 1; } 100% { transform: scale(1.5); opacity: 0; } }
.face { position: relative; border-radius: 18px; overflow: hidden; aspect-ratio: 1; background: #071624; }
.face img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: opacity .35s; }
.face img.on { opacity: 1; }
.face .say { position: absolute; left: 18px; bottom: 18px; right: 18px; padding: 14px 16px; border-radius: 14px; background: rgba(2,10,18,.78); backdrop-filter: blur(6px); }
.face .say b { font-family: var(--h); font-size: 24px; color: var(--lime); display: block; }
.face .say span { font-size: 14px; color: #cfe6f5; }
.fbtn { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
.fbtn button { border: 1px solid var(--line); background: var(--card); border-radius: 30px; padding: 9px 15px; font-size: 14px; font-weight: 600; }
.fbtn button:hover, .fbtn button.on { border-color: var(--lime); color: var(--lime); }

.anat { display: grid; grid-template-columns: .85fr 1fr; gap: 40px; align-items: center; margin-top: 90px; }
.anat .pic { position: relative; border-radius: 18px; overflow: hidden; background: #0b0b0d; }
.anat .pic .pt { position: absolute; transform: translate(-50%, -50%); width: 28px; height: 28px; border-radius: 50%; font-family: var(--m); font-size: 13px; font-weight: 600; color: #000; background: var(--c); border: 2px solid #fff; display: grid; place-items: center; transition: transform .2s; }
.anat .pic .pt.on { transform: translate(-50%, -50%) scale(1.35); box-shadow: 0 0 0 6px rgba(255,255,255,.2); }
.parts { list-style: none; counter-reset: p; }
.parts li { display: grid; grid-template-columns: 34px 1fr; gap: 12px; padding: 11px 12px; border-radius: 10px; cursor: default; transition: background .2s; }
.parts li:hover, .parts li.on { background: rgba(255,255,255,.06); }
.parts li i { font-style: normal; width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center; font-family: var(--m); font-size: 12px; font-weight: 600; color: #000; background: var(--c); }
.parts li b { font-weight: 600; display: block; }
.parts li span { font-size: 14px; color: var(--mut); }

.day { margin-top: 90px; }
.day .stage { position: relative; border-radius: 18px; overflow: hidden; aspect-ratio: 16 / 9; max-height: 560px; width: 100%; background: #061220; }
.day .stage img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: opacity .5s; }
.day .stage img.on { opacity: 1; }
.day .stage .tm { position: absolute; left: 20px; top: 16px; font-family: var(--m); font-size: 40px; font-weight: 500; text-shadow: 0 2px 20px rgba(0,0,0,.5); }
.day .stage .ds { position: absolute; left: 20px; bottom: 18px; max-width: 480px; padding: 14px 16px; border-radius: 14px; background: rgba(2,10,18,.8); }
.day .stage .ds b { font-family: var(--h); font-size: 24px; display: block; color: var(--c, var(--lime)); }
.day .stage .ds span { font-size: 14px; color: #cfe6f5; }
.slider { margin-top: 18px; }
.slider input { width: 100%; accent-color: var(--lime); height: 28px; }
.slider .ticks { display: flex; justify-content: space-between; font-family: var(--m); font-size: 12px; color: var(--mut); }

.states { margin-top: 30px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--line); border-radius: 14px; overflow: hidden; border: 1px solid var(--line); }
.states div { padding: 16px 18px; background: var(--card2); }
.states b { font-family: var(--h); font-weight: 600; font-size: 19px; color: var(--c); }
.states em { font-style: normal; font-family: var(--m); font-size: 11px; color: var(--dim); float: right; margin-top: 5px; }
.states p { font-size: 13px; color: #b7d0df; margin-top: 4px; }

.opts { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 90px; }
.opt { border-radius: 16px; overflow: hidden; background: var(--card); border: 1px solid var(--line); }
.opt img { width: 100%; aspect-ratio: 2.8; object-fit: cover; }
.opt .in { padding: 22px; }
.opt h3 { color: var(--c); }
.opt ul { list-style: none; }
.opt li { font-size: 14px; color: #c3dbea; padding: 5px 0 5px 18px; position: relative; }
.opt li:before { content: ''; position: absolute; left: 0; top: 13px; width: 6px; height: 6px; border-radius: 50%; background: var(--c); }
.opt .best { margin-top: 12px; font-family: var(--h); font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--c); }

.make { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 26px; }
.make div { border-radius: 14px; overflow: hidden; background: var(--card); border: 1px solid var(--line); }
.make img { width: 100%; aspect-ratio: 3 / 2; object-fit: cover; }
.make p { padding: 12px 14px 16px; font-size: 13px; color: #b7d0df; }
.make p b { display: block; font-family: var(--h); font-size: 18px; color: var(--ink); }
.make p i { font-style: normal; font-family: var(--m); font-size: 12px; color: var(--lime); }

.duo { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; }
.ph { position: relative; border-radius: 16px; overflow: hidden; min-height: 340px; display: flex; align-items: flex-end; }
.ph img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.ph:after { content: ''; position: absolute; inset: 0; background: linear-gradient(transparent 40%, rgba(2,8,14,.9)); }
.ph div { position: relative; z-index: 2; padding: 22px; }
.ph b { font-family: var(--h); font-size: 26px; display: block; }
.ph span { font-size: 14px; color: #cfe6f5; }
.heroes { display: grid; grid-template-columns: 1.2fr 1fr; gap: 14px; margin-top: 14px; }
.heroes > img { border-radius: 16px; width: 100%; height: 100%; object-fit: cover; }
.heroes ul { list-style: none; display: grid; gap: 8px; }
.heroes li { padding: 16px 18px; border-radius: 12px; background: var(--card); border: 1px solid var(--line); }
.heroes li b { font-family: var(--h); font-size: 20px; color: var(--lime); display: block; }
.heroes li span { font-size: 14px; color: #c3dbea; }

/* LED-экран */
.led-wrap { border-radius: 20px; background: linear-gradient(#e9edf0, #d9dee2); padding: 26px 26px 18px; color: #1b2a33; }
.led-wrap svg { width: 100%; height: auto; display: block; }
.led-bar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.led-bar .tabs { margin: 0; }
.led-bar .tabs button { background: #fff; border-color: #c6ced4; color: #1b2a33; }
.led-bar .tabs button.on { background: #1b2a33; color: #fff; border-color: #1b2a33; }
.led-bar .sm { color: #5a6a73; }
.led-legend { display: flex; flex-wrap: wrap; gap: 18px; font-size: 13px; color: #4a5a63; margin-top: 10px; }
.led-legend span:before { content: ''; display: inline-block; width: 12px; height: 12px; border-radius: 3px; background: var(--c); margin-right: 6px; vertical-align: -1px; }
.ledk { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 18px; }
.ledk div { padding: 20px; border-radius: 14px; background: var(--card); border: 1px solid var(--line); }
.ledk b { font-family: var(--h); font-size: 36px; line-height: 1; display: block; color: var(--c, var(--ink)); }
.ledk span { font-size: 13px; color: var(--mut); display: block; margin-top: 6px; }
.spec { margin-top: 40px; display: grid; grid-template-columns: 1fr 1fr; gap: 0 40px; }
.spec div { display: grid; grid-template-columns: 170px 1fr; gap: 14px; padding: 13px 0; border-top: 1px solid var(--line); font-size: 15px; }
.spec dt, .spec b { font-weight: 600; color: var(--ink); }
.spec span { color: #c3dbea; }
.qs { margin-top: 50px; }
.qs details { border-top: 1px solid var(--line); }
.qs summary { list-style: none; cursor: pointer; display: grid; grid-template-columns: 42px 1fr 24px; gap: 12px; padding: 15px 0; font-weight: 600; font-size: 16px; }
.qs summary::-webkit-details-marker { display: none; }
.qs summary i { font-style: normal; font-family: var(--m); font-size: 13px; color: var(--lime); padding-top: 2px; }
.qs summary:after { content: '+'; font-family: var(--m); color: var(--mut); font-size: 20px; line-height: 1; }
.qs details[open] summary:after { content: '–'; }
.qs details p { padding: 0 0 18px 54px; color: #c3dbea; font-size: 15px; }
.qs details p b { color: var(--cyan); font-weight: 600; }
.next { margin-top: 30px; padding: 24px 26px; border-radius: 16px; background: rgba(201,236,58,.1); border: 1px solid rgba(201,236,58,.35); }
.next h3 { color: var(--lime); font-size: 24px; }
.next ul { list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 6px 26px; margin-top: 10px; }
.next li { font-size: 15px; color: #dcebf3; padding-left: 20px; position: relative; }
.next li:before { content: '→'; position: absolute; left: 0; color: var(--lime); }

/* Сроки */
.gantt { border-radius: 16px; background: var(--card); border: 1px solid var(--line); padding: 20px 22px; overflow-x: auto; }
.gantt .row { display: grid; grid-template-columns: 290px repeat(16, minmax(30px, 1fr)); align-items: center; min-width: 760px; }
.gantt .row + .row { border-top: 1px solid var(--line); }
.gantt .hd span { font-family: var(--m); font-size: 12px; color: var(--mut); text-align: center; padding: 6px 0; }
.gantt .hd span:first-child { text-align: left; font-family: var(--h); letter-spacing: .14em; text-transform: uppercase; }
.gantt .row > b { font-weight: 500; font-size: 14px; padding: 10px 0; color: #cfe6f5; }
.gantt .row > i { height: 18px; border-radius: 9px; background: var(--c); margin: 0 2px; transform-origin: left; transform: scaleX(0); transition: transform .9s cubic-bezier(.2,.7,.2,1); }
.gantt.in .row > i { transform: scaleX(1); }
.gantt .row.you > b { color: var(--mut); }

/* Опыт */
.cases { display: grid; grid-template-columns: 1.4fr 1fr 1fr; grid-auto-rows: 260px; gap: 12px; }
.case { position: relative; border-radius: 16px; overflow: hidden; text-decoration: none; display: flex; align-items: flex-end; }
.case img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transition: transform .6s; }
.case:hover img { transform: scale(1.05); }
.case:after { content: ''; position: absolute; inset: 0; background: linear-gradient(transparent 30%, rgba(2,8,14,.92)); }
.case div { position: relative; z-index: 2; padding: 18px 20px; }
.case b { font-family: var(--h); font-size: 22px; display: block; line-height: 1.1; }
.case span { font-size: 13px; color: #cfe6f5; display: block; margin-top: 4px; }
.case.big { grid-row: span 2; }
.case.big b { font-size: 32px; }
.case.big .k { font-family: var(--m); font-size: 12px; color: var(--lime); }

/* Состав и цена */
.scope { display: grid; grid-template-columns: 1fr 1.4fr; gap: 40px; align-items: start; }
.price { padding: 28px; border-radius: 18px; background: var(--lime); color: #0e1d06; }
.price h3 { font-size: 30px; }
.price p { font-size: 15px; margin-top: 10px; color: #233a05; }
.scope dl div { display: grid; grid-template-columns: 160px 1fr; gap: 16px; padding: 14px 0; border-top: 1px solid var(--line); }
.scope dt { font-family: var(--h); font-size: 20px; font-weight: 600; }
.scope dd { font-size: 15px; color: #c3dbea; }
.scope .no { color: var(--mut); }
.zamer { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 40px; }
.zamer div { padding: 20px; border-radius: 14px; border: 1px solid var(--line); background: var(--card); }
.zamer b { font-family: var(--h); font-size: 20px; font-weight: 600; display: block; margin-bottom: 4px; }
.zamer span { font-size: 14px; color: #b7d0df; }
.offer { margin-top: 18px; padding: 22px 24px; border-radius: 14px; background: rgba(63,208,232,.1); border: 1px solid rgba(63,208,232,.3); font-size: 17px; }

/* Контакты */
.contacts { padding-bottom: 60px; }
.ct { display: grid; grid-template-columns: 1.2fr 1fr; gap: 40px; align-items: end; }
.ct h2 { font-size: clamp(56px, 8vw, 110px); }
.ct .who b { font-family: var(--h); font-size: 28px; display: block; }
.ct .who span { color: var(--mut); font-size: 15px; }
.ct .btns { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
.ct .btns a { text-decoration: none; padding: 14px 22px; border-radius: 30px; font-weight: 700; font-size: 16px; background: var(--lime); color: #0e1d06; }
.ct .btns a.o { background: transparent; color: var(--ink); border: 1px solid var(--line); }
.ct .btns a.o:hover { border-color: var(--cyan); color: var(--cyan); }
.ct dl { display: grid; grid-template-columns: 120px 1fr; gap: 8px 16px; font-size: 15px; }
.ct dt { color: var(--mut); }
.ct dd a { text-decoration: none; border-bottom: 1px solid var(--line); }
.foot { margin-top: 60px; font-size: 13px; color: var(--dim); }

/* Появление */
.rv { opacity: 0; transform: translateY(26px); transition: opacity .8s, transform .8s; }
.rv.in { opacity: 1; transform: none; }

/* Адаптив */
@media (max-width: 1100px) {
  .gauge { right: 10px; width: 70px; }
  .gauge .val { font-size: 17px; }
  .wrap { padding-right: 96px; }
}
@media (max-width: 900px) {
  body { font-size: 16px; }
  section { padding: 84px 0; }
  .wrap { padding: 0 18px; }
  .top { padding: 10px 16px; }
  .top nav { display: none; }
  .gauge { top: auto; bottom: 14px; transform: none; right: 12px; width: auto; padding: 8px 12px; border-radius: 12px; background: rgba(2,12,20,.72); backdrop-filter: blur(6px); }
  .gauge .tr { display: none; }
  .gauge .lbl { margin-top: 3px; font-size: 10px; }
  .trio, .nums, .cycle, .six, .zamer { grid-template-columns: 1fr; }
  .nums { gap: 22px; }
  .facts2, .modes, .mods, .opts, .duo, .heroes, .next ul, .spec { grid-template-columns: 1fr; }
  .req div { grid-template-columns: 30px 1fr; }
  .req div span { grid-column: 2; }
  .dive, .plan, .paint, .play, .anat, .scope, .ct, .floor-desc { grid-template-columns: 1fr; gap: 26px; }
  .dive .sticky { position: sticky; top: 56px; z-index: 3; }
  .window { aspect-ratio: 16 / 9; }
  .floor { aspect-ratio: 4 / 3.4; }
  .eq div { grid-template-columns: 54px 1fr; }
  .eq div span { grid-column: 2; }
  .eq b { font-size: 32px; }
  .mnum, .ledk { grid-template-columns: 1fr 1fr; }
  .states { grid-template-columns: 1fr; }
  .make { grid-template-columns: 1fr 1fr; }
  .make div:last-child { grid-column: span 2; }
  .paint { padding: 22px 18px; }
  .paint .steps { grid-template-columns: 1fr 1fr; }
  .masc-hero { min-height: 520px; }
  .masc-hero .in { padding: 22px; }
  .cases { grid-template-columns: 1fr 1fr; grid-auto-rows: 200px; }
  .case.big { grid-column: span 2; grid-row: span 1; }
  .spec div { grid-template-columns: 130px 1fr; }
  .led-wrap { padding: 14px 12px 12px; border-radius: 14px; }
  .qs details p { padding-left: 0; }
  .scope dl div { grid-template-columns: 1fr; gap: 4px; }
  .ct dl { grid-template-columns: 96px 1fr; }
}
@media (max-width: 900px) and (orientation: landscape) {
  .hero { min-height: auto; padding-top: 90px; }
  .dive .sticky { position: static; }
  .floor { aspect-ratio: 16 / 7; }
  .masc-hero { min-height: 380px; }
}
@media (max-width: 520px) {
  .mnum b { font-size: 38px; }
  .ledk b { font-size: 28px; }
  .cases { grid-template-columns: 1fr; }
  .case.big { grid-column: auto; }
  .make { grid-template-columns: 1fr; }
  .make div:last-child { grid-column: auto; }
  .gauge .lbl { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  .rays { animation: none; }
  .rv { opacity: 1; transform: none; transition: none; }
}

/* LED: вкладки «контент / модули / кабинеты» */
#led-svg .led-mod, #led-svg .led-cab { display: none; }
#led-svg[data-v="mod"] .led-mod { display: inline; }
#led-svg[data-v="cab"] .led-mod { display: inline; opacity: .35; }
#led-svg[data-v="cab"] .led-cab { display: inline; }
#led-svg[data-v="mod"] .ledc, #led-svg[data-v="cab"] .ledc { opacity: .25; }
.led-rays { animation: ledrays 9s ease-in-out infinite alternate; }
@keyframes ledrays { to { transform: translateX(600px); } }
.chap li { padding-top: 26px; padding-bottom: 26px; }

/* телефон: график без горизонтальной прокрутки, фасад LED листается вбок */
@media (max-width: 900px) {
  .gantt { padding: 14px; overflow: visible; }
  .gantt .row { grid-template-columns: repeat(16, 1fr); min-width: 0; }
  .gantt .row > b { grid-column: 1 / -1; padding: 10px 0 4px; }
  .gantt .hd span { font-size: 10px; }
  .gantt .hd span:first-child { grid-column: 1 / -1; }
  .gantt .row > i { height: 12px; margin-bottom: 8px; }
  #led-svg { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 -12px; padding: 0 12px; }
  #led-svg svg { min-width: 760px; }
  .ledk b { font-size: 26px; }
  .wrap { padding-bottom: 0; }
}
@media (max-width: 900px) {
  .anat .pic, .sheet { max-width: 440px; }
}
@media (max-width: 900px) and (orientation: landscape) {
  .paint, .play, .anat { grid-template-columns: 1fr 1fr; }
}

/* Два варианта: закрытый зал и мультимедийная стена */
.vtabs { margin-top: 30px; }
.plan .plan-svg svg { width: 100%; height: auto; display: block; border-radius: 16px; background: rgba(2,14,22,.75); border: 1px solid var(--line); }
.wall-show { margin-top: 34px; }
.wall-show .six { margin-top: 0; }
.cmp { margin-top: 46px; border-radius: 16px; overflow: hidden; border: 1px solid var(--line); }
.cmp > div { display: grid; grid-template-columns: 170px 1fr 1fr; gap: 0; background: var(--card); }
.cmp > div + div { border-top: 1px solid var(--line); }
.cmp > div > * { padding: 14px 18px; font-size: 15px; }
.cmp > div b { font-weight: 600; }
.cmp > div span { color: #c3dbea; transition: background .3s, color .3s; }
.cmp .hd { background: var(--card2); }
.cmp .hd span { font-family: var(--h); font-size: 16px; letter-spacing: .06em; text-transform: uppercase; color: var(--ink); }
.cmp > div span:nth-child(2) { border-left: 1px solid var(--line); }
.cmp > div span:nth-child(3) { border-left: 1px solid var(--line); }
.cmp:not([data-on="b"]) > div span:nth-child(2), .cmp[data-on="b"] > div span:nth-child(3) { background: rgba(201,236,58,.07); color: var(--ink); }
.cmp:not([data-on="b"]) .hd span:nth-child(2), .cmp[data-on="b"] .hd span:nth-child(3) { color: var(--lime); }
@media (max-width: 900px) {
  .cmp > div { grid-template-columns: 1fr 1fr; }
  .cmp > div > b { grid-column: 1 / -1; padding-bottom: 0; }
  .cmp .hd b { display: none; }
  .cmp > div span:nth-child(2) { border-left: 0; }
  .cmp > div > * { padding: 10px 12px; font-size: 14px; }
}

/* Световая арка и экран в арке */
.arch-light .run { stroke-dasharray: 2600 1400; animation: archrun 6s linear infinite; }
@keyframes archrun { to { stroke-dashoffset: -16000; } }
#led-svg[data-v="mod"] .arch-light, #led-svg[data-v="cab"] .arch-light { opacity: .3; }
#led-svg[data-v="mod"] .arch-light .run, #led-svg[data-v="cab"] .arch-light .run { animation: none; }
.archnew { margin-top: 22px; }
.archnew .kick { margin-bottom: 12px; }
.archnew .six { margin-top: 0; }
.led-wrap .archnew .six > div { background: #1b2a33; border-color: #1b2a33; }
.led-wrap .archnew .six b { color: #fff; }
.led-wrap .archnew .six p { color: #c3dbea; }
.led-wrap .archnew .kick { color: #4b7a00; }
.led-wrap .archnew .kick em { color: #5a6a73; }
@media (prefers-reduced-motion: reduce) { .arch-light .run { animation: none; } }

/* Параметры экранов: верно / иначе */
.qrow { display: grid; grid-template-columns: 42px 1fr; gap: 12px; padding: 16px 0; border-top: 1px solid var(--line); }
.qrow > i { font-style: normal; font-family: var(--m); font-size: 13px; color: var(--lime); padding-top: 3px; }
.qrow b { font-weight: 600; font-size: 16px; }
.qrow p { font-size: 14px; color: #c3dbea; margin-top: 4px; }
.qrow p span { color: var(--cyan); }
.qa { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.qa button { border: 1px solid var(--line); background: var(--card); border-radius: 20px; padding: 6px 14px; font-size: 13px; font-weight: 600; }
.qa button[data-a="ok"].on { background: var(--lime); color: #0e1d06; border-color: var(--lime); }
.qa button[data-a="no"].on { background: var(--orange); color: #241000; border-color: var(--orange); }
.qa input { flex: 1 1 240px; min-width: 0; padding: 7px 12px; border-radius: 10px; border: 1px solid var(--orange); background: rgba(255,255,255,.05); color: var(--ink); font: inherit; font-size: 14px; }

/* Следующий шаг */
.step { display: grid; grid-template-columns: 54px 1fr; gap: 18px; padding: 28px 0; border-top: 1px solid var(--line); }
.step .sn { width: 44px; height: 44px; border-radius: 50%; background: var(--lime); color: #0e1d06; font-family: var(--h); font-weight: 700; font-size: 22px; display: grid; place-items: center; }
.step h3 { margin-bottom: 14px; }
.step .sm a { color: var(--cyan); }
.ideas { display: grid; gap: 18px; }
.igt { font-family: var(--h); font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--mut); margin-bottom: 8px; }
.ig { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 8px; }
.ig .igt { grid-column: 1 / -1; margin-bottom: 0; }
.idea { display: flex; gap: 12px; align-items: flex-start; padding: 14px 16px; border-radius: 12px; border: 1px solid var(--line); background: var(--card); cursor: pointer; transition: border-color .2s, background .2s; }
.idea input { width: 20px; height: 20px; margin-top: 2px; accent-color: var(--lime); flex: none; }
.idea b { display: block; font-weight: 600; font-size: 15px; }
.idea em { font-style: normal; font-size: 13px; color: var(--mut); }
.idea:has(input:checked) { border-color: var(--lime); background: rgba(201,236,58,.08); }
.calc { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; max-width: 760px; }
.calc input, .calc textarea { font: inherit; font-size: 16px; color: var(--ink); padding: 14px 16px; border-radius: 12px; border: 1px solid var(--line); background: rgba(255,255,255,.05); outline: none; }
.calc input:focus, .calc textarea:focus { border-color: var(--cyan); }
.calc textarea, .calc .sum, .calc button, .calc .cerr { grid-column: 1 / -1; }
.calc .hp { position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0; }
.calc .sum { font-size: 14px; color: var(--mut); }
.calc button { border: 0; border-radius: 12px; padding: 16px; background: var(--lime); color: #0e1d06; font-weight: 700; font-size: 17px; }
.calc button[disabled] { opacity: .5; }
.cerr { color: #ff6b78; font-size: 14px; }
.cok { padding: 22px 24px; border-radius: 14px; background: rgba(201,236,58,.12); border: 1px solid rgba(201,236,58,.4); font-size: 17px; max-width: 760px; }
.cok b { color: var(--lime); }
.inside { margin-top: 26px; border-top: 1px solid var(--line); padding-top: 18px; }
.inside summary { cursor: pointer; font-family: var(--h); font-size: 20px; color: var(--mut); }
.inside dl div { display: grid; grid-template-columns: 170px 1fr; gap: 16px; padding: 12px 0; border-top: 1px solid var(--line); }
.inside dl div:first-child { margin-top: 14px; }
.inside dt { font-family: var(--h); font-size: 18px; font-weight: 600; }
.inside dd { font-size: 15px; color: #c3dbea; }
.inside .no { color: var(--mut); }
@media (max-width: 900px) {
  .qrow { grid-template-columns: 30px 1fr; }
  .step { grid-template-columns: 40px 1fr; gap: 12px; }
  .step .sn { width: 34px; height: 34px; font-size: 18px; }
  .calc { grid-template-columns: 1fr; }
  .inside dl div { grid-template-columns: 1fr; gap: 4px; }
}

/* 16.10: драфт маскота, где заказывать, кейсы ровной сеткой */
.draft { margin-top: 14px; padding: 14px 18px; border-radius: 12px; border: 1px dashed rgba(255,154,46,.6); background: rgba(255,154,46,.08); font-size: 15px; color: #f1dcc4; }
.draft b { color: var(--orange); }
.supply { margin-top: 18px; padding: 18px 20px; border-radius: 14px; background: rgba(63,208,232,.08); border: 1px solid rgba(63,208,232,.3); font-size: 16px; color: #dcebf3; max-width: 900px; }
.supply b { color: var(--cyan); }
.supply a { color: var(--lime); }
.supply-pick .idea input { accent-color: var(--cyan); }
.saved { grid-column: 1 / -1; }
.cerr a { color: var(--lime); }
.cases { grid-template-columns: repeat(3, 1fr); }
.case.big { grid-row: auto; }
.case.big b { font-size: 22px; }
@media (max-width: 900px) {
  .case.big { grid-column: auto; }
  .gantt .hd span { font-size: 9px; }
}

/* PDF для печати */
.pdfrow { display: flex; align-items: center; gap: 16px; margin-top: 18px; flex-wrap: wrap; }
.pdf-btn { display: inline-flex; align-items: center; gap: 8px; text-decoration: none; font-weight: 700; font-size: 15px; padding: 11px 18px; border-radius: 30px; border: 1px solid var(--line); background: rgba(4,20,34,.55); }
.pdf-btn:before { content: '↓'; color: var(--lime); }
.pdf-btn:hover { border-color: var(--lime); }
.pdfrow span { font-size: 13px; color: var(--mut); max-width: 560px; }

</style>
</head>
<body>
<div id="bg"></div><div class="rays"></div><canvas id="sea" aria-hidden="true"></canvas>
<header class="top"><img src="hm-logo.svg" alt="Hand Marketing"><span class="x">× Самарский океанариум</span><nav><a href="#wow">WOW-зона</a><a href="#mascot">Маскот</a><a href="#led">LED-экран</a><a href="#next">Расчёт</a><a href="#contacts">Контакты</a></nav></header>
<div class="gauge" aria-hidden="true"><div class="val"><span id="gv">0</span><small>м</small></div><div class="lbl" id="gl">поверхность</div><div class="tr"><i id="gi"></i><b style="top:0%">0</b><b style="top:25%">30</b><b style="top:50%">1000</b><b style="top:75%">4000</b><b style="top:100%">11 000</b></div></div>
<section class="hero" data-depth="0"><div class="wrap"><div class="kick">Самарский океанариум · мультимедиа <em>материалы на одной странице</em></div><h1>Глубина.<span>Три проекта для океанариума</span></h1><p class="lead">Всё, что мы подготовили для вас, собрано здесь и работает вживую: иммерсивный зал, где за пять минут посетитель опускается на дно Марианской впадины, пингвин с живым лицом и LED-экраны на входе. Проведите мышью или пальцем по экрану: рыбы вас заметят.</p><div class="trio"><a href="#wow"><i>01 · 0 → 11 000 м</i><b>WOW-зона «Глубина»</b><span>Закрытый зал или стена на маршруте, интерактивный пол, модули</span></a><a href="#mascot"><i>02 · 1,9 м</i><b>Пингвин Гумбольдта</b><span>Ростовой маскот с 3D-печати, лицо рисует свет изнутри головы</span></a><a href="#led"><i>03 · ТЗ версия 2</i><b>LED-экраны у входа</b><span>Два экрана по 13,4 кв. м по обе стороны арки, вопросы на подтверждение</span></a></div><div class="pdfrow"><a class="pdf-btn" href="?pdf=1">Скачать PDF</a><span>Версия для печати. Схемы в движении, демо пола, касания маскота и выбор идей для расчёта работают только на этой странице.</span></div><div class="scrollhint">Листайте вниз: глубиномер справа покажет, насколько глубоко вы уже опустились</div></div></section>
<section id="wow" data-depth="10"><div class="wrap"><div class="kick">01 · WOW-зона <em>ваш запрос построчно</em></div><h2 class="rv">Каждое требование и как мы его закрываем</h2><div class="req rv"><div><i>01</i><b>Бесшовная проекция на стены и пол</b><span>7 лазерных проекторов: 5 на три стены, 2 на пол. Сшивка и смешение краёв на медиасервере, швов не видно</span></div><div><i>02</i><b>Интерактивный пол</b><span>Если есть техническая возможность: две камеры глубины над залом, пол отвечает на каждый шаг, светится планктон, расходятся рыбы, поднимаются скаты</span></div><div><i>03</i><b>Датчики движения</b><span>Датчик на входе считает группу и запускает сеанс. Камеры видят, где стоят люди, и стены реагируют на толпу</span></div><div><i>04</i><b>Пространственный звук</b><span>8 точек по периметру и сабвуфер. Голос кита проходит вокруг зрителя, а не звучит из одной колонки</span></div><div><i>05</i><b>Реалистичный 3D-контент</b><span>Собственный продакшн на Unreal Engine: шоу 5 минут, 3 интерактивные сцены, фоновая петля</span></div><div><i>06</i><b>Ежедневный интенсивный поток</b><span>Лазерный источник на 20 000 часов, автозапуск по расписанию, удалённый мониторинг, техника вне зоны доступа рук</span></div><div class="plus"><i>+</i><b>Точка съёмки</b><span>То, о чём вы не спрашивали, но без чего зона не станет поводом для PR: место под вертикальное видео, где в финале сеанса глаз кашалота встаёт ровно за спиной гостя</span></div></div><p class="note">Так закрываем запрос, если есть возможность построить закрытую зону. Дополнительно рассматриваем мультимедийную стену прямо на маршруте: какой вариант подходит, станет понятно после технического визита. <a href="#variants" style="color:var(--cyan)">Сравнение вариантов</a></p></div></section>
<section data-depth="20"><div class="wrap"><div class="kick">Объект <em>план аренды и режим работы</em></div><h2 class="rv">Зона должна быть сильнее акул в тоннеле</h2><div class="nums rv"><div><b class="c-lime">2015 кв. м</b><span>площадь океанариума по приложению 1.2 к договору аренды, цокольный этаж LETOUT</span></div><div><b class="c-cyan">3800 часов</b><span>работы техники в год: 11 часов в день, санитарный день раз в месяц</span></div><div><b class="c-mag">50 метров</b><span>главный аквариум плюс 15-метровый тоннель с акулами</span></div></div><div class="facts2 rv"><p>Вы арендатор в ТЦ. Подвесы, мощность и ночной монтаж согласуем с управляющей компанией, пакет документов готовим мы.</p><p>Воздух влажный и с солью. Технику ставим вне экспозиции с водой, закладываем фильтры и регламент чистки.</p><p>Ресурс считаем по 3800 часам в год, поэтому только лазерные проекторы: ламповые не подходят.</p><p>Точка подвода электричества А далеко от свободной части зала. Нужна отдельная линия до щита зоны, до 8 кВт.</p></div><p class="note">Мы разобрали 22 проекта в океанариумах мира (SeaWorld Abu Dhabi, Atlantis The Palm, Xpark × NAKED, OdySea, Sumida, Singapore Oceanarium) и российский рынок: в Москвариуме иммерсивное шоу продают отдельным билетом от 1750 ₽. Гости остаются в иммерсивных экспозициях в 2-6 раз дольше, чем у статичных. «Глубина» может входить в билет или продаваться отдельно: сеансы по расписанию, датчик на входе считает посетителей.</p></div></section>
<section data-depth="30"><div class="wrap"><div class="kick">Концепция <em>шоу 5 минут, пять глав</em></div><h2 class="rv">11 километров вниз за пять минут</h2><p class="lead rv">Посетитель входит в тёмный зал и начинает погружение. На стене глубиномер, цифры растут. С каждой главой меняются свет, звук и обитатели. Это не мультфильм про море, а путь, который невозможно пройти в реальности: тот же океан, что за стеклом аквариумов, только на глубине, куда человек не спускается.</p><div class="dive" style="margin-top:46px"><div class="sticky"><div class="window" id="dive"><canvas></canvas><div class="meter"><span id="dm">0</span><small>м</small></div><div class="cap" id="dc">Окно в зал: сцена меняется по главам, нажмите на главу</div></div></div><div><ol class="chap" id="chap"><li data-i="0" style="--c:#3fd0e8" class=on><span class="d">0 м</span><span class="n">Поверхность</span><p>Солнечные блики, пингвины Гумбольдта ныряют сквозь зал</p></li><li data-i="1" style="--c:#2fb39a"><span class="d">30 м</span><span class="n">Риф</span><p>Рифовые акулы и скаты проходят вдоль стен, косяк рыб кружит над головой</p></li><li data-i="2" style="--c:#e64bd0"><span class="d">1 000 м</span><span class="n">Сумерки</span><p>Свет гаснет. Мимо проходит кашалот в натуральную величину, его глаз смотрит на вас</p></li><li data-i="3" style="--c:#c9ec3a"><span class="d">4 000 м</span><span class="n">Бездна</span><p>Биолюминесценция: светится всё, что движется, включая следы посетителей</p></li><li data-i="4" style="--c:#ff9a2e"><span class="d">11 000 м</span><span class="n">Дно впадины</span><p>Тишина и темнота. На подъёме кашалот встречает зал снова и замирает у торцевой стены</p></li></ol><div class="link"><b>Связь с коллекцией.</b> Героями глав становятся ваши обитатели: пингвины Гумбольдта, рифовые акулы, скаты. После зала посетитель ищет их за стеклом.</div></div></div></div></section>
<section data-depth="1000"><div class="wrap"><div class="kick">Опыт посетителя <em>зал не простаивает</em></div><h2 class="rv">Два режима и ни минуты простоя</h2><div class="modes rv"><div class="mode"><div class="k">Режим 1 · между сеансами</div><h3>Свободное плавание</h3><ul><li>Стены показывают спокойный океан, петля 10 минут без повторов в кадре</li><li>Пол интерактивный: одна из трёх сцен, сцены меняются по кругу</li><li>Дети бегают, взрослые снимают. Зал живой даже без шоу</li><li>Длительность 1 минута, пока группа входит и выходит</li></ul></div><div class="mode"><div class="k">Режим 2 · сеанс</div><h3>Погружение</h3><ul><li>Запуск автоматически, когда датчик на входе видит группу</li><li>5 минут, пять глав, глубиномер на стене</li><li>Звук 8.1: кашалот проходит вокруг зрителя</li><li>Финал: свет поднимается, на стене кадр для соцсетей</li></ul></div></div><div class="cycle rv"><div><b class="c-lime">25</b><span>человек одновременно, около 2 кв. м на гостя</span></div><div><b class="c-cyan">6 минут</b><span>полный цикл: сеанс и смена группы</span></div><div><b class="c-orange">250</b><span>посетителей в час на пике выходного дня</span></div></div></div></section>
<section data-depth="1500"><div class="wrap"><div class="kick">Интерактив <em>демо прямо на странице</em></div><h2 class="rv">Пол отвечает на каждый шаг</h2><p class="lead rv">Ведите курсором или пальцем по полю ниже: так пол зала видит посетителей. Четыре сцены, переключаются кнопками.</p><p class="sm rv" style="margin-top:8px">Интерактивный пол делаем, если есть техническая возможность: высота потолка, точки подвеса и покрытие пола проверяем на техническом визите.</p><div class="tabs" id="ftabs"><button type="button" data-m="plankton" class=on><i>01</i>Планктон</button><button type="button" data-m="school"><i>02</i>Косяк</button><button type="button" data-m="rays"><i>03</i>Скаты</button><button type="button" data-m="clean"><i>04</i>Чистое дно</button></div><div class="floor" id="floor"><canvas></canvas><div class="hint" id="fhint">Пройдитесь по дну</div><div class="stat" id="fstat"></div></div><div class="floor-desc"><div id="fdesc"><p data-m="plankton">За каждым шагом остаётся светящийся след. В темноте это лучший кадр для сторис: ребёнок рисует ногами по дну океана.</p><p data-m="school" hidden>Тысячи рыб плывут единой стаей и расходятся вокруг ног. Замрёшь на месте, и стая сомкнётся снова.</p><p data-m="rays" hidden>Песчаное дно. От шагов из песка поднимаются скаты и уплывают к стене, где продолжают путь.</p><p data-m="clean" hidden>Четвёртая сцена. По дну несёт пластик: пакеты, бутылки, сетку. Дети наступают на мусор, он исчезает, песок оживает и зарастает травой. Когда дно очищено полностью, приплывают скаты.</p></div><p class="how">Две камеры глубины под потолком видят каждого человека в зале с частотой 30 кадров в секунду. Трекинг работает в полной темноте и не зависит от картинки на полу. Та же система видит, где стоит толпа, и стены отвечают ей: рыбы подплывают туда, где больше людей. Новая сцена к Новому году или ко Дню Волги ставится как файл.</p></div></div></section>
<section id="variants" data-depth="2000"><div class="wrap"><div class="kick">Техническое решение <em>два варианта под ваше помещение</em></div><h2 class="rv">Отдельный зал или стена на маршруте</h2><p class="lead rv">Если закрытую зону построить не получится, тот же океан встаёт на одну мультимедийную стену прямо в экспозиции. Сравните схемы.</p><div class="tabs vtabs" id="vtabs"><button type="button" data-var="a" class="on"><i>А</i>Закрытый зал 8,5 × 6 м</button><button type="button" data-var="b"><i>Б</i>Мультимедийная стена</button></div><div class="var" data-var="a"><div class="plan"><div class="plan-svg"><svg viewBox="-60 -40 970 700" role="img" aria-label="Схема зала 8,5 на 6 метров"><defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="rgba(160,220,255,.12)" stroke-width="2"/></pattern></defs><rect x="0" y="0" width="850" height="600" fill="url(#hatch)" stroke="#cfe6f5" stroke-width="8"/><rect x="-6" y="400" width="12" height="150" fill="#04121e"/><text x="-14" y="470" fill="#8fb3c9" font-size="18" text-anchor="end" font-family="Oswald">ВХОД</text><text x="-14" y="492" fill="#8fb3c9" font-size="18" text-anchor="end" font-family="Oswald">ВЫХОД</text><g class="lyr" data-l="walls"><polygon points="225,30 0,600 425,600" fill="rgba(230,75,208,.13)" stroke="rgba(230,75,208,.55)" stroke-width="2"/><polygon points="630,30 425,600 850,600" fill="rgba(230,75,208,.13)" stroke="rgba(230,75,208,.55)" stroke-width="2"/><polygon points="225,570 0,0 425,0" fill="rgba(230,75,208,.13)" stroke="rgba(230,75,208,.55)" stroke-width="2"/><polygon points="630,570 425,0 850,0" fill="rgba(230,75,208,.13)" stroke="rgba(230,75,208,.55)" stroke-width="2"/><rect x="199" y="555" width="52" height="30" rx="5" fill="#e64bd0"/><text x="225" y="577" fill="#fff" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">П1</text><rect x="604" y="555" width="52" height="30" rx="5" fill="#e64bd0"/><text x="630" y="577" fill="#fff" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">П2</text><rect x="199" y="15" width="52" height="30" rx="5" fill="#e64bd0"/><text x="225" y="37" fill="#fff" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">П3</text><rect x="604" y="15" width="52" height="30" rx="5" fill="#e64bd0"/><text x="630" y="37" fill="#fff" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">П4</text></g><g class="lyr" data-l="end"><polygon points="55,300 850,0 850,600" fill="rgba(201,236,58,.10)" stroke="rgba(201,236,58,.6)" stroke-width="2"/><rect x="29" y="285" width="52" height="30" rx="5" fill="#9cc31d"/><text x="55" y="307" fill="#0e1d06" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">П5</text></g><g class="lyr" data-l="floor"><rect x="0" y="0" width="500" height="600" fill="rgba(47,179,154,.13)"/><rect x="350" y="0" width="500" height="600" fill="rgba(47,179,154,.13)"/><line x1="358" y1="0" x2="358" y2="600" stroke="#3fd0e8" stroke-width="2" stroke-dasharray="10 8"/><line x1="499" y1="0" x2="499" y2="600" stroke="#3fd0e8" stroke-width="2" stroke-dasharray="10 8"/><rect x="227" y="287" width="52" height="30" rx="5" fill="#2fb39a"/><text x="253" y="309" fill="#fff" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">Ф1</text><rect x="575" y="287" width="52" height="30" rx="5" fill="#2fb39a"/><text x="601" y="309" fill="#fff" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">Ф2</text></g><g class="lyr" data-l="sound"><circle cx="0" cy="0" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><circle cx="430" cy="0" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><circle cx="850" cy="0" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><circle cx="0" cy="220" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><circle cx="850" cy="300" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><circle cx="0" cy="600" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><circle cx="430" cy="600" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><circle cx="850" cy="600" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><rect x="748" y="515" width="44" height="30" rx="5" fill="#ff9a2e"/><text x="770" y="536" fill="#000" font-size="14" font-weight="700" text-anchor="middle" font-family="Oswald">SUB</text></g><g class="lyr" data-l="cams"><rect x="268" y="149" width="26" height="26" fill="#c9ec3a" stroke="#04121e" stroke-width="3" transform="rotate(45 281 162)"/><rect x="558" y="429" width="26" height="26" fill="#c9ec3a" stroke="#04121e" stroke-width="3" transform="rotate(45 571 442)"/></g><g class="lyr" data-l="sensor"><rect x="28" y="468" width="22" height="22" fill="#ff4d5e" stroke="#fff" stroke-width="2" transform="rotate(45 39 479)"/></g><g class="lyr" data-l="target"><circle cx="431" cy="302" r="26" fill="none" stroke="#ff4d5e" stroke-width="5"/><circle cx="431" cy="302" r="8" fill="#ff4d5e"/></g><line x1="0" y1="634" x2="850" y2="634" stroke="#5b7d93" stroke-width="2"/><text x="425.0" y="656" fill="#8fb3c9" font-size="20" text-anchor="middle" font-family="IBM Plex Mono">8,5 м</text><line x1="884" y1="0" x2="884" y2="600" stroke="#5b7d93" stroke-width="2"/><text x="902" y="300.0" fill="#8fb3c9" font-size="20" text-anchor="middle" font-family="IBM Plex Mono" transform="rotate(90 902 300.0)">6 м</text></svg></div><div><div class="layers"><button type="button" data-l="walls" style="--c:#e64bd0"><b>П1-П4</b><span>длинные стены, по 2 проектора на стену, свет через зал над головами</span></button><button type="button" data-l="end" style="--c:#c9ec3a"><b>П5</b><span>торцевая стена с точкой съёмки</span></button><button type="button" data-l="floor" style="--c:#2fb39a"><b>Ф1-Ф2</b><span>пол, короткофокусные, светят сверху с перекрытием</span></button><button type="button" data-l="sound" style="--c:#ff9a2e"><b>8 + SUB</b><span>акустика по периметру и сабвуфер</span></button><button type="button" data-l="cams" style="--c:#c9ec3a"><b>2 камеры</b><span>трекинг пола и толпы, ромбы на схеме</span></button><button type="button" data-l="sensor" style="--c:#ff4d5e"><b>Датчик</b><span>у входа, запускает сеанс</span></button><button type="button" data-l="target" style="--c:#ff4d5e"><b>Мишень</b><span>точка съёмки для соцсетей</span></button></div><p class="why"><b>Почему пол на двух проекторах.</b> Один проектор над головой даёт длинные тени от посетителей. Второй светит с другой стороны и заполняет тень, картинка под ногами остаётся целой. Нажмите на строку, чтобы спрятать или показать слой.</p></div></div><p class="note">Расчёт для потолка от 3,8 м. Зал предлагаем ставить в свободной части справа по плану экспозиции: там нет аквариумов, а проектор весит около 10 кг, усиление перекрытий не нужно. Зал встаёт после аквариумов, как финал визита. Две колонны в поле зала обшиваем под скалу или ставим стены по их осям. Раскладку пересчитываем по обмерным планам и 3D-модели помещения.</p></div><div class="var" data-var="b" hidden><div class="plan"><div class="plan-svg"><svg viewBox="-40 -70 1080 760" role="img" aria-label="Схема мультимедийной стены, вид сверху"><defs><pattern id="hatch2" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="rgba(160,220,255,.12)" stroke-width="2"/></pattern><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#8fb3c9"/></marker></defs><rect x="0" y="-26" width="1000" height="26" fill="#cfe6f5" opacity=".5"/><text x="500.0" y="-38" fill="#8fb3c9" font-size="18" text-anchor="middle" font-family="IBM Plex Mono">существующая стена или перегородка</text><rect x="0" y="0" width="1000" height="640" fill="url(#hatch2)"/><rect x="60" y="550" width="220" height="90" rx="6" fill="rgba(63,208,232,.12)" stroke="rgba(63,208,232,.45)" stroke-width="2"/><text x="170" y="602" fill="#3fd0e8" font-size="17" text-anchor="middle" font-family="Oswald">аквариум</text><rect x="390" y="550" width="220" height="90" rx="6" fill="rgba(63,208,232,.12)" stroke="rgba(63,208,232,.45)" stroke-width="2"/><text x="500" y="602" fill="#3fd0e8" font-size="17" text-anchor="middle" font-family="Oswald">аквариум</text><rect x="720" y="550" width="220" height="90" rx="6" fill="rgba(63,208,232,.12)" stroke="rgba(63,208,232,.45)" stroke-width="2"/><text x="830" y="602" fill="#3fd0e8" font-size="17" text-anchor="middle" font-family="Oswald">аквариум</text><g class="lyr" data-l="flow"><path d="M-20,490 C250,520 750,520 1020,490" fill="none" stroke="#8fb3c9" stroke-width="4" stroke-dasharray="14 10" marker-end="url(#arr)"/><text x="500.0" y="482" fill="#8fb3c9" font-size="18" text-anchor="middle" font-family="IBM Plex Mono">маршрут посетителей, проходят мимо без очереди</text></g><g class="lyr" data-l="floor"><rect x="200" y="20" width="350" height="300" fill="rgba(47,179,154,.15)"/><rect x="450" y="20" width="350" height="300" fill="rgba(47,179,154,.15)"/><rect x="200" y="20" width="600" height="300" fill="none" stroke="#2fb39a" stroke-width="3" stroke-dasharray="12 8"/><rect x="304" y="155" width="52" height="30" rx="5" fill="#2fb39a"/><text x="330" y="177" fill="#fff" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">Ф1</text><rect x="644" y="155" width="52" height="30" rx="5" fill="#2fb39a"/><text x="670" y="177" fill="#fff" font-size="18" font-weight="700" text-anchor="middle" font-family="Oswald">Ф2</text><text x="790" y="310" fill="#2fb39a" font-size="17" text-anchor="end" font-family="IBM Plex Mono">пол 6 × 3 м</text></g><g class="lyr" data-l="led"><rect x="100" y="0" width="800" height="22" fill="#e64bd0"/><line x1="150" y1="0" x2="150" y2="22" stroke="#04121e" stroke-width="2"/><line x1="200" y1="0" x2="200" y2="22" stroke="#04121e" stroke-width="2"/><line x1="250" y1="0" x2="250" y2="22" stroke="#04121e" stroke-width="2"/><line x1="300" y1="0" x2="300" y2="22" stroke="#04121e" stroke-width="2"/><line x1="350" y1="0" x2="350" y2="22" stroke="#04121e" stroke-width="2"/><line x1="400" y1="0" x2="400" y2="22" stroke="#04121e" stroke-width="2"/><line x1="450" y1="0" x2="450" y2="22" stroke="#04121e" stroke-width="2"/><line x1="500" y1="0" x2="500" y2="22" stroke="#04121e" stroke-width="2"/><line x1="550" y1="0" x2="550" y2="22" stroke="#04121e" stroke-width="2"/><line x1="600" y1="0" x2="600" y2="22" stroke="#04121e" stroke-width="2"/><line x1="650" y1="0" x2="650" y2="22" stroke="#04121e" stroke-width="2"/><line x1="700" y1="0" x2="700" y2="22" stroke="#04121e" stroke-width="2"/><line x1="750" y1="0" x2="750" y2="22" stroke="#04121e" stroke-width="2"/><line x1="800" y1="0" x2="800" y2="22" stroke="#04121e" stroke-width="2"/><line x1="850" y1="0" x2="850" y2="22" stroke="#04121e" stroke-width="2"/><text x="500" y="52" fill="#e64bd0" font-size="20" font-weight="700" text-anchor="middle" font-family="Oswald">LED-СТЕНА 8 × 3 М</text></g><g class="lyr" data-l="sound"><circle cx="230" cy="250" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><path d="M208,272 Q230,296 252,272" fill="none" stroke="rgba(255,154,46,.6)" stroke-width="2"/><circle cx="410" cy="250" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><path d="M388,272 Q410,296 432,272" fill="none" stroke="rgba(255,154,46,.6)" stroke-width="2"/><circle cx="590" cy="250" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><path d="M568,272 Q590,296 612,272" fill="none" stroke="rgba(255,154,46,.6)" stroke-width="2"/><circle cx="770" cy="250" r="15" fill="#ff9a2e" stroke="#04121e" stroke-width="3"/><path d="M748,272 Q770,296 792,272" fill="none" stroke="rgba(255,154,46,.6)" stroke-width="2"/></g><g class="lyr" data-l="cams"><rect x="117" y="47" width="26" height="26" fill="#c9ec3a" stroke="#04121e" stroke-width="3" transform="rotate(45 130 60)"/><rect x="857" y="47" width="26" height="26" fill="#c9ec3a" stroke="#04121e" stroke-width="3" transform="rotate(45 870 60)"/></g><g class="lyr" data-l="target"><circle cx="500" cy="200" r="26" fill="none" stroke="#ff4d5e" stroke-width="5"/><circle cx="500" cy="200" r="8" fill="#ff4d5e"/></g><line x1="100" y1="670" x2="900" y2="670" stroke="#5b7d93" stroke-width="2"/><text x="500" y="684" fill="#8fb3c9" font-size="18" text-anchor="middle" font-family="IBM Plex Mono" dy="6">8 м стены</text></svg></div><div><div class="layers"><button type="button" data-l="led" style="--c:#e64bd0"><b>LED-стена</b><span>8 × 3 м, шаг 2,5 мм, около 3 200 × 1 200 пикселей. Яркая, работает при свете экспозиции</span></button><button type="button" data-l="floor" style="--c:#2fb39a"><b>Ф1-Ф2</b><span>интерактивный пол 6 × 3 м перед стеной, два короткофокусных проектора с перекрытием</span></button><button type="button" data-l="cams" style="--c:#c9ec3a"><b>2 камеры</b><span>видят людей у стены и на полу: рыбы подплывают к тому, кто подошёл</span></button><button type="button" data-l="sound" style="--c:#ff9a2e"><b>4 точки</b><span>направленный звук над зоной, у соседних аквариумов почти не слышно</span></button><button type="button" data-l="target" style="--c:#ff4d5e"><b>Мишень</b><span>точка съёмки: кашалот встаёт за спиной гостя</span></button><button type="button" data-l="flow" style="--c:#8fb3c9"><b>Поток</b><span>зона на маршруте, без дверей, сеансов и очереди</span></button></div><p class="why"><b>Почему LED, а не проекция.</b> В открытой части свет экспозиции и витрины аквариумов засвечивают проекцию на стене. Светодиодная стена держит яркость и контраст при любом свете, а пол перед ней достаточно чуть приглушить. Нажмите на строку, чтобы спрятать или показать слой.</p></div></div><div class="wall-show"><div class="kick">Как работает стена</div><div class="six"><div style="--c:var(--cyan)"><i>01</i><b>Свободное плавание</b><p>Спокойный океан на стене. Камеры видят, кто подошёл, и рыбы подплывают к нему, косяк расходится перед ладонью.</p></div><div style="--c:var(--mag)"><i>02</i><b>Погружение каждые 10 минут</b><p>Свет над зоной приглушается, на стене глубиномер: за три минуты пять глав от поверхности до дна впадины.</p></div><div style="--c:var(--orange)"><i>03</i><b>Кашалот в рост</b><p>16-метровый кашалот проходит вдоль стены за несколько секунд и останавливает взгляд на гостях у мишени.</p></div></div></div><p class="note">Размеры стены, шаг пикселя и место уточняем по плану и фото места: ориентир от 8 м свободной стены и 3 м пола перед ней. Монтаж стены по тем же правилам, что и в ТЗ на экраны входной группы: своя рама на анкерах, кабели нг(А)-LS, модули меняются спереди.</p></div><div class="cmp rv"><div class="hd"><b></b><span>А · Закрытый зал</span><span>Б · Мультимедийная стена</span></div><div><b>Что строим</b><span>Отдельное помещение 8,5 × 6 м: стены, чёрный потолок, вход и выход</span><span>Ничего. Стена встаёт на свою раму у существующей стены или перегородки</span></div><div><b>Свет вокруг</b><span>Полная темнота, проекция на стены и пол</span><span>Работает при обычном свете экспозиции: LED яркий. Над полом достаточно приглушить свет</span></div><div><b>Погружение</b><span>Со всех сторон: три стены, торец и пол</span><span>Окно в океан: одна стена и пол перед ней</span></div><div><b>Формат</b><span>Сеансы по 5 минут на группу до 25 человек</span><span>Без сеансов. Свободное плавание, каждые 10 минут на стене трёхминутное погружение на дно</span></div><div><b>Пропускная</b><span>До 250 человек в час, вход по группам</span><span>Не ограничена: люди останавливаются и идут дальше</span></div><div><b>Билет</b><span>Можно продавать отдельно</span><span>Входит в общий билет, работает на впечатление от маршрута</span></div><div><b>Согласования</b><span>Стройка с ТЦ и архитектором реновации, подвесы под потолком</span><span>Рама на анкерах и подвес двух проекторов, монтаж ночью</span></div><div><b>Что сохраняется</b><span>Всё из концепции</span><span>Пять глав, кашалот, интерактивный пол, точка съёмки, сезонная смена контента файлом</span></div></div></div></section>
<section data-depth="3000"><div class="wrap"><div class="kick">Оборудование <em>ориентировочный состав</em></div><h2 class="rv">Зал выдерживает поток 350 дней в году</h2><p class="note" style="margin:0 0 18px">Состав оборудования приблизительный, пока без расчёта проектировщика и инженера. Модели и количество уточняем в проекте.</p><div class="eq rv"><div><b>7</b><strong>Лазерные проекторы 6000 лм, WUXGA</strong><span>5 со стандартным объективом на стены, 2 короткофокусных 0,44:1 на пол. Ресурс источника 20 000 часов</span></div><div><b>2</b><strong>Узла медиасервера, 8 выходов</strong><span>Рендер Unreal Engine, сшивка и смешение краёв, синхронизация кадров между узлами</span></div><div><b>2</b><strong>Камеры глубины и датчик входа</strong><span>Трекинг пола и толпы в темноте, счётчик группы для запуска сеанса</span></div><div><b>9</b><strong>Точек звука 8.1</strong><span>8 инсталляционных акустических систем, сабвуфер, многоканальный усилитель, аудиоинтерфейс</span></div><div><b>1</b><strong>Шкаф управления</strong><span>ИБП, сеть, оптические линии HDMI до проекторов, удалённый доступ для мониторинга</span></div></div><div class="six rv"><div style="--c:var(--lime)"><i>01</i><b>Без ламп</b><p>Лазерный источник, ресурс по паспорту производителя около 20 000 часов. Лампы менять не нужно.</p></div><div style="--c:var(--cyan)"><i>02</i><b>Без оператора</b><p>Зал включается и выключается по расписанию. Если узел завис, система перезапускает его сама.</p></div><div style="--c:var(--mag)"><i>03</i><b>Вне зоны рук</b><p>Проекторы и камеры под потолком, сервер в техническом помещении. Посетитель может трогать только стены и пол.</p></div><div style="--c:var(--orange)"><i>04</i><b>Защита от соли</b><p>Пылевые фильтры на проекторах, шкаф с климатом, регламент чистки оптики раз в месяц.</p></div><div style="--c:var(--teal)"><i>05</i><b>Пол не изнашивается</b><p>Картинка на полу это свет, а не экран. Покрытие класса 43 моется каждый день.</p></div><div style="--c:var(--red)"><i>06</i><b>Мы на связи</b><p>Удалённый мониторинг. Условия гарантии и сервиса фиксируем в договоре.</p></div></div></div></section>
<section data-depth="4000"><div class="wrap"><div class="kick">Модули <em>берутся сразу или во вторую очередь</em></div><div class="paint rv"><div><div class="kick">Нарисуй рыбу и отпусти её в океан</div><h2>Раскрасьте свою рыбу</h2><p class="lead">В зале это стол на 6 мест и сканер: ребёнок раскрашивает бланк, кладёт под сканер, и через пять секунд его рыба плывёт по стене в общем косяке. Здесь то же самое: выберите цвет, нажмите на части рыбы и отпустите её на страницу.</p><div class="steps"><div><i>01</i><b>Раскрась</b>Бланки печатаем мы</div><div><i>02</i><b>Отсканируй</b>Одна кнопка, без приложения</div><div><i>03</i><b>Отпусти</b>Рыба плывёт до конца дня</div><div><i>04</i><b>Забери</b>Рисунок в фирменной рамке</div></div><p class="sm" style="color:#5a6a73;margin-top:16px">Место 4 кв. м рядом с залом, розетка и точка сети. Пять видов рыб, анимация плавания и стаи. Приём проверен teamLab.</p></div><div class="sheet"><div class="t"><span>Бланк · Самарский океанариум</span><span>№ 001</span></div><svg viewBox="-62 -42 124 84" aria-label="Контур рыбы для раскраски">
<path data-part="tail" d="M-27,0 L-54,-22 C-47,-8 -47,8 -54,22 Z" fill="#fff"/>
<path data-part="fin" d="M-8,-19 C0,-38 18,-36 24,-17 Z" fill="#fff"/>
<path data-part="fin" d="M-6,17 C0,30 12,30 17,16 Z" fill="#fff"/>
<path data-part="body" d="M-32,0 C-22,-24 22,-28 44,-4 C48,0 48,2 44,6 C22,28 -22,24 -32,0 Z" fill="#fff"/>
<path data-part="stripe" d="M2,-23 C12,-10 12,10 2,23 L-8,21 C1,9 1,-9 -8,-21 Z" fill="#fff"/>
<circle cx="31" cy="-5" r="5.5" fill="#fff" stroke="#1c2b33" stroke-width="3"/><circle cx="32.5" cy="-5" r="2.4" fill="#1c2b33"/>
</svg><div class="pal" id="pal"><button type="button" style="background:#ff9a2e" data-c="#ff9a2e" aria-label="Цвет #ff9a2e" class=on></button><button type="button" style="background:#e64bd0" data-c="#e64bd0" aria-label="Цвет #e64bd0"></button><button type="button" style="background:#3fd0e8" data-c="#3fd0e8" aria-label="Цвет #3fd0e8"></button><button type="button" style="background:#c9ec3a" data-c="#c9ec3a" aria-label="Цвет #c9ec3a"></button><button type="button" style="background:#ff4d5e" data-c="#ff4d5e" aria-label="Цвет #ff4d5e"></button><button type="button" style="background:#2f6fe0" data-c="#2f6fe0" aria-label="Цвет #2f6fe0"></button><button type="button" style="background:#ffd23f" data-c="#ffd23f" aria-label="Цвет #ffd23f"></button><button type="button" style="background:#2fb39a" data-c="#2fb39a" aria-label="Цвет #2fb39a"></button><button type="button" style="background:#7a3cff" data-c="#7a3cff" aria-label="Цвет #7a3cff"></button><button type="button" style="background:#ffffff" data-c="#ffffff" aria-label="Цвет #ffffff"></button></div><button type="button" class="release" id="release">Отпустить в океан</button><div class="released" id="released"></div></div></div><div class="mods"><div class="mod rv" style="--c:var(--cyan)"><div class="k">две удочки у стены с проекцией</div><h3>Рыбалка «Поймай и отпусти»</h3><p>Гость забрасывает по-настоящему, снасть отзывается натяжением, а на стене идёт своя рыба. Сом с Волги тянет иначе, чем рифовая. Поймал, узнал вид по карточке, отпустил: на стене счётчик отпущенных рыб за день.</p><div class="flow"><span>Заброс</span><span>Поклёвка</span><span>Вываживание</span><span>Отпускание</span></div><div class="term">Стена 3 м и 6 кв. м перед ней</div></div><div class="mod rv" style="--c:var(--mag)"><div class="k">фотозона у выхода из зала</div><h3>Кадр с кашалотом</h3><p>Вертикальный экран работает как зеркало: гость видит себя в реальном времени, кашалот подплывает из глубины и замирает за спиной. Снимок уходит на почту с готовым текстом и хэштегами.</p><div class="flow"><span>Экран</span><span>Камера</span><span>Кадр 9:16</span><span>База контактов</span></div><div class="term">Экран, камера, компьютер и стойка</div></div><div class="mod rv" style="--c:var(--orange)"><div class="k">стойка-челлендж рядом с залом</div><h3>Задержи дыхание</h3><p>Гость жмёт кнопку и задерживает дыхание. На экране рядом ныряет кашалот, который держится до 90 минут. Результат сравнивается с ним и с рекордом дня, таблицу рекордов фотографируют.</p><div class="flow"><span>Кнопка</span><span>Нырок кашалота</span><span>Рекорд дня</span></div><div class="term">Экран, кнопка, графика и звук</div></div><div class="mod rv" style="--c:var(--teal)"><div class="k">четвёртая сцена интерактивного пола</div><h3>Чистое дно</h3><p>Природоохранная тема без лекции и таблички: мусор исчезает под ногами, дно зарастает травой, приплывают скаты. Попробуйте в демо пола выше.</p><div class="flow"><span>Те же камеры</span><span>Нового железа нет</span></div><div class="term">Работает на уже установленных камерах</div></div></div><p class="note">Модули можно взять сразу или во вторую очередь, считаются отдельно от зала.</p></div></section>
<section id="mascot" data-depth="5000"><div class="wrap"><div class="kick">02 · Маскот <em>модуль для зала</em></div><div class="masc-hero rv"><img src="img/p-hug.jpg" alt="Ростовой пингвин с детьми у аквариума" loading=lazy decoding=async><div class="in"><h2>Пингвин, которого хочется обнять</h2><p class="lead">Ваш пингвин Гумбольдта из вольера, только его можно трогать. Ростовая фигура с 3D-печати, лицо у неё не нарисовано, а проецируется изнутри головы: маскот моргает, говорит, следит взглядом и меняет настроение.</p></div></div><p class="draft rv"><b>Драфт.</b> Предложение по маскоту будет скорректировано после разработки проекта: размеры, оснащение и сценарии уточним вместе с вами.</p><div class="mnum rv"><div><b class="c-lime">1,9 м</b><span>рост, как у взрослого</span></div><div><b class="c-cyan">0,1 с</b><span>от касания до реакции лица</span></div><div><b class="c-mag">9</b><span>состояний: от сна до праздника</span></div><div><b class="c-orange">0</b><span>движущихся частей, ломать нечего</span></div></div><div class="play"><div><div class="kick">Живое лицо</div><h2 class="rv" style="font-size:clamp(34px,4vw,54px)">Потрогайте его</h2><p class="lead">Нажмите на ласту, клюв или живот. Под скорлупой 6-8 ёмкостных зон, и у каждой своя реакция. Двойное касание клюва включает фотопозу.</p><div class="pg" id="pg" style="margin-top:22px;max-width:420px"><img src="img/p-stand.jpg" alt="Маскот-пингвин в полный рост" loading=lazy decoding=async><button type="button" class="hs" data-h="flip" style="left:29%;top:55%" aria-label="Потрогать: ласта"><span>ласта</span></button><button type="button" class="hs" data-h="beak" style="left:67%;top:17%" aria-label="Потрогать: клюв"><span>клюв</span></button><button type="button" class="hs" data-h="belly" style="left:55%;top:60%" aria-label="Потрогать: живот"><span>живот</span></button></div></div><div><div class="face" id="face"><img src="img/f-laugh.jpg" alt="Лицо маскота: Смеётся" data-f="laugh" class=on loading="lazy"><img src="img/f-wow.jpg" alt="Лицо маскота: Удивляется" data-f="wow" loading="lazy"><img src="img/f-sleep.jpg" alt="Лицо маскота: Засыпает" data-f="sleep" loading="lazy"><img src="img/f-wink.jpg" alt="Лицо маскота: Подмигивает" data-f="wink" loading="lazy"><div class="say"><b id="fs">Смеётся</b><span id="ft">Тронули ласту или живот</span></div></div><div class="fbtn" id="fbtn"><button type="button" data-f="wow">Подойти ближе</button><button type="button" data-f="wink">Фото</button><button type="button" data-f="sleep">Вечер</button></div></div></div><div class="anat"><div class="pic" id="anat"><img src="img/p-inside.jpg" alt="Маскот в разрезе" loading=lazy decoding=async><span class="pt" data-p="0" style="left:52%;top:15%;--c:var(--lime)">1</span><span class="pt" data-p="1" style="left:43%;top:11%;--c:var(--cyan)">2</span><span class="pt" data-p="2" style="left:41%;top:37%;--c:var(--mag)">3</span><span class="pt" data-p="3" style="left:57%;top:26%;--c:var(--orange)">4</span><span class="pt" data-p="4" style="left:58%;top:64%;--c:var(--lime)">5</span><span class="pt" data-p="5" style="left:41%;top:52%;--c:var(--cyan)">6</span><span class="pt" data-p="6" style="left:40%;top:68%;--c:var(--mag)">7</span><span class="pt" data-p="7" style="left:45%;top:92%;--c:var(--orange)">8</span></div><div><div class="kick">Как устроен</div><h2 class="rv" style="font-size:clamp(34px,4vw,54px)">Что внутри</h2><ol class="parts" id="parts"><li data-p="0" style="--c:var(--lime)"><i>1</i><div><b>Лицевая маска</b><span>Светорассеивающий пластик 3 мм, светится изнутри. Меняется за 10 минут</span></div></li><li data-p="1" style="--c:var(--cyan)"><i>2</i><div><b>Зеркало</b><span>Разворачивает луч проектора в голову. Настраивается один раз</span></div></li><li data-p="2" style="--c:var(--mag)"><i>3</i><div><b>Лазерный проектор</b><span>Обратная проекция: ребёнок обнимает, а тени на лице нет</span></div></li><li data-p="3" style="--c:var(--orange)"><i>4</i><div><b>Радар 24 ГГц</b><span>Видит до трёх человек и где они стоят. Камеры нет</span></div></li><li data-p="4" style="--c:var(--lime)"><i>5</i><div><b>Сенсорные зоны</b><span>6-8 зон под скорлупой: ласты, живот, клюв</span></div></li><li data-p="5" style="--c:var(--cyan)"><i>6</i><div><b>Компьютер</b><span>Сценарии, мимика и голос. Работает и без сети</span></div></li><li data-p="6" style="--c:var(--mag)"><i>7</i><div><b>Динамики</b><span>Два по 40 Вт, громкость ограничена программно</span></div></li><li data-p="7" style="--c:var(--orange)"><i>8</i><div><b>Основание</b><span>Анкеры в пол и считыватель карточек</span></div></li></ol><p class="sm" style="margin-top:14px">Проекция лица на скульптуру работает в аттракционах Disney с 1969 года, в исследованиях приём называют shader lamps. Мы собираем это на лазерных источниках и своих сценариях.</p></div></div><div class="day"><div class="kick">Сценарии <em>переключается сам</em></div><h2 class="rv" style="font-size:clamp(34px,4vw,54px)">Один день пингвина</h2><div class="stage" id="day"><img src="img/d-1.jpg" alt="Утро" data-d="0" class=on loading="lazy"><img src="img/d-2.jpg" alt="Первые гости" data-d="1" loading="lazy"><img src="img/d-3.jpg" alt="День" data-d="2" loading="lazy"><img src="img/d-4.jpg" alt="Фотозона" data-d="3" loading="lazy"><img src="img/d-5.jpg" alt="Закрытие" data-d="4" loading="lazy"><div class="tm" id="dtm">10:00</div><div class="ds" id="dds" style="--c:var(--mag)"><b>Утро</b><span>Открывает глаза, зевает, оглядывает зал. Звук пока молчит</span></div></div><div class="slider"><input type="range" min="0" max="4" step="1" value="0" id="drange" aria-label="Время дня"><div class="ticks"><span>10:00</span><span>11:30</span><span>14:00</span><span>17:00</span><span>21:50</span></div></div><div class="states"><div style="--c:var(--cyan)"><b>Покой</b><em>бесконечно</em><p>Рядом никого ближе 4 м. Дышит, моргает, иногда зевает, разглядывает зал</p></div><div style="--c:var(--lime)"><b>Приветствие</b><em>4-6 с</em><p>Гость вошёл в зону 2,5 м. Поворачивает взгляд, здоровается фразой из пула на 12 вариантов</p></div><div style="--c:var(--teal)"><b>Внимание</b><em>пока рядом</em><p>Следит взглядом за ближайшим, живая мимика, реплика раз в 30-40 секунд</p></div><div style="--c:var(--orange)"><b>Касание</b><em>3-5 с</em><p>Ласта смешит, клюв удивляет, живот заставляет икать</p></div><div style="--c:var(--mag)"><b>Квест</b><em>20-40 с</em><p>Приложили карточку или билет: здоровается с героем карточки, даёт задание по маршруту</p></div><div style="--c:var(--lime)"><b>Фотопоза</b><em>5 с</em><p>Двойное касание клюва: замирает, подмигивает, на маске обратный отсчёт</p></div><div style="--c:var(--red)"><b>Праздник</b><em>весь день</em><p>Новый год, День Волги, дни рождения: другое лицо, голос и фразы</p></div><div style="--c:var(--cyan)"><b>Тихий режим</b><em>по расписанию</em><p>Звук выключен, мимика мягче. Для гостей, которым громко и ярко тяжело</p></div><div style="--c:var(--orange)"><b>Сон</b><em>до открытия</em><p>Прощается, закрывает глаза. Утром поднимается сам</p></div></div><p class="note">Персонал нужен, только чтобы включить тихий режим или праздничную программу. Радар отдаёт только координаты, камеры в фигуре нет: детей никто не снимает. Весь контент лежит внутри, без сети маскот работает так же.</p></div><div class="opts"><div class="opt" style="--c:var(--lime)"><img src="img/opt-mask.jpg" alt="Вариант: проектор на всю маску" loading=lazy decoding=async><div class="in"><h3>Проектор на всю маску</h3><ul><li>Мимика на всё лицо: брови, щёки, румянец</li><li>Маска повторяет форму головы, лицо часть скульптуры</li><li>Маска стоит копейки и меняется за 10 минут</li><li>Внутри 150-250 Вт тепла, нужна тихая вентиляция</li></ul><div class="best">Лучше для затемнённого зала</div></div></div><div class="opt" style="--c:var(--orange)"><img src="img/opt-eyes.jpg" alt="Вариант: экраны в глазах" loading=lazy decoding=async><div class="in"><h3>Экраны в глазах</h3><ul><li>Два круглых дисплея 4-5 дюймов под линзами</li><li>Лицо скульптурное и расписанное, светятся только глаза</li><li>Почти не греется, 40-80 Вт, оптику настраивать не нужно</li><li>Мимика скромнее: только глаза и брови</li></ul><div class="best">Лучше для светлого входа</div></div></div></div><div style="margin-top:90px"><div class="kick">Производство <em>3D-ферма партнёра</em></div><h2 class="rv" style="font-size:clamp(34px,4vw,54px)">От эскиза до зала</h2><div class="make"><div><img src="img/mk-1.jpg" alt="Эскиз" loading=lazy decoding=async><p><i>01</i><b>Эскиз</b>Рисуем героя под ваш океанариум и согласуем мимику</p></div><div><img src="img/mk-2.jpg" alt="3D-модель" loading=lazy decoding=async><p><i>02</i><b>3D-модель</b>Лепим цифровую скульптуру и режем на детали для печати</p></div><div><img src="img/mk-3.jpg" alt="Печать" loading=lazy decoding=async><p><i>03</i><b>Печать</b>45-60 деталей на 3D-ферме партнёра, PETG или ABS</p></div><div><img src="img/mk-4.jpg" alt="Сборка" loading=lazy decoding=async><p><i>04</i><b>Сборка</b>Стальной каркас, шпатлёвка, автогрунт, эмаль, лак</p></div><div><img src="img/mk-5.jpg" alt="Зал" loading=lazy decoding=async><p><i>05</i><b>Зал</b>Монтаж, настройка проекции и сценариев на месте</p></div></div></div><div class="duo"><div class="ph"><img src="img/p-farm.jpg" alt="3D-ферма партнёра" loading=lazy decoding=async><div><b>Деталь печатается заново</b><span>Повреждённый фрагмент печатается и меняется на месте. Высота 1,9 м (от 1,6 до 2,2), 45-60 деталей, масса 60-80 кг, стальной каркас 40 × 40 мм</span></div></div><div class="ph"><img src="img/p-ny.jpg" alt="Маскот в новогоднем образе" loading=lazy decoding=async><div><b>На праздник другое лицо</b><span>Новый год, День Волги, день рождения океанариума: свой голос, мимика и фразы. Меняется файлом, без выезда бригады</span></div></div></div><div class="heroes"><img src="img/p-heroes.jpg" alt="Варианты героя: пингвин, детёныш кашалота, скат" loading=lazy decoding=async><ul><li><b>Пингвин</b><span>Ваш пингвин Гумбольдта. Самый узнаваемый житель, любимец детей</span></li><li><b>Детёныш кашалота</b><span>Если хотите связать маскота с новым залом «Глубина»</span></li><li><b>Скат</b><span>Плавный, спокойный, хорошо смотрится на входе</span></li><li><b>Свой персонаж</b><span>Нарисуем героя с нуля под айдентику океанариума</span></li><li style="background:rgba(201,236,58,.1);border-color:rgba(201,236,58,.35)"><b style="color:var(--ink)">Что нужно от вас</b><span>Место от 4 кв. м, розетка 220 В, точка сети и приглушённый свет рядом с фигурой</span></li></ul></div></div></section>
<section id="led" data-depth="7000"><div class="wrap"><div class="kick">03 · LED-экраны входной группы <em>проект ТЗ, параметры ориентировочные</em></div><h2 class="rv">Три экрана и световая арка в одной композиции</h2><p class="lead rv">Два экрана по обе стороны арки, третий экран внутри арки над входом и световой контур по самой арке. Всё работает от одного видеопроцессора как одна картинка: рыба уплывает с левого экрана и появляется на правом, в арке косяк собирается в кольцо, а по контуру арки в такт бежит свет.</p><div class="led-wrap rv" style="margin-top:34px"><div class="led-bar"><div class="tabs" id="ledtabs"><button type="button" data-v="content" class="on">Контент</button><button type="button" data-v="mod">Модули 250 × 250</button><button type="button" data-v="cab">Кабинеты 500 × 500</button></div><span class="sm">Размеры в мм, контур арки условный до чертежа</span></div><div id="led-svg" data-v="content"><svg viewBox="-300 -200 16120 9600" role="img" aria-label="Фасад входной группы с двумя LED-экранами"><defs><linearGradient id="ledsea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d6fa3"/><stop offset=".6" stop-color="#063a5e"/><stop offset="1" stop-color="#021626"/></linearGradient><clipPath id="ledclip"><rect x="0" y="8050" width="3500" height="250"/><rect x="12020" y="8050" width="3500" height="250"/><rect x="0" y="7800" width="3500" height="250"/><rect x="12020" y="7800" width="3500" height="250"/><rect x="0" y="7550" width="3500" height="250"/><rect x="12020" y="7550" width="3500" height="250"/><rect x="0" y="7300" width="3500" height="250"/><rect x="12020" y="7300" width="3500" height="250"/><rect x="0" y="7050" width="3750" height="250"/><rect x="11770" y="7050" width="3750" height="250"/><rect x="0" y="6800" width="3750" height="250"/><rect x="11770" y="6800" width="3750" height="250"/><rect x="0" y="6550" width="3750" height="250"/><rect x="11770" y="6550" width="3750" height="250"/><rect x="0" y="6300" width="3750" height="250"/><rect x="11770" y="6300" width="3750" height="250"/><rect x="0" y="6050" width="4000" height="250"/><rect x="11520" y="6050" width="4000" height="250"/><rect x="0" y="5800" width="4000" height="250"/><rect x="11520" y="5800" width="4000" height="250"/><rect x="0" y="5550" width="4000" height="250"/><rect x="11520" y="5550" width="4000" height="250"/><rect x="0" y="5300" width="4250" height="250"/><rect x="11270" y="5300" width="4250" height="250"/><rect x="0" y="5050" width="4250" height="250"/><rect x="11270" y="5050" width="4250" height="250"/><rect x="0" y="4800" width="4250" height="250"/><rect x="11270" y="4800" width="4250" height="250"/><rect x="5010" y="5300" width="5500" height="250"/><rect x="5010" y="5050" width="5500" height="250"/><rect x="5260" y="4800" width="5000" height="250"/><rect x="5260" y="4550" width="5000" height="250"/><rect x="5260" y="4300" width="5000" height="250"/><rect x="5510" y="4050" width="4500" height="250"/><rect x="5510" y="3800" width="4500" height="250"/><rect x="5760" y="3550" width="4000" height="250"/><rect x="6010" y="3300" width="3500" height="250"/><rect x="6010" y="3050" width="3500" height="250"/><rect x="6260" y="2800" width="3000" height="250"/></clipPath><linearGradient id="archlight" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3fd0e8"/><stop offset=".5" stop-color="#c9ec3a"/><stop offset="1" stop-color="#e64bd0"/></linearGradient><filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="90"/></filter></defs><rect x="-300" y="-200" width="16120" height="8500" fill="#f4f6f7"/><line x1="-300" y1="8300" x2="15820" y2="8300" stroke="#1b2a33" stroke-width="40"/><polygon points="3760,8300 3760,8200 3761,8100 3762,8000 3764,7900 3767,7800 3770,7700 3774,7600 3780,7500 3786,7400 3793,7300 3801,7200 3810,7100 3820,7000 3831,6900 3844,6800 3857,6700 3872,6600 3888,6500 3904,6400 3923,6300 3942,6200 3963,6100 3985,6000 4008,5900 4032,5800 4058,5700 4085,5600 4114,5500 4144,5400 4175,5300 4208,5200 4242,5100 4277,5000 4314,4900 4353,4800 4392,4700 4434,4600 4477,4500 4521,4400 4567,4300 4614,4200 4663,4100 4713,4000 4765,3900 4819,3800 4874,3700 4931,3600 4989,3500 5049,3400 5111,3300 5174,3200 5239,3100 5305,3000 5373,2900 5443,2800 5515,2700 5588,2600 5663,2500 5740,2400 5818,2300 5898,2200 5980,2100 6064,2000 6149,1900 6236,1800 6325,1700 6416,1600 6508,1500 6602,1400 6698,1300 6796,1200 6896,1100 6997,1000 7101,900 7206,800 7313,700 7422,600 7533,500 7645,400 7760,300 7760,300 7875,400 7987,500 8098,600 8207,700 8314,800 8419,900 8523,1000 8624,1100 8724,1200 8822,1300 8918,1400 9012,1500 9104,1600 9195,1700 9284,1800 9371,1900 9456,2000 9540,2100 9622,2200 9702,2300 9780,2400 9857,2500 9932,2600 10005,2700 10077,2800 10147,2900 10215,3000 10281,3100 10346,3200 10409,3300 10471,3400 10531,3500 10589,3600 10646,3700 10701,3800 10755,3900 10807,4000 10857,4100 10906,4200 10953,4300 10999,4400 11043,4500 11086,4600 11128,4700 11167,4800 11206,4900 11243,5000 11278,5100 11312,5200 11345,5300 11376,5400 11406,5500 11435,5600 11462,5700 11488,5800 11512,5900 11535,6000 11557,6100 11578,6200 11597,6300 11616,6400 11632,6500 11648,6600 11663,6700 11676,6800 11689,6900 11700,7000 11710,7100 11719,7200 11727,7300 11734,7400 11740,7500 11746,7600 11750,7700 11753,7800 11756,7900 11758,8000 11759,8100 11760,8200 11760,8300" fill="#e8b46a" opacity=".55"/><polygon points="4260,8300 4260,8200 4261,8100 4262,8000 4264,7900 4267,7800 4270,7700 4275,7600 4280,7500 4286,7400 4293,7300 4302,7200 4311,7100 4321,7000 4332,6900 4345,6800 4359,6700 4374,6600 4390,6500 4407,6400 4425,6300 4445,6200 4466,6100 4488,6000 4512,5900 4537,5800 4563,5700 4590,5600 4619,5500 4650,5400 4682,5300 4715,5200 4749,5100 4785,5000 4823,4900 4862,4800 4902,4700 4944,4600 4988,4500 5033,4400 5079,4300 5127,4200 5177,4100 5228,4000 5281,3900 5335,3800 5391,3700 5449,3600 5508,3500 5569,3400 5632,3300 5696,3200 5762,3100 5829,3000 5899,2900 5970,2800 6042,2700 6117,2600 6193,2500 6271,2400 6350,2300 6432,2200 6515,2100 6600,2000 6686,1900 6775,1800 6865,1700 6957,1600 7051,1500 7147,1400 7244,1300 7344,1200 7445,1100 7548,1000 7653,900 7760,800 7760,800 7867,900 7972,1000 8075,1100 8176,1200 8276,1300 8373,1400 8469,1500 8563,1600 8655,1700 8745,1800 8834,1900 8920,2000 9005,2100 9088,2200 9170,2300 9249,2400 9327,2500 9403,2600 9478,2700 9550,2800 9621,2900 9691,3000 9758,3100 9824,3200 9888,3300 9951,3400 10012,3500 10071,3600 10129,3700 10185,3800 10239,3900 10292,4000 10343,4100 10393,4200 10441,4300 10487,4400 10532,4500 10576,4600 10618,4700 10658,4800 10697,4900 10735,5000 10771,5100 10805,5200 10838,5300 10870,5400 10901,5500 10930,5600 10957,5700 10983,5800 11008,5900 11032,6000 11054,6100 11075,6200 11095,6300 11113,6400 11130,6500 11146,6600 11161,6700 11175,6800 11188,6900 11199,7000 11209,7100 11218,7200 11227,7300 11234,7400 11240,7500 11245,7600 11250,7700 11253,7800 11256,7900 11258,8000 11259,8100 11260,8200 11260,8300" fill="#fbfcfc" stroke="#1b2a33" stroke-width="30"/><g class="arch-light"><path d="M3760,8300 L3760,8200 L3761,8100 L3762,8000 L3764,7900 L3767,7800 L3770,7700 L3774,7600 L3780,7500 L3786,7400 L3793,7300 L3801,7200 L3810,7100 L3820,7000 L3831,6900 L3844,6800 L3857,6700 L3872,6600 L3888,6500 L3904,6400 L3923,6300 L3942,6200 L3963,6100 L3985,6000 L4008,5900 L4032,5800 L4058,5700 L4085,5600 L4114,5500 L4144,5400 L4175,5300 L4208,5200 L4242,5100 L4277,5000 L4314,4900 L4353,4800 L4392,4700 L4434,4600 L4477,4500 L4521,4400 L4567,4300 L4614,4200 L4663,4100 L4713,4000 L4765,3900 L4819,3800 L4874,3700 L4931,3600 L4989,3500 L5049,3400 L5111,3300 L5174,3200 L5239,3100 L5305,3000 L5373,2900 L5443,2800 L5515,2700 L5588,2600 L5663,2500 L5740,2400 L5818,2300 L5898,2200 L5980,2100 L6064,2000 L6149,1900 L6236,1800 L6325,1700 L6416,1600 L6508,1500 L6602,1400 L6698,1300 L6796,1200 L6896,1100 L6997,1000 L7101,900 L7206,800 L7313,700 L7422,600 L7533,500 L7645,400 L7760,300 L7760,300 L7875,400 L7987,500 L8098,600 L8207,700 L8314,800 L8419,900 L8523,1000 L8624,1100 L8724,1200 L8822,1300 L8918,1400 L9012,1500 L9104,1600 L9195,1700 L9284,1800 L9371,1900 L9456,2000 L9540,2100 L9622,2200 L9702,2300 L9780,2400 L9857,2500 L9932,2600 L10005,2700 L10077,2800 L10147,2900 L10215,3000 L10281,3100 L10346,3200 L10409,3300 L10471,3400 L10531,3500 L10589,3600 L10646,3700 L10701,3800 L10755,3900 L10807,4000 L10857,4100 L10906,4200 L10953,4300 L10999,4400 L11043,4500 L11086,4600 L11128,4700 L11167,4800 L11206,4900 L11243,5000 L11278,5100 L11312,5200 L11345,5300 L11376,5400 L11406,5500 L11435,5600 L11462,5700 L11488,5800 L11512,5900 L11535,6000 L11557,6100 L11578,6200 L11597,6300 L11616,6400 L11632,6500 L11648,6600 L11663,6700 L11676,6800 L11689,6900 L11700,7000 L11710,7100 L11719,7200 L11727,7300 L11734,7400 L11740,7500 L11746,7600 L11750,7700 L11753,7800 L11756,7900 L11758,8000 L11759,8100 L11760,8200 L11760,8300" fill="none" stroke="url(#archlight)" stroke-width="140" filter="url(#glow)" opacity=".7"/><path class="run" d="M3760,8300 L3760,8200 L3761,8100 L3762,8000 L3764,7900 L3767,7800 L3770,7700 L3774,7600 L3780,7500 L3786,7400 L3793,7300 L3801,7200 L3810,7100 L3820,7000 L3831,6900 L3844,6800 L3857,6700 L3872,6600 L3888,6500 L3904,6400 L3923,6300 L3942,6200 L3963,6100 L3985,6000 L4008,5900 L4032,5800 L4058,5700 L4085,5600 L4114,5500 L4144,5400 L4175,5300 L4208,5200 L4242,5100 L4277,5000 L4314,4900 L4353,4800 L4392,4700 L4434,4600 L4477,4500 L4521,4400 L4567,4300 L4614,4200 L4663,4100 L4713,4000 L4765,3900 L4819,3800 L4874,3700 L4931,3600 L4989,3500 L5049,3400 L5111,3300 L5174,3200 L5239,3100 L5305,3000 L5373,2900 L5443,2800 L5515,2700 L5588,2600 L5663,2500 L5740,2400 L5818,2300 L5898,2200 L5980,2100 L6064,2000 L6149,1900 L6236,1800 L6325,1700 L6416,1600 L6508,1500 L6602,1400 L6698,1300 L6796,1200 L6896,1100 L6997,1000 L7101,900 L7206,800 L7313,700 L7422,600 L7533,500 L7645,400 L7760,300 L7760,300 L7875,400 L7987,500 L8098,600 L8207,700 L8314,800 L8419,900 L8523,1000 L8624,1100 L8724,1200 L8822,1300 L8918,1400 L9012,1500 L9104,1600 L9195,1700 L9284,1800 L9371,1900 L9456,2000 L9540,2100 L9622,2200 L9702,2300 L9780,2400 L9857,2500 L9932,2600 L10005,2700 L10077,2800 L10147,2900 L10215,3000 L10281,3100 L10346,3200 L10409,3300 L10471,3400 L10531,3500 L10589,3600 L10646,3700 L10701,3800 L10755,3900 L10807,4000 L10857,4100 L10906,4200 L10953,4300 L10999,4400 L11043,4500 L11086,4600 L11128,4700 L11167,4800 L11206,4900 L11243,5000 L11278,5100 L11312,5200 L11345,5300 L11376,5400 L11406,5500 L11435,5600 L11462,5700 L11488,5800 L11512,5900 L11535,6000 L11557,6100 L11578,6200 L11597,6300 L11616,6400 L11632,6500 L11648,6600 L11663,6700 L11676,6800 L11689,6900 L11700,7000 L11710,7100 L11719,7200 L11727,7300 L11734,7400 L11740,7500 L11746,7600 L11750,7700 L11753,7800 L11756,7900 L11758,8000 L11759,8100 L11760,8200 L11760,8300" fill="none" stroke="url(#archlight)" stroke-width="60" stroke-linecap="round"/><path d="M4260,8300 L4260,8200 L4261,8100 L4262,8000 L4264,7900 L4267,7800 L4270,7700 L4275,7600 L4280,7500 L4286,7400 L4293,7300 L4302,7200 L4311,7100 L4321,7000 L4332,6900 L4345,6800 L4359,6700 L4374,6600 L4390,6500 L4407,6400 L4425,6300 L4445,6200 L4466,6100 L4488,6000 L4512,5900 L4537,5800 L4563,5700 L4590,5600 L4619,5500 L4650,5400 L4682,5300 L4715,5200 L4749,5100 L4785,5000 L4823,4900 L4862,4800 L4902,4700 L4944,4600 L4988,4500 L5033,4400 L5079,4300 L5127,4200 L5177,4100 L5228,4000 L5281,3900 L5335,3800 L5391,3700 L5449,3600 L5508,3500 L5569,3400 L5632,3300 L5696,3200 L5762,3100 L5829,3000 L5899,2900 L5970,2800 L6042,2700 L6117,2600 L6193,2500 L6271,2400 L6350,2300 L6432,2200 L6515,2100 L6600,2000 L6686,1900 L6775,1800 L6865,1700 L6957,1600 L7051,1500 L7147,1400 L7244,1300 L7344,1200 L7445,1100 L7548,1000 L7653,900 L7760,800 L7760,800 L7867,900 L7972,1000 L8075,1100 L8176,1200 L8276,1300 L8373,1400 L8469,1500 L8563,1600 L8655,1700 L8745,1800 L8834,1900 L8920,2000 L9005,2100 L9088,2200 L9170,2300 L9249,2400 L9327,2500 L9403,2600 L9478,2700 L9550,2800 L9621,2900 L9691,3000 L9758,3100 L9824,3200 L9888,3300 L9951,3400 L10012,3500 L10071,3600 L10129,3700 L10185,3800 L10239,3900 L10292,4000 L10343,4100 L10393,4200 L10441,4300 L10487,4400 L10532,4500 L10576,4600 L10618,4700 L10658,4800 L10697,4900 L10735,5000 L10771,5100 L10805,5200 L10838,5300 L10870,5400 L10901,5500 L10930,5600 L10957,5700 L10983,5800 L11008,5900 L11032,6000 L11054,6100 L11075,6200 L11095,6300 L11113,6400 L11130,6500 L11146,6600 L11161,6700 L11175,6800 L11188,6900 L11199,7000 L11209,7100 L11218,7200 L11227,7300 L11234,7400 L11240,7500 L11245,7600 L11250,7700 L11253,7800 L11256,7900 L11258,8000 L11259,8100 L11260,8200 L11260,8300" fill="none" stroke="url(#archlight)" stroke-width="140" filter="url(#glow)" opacity=".7"/><path class="run" d="M4260,8300 L4260,8200 L4261,8100 L4262,8000 L4264,7900 L4267,7800 L4270,7700 L4275,7600 L4280,7500 L4286,7400 L4293,7300 L4302,7200 L4311,7100 L4321,7000 L4332,6900 L4345,6800 L4359,6700 L4374,6600 L4390,6500 L4407,6400 L4425,6300 L4445,6200 L4466,6100 L4488,6000 L4512,5900 L4537,5800 L4563,5700 L4590,5600 L4619,5500 L4650,5400 L4682,5300 L4715,5200 L4749,5100 L4785,5000 L4823,4900 L4862,4800 L4902,4700 L4944,4600 L4988,4500 L5033,4400 L5079,4300 L5127,4200 L5177,4100 L5228,4000 L5281,3900 L5335,3800 L5391,3700 L5449,3600 L5508,3500 L5569,3400 L5632,3300 L5696,3200 L5762,3100 L5829,3000 L5899,2900 L5970,2800 L6042,2700 L6117,2600 L6193,2500 L6271,2400 L6350,2300 L6432,2200 L6515,2100 L6600,2000 L6686,1900 L6775,1800 L6865,1700 L6957,1600 L7051,1500 L7147,1400 L7244,1300 L7344,1200 L7445,1100 L7548,1000 L7653,900 L7760,800 L7760,800 L7867,900 L7972,1000 L8075,1100 L8176,1200 L8276,1300 L8373,1400 L8469,1500 L8563,1600 L8655,1700 L8745,1800 L8834,1900 L8920,2000 L9005,2100 L9088,2200 L9170,2300 L9249,2400 L9327,2500 L9403,2600 L9478,2700 L9550,2800 L9621,2900 L9691,3000 L9758,3100 L9824,3200 L9888,3300 L9951,3400 L10012,3500 L10071,3600 L10129,3700 L10185,3800 L10239,3900 L10292,4000 L10343,4100 L10393,4200 L10441,4300 L10487,4400 L10532,4500 L10576,4600 L10618,4700 L10658,4800 L10697,4900 L10735,5000 L10771,5100 L10805,5200 L10838,5300 L10870,5400 L10901,5500 L10930,5600 L10957,5700 L10983,5800 L11008,5900 L11032,6000 L11054,6100 L11075,6200 L11095,6300 L11113,6400 L11130,6500 L11146,6600 L11161,6700 L11175,6800 L11188,6900 L11199,7000 L11209,7100 L11218,7200 L11227,7300 L11234,7400 L11240,7500 L11245,7600 L11250,7700 L11253,7800 L11256,7900 L11258,8000 L11259,8100 L11260,8200 L11260,8300" fill="none" stroke="url(#archlight)" stroke-width="60" stroke-linecap="round"/></g><rect x="5160" y="5900" width="1600" height="2400" fill="#fff" stroke="#1b2a33" stroke-width="30"/><text x="5960" y="7000" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="300" fill="#1b2a33">ВХОД</text><text x="5960" y="7300" text-anchor="middle" font-family="IBM Plex Mono" font-size="170" fill="#7a8a93">1600×2400</text><rect x="8760" y="5900" width="1600" height="2400" fill="#fff" stroke="#1b2a33" stroke-width="30"/><text x="9560" y="7000" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="300" fill="#1b2a33">ВЫХОД</text><text x="9560" y="7300" text-anchor="middle" font-family="IBM Plex Mono" font-size="170" fill="#7a8a93">1600×2400</text><g clip-path="url(#ledclip)" class="ledc"><rect x="0" y="2800" width="15520" height="5500" fill="url(#ledsea)"/><g class="led-rays"><polygon points="0,4800 500,4800 -600,8300 -1200,8300" fill="#bfe9ff" opacity=".07"/><polygon points="1700,4800 2200,4800 1100,8300 500,8300" fill="#bfe9ff" opacity=".07"/><polygon points="3400,4800 3900,4800 2800,8300 2200,8300" fill="#bfe9ff" opacity=".07"/><polygon points="5100,4800 5600,4800 4500,8300 3900,8300" fill="#bfe9ff" opacity=".07"/><polygon points="6800,4800 7300,4800 6200,8300 5600,8300" fill="#bfe9ff" opacity=".07"/><polygon points="8500,4800 9000,4800 7900,8300 7300,8300" fill="#bfe9ff" opacity=".07"/><polygon points="10200,4800 10700,4800 9600,8300 9000,8300" fill="#bfe9ff" opacity=".07"/><polygon points="11900,4800 12400,4800 11300,8300 10700,8300" fill="#bfe9ff" opacity=".07"/><polygon points="13600,4800 14100,4800 13000,8300 12400,8300" fill="#bfe9ff" opacity=".07"/><polygon points="15300,4800 15800,4800 14700,8300 14100,8300" fill="#bfe9ff" opacity=".07"/></g><g id="ledfish"></g><g id="ledring" transform="translate(7760 4200)"></g></g><g class="led-mod"><rect x="8" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15278" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="8058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="8" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15278" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="7808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="8" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15278" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="7558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="8" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15278" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="7308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="8" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="7058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="7058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="7058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="6808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="6808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="6808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="6558" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="6558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="6558" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="6308" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="6308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="6308" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="6058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="3758" y="6058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="6058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="6058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11528" y="6058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="5808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="3758" y="5808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="5808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="5808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11528" y="5808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="5558" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="3758" y="5558" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="5558" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="5558" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11528" y="5558" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="5308" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="3758" y="5308" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="4008" y="5308" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="5308" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="5308" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11528" y="5308" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11278" y="5308" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="5058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="3758" y="5058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="4008" y="5058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="5058" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="5058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11528" y="5058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11278" y="5058" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="8" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="258" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="508" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="758" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1008" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1258" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1508" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="1758" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2008" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2258" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2508" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="2758" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3008" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3258" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="3508" y="4808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="3758" y="4808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="4008" y="4808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="15278" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="15028" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14778" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14528" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14278" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="14028" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13778" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13528" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13278" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="13028" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12778" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12528" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12278" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="12028" y="4808" width="234" height="234" fill="rgba(63,208,232,.28)" stroke="#2a9fc0" stroke-width="10"/><rect x="11778" y="4808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11528" y="4808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="11278" y="4808" width="234" height="234" fill="rgba(255,154,46,.30)" stroke="#e07a10" stroke-width="10"/><rect x="5018" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5268" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5518" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5768" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9518" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9768" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="10018" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="10268" y="5308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5018" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5268" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5518" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5768" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9518" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9768" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="10018" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="10268" y="5058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5268" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5518" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5768" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9518" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9768" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="10018" y="4808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5268" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5518" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5768" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9518" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9768" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="10018" y="4558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5268" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5518" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5768" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9518" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9768" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="10018" y="4308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5518" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5768" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9518" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9768" y="4058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5518" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5768" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9518" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9768" y="3808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="5768" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9518" y="3558" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="3308" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6018" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9268" y="3058" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6268" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6518" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="6768" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7018" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7268" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7518" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="7768" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8018" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8268" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8518" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="8768" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/><rect x="9018" y="2808" width="234" height="234" fill="rgba(230,75,208,.28)" stroke="#b0309c" stroke-width="10"/></g><g class="led-cab"><rect x="0" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="15020" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="500" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14520" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1000" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14020" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1500" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13520" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2000" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13020" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2500" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12520" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="3000" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12020" y="7800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="0" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="15020" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="500" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14520" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1000" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14020" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1500" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13520" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2000" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13020" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2500" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12520" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="3000" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12020" y="7300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="0" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="15020" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="500" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14520" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1000" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14020" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1500" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13520" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2000" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13020" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2500" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12520" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="3000" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12020" y="6800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="0" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="15020" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="500" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14520" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1000" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14020" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1500" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13520" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2000" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13020" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2500" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12520" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="3000" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12020" y="6300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="0" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="15020" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="500" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14520" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1000" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14020" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1500" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13520" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2000" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13020" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2500" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12520" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="3000" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12020" y="5800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="0" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="15020" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="500" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14520" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1000" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14020" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1500" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13520" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2000" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13020" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2500" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12520" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="3000" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12020" y="5300" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="0" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="15020" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="500" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14520" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1000" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="14020" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="1500" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13520" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2000" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="13020" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="2500" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12520" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="3000" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/><rect x="12020" y="4800" width="500" height="500" fill="none" stroke="#1b2a33" stroke-width="22"/></g><text x="1750" y="4600" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="300" fill="#1b2a33">ЭКРАН Л</text><text x="1750" y="4270" text-anchor="middle" font-family="IBM Plex Mono" font-size="190" fill="#4a5a63">13,4 кв. м · 215 модулей</text><text x="13770" y="4600" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="300" fill="#1b2a33">ЭКРАН П</text><text x="13770" y="4270" text-anchor="middle" font-family="IBM Plex Mono" font-size="190" fill="#4a5a63">13,4 кв. м · 215 модулей</text><text x="7760" y="2300" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="240" fill="#1b2a33">ЭКРАН В АРКЕ</text><text x="7760" y="2510" text-anchor="middle" font-family="IBM Plex Mono" font-size="150" fill="#4a5a63">12,25 кв. м · 196 модулей</text><line x1="0" y1="8560" x2="3500" y2="8560" stroke="#4a5a63" stroke-width="16"/><line x1="0" y1="8470" x2="0" y2="8650" stroke="#4a5a63" stroke-width="16"/><line x1="3500" y1="8470" x2="3500" y2="8650" stroke="#4a5a63" stroke-width="16"/><text x="1750.0" y="8810" text-anchor="middle" font-family="IBM Plex Mono" font-size="190" fill="#1b2a33">3500</text><line x1="12020" y1="8560" x2="15520" y2="8560" stroke="#4a5a63" stroke-width="16"/><line x1="12020" y1="8470" x2="12020" y2="8650" stroke="#4a5a63" stroke-width="16"/><line x1="15520" y1="8470" x2="15520" y2="8650" stroke="#4a5a63" stroke-width="16"/><text x="13770.0" y="8810" text-anchor="middle" font-family="IBM Plex Mono" font-size="190" fill="#1b2a33">3500</text><line x1="3760" y1="8560" x2="11760" y2="8560" stroke="#4a5a63" stroke-width="16"/><line x1="3760" y1="8470" x2="3760" y2="8650" stroke="#4a5a63" stroke-width="16"/><line x1="11760" y1="8470" x2="11760" y2="8650" stroke="#4a5a63" stroke-width="16"/><text x="7760.0" y="8810" text-anchor="middle" font-family="IBM Plex Mono" font-size="190" fill="#1b2a33">8000 арка</text><line x1="0" y1="8940" x2="15520" y2="8940" stroke="#4a5a63" stroke-width="16"/><line x1="0" y1="8850" x2="0" y2="9030" stroke="#4a5a63" stroke-width="16"/><line x1="15520" y1="8850" x2="15520" y2="9030" stroke="#4a5a63" stroke-width="16"/><text x="7760.0" y="9190" text-anchor="middle" font-family="IBM Plex Mono" font-size="190" fill="#1b2a33">15 520 между стенами</text><text x="7760" y="240" text-anchor="middle" font-family="IBM Plex Mono" font-size="170" fill="#4a5a63">h 8000 / 7500</text></svg></div><div class="led-legend"><span style="--c:#3fd0e8">прямоугольная часть 3 500 × 3 500</span><span style="--c:#ff9a2e">ступенчатый край под аркой, 19 модулей</span><span style="--c:#e64bd0">экран в арке, ступени по внутреннему контуру</span><span style="--c:#c9ec3a">световая арка: адресный контур по двум кромкам</span><span style="--c:#e8b46a">декоративное обрамление 300 мм</span></div></div><div class="archnew"><div class="kick">Добавлено 15.10 <em>к ТЗ версии 2, по фото входной группы</em></div><div class="six"><div style="--c:var(--lime)"><i>10</i><b>Световая арка</b><p>Адресная пиксельная лента в рассеивающем профиле по наружной и внутренней кромке арки, около 36 м и 2 100 управляемых точек. Свет ведёт тот же медиасервер через пиксельный контроллер, поэтому контур живёт вместе с контентом: волна бежит по арке, когда рыба переплывает с экрана на экран. Яркость и тихий режим по расписанию.</p></div><div style="--c:var(--mag)"><i>11</i><b>Экран в арке</b><p>Над входом, по внутреннему контуру ступенями: ориентир 196 модулей 250 × 250, около 12,25 кв. м, от 2,75 до 5,5 м по высоте. Та же технология, что у боковых экранов, один процессор и общая калибровка, иначе на стыке будет видна разница цвета. В спокойном режиме косяк складывается в кольцо, как в вашем знаке.</p></div><div style="--c:var(--cyan)"><i>12</i><b>Что меняется в ТЗ</b><p>Общий холст растёт по высоте под экран в арке, поставщик выдаёт единую карту пикселей трёх экранов. В расчёт мощности и однолинейную схему добавляются экран в арке и контроллеры света. Крепление экрана к арке считаем по чертежу арки.</p></div></div></div><div class="ledk"><div style="--c:var(--lime)"><b>P2.0</b><span>шаг пикселя, защита COB на всю площадь или в нижней зоне</span></div><div style="--c:var(--cyan)"><b>26,88 кв. м</b><span>активная площадь, 2 × 215 модулей</span></div><div style="--c:var(--mag)"><b>от 3 840 Гц</b><span>желательно, чтобы было меньше полос при съёмке на телефон</span></div><div style="--c:var(--orange)"><b>3 экрана</b><span>боковые и в арке, один процессор и общая калибровка</span></div></div><div class="spec"><div><b>Шаг пикселя</b><span>2,0 мм, минимальная дистанция просмотра 2 м</span></div><div><b>Технология</b><span>COB (Chip on Board): светодиоды посажены прямо на плату и залиты сплошным защитным слоем, поверхность ровная и держит касания. Ставим на всю площадь или только в нижней зоне, куда достают руки и тележки. Для сравнения цены считаем GOB: обычные модули под защитным клеевым слоем</span></div><div><b>Защита</b><span>Касания, удары детской тележкой, влажная уборка нейтральными средствами</span></div><div><b>Ремонт</b><span>Модули меняются спереди, запас из той же партии с калибровочными данными</span></div><div><b>Яркость</b><span>800-1 000 кд/кв. м после калибровки, регулировка 5-100%, датчик освещённости</span></div><div><b>Частота обновления</b><span>Желательно от 3 840 Гц: чем выше, тем меньше полос, когда экран снимают на телефон</span></div><div><b>Обработка</b><span>Не ниже 14 бит, 16 бит предпочтительно, scan не хуже 1/32</span></div><div><b>Контраст и цвет</b><span>От 10 000:1, 6 500 K с регулировкой 3 200-9 300 K, равномерность от 97%</span></div><div><b>Углы обзора</b><span>Не менее 160° по горизонтали и вертикали</span></div><div><b>Битые пиксели</b><span>Не более 1 на 10 000, без соседних и без погасших рядов</span></div><div><b>Ресурс</b><span>До 50% яркости не менее 100 000 часов, 0…+40 °C, влажность 10-80%</span></div><div><b>Шум</b><span>Не выше 35 дБА на 1 м, предпочтительно без вентиляторов</span></div></div><div class="six" style="margin-top:40px"><div style="--c:var(--cyan)"><i>04</i><b>Конструкция</b><p>Своя стальная рама на анкерах в пол, перегородка из ГКЛ нагрузку не несёт. Металл заземлён, острых элементов в зоне посетителей нет, кабели нг(А)-LS.</p></div><div style="--c:var(--lime)"><i>05</i><b>Питание</b><p>380/220 В, 3 фазы, блоки питания распределены по фазам. Ориентир до расчёта: пик до 16 кВт, в среднем около 5,4 кВт. После отключения сети экран включается сам.</p></div><div style="--c:var(--orange)"><i>03</i><b>Синхронность</b><p>Один видеопроцессор ведёт оба экрана кадр в кадр. Если откажет один экран или приёмная карта, второй продолжает работать.</p></div><div style="--c:var(--teal)"><i>07</i><b>Документы</b><p>До производства: спецификация, раскладка по точному контуру арки, карта пикселей и маска, расчёт рамы и анкеров, однолинейная схема.</p></div><div style="--c:var(--red)"><i>08</i><b>Сервис</b><p>Модули меняются спереди, запасные модули из той же партии. Условия гарантии и сервиса фиксируем в договоре.</p></div></div><div class="qs" id="ledq"><div class="kick">09 · Параметры для просчёта, Оренбург <em>15 пунктов, 13-15 добавлены к арке</em></div><p class="sm" style="margin-bottom:14px">Отметьте «Верно» или впишите свой вариант. Ответы уйдут вместе с выбором идей в блоке «Расчёт» ниже.</p><div class="qrow" data-q="01"><i>01</i><div><b>Чистовая отметка пола и низа экрана, пороги, плинтусы?</b><p><span>Наше предложение:</span> Низ экрана на чистовом полу ±0,000, без плинтуса</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 1" hidden></div></div></div><div class="qrow" data-q="02"><i>02</i><div><b>Контур арки: есть DWG/DXF или лист «Вид-1»?</b><p><span>Наше предложение:</span> Нет. До получения чертежа контур принят условно, в производство не запускаем</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 2" hidden></div></div></div><div class="qrow" data-q="03"><i>03</i><div><b>Экран заходит под арку по изгибу (шире кверху), как на схеме?</b><p><span>Наше предложение:</span> Да, по изгибу. Альтернатива: прямоугольник 3 500 × 3 500 мм у арки</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 3" hidden></div></div></div><div class="qrow" data-q="04"><i>04</i><div><b>Справа по эскизу 3 450 мм. Возможно ли 3 500?</b><p><span>Наше предложение:</span> Уточняем по чертежу. Если нельзя, обе стороны по 3 250 мм с новой схемой</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 4" hidden></div></div></div><div class="qrow" data-q="05"><i>05</i><div><b>Декоративное обрамление арки: кто проектирует, делает и отвечает за пожарные свойства?</b><p><span>Наше предложение:</span> Мы проектируем и изготавливаем, материал класса КМ1 или НГ, цвет согласуем</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 5" hidden></div></div></div><div class="qrow" data-q="06"><i>06</i><div><b>Разрешит ли ТЦ анкеровку рамы в пол? Кто в УК отвечает за согласование?</b><p><span>Наше предложение:</span> Разрешит после расчёта и схемы анкеров. Нужен контакт в УК</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 6" hidden></div></div></div><div class="qrow" data-q="07"><i>07</i><div><b>Где электрощит, какая мощность выделена, есть ли 380/220 В, 5 проводов?</b><p><span>Наше предложение:</span> Выделено до 16 кВт от щита в радиусе 20 м. Уточняется</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 7" hidden></div></div></div><div class="qrow" data-q="08"><i>08</i><div><b>Шаг 2 мм и защита COB: на всю площадь или только в нижней зоне, куда достают руки и тележки?</b><p><span>Наше предложение:</span> Считаем оба варианта. Граница двух технологий на одном экране может быть заметна, проверим на образцах</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 8" hidden></div></div></div><div class="qrow" data-q="09"><i>09</i><div><b>График работы, ночной режим, тихие часы?</b><p><span>Наше предложение:</span> Ежедневно 10:00-22:00, вечером яркость снижается по расписанию</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 9" hidden></div></div></div><div class="qrow" data-q="10"><i>10</i><div><b>Кто делает контент, адаптирует ролики, управляет расписанием, хранит исходники?</b><p><span>Наше предложение:</span> Контент и адаптацию делаем мы отдельным заказом. Расписание ведёт ваш персонал после обучения</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 10" hidden></div></div></div><div class="qrow" data-q="11"><i>11</i><div><b>Адрес и данные объекта для пропусков и документов?</b><p><span>Наше предложение:</span> Сверим с договором</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 11" hidden></div></div></div><div class="qrow" data-q="12"><i>12</i><div><b>Что обозначают голубые зоны на плане? Одна пересекает зону слева от арки</b><p><span>Наше предложение:</span> Нужна расшифровка: инженерные сети или ограничения монтажа</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 12" hidden></div></div></div><div class="qrow" data-q="13"><i>13</i><div><b>Экран в арке: знак на стене за ним сохраняем или он становится частью контента?</b><p><span>Наше предложение:</span> Знак становится частью контента: кольцо из рыб на экране. Стену за экраном не трогаем</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 13" hidden></div></div></div><div class="qrow" data-q="14"><i>14</i><div><b>Из чего сделана арка, можно ли сделать паз под световой профиль по кромкам?</b><p><span>Наше предложение:</span> Уточняем по чертежу и фото. Если паз нельзя, ставим накладной профиль в цвет арки</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 14" hidden></div></div></div><div class="qrow" data-q="15"><i>15</i><div><b>Свет арки синхронно с экранами или отдельно по расписанию?</b><p><span>Наше предложение:</span> Синхронно, от одного медиасервера. Отдельный ночной сценарий тоже есть</p><div class="qa"><button type="button" data-a="ok">Верно</button><button type="button" data-a="no">Иначе</button><input type="text" maxlength="140" placeholder="Ваш вариант" aria-label="Ваш вариант к пункту 15" hidden></div></div></div></div><div class="next"><h3>Что ещё нужно для просчёта экранов</h3><ul><li>Лист «Вид-1» и чертёж арки в DWG или DXF</li><li>Контакт ответственного в управляющей компании ТЦ</li><li>Место электрощита и выделенная мощность</li><li>2-3 фото места установки</li></ul></div></div></section>
<section data-depth="9000"><div class="wrap"><div class="kick">Сроки WOW-зоны <em>ориентир, уточняется в расчёте</em></div><h2 class="rv">Около 80 рабочих дней от договора до запуска</h2><div class="gantt" id="gantt"><div class="row hd"><span>Неделя</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span><span>16</span></div><div class="row"><b>Обмерные планы, 3D-модель, концепция</b><i style="--c:#9b2a8f;grid-column:span 2"></i><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div><div class="row"><b>Документация, согласования с ТЦ</b><span></span><i style="--c:#93508a;grid-column:span 4"></i><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div><div class="row"><b>Закупка и поставка оборудования</b><span></span><span></span><i style="--c:#5e9a2e;grid-column:span 9"></i><span></span><span></span><span></span><span></span><span></span></div><div class="row"><b>Раскадровка и аниматик шоу</b><span></span><span></span><i style="--c:#e06a12;grid-column:span 4"></i><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div><div class="row"><b>Производство 3D-контента и звука</b><span></span><span></span><span></span><span></span><span></span><i style="--c:#f2a20a;grid-column:span 7"></i><span></span><span></span><span></span><span></span></div><div class="row"><b>Программирование интерактива</b><span></span><span></span><span></span><span></span><span></span><span></span><span></span><i style="--c:#2f7d7a;grid-column:span 5"></i><span></span><span></span><span></span><span></span></div><div class="row you"><b>Подготовка помещения (ваша сторона)</b><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><i style="--c:#8d8f8c;grid-column:span 4"></i><span></span><span></span><span></span><span></span></div><div class="row"><b>Монтаж, сшивка, калибровка</b><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><i style="--c:#e01a2c;grid-column:span 3"></i><span></span></div><div class="row"><b>Пусконаладка, обучение, запуск</b><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><i style="--c:#a51fb0;grid-column:span 1"></i></div></div><p class="note">Срок ориентировочный и уточняется в расчёте. Монтаж планируем в ночные окна по регламенту ТЦ. Маскот и модули можно делать параллельно с залом.</p><div class="supply"><b>Где заказывать оборудование и экраны?</b> Производство в Китае обычно дешевле, но поставка дольше. В России быстрее, но дороже. Какой вариант считать: в России, в Китае или оба? Отметьте в блоке <a href="#next">«Расчёт»</a>.</div><p class="note" style="display:none"></p></div></section>
<section data-depth="10000"><div class="wrap"><div class="kick">Опыт <em>проекция, маппинг, датчики, ежедневный поток</em></div><h2 class="rv">Мы уже делали это для Самары</h2><div class="cases"><a class="case big rv" href="https://hand-marketing.ru/portfolio/samara-stand-vdnh" target="_blank" rel="noopener"><img src="img/x-samara.jpg" alt="Стенд Самарской области на выставке «Россия»" loading=lazy decoding=async><div><span class=k>Самара</span><b>Стенд Самарской области на выставке «Россия»</b><span>204 кв. м, 18 млн посетителей, 8 месяцев ежедневной работы. Экран-парус с naked eye 3D и интерактивные панели. Тот же регион, тот же поток людей каждый день</span></div></a><a class="case big rv" href="https://hand-marketing.ru/portfolio/samara-exhibition" target="_blank" rel="noopener"><img src="img/x-alabin.jpg" alt="Выставка «Самара» в Музее Алабина" loading=lazy decoding=async><div><span class=k>Самара</span><b>Выставка «Самара» в Музее Алабина</b><span>Изогнутый экран-парус с 3D-контентом, интерактивы на Kinect, кинетический экран, VR и виртуальный маскот «Ладушка»</span></div></a><a class="case rv" href="https://hand-marketing.ru/3d/stavropol" target="_blank" rel="noopener"><img src="img/x-stavropol.jpg" alt="3D mapping шоу в Ставрополе" loading=lazy decoding=async><div><b>3D mapping шоу в Ставрополе</b><span>Восемь минут на здании краевого парламента, работали в плотном тумане</span></div></a><a class="case rv" href="https://hand-marketing.ru/event/samsung" target="_blank" rel="noopener"><img src="img/x-samsung.jpg" alt="Новый год Samsung" loading=lazy decoding=async><div><b>Новый год Samsung</b><span>Проекция с датчиком: гость опускает открытку, меняется заставка</span></div></a><a class="case rv" href="https://hand-marketing.ru/event/changan" target="_blank" rel="noopener"><img src="img/x-changan.jpg" alt="Презентация Changan CS35" loading=lazy decoding=async><div><b>Презентация Changan CS35</b><span>3D mapping на автомобиль тремя проекторами</span></div></a><a class="case rv" href="https://hand-marketing.ru/event/riviera" target="_blank" rel="noopener"><img src="img/x-riviera.jpg" alt="Презентация ТРЦ «Ривьера»" loading=lazy decoding=async><div><b>Презентация ТРЦ «Ривьера»</b><span>Три экрана в единой композиции и ролик «Четыре стихии»</span></div></a></div></div></section>
<section id="next" data-depth="10500"><div class="wrap"><div class="kick">Следующий шаг <em>расчёт по вашему выбору</em></div><h2 class="rv">Выберите, что считаем</h2><p class="lead rv">Отметьте идеи, которые хотите видеть в смете, и подтвердите параметры экранов для Оренбурга. Посчитаем только выбранное и вернёмся с постатейным расчётом.</p><div class="step"><div class="sn">1</div><div><h3>Идеи для расчёта</h3><div class="ideas"><div class="ig" data-g="wow"><div class="igt">WOW-зона</div><label class="idea"><input type="checkbox" value="wow-a" data-label="Вариант А: закрытый зал 8,5 × 6 м"><span><b>Вариант А: закрытый зал 8,5 × 6 м</b><em>проекция на стены и пол, звук 8.1, сеансы по 5 минут</em></span></label><label class="idea"><input type="checkbox" value="wow-b" data-label="Вариант Б: мультимедийная стена"><span><b>Вариант Б: мультимедийная стена</b><em>LED 8 × 3 м и интерактивный пол прямо на маршруте</em></span></label></div><div class="ig" data-g="mod"><div class="igt">Модули</div><label class="idea"><input type="checkbox" value="m-fish" data-label="Нарисуй рыбу"><span><b>Нарисуй рыбу</b><em>стол, сканер, рыба плывёт по стене</em></span></label><label class="idea"><input type="checkbox" value="m-fishing" data-label="Рыбалка «Поймай и отпусти»"><span><b>Рыбалка «Поймай и отпусти»</b><em>две удочки у стены с проекцией</em></span></label><label class="idea"><input type="checkbox" value="m-whale" data-label="Кадр с кашалотом"><span><b>Кадр с кашалотом</b><em>фотозона-зеркало у выхода</em></span></label><label class="idea"><input type="checkbox" value="m-breath" data-label="Задержи дыхание"><span><b>Задержи дыхание</b><em>стойка-челлендж с рекордом дня</em></span></label><label class="idea"><input type="checkbox" value="m-clean" data-label="Чистое дно"><span><b>Чистое дно</b><em>четвёртая сцена интерактивного пола</em></span></label></div><div class="ig" data-g="mascot"><div class="igt">Маскот</div><label class="idea"><input type="checkbox" value="p-mask" data-label="Пингвин: проекция на всю маску"><span><b>Пингвин: проекция на всю маску</b><em>мимика на всё лицо, лучше для тёмной зоны</em></span></label><label class="idea"><input type="checkbox" value="p-eyes" data-label="Пингвин: экраны в глазах"><span><b>Пингвин: экраны в глазах</b><em>лучше для светлого входа</em></span></label><label class="idea"><input type="checkbox" value="p-other" data-label="Другой герой"><span><b>Другой герой</b><em>детёныш кашалота, скат или свой персонаж</em></span></label></div><div class="ig" data-g="led"><div class="igt">Входная группа, Оренбург</div><label class="idea"><input type="checkbox" value="led-side" data-label="Экраны Л и П"><span><b>Экраны Л и П</b><em>2 × 13,4 кв. м, шаг 2 мм</em></span></label><label class="idea"><input type="checkbox" value="led-arch" data-label="Экран в арке"><span><b>Экран в арке</b><em>около 12,25 кв. м над входом</em></span></label><label class="idea"><input type="checkbox" value="led-light" data-label="Световая арка"><span><b>Световая арка</b><em>адресный контур по двум кромкам</em></span></label><label class="idea"><input type="checkbox" value="led-content" data-label="Контент для экранов"><span><b>Контент для экранов</b><em>ролики под общий холст и сезонные версии</em></span></label></div></div></div></div><div class="step"><div class="sn">2</div><div><h3>Где заказывать оборудование и экраны</h3><div class="ig supply-pick"><label class="idea"><input type="radio" name="supply" value="Россия" data-label="В России"><span><b>В России</b><em>быстрее, но дороже</em></span></label><label class="idea"><input type="radio" name="supply" value="Китай" data-label="В Китае"><span><b>В Китае</b><em>дешевле, но поставка дольше</em></span></label><label class="idea"><input type="radio" name="supply" value="оба варианта" data-label="Оба варианта" checked><span><b>Оба варианта</b><em>посчитаем и сравним</em></span></label></div></div></div><div class="step"><div class="sn">3</div><div><h3>Параметры экранов в Оренбурге</h3><p class="sm">Подтверждено <b id="qcount">0</b> из 15. Без ответа считаем по нашему предложению. <a href="#ledq">Перейти к вопросам</a></p><p class="sm" style="margin-top:6px">Для точного расчёта пришлите на почту: лист «Вид-1» и чертёж арки в DWG или DXF, место электрощита и выделенную мощность, 2-3 фото места установки.</p></div></div><div class="step"><div class="sn">4</div><div><h3>Отправить на расчёт</h3><form class="calc" id="calc" novalidate><input type="text" name="name" placeholder="Имя" autocomplete="name"><input type="text" name="contact" placeholder="Телефон или e-mail" autocomplete="email" required><textarea name="comment" rows="3" placeholder="Комментарий: сроки, бюджетные рамки, что важно учесть"></textarea><input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true"><div class="sum" id="csum">Пока ничего не выбрано</div><button type="submit">Отправить выбор на расчёт</button><p class="cerr" id="cerr" hidden></p><p class="sm saved">Выбор сохраняется в этом браузере: можно закрыть страницу и вернуться.</p></form><div class="cok" id="cok" hidden><b>Получили ваш выбор.</b> Свяжемся, чтобы уточнить детали, и пришлём расчёт по выбранным идеям.</div></div></div><details class="inside"><summary>Что входит в проект WOW-зоны</summary><dl><div><dt>Проект</dt><dd>Концепция и сценарий, 3D-модель, раскладка проекции, рабочая документация, пакет согласований с ТЦ</dd></div><div><dt>Оборудование</dt><dd>Проекторы или LED-стена, медиасервер, трекинг, звук, коммутация, крепления и подвес</dd></div><div><dt>Контент</dt><dd>Шоу на пять глав, сцены интерактивного пола, фоновая петля, звуковой дизайн, программирование</dd></div><div><dt>Монтаж и запуск</dt><dd>Монтаж, калибровка, пусконаладка, обучение вашего персонала</dd></div><div><dt>Оплата</dt><dd>Оборудование закупаем под проект, это авансируемая часть. Работы, контент и пусконаладку берём в постоплату</dd></div><div><dt class="no">Не входит</dt><dd class="no">Строительная подготовка помещения по нашему ТЗ. Сервис после гарантийного года по отдельному договору</dd></div></dl></details></div></section>
<section class="contacts" id="contacts" data-depth="11000"><div class="wrap"><div class="kick">11 000 м <em>дно впадины</em></div><div class="ct"><div><h2>Поднимаемся?</h2><p class="lead">Посчитаем выбранные идеи, нарисуем эскиз героя под ваш океанариум и ответим на вопросы по ТЗ экранов.</p><div class="btns"><a href="https://t.me/narodetskii" target="_blank" rel="noopener">Написать в Telegram</a><a class="o" href="tel:+79859998783">+7 985 999-87-83</a><a class="o" href="mailto:info@hand-marketing.ru?subject=Океанариум">info@hand-marketing.ru</a><a class="o pdf-btn" href="?pdf=1">Скачать PDF</a></div><p class="sm" style="margin-top:10px">PDF это версия для печати, интерактив работает только на странице.</p></div><div><div class="who" style="margin-bottom:20px"><b>Александр Народецкий</b><span>Client Service Director</span></div><dl><dt>Мобильный</dt><dd><a href="tel:+79859998783">+7 985 999-87-83</a>, WhatsApp, Telegram</dd><dt>Офис</dt><dd><a href="tel:+74955807537">+7 495 580-75-37</a></dd><dt>Адрес</dt><dd>123022, Москва, ул. Рочдельская, 14А</dd><dt>Проекты</dt><dd><a href="https://hand-marketing.ru/project" target="_blank" rel="noopener">hand-marketing.ru/project</a></dd><dt>Реквизиты</dt><dd>ООО «Хэнд-маркетинг» · ИНН 7709931482 · ОГРН 1137746525608</dd></dl></div></div><p class="foot">Страница подготовлена для Самарского океанариума · доступ по личному приглашению · изображения маскота и зала концептуальные</p></div></section>
<script>window.OC = {"chapters": [[0, "Поверхность", "Солнечные блики, пингвины Гумбольдта ныряют сквозь зал"], [30, "Риф", "Рифовые акулы и скаты проходят вдоль стен, косяк рыб кружит над головой"], [1000, "Сумерки", "Свет гаснет. Мимо проходит кашалот в натуральную величину, его глаз смотрит на вас"], [4000, "Бездна", "Биолюминесценция: светится всё, что движется, включая следы посетителей"], [11000, "Дно впадины", "Тишина и темнота. На подъёме кашалот встречает зал снова и замирает у торцевой стены"]], "faces": {"laugh": ["f-laugh", "Смеётся", "Тронули ласту или живот"], "wow": ["f-wow", "Удивляется", "Кто-то подошёл совсем близко или тронул клюв"], "sleep": ["f-sleep", "Засыпает", "Вечер, зал пустеет"], "wink": ["f-wink", "Подмигивает", "Двойное касание клюва: фотопоза на пять секунд"]}, "day": [["10:00", "Утро", "Открывает глаза, зевает, оглядывает зал. Звук пока молчит", "--mag"], ["11:30", "Первые гости", "Замечает детей, поворачивает голову, здоровается", "--lime"], ["14:00", "День", "Играет, смеётся, даёт задания по маршруту: найди меня за стеклом, найди ската, посчитай акул", "--orange"], ["17:00", "Фотозона", "Позирует и подмигивает. Родители снимают", "--teal"], ["21:50", "Закрытие", "За 10 минут до закрытия прощается, закрывает глаза, проектор гаснет", "--red"]]};</script>
<script>
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

</script>
<script id="hm-oc-analytics">
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

</script>
<script>
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym(71125393, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true, params:{ private_page:'oceanarium' } });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute; left:-9999px;" alt=""></div></noscript>
</body>
</html>
