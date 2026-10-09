<?php
// Персональная страница для ГК АЛИДИ: имиджевый фильм к 35-летию. Доступ по коду.
// Собирается scripts/alidi-page/build.py, руками не править.
// В файле только SHA-256 хеш кода. Аналитика визитов: _analytics.php, отчёт по ?stats=<ключ>.
define('HM_ALIDI', 1);
date_default_timezone_set('Europe/Moscow');
require __DIR__ . '/_analytics.php';

$ACCESS_HASH = '156abb09c845b428d02f8822a212502a76306d57c6d0eba3ba689d08c8bd778c';
$COOKIE_NAME = 'hm_al_access';

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
        setcookie($COOKIE_NAME, $ACCESS_HASH, time() + 60 * 60 * 24 * 30, '/for/alidi/', '', hm_https(), true);
        $g = hm_geo(hm_ip());
        hm_event('login_ok', array('geo' => $g));
        hm_tg("🔓 <b>АЛИДИ открыли страницу</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where($g) . "\n" . date('d.m H:i'));
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
<title>Доступ к странице · АЛИДИ × Hand Marketing</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/react-main.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Inter',system-ui,sans-serif; color:#141417; background:#141417;
    min-height:100vh; display:flex; align-items:center; justify-content:center; padding:20px; }
  .gate { background:#fff; border-radius:6px; padding:44px 36px 34px; max-width:430px; width:100%; position:relative; overflow:hidden; }
  .gate:before { content:''; position:absolute; left:0; top:0; right:0; height:6px; background:#0041EA; }
  .logos { display:flex; align-items:center; gap:16px; margin-bottom:34px; }
  .logos svg { height:20px; width:auto; color:#141417; }
  .logos img { height:34px; }
  .logos i { width:1px; height:26px; background:#d6d6dc; }
  h1 { font-family:'Montserrat',sans-serif; font-weight:800; font-size:24px; line-height:1.2; letter-spacing:-.02em; margin-bottom:10px; }
  .sub { font-size:15px; color:#6e6e78; margin-bottom:24px; }
  form { display:flex; flex-direction:column; gap:10px; }
  input { font-family:'Montserrat',sans-serif; font-weight:600; font-size:17px; letter-spacing:.08em; text-align:center; text-transform:uppercase;
    padding:15px; border:1.5px solid #e1e1e6; border-radius:4px; outline:none; background:#f5f5f2; }
  input:focus { border-color:#0041EA; background:#fff; }
  button { font-family:'Montserrat',sans-serif; font-weight:700; font-size:15px; color:#fff; background:#0041EA; border:0;
    border-radius:4px; padding:16px; cursor:pointer; }
  button:hover { background:#0034bb; }
  .gate-error { color:#d92d2d; font-size:13px; margin-top:4px; text-align:center; }
  .note { margin-top:24px; font-size:12px; color:#8a8a93; text-align:center; }
</style>
</head>
<body>
  <div class="gate">
    <div class="logos"><svg class="alidi-logo" role="img" aria-label="АЛИДИ" viewBox="0 0 260 46" fill="none" xmlns="http://www.w3.org/2000/svg"> <g clip-path="url(#alc)"> <path d="M148.502 0H139.185V46H148.502V0Z" fill="currentColor"/> <path d="M240.775 0H231.457V46H240.775V0Z" fill="currentColor"/> <path d="M198.271 0H163.367V46H198.271C211.314 46 221.889 35.7008 221.889 22.9982C221.889 10.2955 211.314 0 198.271 0ZM198.271 9.07543C206.158 9.07543 212.568 15.3223 212.568 22.9982C212.568 30.674 206.158 36.9209 198.271 36.9209H172.684V9.07543H198.271Z" fill="currentColor"/> <path d="M81.5839 0.161211V45.978H128.629V36.9026H90.9014V0.161211H81.5839Z" fill="currentColor"/> <path d="M23.7804 0L0 46H11.5106L35.2873 0H23.7804Z" fill="currentColor"/> <path d="M35.2873 0L59.0677 46H70.5782L46.7978 0H35.2873Z" fill="currentColor"/> <path d="M24.5397 45.978H46.0423L35.2873 25.2258L24.5397 45.978Z" fill="#0041EA"/> <path d="M254.025 38.6686H253.288V40.3356H254.106C254.998 40.3356 255.352 40.0572 255.352 39.5076C255.352 38.8371 254.828 38.6686 254.036 38.6686H254.025ZM254.349 41.2333H253.277V43.3657H252.105V37.7563H253.826C255.481 37.7563 256.487 38.0531 256.487 39.4966C256.488 39.8154 256.391 40.1269 256.208 40.389C256.026 40.6511 255.767 40.8512 255.466 40.9622L256.767 43.3327H255.496L254.353 41.2003L254.349 41.2333ZM254.18 45.0657C256.612 45.0657 258.422 43.3437 258.422 40.7643C258.422 38.185 256.612 36.419 254.18 36.419C251.747 36.419 249.926 38.1593 249.926 40.7643C249.926 43.3693 251.806 45.0657 254.18 45.0657ZM254.18 35.481C254.881 35.4623 255.579 35.586 256.231 35.8447C256.883 36.1033 257.475 36.4915 257.971 36.9853C258.466 37.4792 258.856 38.0684 259.115 38.7169C259.373 39.3654 259.496 40.0596 259.476 40.757C259.476 43.8969 257.114 46 254.187 46C253.48 46.0186 252.776 45.8961 252.118 45.64C251.459 45.3838 250.859 44.9991 250.352 44.5085C249.845 44.018 249.443 43.4315 249.168 42.7837C248.893 42.1359 248.751 41.4399 248.751 40.7368C248.751 40.0337 248.893 39.3378 249.168 38.69C249.443 38.0422 249.845 37.4557 250.352 36.9651C250.859 36.4746 251.459 36.0899 252.118 35.8337C252.776 35.5776 253.48 35.4551 254.187 35.4737" fill="currentColor"/> </g> <defs> <clipPath id="alc"> <rect width="259.469" height="46" fill="white"/> </clipPath> </defs> </svg><i></i><img src="hm-logo.svg" alt="Hand Marketing"></div>
    <h1>Имиджевый фильм<br>к 35-летию АЛИДИ</h1>
    <p class="sub">Введите код доступа из письма</p>
    <form method="post" action="./" autocomplete="off">
      <input type="text" name="code" placeholder="код доступа" maxlength="30" autocapitalize="characters" spellcheck="false" autofocus required>
      <button type="submit">Открыть страницу</button>
      {$errHtml}
    </form>
    <p class="note">Hand Marketing · доступ по личному приглашению</p>
  </div>
</body>
</html>
GATE;
    exit;
}
// PDF только после входа: файлы лежат рядом, прямой доступ закрыт в .htaccess.
// ?pdf=1 текущая версия материалов (собирается scripts/alidi-page/pdf.mjs), ?pdf=portfolio портфолио от 30 сентября
if (isset($_GET['pdf'])) {
    $old = $_GET['pdf'] === 'portfolio';
    $f = __DIR__ . ($old ? '/alidi-portfolio.pdf' : '/alidi-materials.pdf');
    if (!is_file($f)) { http_response_code(404); exit; }
    hm_event('pdf_download', array('file' => $old ? 'portfolio' : 'materials'));
    hm_tg("📄 <b>АЛИДИ скачали PDF</b>" . ($old ? " (портфолио)" : " (материалы 9 октября 2026)") . "\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where(hm_geo(hm_ip())) . "\n" . date('d.m H:i'));
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="' . ($old ? 'Hand_Marketing_ALIDI_portfolio.pdf' : 'Hand_Marketing_ALIDI_2026-10-09.pdf') . '"');
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
<title>Hand Marketing для ГК АЛИДИ: имиджевый фильм к 35-летию</title>
<meta name="description" content="Корпоративные и имиджевые фильмы, съёмки на складах и производстве, работа в Казахстане и Беларуси. Кейсы со ссылками.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/react-main.css">
<link rel="stylesheet" href="/fonts/golos-ptserif.css">
<link rel="stylesheet" href="/fonts/plex.css">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
:root {
  --ink:#141417; --ink2:#1e1e23; --bg:#f4f3ef; --card:#fff; --line:#e3e2dc; --grey:#6e6e78; --grey2:#9a9aa3;
  --blue:#0041EA; --blue-d:#0034bb; --blue-l:#e6edfd;
  --rf:#0041EA; --rb:#5a9a2c; --rk:#e2661c;
  --head:'Montserrat','Inter',sans-serif; --r:6px;
}
html { scroll-behavior:smooth; scroll-padding-top:70px; }
body { font-family:'Inter',system-ui,sans-serif; color:var(--ink); background:var(--bg); font-size:16px; line-height:1.55;
  -webkit-font-smoothing:antialiased; overflow-x:hidden; }
img { display:block; max-width:100%; height:auto; }
a { color:inherit; }
button { font:inherit; color:inherit; background:none; border:0; cursor:pointer; }
.wrap { max-width:1240px; margin:0 auto; padding:0 32px; }
h1, h2, h3, h4 { font-family:var(--head); letter-spacing:-.02em; }
h2 { font-weight:800; font-size:clamp(28px,4vw,48px); line-height:1.08; margin-bottom:34px; max-width:900px; }
h3 { font-weight:700; font-size:20px; line-height:1.25; }
.sub { color:var(--grey); max-width:720px; margin:-18px 0 34px; font-size:17px; }

/* фирменный треугольник АЛИДИ (синяя вставка в «А») как маркер разделов */
.tri { width:14px; height:8px; fill:var(--blue); flex:none; }
.eyebrow { display:flex; align-items:center; gap:10px; font-family:var(--head); font-weight:700; font-size:12px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--grey); margin-bottom:16px; }
.eyebrow b { color:var(--ink); }
.eyebrow.light { color:rgba(255,255,255,.6); }
.eyebrow.light b { color:#fff; }

/* шапка */
.top { position:sticky; top:0; z-index:20; background:rgba(20,20,23,.92); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); color:#fff; }
.top-in { display:flex; align-items:center; gap:24px; height:60px; }
.brand { display:flex; align-items:center; gap:14px; text-decoration:none; color:#fff; flex:none; }
.alidi-logo { height:17px; width:auto; }
.brand i { width:1px; height:22px; background:rgba(255,255,255,.25); }
.brand img { height:30px; width:auto; }
.nav { display:flex; gap:22px; margin-left:auto; font-size:14px; }
.nav a { text-decoration:none; opacity:.72; transition:opacity .2s; }
.nav a:hover { opacity:1; }
.pdf-btn { font-family:var(--head); font-weight:700; font-size:13px; text-decoration:none; padding:8px 14px; border:1.5px solid rgba(255,255,255,.35); border-radius:var(--r); }
.top .pdf-btn:hover { background:#fff; color:var(--ink); }

/* первый экран */
.hero { background:var(--ink); color:#fff; padding:80px 0 56px; overflow:hidden; position:relative; border-bottom:6px solid var(--blue); isolation:isolate; }
/* немая нарезка складов, отгрузки и терминалов из наших фильмов (scripts/alidi-page/hero_loop.py) */
.hero-bg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:-2; }
.hero-bg { pointer-events:none; }
/* Safari при запрете автозапуска рисует свою кнопку play: прячем, фоном остаётся постер */
.hero-bg::-webkit-media-controls, .hero-bg::-webkit-media-controls-start-playback-button,
.hero-bg::-webkit-media-controls-panel, .hero-bg::-webkit-media-controls-play-button { display:none !important; -webkit-appearance:none; opacity:0 !important; }
.hero:before { content:''; position:absolute; inset:0; z-index:-1;
  background:linear-gradient(90deg, rgba(20,20,23,.94) 0%, rgba(20,20,23,.82) 42%, rgba(20,20,23,.45) 100%),
             linear-gradient(0deg, rgba(20,20,23,.9) 0%, rgba(20,20,23,0) 45%); }
.hero h1 { font-weight:800; font-size:clamp(40px,7.4vw,96px); line-height:.98; letter-spacing:-.035em; margin-bottom:28px; }
.lead { font-size:clamp(17px,1.6vw,20px); line-height:1.5; max-width:660px; color:rgba(255,255,255,.78); }
.hero-cta { display:flex; flex-wrap:wrap; gap:12px; margin:34px 0 0; }
.btn { display:inline-flex; align-items:center; gap:10px; font-family:var(--head); font-weight:700; font-size:15px; text-decoration:none;
  background:var(--blue); color:#fff; padding:16px 24px; border-radius:var(--r); transition:background .2s, transform .2s; }
.btn:hover { background:var(--blue-d); transform:translateY(-1px); }
.btn.ghost { background:transparent; box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.4); }
.btn.ghost:hover { background:rgba(255,255,255,.1); }
.vid-inline:before { content:''; width:0; height:0; border-left:9px solid currentColor; border-top:6px solid transparent; border-bottom:6px solid transparent; }

.clock { display:grid; grid-template-columns:auto 1fr; gap:48px; align-items:end; margin-top:64px; padding-top:28px; border-top:1px solid rgba(255,255,255,.14); }
.clock-n { display:flex; align-items:flex-end; gap:16px; }
.clock-n b { font-family:var(--head); font-weight:800; font-size:clamp(56px,7vw,88px); line-height:.8; color:#fff; letter-spacing:-.04em; }
.clock-n span { font-size:14px; line-height:1.35; color:rgba(255,255,255,.62); padding-bottom:2px; }
.line { position:relative; height:66px; margin-bottom:46px; border-bottom:2px solid rgba(255,255,255,.18); }
.line .now { position:absolute; left:0; bottom:-2px; height:2px; width:0; background:#fff; }
.mk { position:absolute; left:var(--p); bottom:-6px; transform:translateX(-50%); font-size:12px; line-height:1.3; color:rgba(255,255,255,.55);
  padding-bottom:20px; text-align:center; white-space:nowrap; }
.mk:after { content:''; position:absolute; left:50%; bottom:0; width:10px; height:10px; margin-left:-5px; border-radius:50%; background:var(--ink); border:2px solid rgba(255,255,255,.5); }
.mk b { display:block; color:#fff; font-weight:600; }
.mk:first-child, .mk[style*="0%"] { transform:none; text-align:left; }
.mk[style*="0%"]:after { left:0; margin-left:0; background:#fff; border-color:#fff; }
.mk.blue:after { background:var(--blue); border-color:var(--blue); }
.mk.blue { transform:translateX(calc(-100% + 5px)); text-align:right; }
.mk.blue:after { left:auto; right:0; margin-left:0; }
.mk.end { transform:translateX(-100%); text-align:right; bottom:auto; top:100%; padding:14px 0 0; }
.mk.end:after { left:auto; right:-7px; width:14px; height:14px; top:-8px; bottom:auto; border-radius:0; border:0; background:var(--blue);
  clip-path:polygon(0 100%,50% 0,100% 100%); }
.sign { margin-top:40px; font-size:13px; color:rgba(255,255,255,.5); }


/* разделы */
.sec { padding:110px 0; }
.sec.tint { background:#ebe9e3; }
.sec.dark { background:var(--ink); color:#fff; }

/* ТЗ */
.tz { display:grid; grid-template-columns:repeat(3,1fr); gap:2px; background:var(--line); border:2px solid var(--line); border-radius:var(--r); overflow:hidden; }
.tz-c { background:var(--card); padding:28px 28px 30px; display:grid; grid-template-columns:auto 1fr; column-gap:16px; align-items:baseline; }
.tz-c .n { font-family:var(--head); font-weight:800; font-size:52px; line-height:1; color:var(--blue); letter-spacing:-.03em; }
.tz-c .cap { font-family:var(--head); font-weight:700; font-size:13px; text-transform:uppercase; letter-spacing:.08em; }
.tz-c p { grid-column:1 / -1; margin-top:14px; color:#46464e; font-size:15px; }
.note { margin-top:24px; padding:20px 24px; background:var(--blue-l); border-left:4px solid var(--blue); border-radius:0 var(--r) var(--r) 0; font-size:15px; max-width:980px; }
.note b { font-family:var(--head); }

.geo { display:grid; grid-template-columns:320px 1fr; gap:40px; margin-top:64px; align-items:center; background:var(--card); border-radius:var(--r); padding:36px; }
.geo-t p { color:#46464e; margin:14px 0 20px; font-size:15px; }
.geo-l { list-style:none; display:flex; flex-direction:column; gap:8px; font-size:14px; font-weight:600; }
.geo-l li { display:flex; align-items:center; gap:10px; }
.geo-l i { width:12px; height:10px; clip-path:polygon(0 100%,50% 0,100% 100%); }
.c-rf { background:var(--rf); } .c-rb { background:var(--rb); } .c-rk { background:var(--rk); }
.geo-svg { width:100%; height:auto; overflow:visible; font-family:'Inter',sans-serif; }
.geo-svg .mer { stroke:#ebe9e3; stroke-width:1; }
.geo-svg .deg { font-size:10px; fill:#b3b2ab; }
.geo-svg .route { fill:none; stroke:var(--ink); stroke-width:1.4; stroke-dasharray:4 5; opacity:0; }
.geo-svg .halo { fill:currentColor; opacity:.14; transform-box:fill-box; transform-origin:center; }
.geo-svg .tri-pt { fill:currentColor; }
.geo-svg .pt { color:var(--rf); opacity:0; }
.geo-svg .pt-РБ { color:var(--rb); } .geo-svg .pt-РК { color:var(--rk); }
.geo-svg .nm { font-family:var(--head); font-weight:700; font-size:15px; fill:var(--ink); }
.geo-svg .cc { font-size:11px; fill:var(--grey); }
.geo.in .route { animation:draw .9s ease forwards var(--d); }
.geo.in .pt { animation:pop .5s ease forwards var(--d); }
.geo.in .halo { animation:pulse 2.4s ease-out infinite calc(var(--d) + .6s); }
@keyframes draw { from { opacity:1; stroke-dashoffset:400; } to { opacity:.55; stroke-dashoffset:0; } }
@keyframes pop { to { opacity:1; } }
@keyframes pulse { 0% { transform:scale(.6); opacity:.35; } 100% { transform:scale(2.2); opacity:0; } }

/* опыт под задачу */
.match { display:grid; grid-template-columns:minmax(320px,470px) 1fr; gap:48px; align-items:start; }
.m-list { display:flex; flex-direction:column; border-top:1px solid rgba(255,255,255,.14); }
.m-row { display:flex; gap:18px; align-items:baseline; text-align:left; padding:26px 4px; border-bottom:1px solid rgba(255,255,255,.14);
  color:rgba(255,255,255,.55); transition:color .2s, padding .25s; }
.m-row:hover { color:#fff; }
.m-row.on { color:#fff; padding-left:14px; box-shadow:inset 3px 0 0 var(--blue); }
.m-n { font-family:var(--head); font-weight:800; font-size:15px; color:var(--blue); filter:brightness(1.6); }
.m-need { font-family:var(--head); font-weight:700; font-size:clamp(20px,1.9vw,25px); line-height:1.25; }
.m-pane { display:none; }
.m-pane.on { display:block; animation:fade .4s ease; }
@keyframes fade { from { transform:translateY(8px); } }
.m-shots { display:grid; gap:6px; margin-bottom:22px; border-radius:var(--r); overflow:hidden; }
.m-shots.n3 { grid-template-columns:2fr 1fr; grid-template-rows:1fr 1fr; aspect-ratio:16/8; }
.m-shots.n3 figure:first-child { grid-row:1 / 3; }
.m-shots.n2 { grid-template-columns:1fr 1fr; aspect-ratio:16/8; }
.m-shots.n4 { grid-template-columns:repeat(4,1fr); }
.m-shots.n4 figure { aspect-ratio:3/4; }
.m-shots figure { position:relative; min-height:0; }
.m-shots img { width:100%; height:100%; object-fit:cover; }
.m-shots figcaption { position:absolute; left:6px; bottom:6px; background:var(--blue); color:#fff; font-family:var(--head); font-weight:700; font-size:11px;
  padding:4px 7px; border-radius:3px; }
.m-pane p { font-size:19px; line-height:1.5; color:rgba(255,255,255,.85); max-width:640px; }
.m-need-m { display:none; }
.m-link { display:inline-flex; gap:8px; margin-top:16px; font-family:var(--head); font-weight:700; font-size:14px; color:#fff; text-decoration:none;
  border-bottom:1.5px solid var(--blue); padding-bottom:3px; }
.m-link span { color:#7c9cff; }

/* видео-обложки */
.vid { position:relative; display:block; width:100%; aspect-ratio:16/9; border-radius:var(--r); overflow:hidden; background:#000; }
.vid img { width:100%; height:100%; object-fit:cover; transition:transform .5s ease, opacity .3s; }
.vid:hover img { transform:scale(1.03); opacity:.85; }
.play { position:absolute; left:50%; top:50%; width:72px; height:72px; margin:-36px 0 0 -36px; border-radius:50%; background:var(--blue);
  display:flex; align-items:center; justify-content:center; box-shadow:0 10px 30px rgba(0,0,0,.3); transition:transform .2s; }
.play svg { width:30px; height:30px; fill:#fff; margin-left:3px; }
.vid:hover .play { transform:scale(1.08); }
.vid video { width:100%; height:100%; display:block; background:#000; }

/* корпоративные фильмы */
.film { display:grid; grid-template-columns:1.1fr 1fr; gap:48px; padding:48px 0; border-top:1px solid var(--line); }
.film:first-of-type { border-top:0; padding-top:8px; }
.film.rev .film-v { order:2; }
.film > div { min-width:0; }
.part { font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:var(--grey); margin:0 0 8px; }
.vid + .part { margin-top:18px; }
.film-v .accent { margin-top:18px; font-family:var(--head); font-weight:800; font-size:clamp(20px,2vw,26px); line-height:1.2; color:var(--c); letter-spacing:-.02em; }
.tag { font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:var(--c); margin-bottom:10px; }
.film-t h3 { font-size:clamp(22px,2.3vw,30px); font-weight:800; margin-bottom:16px; }
.film-t > p { color:#46464e; font-size:15.5px; }
.stats { display:grid; grid-template-columns:repeat(3,1fr); gap:2px; margin:24px 0 0; background:var(--line); border:2px solid var(--line); border-radius:var(--r); overflow:hidden; }
.stats.n4 { grid-template-columns:repeat(2,1fr); }
.stats div { background:var(--card); padding:16px 18px; }
.stats b { display:block; font-family:var(--head); font-weight:800; font-size:28px; line-height:1.1; color:var(--c); letter-spacing:-.02em; }
.stats span { display:block; font-size:13px; color:var(--grey); line-height:1.4; margin-top:6px; }
blockquote { margin-top:22px; font-family:var(--head); font-weight:700; font-size:19px; line-height:1.35; padding-left:18px; border-left:4px solid var(--c); }
cite { display:block; margin-top:8px; font-family:'Inter',sans-serif; font-style:normal; font-weight:400; font-size:13px; color:var(--grey); }
.case-link { display:inline-flex; gap:8px; margin-top:22px; font-family:var(--head); font-weight:700; font-size:14px; text-decoration:none;
  border-bottom:1.5px solid var(--c, var(--blue)); padding-bottom:3px; }
.case-link span { color:var(--c, var(--blue)); }

/* стена лиц */
.faces { background:var(--ink); color:#fff; padding:0; overflow:hidden; }
.faces-in { display:grid; grid-template-columns:340px 1fr; gap:48px; align-items:center; padding-top:90px; padding-bottom:90px; }
.faces-t h2 { margin-bottom:20px; font-size:clamp(28px,3vw,40px); }
.faces-t p { color:rgba(255,255,255,.75); }
.wall { display:grid; grid-template-columns:repeat(12,1fr); gap:3px; }
.wall img { width:100%; aspect-ratio:3/4; object-fit:cover; transition:transform .3s; }
.wall img:hover { transform:scale(1.08); position:relative; z-index:1; box-shadow:0 8px 24px rgba(0,0,0,.5); }

/* площадки */
.places { display:grid; grid-template-columns:repeat(3,1fr); gap:28px; }
.place .meta { margin-top:16px; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:var(--blue); }
.place h3 { margin:6px 0 10px; }
.place p { font-size:15px; color:#46464e; }
.place .case-link { margin-top:14px; }

/* серии */
.series { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; }
.ser { position:relative; background:var(--card); border-radius:var(--r); padding:22px 22px 26px; text-decoration:none; transition:transform .25s, box-shadow .25s; }
.ser:hover { transform:translateY(-4px); box-shadow:0 18px 40px rgba(20,20,23,.1); }
.ser img { width:72%; margin:0 auto 6px; aspect-ratio:476/396; object-fit:contain; }
.ser-n { font-size:13px; color:var(--grey); }
.ser-n b { font-family:var(--head); font-weight:800; font-size:34px; color:var(--blue); letter-spacing:-.03em; margin-right:4px; }
.ser h3 { font-size:17px; margin:4px 0 8px; }
.ser p { font-size:14px; color:#55555d; }
.arr { position:absolute; top:18px; right:20px; color:var(--blue); font-weight:700; }

/* умеем */
.skills { display:grid; grid-template-columns:repeat(4,1fr); border-top:2px solid var(--ink); }
.sk { padding:26px 26px 30px 0; border-bottom:1px solid var(--line); }
.sk:not(:nth-child(4n+1)) { padding-left:26px; border-left:1px solid var(--line); }
.sk-n { font-family:var(--head); font-weight:700; font-size:12px; color:var(--blue); }
.sk h3 { margin:8px 0 8px; font-size:19px; }
.sk p { font-size:15px; color:#55555d; }
.sk a { display:inline-block; margin-top:12px; font-size:13px; font-weight:600; color:var(--blue); text-decoration:none; }
.sk a:hover { text-decoration:underline; }

/* отзывы */
.revs { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.rev { background:var(--ink2); border-radius:var(--r); padding:66px 28px 26px; display:flex; flex-direction:column; justify-content:space-between; gap:24px; position:relative; }
.rev:before { content:'“'; position:absolute; top:18px; left:26px; font-family:var(--head); font-weight:800; font-size:64px; line-height:1; color:var(--blue); filter:brightness(1.5); }
.rev blockquote { border:0; padding:0; margin:0; font-family:'Inter',sans-serif; font-weight:400; font-size:17px; line-height:1.5; color:rgba(255,255,255,.9); }
.rev.big { grid-column:span 2; background:var(--blue); }
.rev.big:before { color:rgba(255,255,255,.4); filter:none; }
.rev.big blockquote { font-family:var(--head); font-weight:700; font-size:clamp(22px,2.3vw,30px); line-height:1.3; color:#fff; }
.rev figcaption { font-size:13px; color:rgba(255,255,255,.55); line-height:1.45; }
.rev.big figcaption { color:rgba(255,255,255,.8); }
.rev figcaption b { display:block; font-family:var(--head); font-size:15px; color:#fff; margin-bottom:2px; }
.rev figcaption a { margin-left:10px; color:#fff; font-weight:600; text-decoration:none; border-bottom:1px solid rgba(255,255,255,.4); }
.revs-note { margin-top:20px; font-size:13px; color:rgba(255,255,255,.45); }

/* все проекты */
.tabs { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:28px; }
.tabs button { font-family:var(--head); font-weight:700; font-size:14px; padding:10px 16px; border-radius:var(--r); background:var(--card); transition:background .2s, color .2s; }
.tabs button i { font-style:normal; font-weight:500; opacity:.5; margin-left:4px; }
.tabs button.on { background:var(--ink); color:#fff; }
.grid { display:grid; grid-template-columns:repeat(5,1fr); gap:14px; }
.card { background:var(--card); border-radius:var(--r); padding:18px 18px 22px; text-decoration:none; transition:transform .25s, box-shadow .25s; }
.card:hover { transform:translateY(-3px); box-shadow:0 14px 34px rgba(20,20,23,.09); }
.card img { width:64%; margin:0 auto 10px; aspect-ratio:476/396; object-fit:contain; }
.card .cl { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.08em; color:var(--blue); }
.card h4 { font-size:15.5px; font-weight:700; line-height:1.3; margin:4px 0 6px; }
.card p { font-size:13.5px; line-height:1.45; color:#5b5b63; }
.card.hide { display:none; }

/* шаги */
.steps { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.st:not(:last-child):after { content:''; position:absolute; right:-13px; top:44px; width:10px; height:10px; border-top:2px solid var(--blue); border-right:2px solid var(--blue); transform:rotate(45deg); z-index:1; }
.par { display:grid; grid-template-columns:auto 1fr; gap:24px; align-items:center; margin-top:16px; padding:22px 26px; border-radius:var(--r);
  border:2px dashed var(--blue); background:var(--card); }
.par-l { font-family:var(--head); font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:.12em; color:#fff; background:var(--blue); padding:7px 12px; border-radius:3px; }
.par h3 { font-size:18px; margin-bottom:4px; }
.par p { font-size:14.5px; color:#55555d; }
.st { background:var(--card); border-radius:var(--r); padding:26px; position:relative; }
.st b { font-family:var(--head); font-weight:800; font-size:40px; color:var(--blue); letter-spacing:-.03em; line-height:1; }
.st h3 { margin:16px 0 8px; font-size:18px; }
.st p { font-size:14.5px; color:#55555d; }

/* финал */
.final { background:var(--ink); color:#fff; padding:100px 0 30px; }
.fin { display:grid; grid-template-columns:1fr 1fr; gap:56px; }
.final h2 { font-size:clamp(36px,5vw,64px); margin-bottom:20px; }
.cont { display:grid; grid-template-columns:150px 1fr; row-gap:14px; column-gap:20px; font-size:15px; align-content:start; padding-top:8px; }
.cont dt { color:rgba(255,255,255,.45); font-size:12px; text-transform:uppercase; letter-spacing:.08em; padding-top:3px; }
.cont a { text-decoration:none; border-bottom:1px solid rgba(255,255,255,.3); }
.foot { margin-top:80px; padding-top:20px; border-top:1px solid rgba(255,255,255,.1); font-size:12px; color:rgba(255,255,255,.35); }

/* окно ролика */
.modal { position:fixed; inset:0; z-index:50; background:rgba(10,10,12,.92); display:flex; align-items:center; justify-content:center; padding:4vw; }
.modal[hidden] { display:none; }
.modal .mv { width:min(1200px,100%); aspect-ratio:16/9; max-height:100%; }
.modal video { width:100%; height:100%; background:#000; }
.modal .x { position:absolute; top:14px; right:20px; color:#fff; font-size:40px; line-height:1; }

/* адаптив */
@media (max-width:1240px) { .grid { grid-template-columns:repeat(4,1fr); } }
@media (max-width:1100px) {
  .nav { display:none; }
  .top .pdf-btn { margin-left:auto; }
  .grid { grid-template-columns:repeat(3,1fr); }
  .series { grid-template-columns:repeat(2,1fr); }
  .faces-in { grid-template-columns:1fr; }
}
@media (max-width:980px) {
  .sec { padding:80px 0; }
  .tz { grid-template-columns:repeat(2,1fr); }
  .geo { grid-template-columns:1fr; padding:28px; }
  .match { grid-template-columns:1fr; gap:0; }
  .m-list { display:none; }
  .m-pane, .m-pane.on { display:block; animation:none; padding:28px 0; border-top:1px solid rgba(255,255,255,.14); }
  .m-need-m { display:block; font-family:var(--head); font-weight:700; font-size:20px !important; color:#fff !important; margin-bottom:8px; }
  .m-pane .m-shots { margin-bottom:18px; }
  .film, .film.rev { grid-template-columns:1fr; gap:24px; }
  .film.rev .film-v { order:0; }
  .places { grid-template-columns:1fr; }
  .place { display:grid; grid-template-columns:1fr 1fr; column-gap:24px; align-content:start; }
  .place .vid { grid-row:1 / 6; }
  .place .meta { margin-top:0; }
  .skills { grid-template-columns:1fr 1fr; }
  .sk, .sk:not(:nth-child(4n+1)) { padding:22px 22px 26px 0; border-left:0; }
  .sk:nth-child(2n) { padding-left:22px; border-left:1px solid var(--line); }
  .steps { grid-template-columns:1fr; }
  .revs { grid-template-columns:1fr 1fr; }
  .rev.big { grid-column:1 / -1; }
  .st:not(:last-child):after { right:auto; left:40px; top:auto; bottom:-13px; transform:rotate(135deg); }
  .par { grid-template-columns:1fr; gap:12px; }
  .par-l { justify-self:start; }
  .fin { grid-template-columns:1fr; gap:40px; }
  .clock { grid-template-columns:1fr; gap:28px; }
  .line { margin:0 10px 0 0; }
}
@media (max-width:640px) {
  .wrap { padding:0 16px; }
  .hero { padding-top:48px; padding-bottom:40px; }
  .hero:before { background:linear-gradient(0deg, rgba(20,20,23,.95) 0%, rgba(20,20,23,.8) 55%, rgba(20,20,23,.6) 100%); }
  .sec { padding:64px 0; }
  .tz { grid-template-columns:1fr; }
  .stats, .stats.n4 { grid-template-columns:1fr 1fr; }
  .stats.n3 div:last-child { grid-column:1 / -1; }
  .stats b { font-size:24px; }
  .tz-c { padding:22px; }
  .tz-c .n { font-size:42px; }
  .geo { padding:20px 14px; margin-top:44px; }
  .geo-m { overflow-x:auto; -webkit-overflow-scrolling:touch; margin:0 -14px; padding:0 14px 6px; }
  .geo-svg { width:620px; max-width:none; }
  .geo-m:after { content:'листайте карту →'; display:block; font-size:12px; color:var(--grey2); margin-top:4px; }
  .places, .skills, .steps, .revs { grid-template-columns:1fr; }
  .rev { padding:58px 20px 20px; }
  .rev:before { left:18px; top:14px; }
  .place { display:block; }
  .place .meta { margin-top:16px; }
  .sk:nth-child(2n) { padding-left:0; border-left:0; }
  .grid { grid-template-columns:1fr 1fr; gap:10px; }
  .card { padding:14px 12px 16px; }
  .card h4 { font-size:14px; }
  .card p { display:none; }
  .series { grid-template-columns:1fr 1fr; gap:10px; }
  .ser { padding:16px 14px 18px; }
  .ser p { font-size:13px; }
  .ser-n b { font-size:26px; }
  .wall { grid-template-columns:repeat(8,1fr); gap:2px; }
  .faces-in { padding-top:64px; padding-bottom:64px; gap:32px; }
  .cont { grid-template-columns:1fr; row-gap:4px; }
  .cont dd { margin-bottom:12px; }
  .mk { font-size:11px; }
  .m-shots.n4 { gap:3px; }
  .m-shots figcaption { font-size:9px; padding:3px 5px; left:3px; bottom:3px; }
  .mk[data-d="2027-02-01"] { display:none; }
  .brand img { height:26px; }
  .alidi-logo { height:14px; }
  .btn { padding:14px 18px; font-size:14px; }
}
@media (prefers-reduced-motion:reduce) {
  .hero-bg { display:none; }
  .geo .route, .geo .pt { opacity:1 !important; animation:none !important; }
}

/* архив под кнопкой */
.arch-bar { background:#ebe9e3; padding:44px 0; border-top:1px solid var(--line); }
.arch-in { display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap; }
.arch-in h3 { font-size:clamp(22px,2.4vw,30px); font-weight:800; margin-bottom:6px; }
.arch-in p { color:#55555d; }
.arch-in .eyebrow { margin-bottom:8px; }
.btn.ghost-d { background:var(--ink); }
.btn.ghost-d:hover { background:#000; }
.btn.ghost-d[aria-expanded="true"] { background:transparent; color:var(--ink); box-shadow:inset 0 0 0 1.5px var(--ink); }
@media (max-width:640px) { .arch-bar { padding:32px 0; } .arch-in .btn { width:100%; justify-content:center; } }

/* письмо после встречи */
.mono { font-family:'IBM Plex Mono',ui-monospace,monospace; font-size:14px; letter-spacing:.02em; }
.dim { color:var(--grey); }
.memo { background:#fbfaf6; padding:96px 0 90px; }
.memo-in { display:grid; grid-template-columns:220px minmax(0,660px); gap:64px; }
.memo-side { padding-top:14px; }
.memo-side .mono:first-child { font-size:17px; color:var(--ink); font-weight:600; }
.memo-to { margin-top:44px; padding-top:18px; border-top:1px solid var(--line); }
.memo-to .alidi-logo { height:14px; width:auto; color:var(--ink); display:block; margin-bottom:10px; }
.memo-to span { font-size:13px; color:var(--grey); line-height:1.45; }
.memo-body { font-family:'PT Serif',Georgia,serif; font-size:20px; line-height:1.62; color:#232327; }
.memo-body h1 { font-family:var(--head); font-weight:800; font-size:clamp(38px,5vw,60px); line-height:1; letter-spacing:-.03em; color:var(--ink); margin-bottom:30px; }
.memo-body p { margin-bottom:18px; }
.memo-body blockquote { margin:30px 0 30px -28px; padding:4px 0 4px 24px; border-left:3px solid var(--blue); font-family:'PT Serif',Georgia,serif; font-weight:400; font-style:italic; font-size:24px; line-height:1.4; color:var(--ink); }
.memo-body blockquote cite { display:block; margin-top:8px; font-family:'IBM Plex Mono',monospace; font-style:normal; font-size:12px; color:var(--grey); }
.memo-body .sign { margin-top:34px; color:var(--ink); font-family:'Inter',sans-serif; font-size:16px; font-weight:600; line-height:1.4; }
.memo-body .sign span { font-weight:400; color:var(--grey); }
.proto { margin-top:70px; border-top:2px solid var(--ink); padding-top:18px; }
.proto-h { display:flex; align-items:baseline; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:8px; }
.proto-h h2 { font-size:26px; margin:0; }
.proto table { width:100%; border-collapse:collapse; font-size:16px; }
.proto th { text-align:left; font-family:'IBM Plex Mono',monospace; font-weight:500; font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--grey); padding:12px 12px 10px 0; border-bottom:1px solid var(--line); }
.proto td { padding:15px 16px 15px 0; border-bottom:1px solid var(--line); vertical-align:top; color:#2b2b30; }
.proto td:nth-child(2) { color:var(--grey); white-space:nowrap; }
.proto td.dt { font-family:'IBM Plex Mono',monospace; font-size:15px; white-space:nowrap; text-align:right; padding-right:0; }
.proto tr.hot td { font-weight:600; color:var(--ink); }
.proto tr.hot td.dt { font-size:30px; font-weight:600; color:var(--blue); line-height:1; }

/* география */
.route { background:var(--ink); color:#fff; padding:96px 0 88px; }
.route-h { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,420px); gap:48px; align-items:end; margin-bottom:56px; }
.route-h h2 { margin:0; font-size:clamp(36px,5vw,64px); }
.route-h p { color:rgba(255,255,255,.7); font-size:16px; }
.route .geo2 .ln { stroke:#fff; }
.route .geo2 .nm { fill:#fff; }
.route .geo2 .sb { fill:rgba(255,255,255,.55); }
.route .geo2 .km { fill:rgba(255,255,255,.55); }
.route .geo2 .g2 { color:#5b86ff; } .route .geo2 .g2-flag { color:#ff7a33; } .route .geo2 .g2-new { color:#5b86ff; }
.route .geo2 .g2-option { color:#9a9aa3; } .route .geo2 .g2-stock { color:#6b6b73; }
.route .geo2 .g2-new .sb { fill:#8fb0ff; }
@media (max-width:980px) { .memo-in { grid-template-columns:1fr; gap:24px; } .memo-side { display:flex; gap:16px; align-items:baseline; flex-wrap:wrap; padding:0; } .memo-to { display:none; } .route-h { grid-template-columns:1fr; gap:16px; } }
@media (max-width:640px) {
  .memo { padding:56px 0; } .memo-body { font-size:18px; } .memo-body blockquote { margin-left:0; font-size:20px; }
  .proto table, .proto thead, .proto tbody, .proto tr, .proto td { display:block; } .proto thead { display:none; }
  .proto tr { padding:12px 0; border-bottom:1px solid var(--line); } .proto td { border:0; padding:2px 0; text-align:left !important; }
  .proto tr.hot td.dt { font-size:24px; margin-top:4px; }
  .route { padding:60px 0; }
}

/* схема-линия (общие стили) */
.geo2 { width:100%; height:auto; overflow:visible; font-family:'Inter',sans-serif; }
.geo2 .ln { stroke-width:3; fill:none; stroke-linecap:round; stroke-linejoin:round; }
.geo2 .br { stroke-width:2; opacity:.6; }
.geo2 .km { font-size:12px; font-weight:600; }
.geo2 .g2 path { fill:currentColor; } .geo2 .hl { fill:currentColor; opacity:.18; }
.geo2 .nm { font-family:var(--head); font-weight:700; font-size:15px; }
.geo2 .sb { font-size:12px; }
.geo2.vt { display:none; max-width:340px; }
@media (max-width:640px) { .geo2.hz { display:none; } .geo2.vt { display:block; } }
@media (max-width:640px) {
  .proto td:nth-child(2), .proto td.dt { display:inline-block; font-size:13px; }
  .proto td:nth-child(2):after { content:'·'; margin:0 6px; color:var(--line); }
  .proto tr.hot td.dt { display:block; font-size:24px; }
}

/* пять идей */
.ideas { background:#fbfaf6; padding:96px 0 90px; }
.ideas-h { display:flex; align-items:baseline; justify-content:space-between; gap:24px; flex-wrap:wrap; margin-bottom:28px; }
.ideas-h h2 { margin:0; font-size:clamp(36px,5vw,60px); }
.ideas-h p { color:var(--grey); font-size:16px; max-width:420px; }
.ideas-l { list-style:none; border-top:2px solid var(--ink); }
.ideas-l li { display:grid; grid-template-columns:48px minmax(0,1fr) minmax(0,1fr); gap:24px; padding:22px 0; border-bottom:1px solid var(--line); align-items:baseline; }
.ideas-l h3 { font-size:21px; margin-bottom:4px; }
.ideas-l p { font-size:15.5px; color:#55555d; }
.ideas-l .ifin { font-family:'PT Serif',Georgia,serif; font-style:italic; font-size:19px; color:var(--ink); }
.vers { display:grid; grid-template-columns:repeat(3,1fr); gap:0; margin-top:48px; }
.vers div { padding:0 24px 0 0; }
.vers div + div { padding-left:24px; border-left:1px solid var(--line); }
.vers b { font-family:var(--head); font-size:18px; display:block; }
.vers .mono { color:var(--blue); font-size:15px; display:block; margin:4px 0 6px; }
.vers p { font-size:14.5px; color:#55555d; }
@media (max-width:980px) { .ideas-l li { grid-template-columns:40px 1fr; } .ideas-l .ifin { grid-column:2; } }
@media (max-width:640px) { .ideas { padding:56px 0; } .vers { grid-template-columns:1fr; gap:18px; } .vers div, .vers div + div { padding:0; border:0; } }

/* как снимаем */
.how { padding:96px 0 90px; background:var(--bg); }
.ex { display:grid; grid-template-columns:minmax(0,380px) minmax(0,1fr); gap:48px; padding:44px 0; border-top:2px solid var(--ink); }
.ex h3 { font-size:26px; margin:8px 0 12px; }
.ex-t p { font-size:15.5px; color:#46464e; margin-bottom:12px; }
.ex-t .ex-for { color:var(--ink); font-weight:600; }
.ex-note { font-size:14px !important; color:var(--grey) !important; padding-left:14px; border-left:2px solid var(--line); }
.ex-v video, .vid0 video { width:100%; aspect-ratio:16/9; background:#000; display:block; border-radius:4px; }
.tp-h { margin:16px 0 8px; }
.tps { display:grid; grid-template-columns:repeat(5,1fr); gap:10px; }
.tp, .pc { text-align:left; padding:0; background:none; border:0; cursor:pointer; }
.tp img { width:100%; aspect-ratio:3/4; object-fit:cover; border-radius:3px; filter:grayscale(.25); transition:filter .2s, outline-color .2s; outline:2px solid transparent; outline-offset:2px; }
.tp b { display:block; font-size:12.5px; line-height:1.25; margin-top:6px; }
.tp span { display:block; font-size:11.5px; color:var(--grey); line-height:1.25; }
.tp:hover img, .tp.on img { filter:none; outline-color:var(--blue); }
.pcs { display:grid; grid-template-columns:repeat(6,1fr); gap:8px; margin-top:10px; }
.pc img { width:100%; aspect-ratio:16/9; object-fit:cover; border-radius:3px; outline:2px solid transparent; outline-offset:2px; }
.pc span { display:block; font-size:12px; color:#55555d; margin-top:4px; line-height:1.2; }
.pc:hover img, .pc.on img { outline-color:var(--blue); }
.ex-cine { grid-template-columns:1fr; gap:22px; }
.ex-cine .ex-t { max-width:640px; }
.cines { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }
.cn b { display:block; font-family:var(--head); font-size:16px; margin-top:10px; }
.cn span { font-size:13.5px; color:var(--grey); }
@media (max-width:980px) { .ex { grid-template-columns:1fr; gap:22px; } .cines { grid-template-columns:1fr 1fr; } }
@media (max-width:640px) { .how { padding:56px 0; } .tps { grid-template-columns:repeat(3,1fr); } .pcs { grid-template-columns:repeat(3,1fr); } .cines { grid-template-columns:1fr; } }

/* карта в фильме */
.maps { padding:90px 0 84px; background:var(--bg); }
.mp-grid { display:grid; grid-template-columns:1fr 1fr; gap:28px 24px; border-top:2px solid var(--ink); padding-top:28px; }
.mp { margin:0; }
.mp-v { width:100%; aspect-ratio:16/9; object-fit:cover; display:block; background:#111; border-radius:4px; }
.mp figcaption { display:grid; grid-template-columns:auto 1fr auto; gap:4px 12px; align-items:baseline; margin-top:12px; }
.mp b { font-family:var(--head); font-size:17px; }
.mp span { font-size:14.5px; color:#55555d; }
.mp a { font-size:13px; color:var(--blue); text-decoration:none; white-space:nowrap; }
@media (max-width:640px) { .maps { padding:56px 0; } .mp-grid { grid-template-columns:1fr; } .mp figcaption { grid-template-columns:1fr auto; } .mp span { grid-column:1 / -1; } }

.mp-wide { grid-column:1 / -1; }
.mp-wide .mp-v { aspect-ratio:21/9; }
.pc.yr span { font-size:13px; color:var(--ink); }
@media (max-width:640px) { .mp-wide .mp-v { aspect-ratio:16/9; } }

.mp-for { background:var(--ink); color:#fff; border-radius:4px; padding:28px 30px; display:flex; flex-direction:column; justify-content:center; }
.mp-for h3 { font-size:24px; margin:8px 0 12px; }
.mp-for p:last-child { color:rgba(255,255,255,.75); font-size:15px; }

.proto tr.done td { color:var(--grey); }
.proto tr.done td:first-child { text-decoration:line-through; text-decoration-color:rgba(0,0,0,.25); }
.proto tr.done td a { text-decoration:none; color:var(--blue); font-size:14px; white-space:nowrap; }
.proto tr.done td.dt { color:#2f8a3e; }
/* проверка СБ */
.sb { background:#fbfaf6; padding:0 0 80px; }
.sb-in { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,560px); gap:32px; align-items:center; border:1px solid var(--line); border-radius:6px; padding:26px 30px; background:#fff; }
.sb h3 { font-size:22px; margin-top:6px; }
.sb ul { list-style:none; }
.sb li { display:flex; justify-content:space-between; gap:16px; padding:10px 0; border-bottom:1px solid var(--line); font-size:15.5px; }
.sb li:last-child { border-bottom:0; }
.sb li b { font-weight:500; font-size:14px; white-space:nowrap; }
.sb li.ok b { color:#2f8a3e; } .sb li.wip b { color:#c77700; }
@media (max-width:980px) { .sb-in { grid-template-columns:1fr; } }
@media (max-width:640px) { .sb { padding-bottom:48px; } .sb-in { padding:20px 18px; } }
.proto tr.done td a { display:inline-block; margin-left:6px; }

.ex-link { display:inline-block; margin-top:4px; font-size:14px; font-weight:600; color:var(--blue); text-decoration:none; border-bottom:1px solid rgba(0,65,234,.3); }
.ex-link:hover { border-bottom-color:var(--blue); }
.cn .ex-link { display:block; width:max-content; margin-top:6px; font-size:13px; }

/* если понадобится ещё что-то */
.more { background:#ebe9e3; padding:64px 0 60px; }
.more-h { display:flex; align-items:baseline; justify-content:space-between; gap:20px; flex-wrap:wrap; margin-bottom:26px; }
.more-h h2 { margin:0; font-size:clamp(24px,2.6vw,32px); }
.more-h p { color:var(--grey); font-size:15px; }
.more-g { display:grid; grid-template-columns:repeat(3,1fr); gap:0; border-top:1px solid #cfcdc6; }
.mc { padding:22px 26px 0 0; }
.mc + .mc { padding-left:26px; border-left:1px solid #cfcdc6; }
.mc h3 { font-size:18px; margin-bottom:6px; }
.mc > p { font-size:14.5px; color:#55555d; margin-bottom:14px; }
.mc ul { list-style:none; }
.mc li a { display:flex; align-items:center; gap:10px; padding:5px 0; text-decoration:none; color:var(--ink); font-size:14px; line-height:1.3; }
.mc li img { width:44px; height:44px; object-fit:contain; flex:none; }
.mc li img.ph { object-fit:cover; border-radius:50%; width:36px; height:36px; margin:4px; }
.mc li span { flex:1; }
.mc li i { font-style:normal; color:var(--blue); }
.mc li a:hover span { color:var(--blue); }
@media (max-width:980px) { .more-g { grid-template-columns:1fr; } .mc, .mc + .mc { padding:20px 0; border-left:0; border-bottom:1px solid #cfcdc6; } }

.more-g { grid-template-columns:repeat(4,1fr); }
@media (max-width:1100px) { .more-g { grid-template-columns:1fr 1fr; } .mc:nth-child(3) { padding-left:0; border-left:0; } .mc:nth-child(n+3) { border-top:1px solid #cfcdc6; margin-top:18px; } }
@media (max-width:640px) { .more-g { grid-template-columns:1fr; } .mc, .mc + .mc { padding:20px 0; border-left:0; margin-top:0; } }

.pdf-dl { display:inline-flex; flex-direction:column; gap:2px; margin-top:22px; padding:10px 14px; border:1.5px solid var(--ink); border-radius:4px; text-decoration:none; color:var(--ink); font-weight:600; font-size:14px; }
.pdf-dl .mono { font-size:11px; color:var(--grey); font-weight:400; }
.pdf-dl:hover { background:var(--ink); color:#fff; } .pdf-dl:hover .mono { color:rgba(255,255,255,.7); }
.arch-in p a { color:var(--blue); text-decoration:none; white-space:nowrap; margin-left:6px; }
@media (max-width:980px) { .pdf-dl { margin-top:0; } }

/* печать в PDF: только новая версия, ролики заменены обложками */
.print-only { display:none; }
@media print {
  @page { size:A4; margin:12mm 0; }
  html { scroll-behavior:auto; }
  body { background:#fff; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .top, .arch-bar, #archive, .modal, .pdf-dl, .tp-h, .hero-cta, .fin .btn { display:none !important; }
  .print-only { display:block; }
  .memo { padding-top:10px; }
  section { break-inside:auto; }
  .ex, .mp, .ideas-l li, .proto tr, .sb-in, .mc, .mp-for, .route-map, .hd-l, .vers, .cn { break-inside:avoid; }
  .route, .maps, .how, .ideas, .more, .final { padding-top:40px !important; padding-bottom:40px !important; }
  .ex-v img.pv, .vid0 img.pv, .mp img.pv { width:100%; aspect-ratio:16/9; object-fit:cover; display:block; border-radius:4px; }
  .ex-v .pv-wrap, .vid0 .pv-wrap, .mp .pv-wrap { position:relative; }
  .pv-wrap:after { content:''; position:absolute; left:50%; top:50%; width:46px; height:46px; margin:-23px 0 0 -23px; border-radius:50%; background:rgba(0,0,0,.55) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='white' d='M9 6v12l9-6z'/%3E%3C/svg%3E") center/26px no-repeat; }
  .mp .pv-wrap:after { display:none; }
  a[href^="http"] { text-decoration:none; }
}

</style>
</head>
<body>
<header class="top"><div class="wrap top-in"><a class="brand" href="#top" aria-label="В начало"><svg class="alidi-logo" role="img" aria-label="АЛИДИ" viewBox="0 0 260 46" fill="none" xmlns="http://www.w3.org/2000/svg"> <g clip-path="url(#alc)"> <path d="M148.502 0H139.185V46H148.502V0Z" fill="currentColor"/> <path d="M240.775 0H231.457V46H240.775V0Z" fill="currentColor"/> <path d="M198.271 0H163.367V46H198.271C211.314 46 221.889 35.7008 221.889 22.9982C221.889 10.2955 211.314 0 198.271 0ZM198.271 9.07543C206.158 9.07543 212.568 15.3223 212.568 22.9982C212.568 30.674 206.158 36.9209 198.271 36.9209H172.684V9.07543H198.271Z" fill="currentColor"/> <path d="M81.5839 0.161211V45.978H128.629V36.9026H90.9014V0.161211H81.5839Z" fill="currentColor"/> <path d="M23.7804 0L0 46H11.5106L35.2873 0H23.7804Z" fill="currentColor"/> <path d="M35.2873 0L59.0677 46H70.5782L46.7978 0H35.2873Z" fill="currentColor"/> <path d="M24.5397 45.978H46.0423L35.2873 25.2258L24.5397 45.978Z" fill="#0041EA"/> <path d="M254.025 38.6686H253.288V40.3356H254.106C254.998 40.3356 255.352 40.0572 255.352 39.5076C255.352 38.8371 254.828 38.6686 254.036 38.6686H254.025ZM254.349 41.2333H253.277V43.3657H252.105V37.7563H253.826C255.481 37.7563 256.487 38.0531 256.487 39.4966C256.488 39.8154 256.391 40.1269 256.208 40.389C256.026 40.6511 255.767 40.8512 255.466 40.9622L256.767 43.3327H255.496L254.353 41.2003L254.349 41.2333ZM254.18 45.0657C256.612 45.0657 258.422 43.3437 258.422 40.7643C258.422 38.185 256.612 36.419 254.18 36.419C251.747 36.419 249.926 38.1593 249.926 40.7643C249.926 43.3693 251.806 45.0657 254.18 45.0657ZM254.18 35.481C254.881 35.4623 255.579 35.586 256.231 35.8447C256.883 36.1033 257.475 36.4915 257.971 36.9853C258.466 37.4792 258.856 38.0684 259.115 38.7169C259.373 39.3654 259.496 40.0596 259.476 40.757C259.476 43.8969 257.114 46 254.187 46C253.48 46.0186 252.776 45.8961 252.118 45.64C251.459 45.3838 250.859 44.9991 250.352 44.5085C249.845 44.018 249.443 43.4315 249.168 42.7837C248.893 42.1359 248.751 41.4399 248.751 40.7368C248.751 40.0337 248.893 39.3378 249.168 38.69C249.443 38.0422 249.845 37.4557 250.352 36.9651C250.859 36.4746 251.459 36.0899 252.118 35.8337C252.776 35.5776 253.48 35.4551 254.187 35.4737" fill="currentColor"/> </g> <defs> <clipPath id="alc"> <rect width="259.469" height="46" fill="white"/> </clipPath> </defs> </svg><i></i><img src="hm-logo.svg" alt="Hand Marketing" width="34" height="34"></a><nav class="nav"><a href="#top">Материалы</a><a href="#archive-open">Наши работы</a><a href="#contacts">Контакты</a></nav><a class="pdf-btn" href="?pdf=1">PDF</a></div></header>
<section class="memo" id="top"><div class="wrap memo-in"><aside class="memo-side"><p class="mono">9.10.2026</p><p class="mono dim">после встречи 7 октября</p><a class="pdf-dl pdf-btn" href="?pdf=1">Скачать PDF<span class="mono">версия от 9 октября 2026</span></a><div class="memo-to"><svg class="alidi-logo" role="img" aria-label="АЛИДИ" viewBox="0 0 260 46" fill="none" xmlns="http://www.w3.org/2000/svg"> <g clip-path="url(#alc)"> <path d="M148.502 0H139.185V46H148.502V0Z" fill="currentColor"/> <path d="M240.775 0H231.457V46H240.775V0Z" fill="currentColor"/> <path d="M198.271 0H163.367V46H198.271C211.314 46 221.889 35.7008 221.889 22.9982C221.889 10.2955 211.314 0 198.271 0ZM198.271 9.07543C206.158 9.07543 212.568 15.3223 212.568 22.9982C212.568 30.674 206.158 36.9209 198.271 36.9209H172.684V9.07543H198.271Z" fill="currentColor"/> <path d="M81.5839 0.161211V45.978H128.629V36.9026H90.9014V0.161211H81.5839Z" fill="currentColor"/> <path d="M23.7804 0L0 46H11.5106L35.2873 0H23.7804Z" fill="currentColor"/> <path d="M35.2873 0L59.0677 46H70.5782L46.7978 0H35.2873Z" fill="currentColor"/> <path d="M24.5397 45.978H46.0423L35.2873 25.2258L24.5397 45.978Z" fill="#0041EA"/> <path d="M254.025 38.6686H253.288V40.3356H254.106C254.998 40.3356 255.352 40.0572 255.352 39.5076C255.352 38.8371 254.828 38.6686 254.036 38.6686H254.025ZM254.349 41.2333H253.277V43.3657H252.105V37.7563H253.826C255.481 37.7563 256.487 38.0531 256.487 39.4966C256.488 39.8154 256.391 40.1269 256.208 40.389C256.026 40.6511 255.767 40.8512 255.466 40.9622L256.767 43.3327H255.496L254.353 41.2003L254.349 41.2333ZM254.18 45.0657C256.612 45.0657 258.422 43.3437 258.422 40.7643C258.422 38.185 256.612 36.419 254.18 36.419C251.747 36.419 249.926 38.1593 249.926 40.7643C249.926 43.3693 251.806 45.0657 254.18 45.0657ZM254.18 35.481C254.881 35.4623 255.579 35.586 256.231 35.8447C256.883 36.1033 257.475 36.4915 257.971 36.9853C258.466 37.4792 258.856 38.0684 259.115 38.7169C259.373 39.3654 259.496 40.0596 259.476 40.757C259.476 43.8969 257.114 46 254.187 46C253.48 46.0186 252.776 45.8961 252.118 45.64C251.459 45.3838 250.859 44.9991 250.352 44.5085C249.845 44.018 249.443 43.4315 249.168 42.7837C248.893 42.1359 248.751 41.4399 248.751 40.7368C248.751 40.0337 248.893 39.3378 249.168 38.69C249.443 38.0422 249.845 37.4557 250.352 36.9651C250.859 36.4746 251.459 36.0899 252.118 35.8337C252.776 35.5776 253.48 35.4551 254.187 35.4737" fill="currentColor"/> </g> <defs> <clipPath id="alc"> <rect width="259.469" height="46" fill="white"/> </clipPath> </defs> </svg><span>ГК АЛИДИ<br>имиджевый фильм к 35-летию</span></div></aside><div class="memo-body"><h1>Спасибо за разговор.</h1><p>Записали главное, чтобы не держать в голове.</p><p>Сейчас вам нужен не сценарий, а понятная сумма: заложить её в бюджет на 2027 год и сравнить подрядчиков на одинаковом объёме. Поэтому до 20 октября пришлём драфт-бюджет на три версии фильма: к 35-летию, партнёрскую и для HH.ru. Русский язык, съёмки на всех площадках, озвучка, графика, музыка. Если по дороге понадобится что-то сверх этого, например переводы, посчитаем отдельно и скажем заранее.</p><blockquote>«Питер… это в целом красивая картинка, которую можно показать»<cite>из разговора 7 октября</cite></blockquote><p>Петербург добавляем, для партнёрской версии он сильный. Казань посчитаем отдельной строкой, решите, когда увидите цифры.</p><p>Форма, порядок в кадре и логотипы на вашей стороне, мы подстроимся под дни с меньшей нагрузкой. Без киношного грима, договорились. Как мы снимаем руководителей и сотрудников в обычной рабочей обстановке, покажем на примерах.</p><p class="sign">Александр Народецкий<br><span>Hand Marketing</span></p></div></div><div class="wrap"><div class="proto"><div class="proto-h"><h2>Договорились</h2><p class="mono dim">обновляем здесь по мере движения</p></div><table><thead><tr><th>Что</th><th>Кто</th><th>Когда</th></tr></thead><tbody><tr class="hot"><td>Драфт-бюджет: три версии, русский язык, все площадки</td><td>Hand Marketing</td><td class="dt">20 октября</td></tr><tr class=""><td>Таблица фактов и цифр для заполнения</td><td>Hand Marketing</td><td class="dt">вместе с бюджетом</td></tr><tr class="done"><td>Примеры: как снимаем руководителей и сотрудников, и кино для сравнения <a href="#how">на этой странице ↓</a></td><td>Hand Marketing</td><td class="dt">✓ готово</td></tr><tr class="done"><td>Петербург в брифе <a href="#geo2">на этой странице ↓</a></td><td>АЛИДИ</td><td class="dt">✓ готово</td></tr><tr class=""><td>Список логотипов, которые можно показывать</td><td>АЛИДИ</td><td class="dt">до съёмок</td></tr><tr class=""><td>Брендбук и гайды</td><td>АЛИДИ</td><td class="dt">до сценария</td></tr><tr class=""><td>Даты съёмок по загрузке складов</td><td>вместе</td><td class="dt">после выбора идеи</td></tr></tbody></table></div></div></section>
<section class="sb" id="sb"><div class="wrap"><div class="sb-in"><div><p class="mono dim">проверка службой безопасности</p><h3>Документы на tender.alidi.ru</h3></div><ul><li class="ok"><span>Регистрация на tender.alidi.ru</span><b class="mono">✓ готово</b></li><li class="ok"><span>Учредительные документы</span><b class="mono">✓ загружены</b></li><li class="wip"><span>Бухгалтерские документы</span><b class="mono">в работе</b></li></ul></div></div></section>
<section class="route" id="geo2"><div class="wrap"><div class="route-h"><h2>От Калининграда<br>до Алматы.</h2><p>Снимаем шесть городов, остальные филиалы показываем на карте стоками и архивом. Москва без командировок, в смете отдельно Петербург, Нижний, Минск, Алматы и, по желанию, Казань.</p></div><div class="route-map"><svg class="geo2 hz" viewBox="0 0 820 190" role="img" aria-label="Съёмки с запада на восток"><line class="ln" x1="40" y1="95" x2="640" y2="95"/><path class="ln br" d="M640,95 l10,-10 l12,20 l12,-20 l12,20 l10,-10"/><line class="ln" x1="696" y1="95" x2="780" y2="95"/><text class="km" x="674" y="71" text-anchor="middle">≈3 000 км</text><g class="g2 g2-stock"><circle cx="40" cy="95" r="17" class="hl"/><path d="M31,101.3 L40,86 L49,101.3z"/><text x="40" y="57" text-anchor="middle"><tspan class="nm">Калининград</tspan><tspan class="sb" x="40" dy="16">стоки и архив</tspan></text></g><g class="g2 g2-shoot"><circle cx="152" cy="95" r="17" class="hl"/><path d="M143,101.3 L152,86 L161,101.3z"/><text x="152" y="135" text-anchor="middle"><tspan class="nm">Минск</tspan><tspan class="sb" x="152" dy="16">склад и офис</tspan></text></g><g class="g2 g2-new"><circle cx="264" cy="95" r="17" class="hl"/><path d="M255,101.3 L264,86 L273,101.3z"/><text x="264" y="57" text-anchor="middle"><tspan class="nm">Санкт-Петербург</tspan><tspan class="sb" x="264" dy="16">добавили 7 октября</tspan></text></g><g class="g2 g2-shoot"><circle cx="376" cy="95" r="17" class="hl"/><path d="M367,101.3 L376,86 L385,101.3z"/><text x="376" y="135" text-anchor="middle"><tspan class="nm">Москва</tspan><tspan class="sb" x="376" dy="16">офис и Валищево</tspan></text></g><g class="g2 g2-flag"><circle cx="488" cy="95" r="19" class="hl"/><path d="M477,102.7 L488,84 L499,102.7z"/><text x="488" y="57" text-anchor="middle"><tspan class="nm">Нижний Новгород</tspan><tspan class="sb" x="488" dy="16">отсюда с 1992 года</tspan></text></g><g class="g2 g2-option"><circle cx="600" cy="95" r="17" class="hl"/><path d="M591,101.3 L600,86 L609,101.3z"/><text x="600" y="135" text-anchor="middle"><tspan class="nm">Казань</tspan><tspan class="sb" x="600" dy="16">отдельной строкой</tspan></text></g><g class="g2 g2-shoot"><circle cx="780" cy="95" r="17" class="hl"/><path d="M771,101.3 L780,86 L789,101.3z"/><text x="780" y="57" text-anchor="middle"><tspan class="nm">Алматы</tspan><tspan class="sb" x="780" dy="16">склад и офис</tspan></text></g></svg><svg class="geo2 vt" viewBox="0 0 320 470" role="img" aria-label="Съёмки с запада на восток"><line class="ln" x1="40" y1="30" x2="40" y2="364"/><path class="ln br" d="M40,364 l-9,8 l18,10 l-18,10 l9,8"/><line class="ln" x1="40" y1="400" x2="40" y2="450"/><text class="km" x="64" y="386">≈3 000 км</text><g class="g2 g2-stock"><circle cx="40" cy="30" r="17" class="hl"/><path d="M31,36.3 L40,21 L49,36.3z"/><text x="66" y="28"><tspan class="nm">Калининград</tspan><tspan class="sb" x="66" dy="16">стоки и архив</tspan></text></g><g class="g2 g2-shoot"><circle cx="40" cy="92" r="17" class="hl"/><path d="M31,98.3 L40,83 L49,98.3z"/><text x="66" y="90"><tspan class="nm">Минск</tspan><tspan class="sb" x="66" dy="16">склад и офис</tspan></text></g><g class="g2 g2-new"><circle cx="40" cy="154" r="17" class="hl"/><path d="M31,160.3 L40,145 L49,160.3z"/><text x="66" y="152"><tspan class="nm">Санкт-Петербург</tspan><tspan class="sb" x="66" dy="16">добавили 7 октября</tspan></text></g><g class="g2 g2-shoot"><circle cx="40" cy="216" r="17" class="hl"/><path d="M31,222.3 L40,207 L49,222.3z"/><text x="66" y="214"><tspan class="nm">Москва</tspan><tspan class="sb" x="66" dy="16">офис и Валищево</tspan></text></g><g class="g2 g2-flag"><circle cx="40" cy="278" r="19" class="hl"/><path d="M29,285.7 L40,267 L51,285.7z"/><text x="66" y="276"><tspan class="nm">Нижний Новгород</tspan><tspan class="sb" x="66" dy="16">отсюда с 1992 года</tspan></text></g><g class="g2 g2-option"><circle cx="40" cy="340" r="17" class="hl"/><path d="M31,346.3 L40,331 L49,346.3z"/><text x="66" y="338"><tspan class="nm">Казань</tspan><tspan class="sb" x="66" dy="16">отдельной строкой</tspan></text></g><g class="g2 g2-shoot"><circle cx="40" cy="450" r="17" class="hl"/><path d="M31,456.3 L40,441 L49,456.3z"/><text x="66" y="448"><tspan class="nm">Алматы</tspan><tspan class="sb" x="66" dy="16">склад и офис</tspan></text></g></svg></div></div></section>
<section class="maps" id="maps"><div class="wrap"><div class="ideas-h"><h2>Карта в фильме.</h2><p>Так мы уже показывали масштаб в роликах: плоско, на глобусе и в 3D.</p></div><div class="mp-grid"><figure class="mp"><video class="mp-v" muted loop playsinline preload="none" poster="img/map-rzd.jpg" data-src="img/map-rzd.mp4" aria-hidden="true"></video><figcaption><b>ЦМ РЖД</b><span>Сеть терминалов прорастает с запада на восток, от Калининграда до Находки.</span><a href="https://hand-marketing.ru/video/rgd/history/" target="_blank" rel="noopener">страница кейса ↗</a></figcaption></figure><figure class="mp"><video class="mp-v" muted loop playsinline preload="none" poster="img/map-iso.jpg" data-src="img/map-iso.mp4" aria-hidden="true"></video><figcaption><b>«Изотек»</b><span>Города присутствия по одному загораются на карте России.</span><a href="https://hand-marketing.ru/isotec/" target="_blank" rel="noopener">страница кейса ↗</a></figcaption></figure><figure class="mp"><video class="mp-v" muted loop playsinline preload="none" poster="img/map-zub.jpg" data-src="img/map-zub.mp4" aria-hidden="true"></video><figcaption><b>Технопарк «Зубово»</b><span>Регион на карте страны, затем подъезды к площадке: аэропорт, станция, трасса.</span><a href="https://hand-marketing.ru/zubovo/" target="_blank" rel="noopener">страница кейса ↗</a></figcaption></figure><figure class="mp"><video class="mp-v" muted loop playsinline preload="none" poster="img/map-bek.jpg" data-src="img/map-bek.mp4" aria-hidden="true"></video><figcaption><b>Технопарк «Бекабад»</b><span>Страна на карте мира и торговые коридоры во все стороны.</span><a href="https://hand-marketing.ru/bekobod1/" target="_blank" rel="noopener">страница кейса ↗</a></figcaption></figure><figure class="mp"><video class="mp-v" muted loop playsinline preload="none" poster="img/map-silk.jpg" data-src="img/map-silk.mp4" aria-hidden="true"></video><figcaption><b>Silk Way Rally · 3D</b><span>Глобус приближается к городу старта, этап поднимается рельефом по координатам маршрута.</span><a href="https://hand-marketing.ru/video/silkway/" target="_blank" rel="noopener">страница кейса ↗</a></figcaption></figure><div class="mp-for"><p class="mono dim">для АЛИДИ</p><h3>Россия, Беларусь и Казахстан на одной карте</h3><p>Точки всплывают от Калининграда до Алматы, на каждую короткий кадр с площадки. Шесть городов снимаем, остальные филиалы даём стоками и архивом. Стиль карты подбираем под ваш брендбук.</p></div></div></div></section>
<section class="ideas" id="ideas"><div class="wrap"><div class="ideas-h"><h2>Пять идей.</h2><p>Выбираем две, обе доводим до сценария. Из одних съёмок собираем три версии.</p></div><ol class="ideas-l"><li><span class="mono dim">01</span><div><h3>Сутки без остановки</h3><p>Один рабочий день компании: начинается в 05:52 в Алматы, заканчивается ночной сменой. Солнце идёт с востока на запад вместе с фильмом, у каждого города свой час, между городами переходим через ворота склада. Время в титре всегда настоящее.</p></div><p class="ifin">«Обычный день АЛИДИ. 12&nbsp;783-й подряд.»</p></li><li><span class="mono dim">02</span><div><h3>Год приёма</h3><p>Историю рассказывают сотрудники, каждый называет год, когда пришёл. Люди выстроены по годам от самых первых до пришедших в 2027-м, и через их места работы видно, как росла компания. Без хроники и диктора.</p></div><p class="ifin">Финал: самый опытный и самый новый встают рядом, за ними все герои.</p></li><li><span class="mono dim">03</span><div><h3>Невидимый партнёр</h3><p>От полки в магазине назад по цепочке: склад, заказ, приёмка. Фильм начинается с обычного утра покупателя и показывает, сколько людей и решений стоит за одним товаром. Сроки «за 2 часа», «за 9 часов» берём настоящие.</p></div><p class="ifin">«Ни на одной полке нет нашего логотипа. На каждой есть наша работа.»</p></li><li><span class="mono dim">04</span><div><h3>Одна минута</h3><p>Одно и то же движение в пяти городах: стандарт один везде. Коробку берут в Алматы, сканируют в Минске, ставят на паллет в Нижнем, а склейка получается только потому, что процессы действительно одинаковые.</p></div><p class="ifin">«Пять городов. Одна компания.»</p></li><li><span class="mono dim">05</span><div><h3>Та же точка, 35 лет спустя</h3><p>Архивное фото в руке на фоне того же места сегодня. Так проходим вехи от первого здания в Нижнем Новгороде до сегодняшних площадок в трёх странах, рассказывает голос человека, который всё это видел.</p></div><p class="ifin">«Тогда хватало одного кадра. Сегодня нужны три страны.»</p></li></ol><div class="vers"><div><b>К 35-летию</b><span class="mono">4–5 минут</span><p>большой экран, со звуком</p></div><div><b>Партнёрская</b><span class="mono">2:30–3:00</span><p>переговоры и тендеры по контрактам</p></div><div><b>Для HH.ru</b><span class="mono">60–90 секунд</span><p>телефон, вертикаль, без звука</p></div></div></div></section>
<section class="how" id="how"><div class="wrap"><div class="ideas-h"><h2>Как снимаем.</h2><p>Шесть примеров: на что смотреть и к какой версии вашего фильма это относится.</p></div><div class="ex"><div class="ex-t"><p class="mono dim">01 · руководители</p><h3>Интервью топ-менеджеров</h3><p>Saint-Gobain, фильм «Клиентский опыт». Руководителей снимали на трёх площадках: две локации в Москве и завод. Снимали между их встречами, свет и звук наши, профессионального грима нет.</p><p class="ex-for">В вашем фильме: Иван Сычёв и руководители направлений, во всех трёх версиях.</p><p class="ex-note">Руководителей из Казахстана и Беларуси в этом фильме мы не снимали: компания прислала их записи отдельно, поэтому в пример их не берём.</p><a class="ex-link" href="https://hand-marketing.ru/video/saintgobain/cx/" target="_blank" rel="noopener">страница кейса ↗</a></div><div class="ex-v"><video id="v-tops" controls preload="none" playsinline poster="img/sg-tops.jpg" src="https://hand-marketing.ru/media/sg-cx-part2.mp4#t=7"></video><p class="mono dim tp-h">выберите, с кого начать</p><div class="tps"><button type="button" class="tp" data-p="v-tops" data-t="7.2"><img src="/images/sgcx/sp-02@280.jpg" alt="" loading="lazy"><b>Маргарита Молодых</b><span>директор бизнес-подразделения</span></button><button type="button" class="tp" data-p="v-tops" data-t="19.2"><img src="/images/sgcx/sp-03@280.jpg" alt="" loading="lazy"><b>Рафаэль Зохрабян</b><span>генеральный директор</span></button><button type="button" class="tp" data-p="v-tops" data-t="28.8"><img src="/images/sgcx/sp-04@280.jpg" alt="" loading="lazy"><b>Артём Гаврилюк</b><span>директор по продажам</span></button><button type="button" class="tp" data-p="v-tops" data-t="36.0"><img src="/images/sgcx/sp-05@280.jpg" alt="" loading="lazy"><b>Елена Сильвестрова</b><span>директор по персоналу</span></button><button type="button" class="tp" data-p="v-tops" data-t="45.6"><img src="/images/sgcx/sp-06@280.jpg" alt="" loading="lazy"><b>Андрей Зарипов</b><span>индустриальный директор</span></button><button type="button" class="tp" data-p="v-tops" data-t="55.2"><img src="/images/sgcx/sp-07@280.jpg" alt="" loading="lazy"><b>Ирина Кочкина</b><span>директор по закупкам</span></button><button type="button" class="tp" data-p="v-tops" data-t="64.8"><img src="/images/sgcx/sp-08@280.jpg" alt="" loading="lazy"><b>Марина Ченцова</b><span>директор по логистике</span></button><button type="button" class="tp" data-p="v-tops" data-t="74.4"><img src="/images/sgcx/sp-09@280.jpg" alt="" loading="lazy"><b>Елена Радченко</b><span>финансовый директор</span></button><button type="button" class="tp" data-p="v-tops" data-t="108.0"><img src="/images/sgcx/sp-12@280.jpg" alt="" loading="lazy"><b>Тимур Сагиров</b><span>директор по IT</span></button><button type="button" class="tp" data-p="v-tops" data-t="122.4"><img src="/images/sgcx/sp-13@280.jpg" alt="" loading="lazy"><b>Юлия Ночёвина</b><span>директор по маркетингу</span></button></div></div></div><div class="ex"><div class="ex-t"><p class="mono dim">02 · сотрудники</p><h3>Путь клиента через всю компанию</h3><p>Тот же фильм, первая часть: один заказ проходит от рекламы до готового дома. В кадре 48 сотрудников на своих местах, каждый подписан по имени. Офис в Москве и два завода в Егорьевске.</p><p class="ex-for">В вашем фильме: склады, офисы и люди в «Сутках», «Годе приёма», HR-версии.</p><a class="ex-link" href="https://hand-marketing.ru/video/saintgobain/cx/" target="_blank" rel="noopener">страница кейса ↗</a></div><div class="ex-v"><video id="v-path" controls preload="none" playsinline poster="/images/sgcx/hero-poster.jpg" src="https://hand-marketing.ru/media/sg-cx-part1.mp4"></video><div class="pcs"><button type="button" class="pc" data-p="v-path" data-t="37.2"><img src="/images/sgcx/sc-road@560.jpg" alt="" loading="lazy"><span>реклама и выбор</span></button><button type="button" class="pc" data-p="v-path" data-t="142.4"><img src="/images/sgcx/sc-gyproc-yard@560.jpg" alt="" loading="lazy"><span>завод</span></button><button type="button" class="pc" data-p="v-path" data-t="196.2"><img src="/images/sgcx/sc-isover-belt@560.jpg" alt="" loading="lazy"><span>линия</span></button><button type="button" class="pc" data-p="v-path" data-t="221.4"><img src="/images/sgcx/sc-pallets@560.jpg" alt="" loading="lazy"><span>склад и отгрузка</span></button><button type="button" class="pc" data-p="v-path" data-t="232.0"><img src="/images/sgcx/sc-mounting@560.jpg" alt="" loading="lazy"><span>монтаж</span></button><button type="button" class="pc" data-p="v-path" data-t="409.5"><img src="/images/sgcx/sc-clients-final@560.jpg" alt="" loading="lazy"><span>финал</span></button></div></div></div><div class="ex"><div class="ex-t"><p class="mono dim">03 · масштаб</p><h3>Вся компания и много площадок в одном фильме</h3><p>Power Technologies на чемпионате мира 2018: 11 городов, 12 стадионов, месяц съёмок мобильными группами. Объекты, работа смен, руководители и инфографика собраны в один рассказ о масштабе.</p><p class="ex-for">В вашем фильме: шесть городов в трёх странах, партнёрская версия.</p><a class="ex-link" href="https://hand-marketing.ru/video/powertechnologies/" target="_blank" rel="noopener">страница кейса ↗</a></div><div class="ex-v"><video id="v-pt" controls preload="none" playsinline poster="/images/powertech/poster-short.jpg" src="https://hand-marketing.ru/media/pt-film-short.mp4"></video><div class="pcs"><button type="button" class="pc" data-p="v-pt" data-t="37.0"><img src="/images/powertech/poster-short.jpg" alt="" loading="lazy"><span>Лужники</span></button><button type="button" class="pc" data-p="v-pt" data-t="66.0"><img src="/images/powertech/obj-match.jpg" alt="" loading="lazy"><span>матч</span></button><button type="button" class="pc" data-p="v-pt" data-t="78.0"><img src="/images/powertech/nums-a.jpg" alt="" loading="lazy"><span>цифры</span></button><button type="button" class="pc" data-p="v-pt" data-t="112.0"><img src="/images/powertech/shoot-fence.jpg" alt="" loading="lazy"><span>обход площадки</span></button><button type="button" class="pc" data-p="v-pt" data-t="165.0"><img src="/images/powertech/shoot-cables.jpg" alt="" loading="lazy"><span>кабельные трассы</span></button><button type="button" class="pc" data-p="v-pt" data-t="225.0"><img src="/images/powertech/shoot-gen.jpg" alt="" loading="lazy"><span>генератор и кран</span></button></div></div></div><div class="ex"><div class="ex-t"><p class="mono dim">04 · история</p><h3>Годы компании в одном ролике</h3><p>Бренд-фильм «Изотек»: двенадцать лет направления, девять вех от 2012 до 2024, каждая вынесена в графику поверх живых кадров производства. Дальше география и итоги в цифрах.</p><p class="ex-for">В вашем фильме: 35 лет от 1992 года, идеи «Та же точка» и «Год приёма».</p><a class="ex-link" href="https://hand-marketing.ru/isotec/" target="_blank" rel="noopener">страница кейса ↗</a></div><div class="ex-v"><video id="v-iso" controls preload="none" playsinline poster="/images/isotec/poster.jpg" src="https://hand-marketing.ru/media/izotek-brand-video.mp4"></video><div class="pcs"><button type="button" class="pc yr" data-p="v-iso" data-t="20"><img src="/images/isotec/tl-1.jpg" alt="" loading="lazy"><span class="mono">2012</span></button><button type="button" class="pc yr" data-p="v-iso" data-t="49"><img src="/images/isotec/tl-3.jpg" alt="" loading="lazy"><span class="mono">2014</span></button><button type="button" class="pc yr" data-p="v-iso" data-t="71"><img src="/images/isotec/tl-5.jpg" alt="" loading="lazy"><span class="mono">2018</span></button><button type="button" class="pc yr" data-p="v-iso" data-t="94"><img src="/images/isotec/tl-7.jpg" alt="" loading="lazy"><span class="mono">2022</span></button><button type="button" class="pc yr" data-p="v-iso" data-t="101"><img src="/images/isotec/tl-8.jpg" alt="" loading="lazy"><span class="mono">2023</span></button><button type="button" class="pc yr" data-p="v-iso" data-t="115"><img src="/images/isotec/tl-9.jpg" alt="" loading="lazy"><span class="mono">2024</span></button></div></div></div><div class="ex"><div class="ex-t"><p class="mono dim">05 · всё вместе</p><h3>История, объект и интервью в одном фильме</h3><p>ТРЦ «Павелецкая Плаза» для MMG, 5:37. Архив Павелецкой площади и та же площадь в проекте, рендеры комплекса, карта зоны охвата и цифры, интервью экспертов и арендаторов: «Эконика», «Теремок».</p><p class="ex-for">В вашем фильме: история с 1992 года, площадки сегодня и голоса руководителей вместе, партнёрская версия и версия к 35-летию.</p><a class="ex-link" href="https://hand-marketing.ru/mmg/" target="_blank" rel="noopener">страница кейса ↗</a></div><div class="ex-v"><video id="v-mmg" controls preload="none" playsinline poster="/images/mmg/poster.jpg" src="https://hand-marketing.ru/media/mmg-paveleckayaplaza.mp4"></video><div class="pcs"><button type="button" class="pc" data-p="v-mmg" data-t="14.5"><img src="/images/mmg/ren-2.jpg" alt="" loading="lazy"><span>объект</span></button><button type="button" class="pc" data-p="v-mmg" data-t="27.0"><img src="/images/mmg/hist-1.jpg" alt="" loading="lazy"><span>история</span></button><button type="button" class="pc" data-p="v-mmg" data-t="38.0"><img src="/images/mmg/was.jpg" alt="" loading="lazy"><span>было и будет</span></button><button type="button" class="pc" data-p="v-mmg" data-t="84.0"><img src="/images/mmg/ex-1.jpg" alt="" loading="lazy"><span>эксперт</span></button><button type="button" class="pc" data-p="v-mmg" data-t="118.5"><img src="/images/mmg/num-2.jpg" alt="" loading="lazy"><span>цифры</span></button><button type="button" class="pc" data-p="v-mmg" data-t="262.0"><img src="/images/mmg/ex-2.jpg" alt="" loading="lazy"><span>арендаторы</span></button></div></div></div><div class="ex ex-cine"><div class="ex-t"><p class="mono dim">06 · для сравнения</p><h3>Кинематографичный уровень</h3><p>Грим, постановочный свет, актёры, раскадровка каждого плана. Для корпоративного фильма в таком объёме это не нужно, показываем, чтобы было с чем сравнить уровни в бюджете.</p></div><div class="cines"><div class="cn"><div class="vid0"><video controls preload="none" playsinline poster="/images/vivax/rest-smile.jpg" src="https://hand-marketing.ru/media/vivax-samburskaya.mp4"></video></div><b>VIVAX SPORT</b><span>реклама с Настасьей Самбурской, 49 с</span><a class="ex-link" href="https://hand-marketing.ru/video/vivax/" target="_blank" rel="noopener">страница кейса ↗</a></div><div class="cn"><div class="vid0"><video controls preload="none" playsinline poster="/images/gaz/poster.jpg" src="https://hand-marketing.ru/media/gazelle-transformer.mp4"></video></div><b>Газель-трансформер</b><span>вирусный ролик для Eaton, 1:42</span><a class="ex-link" href="https://hand-marketing.ru/video/gaz/" target="_blank" rel="noopener">страница кейса ↗</a></div><div class="cn"><div class="vid0"><video controls preload="none" playsinline poster="/images/patriot/poster.jpg" src="https://hand-marketing.ru/media/eaton-yaz.mp4"></video></div><b>УАЗ Патриот</b><span>рекламный ролик для Eaton, 60 с</span><a class="ex-link" href="https://hand-marketing.ru/video/patriot/" target="_blank" rel="noopener">страница кейса ↗</a></div></div></div></div></section>
<section class="more" id="more"><div class="wrap"><div class="more-h"><h2>Готовы участвовать и в других проектах.</h2><p>Не только фильм. То, что мы делаем давно и хорошо.</p></div><div class="more-g"><div class="mc"><h3>Выставочные стенды</h3><p>Строим под ключ, но главное в другом: нестандартную мультимедиа и контент закладываем ещё на этапе проекта, а не добавляем на монтаже.</p><ul><li><a href="https://hand-marketing.ru/portfolio/samara-stand-vdnh/" target="_blank" rel="noopener"><img class="" src="/images/lib/custom-samara-vdnh/cover-main.png" alt="" loading="lazy"><span>Самара на ВДНХ</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/portfolio/stavropol-stand-vdnh/" target="_blank" rel="noopener"><img class="" src="/images/lib/custom-stavropol-vdnh/cover-main.png" alt="" loading="lazy"><span>Ставрополье на ВДНХ</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/exhibition/dizayn-stenda/" target="_blank" rel="noopener"><img class="ph" src="/images/exhibition/samara/render-v1-a.jpg" alt="" loading="lazy"><span>Как разрабатываем: проект стенда Самары, 204 м², 79 листов</span><i>↗</i></a></li></ul></div><div class="mc"><h3>События</h3><p>Наше основное направление с открытия агентства. Одна идея проходит через всё мероприятие: приглашение, площадку, сцену, экраны и подарки.</p><ul><li><a href="https://hand-marketing.ru/event/riviera/" target="_blank" rel="noopener"><img class="" src="/images/lib/as3062-3363-4134-b333-623232303134/__-22.png" alt="" loading="lazy"><span>«Внутри стихии», ТРЦ Ривьера</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/event/samsung/" target="_blank" rel="noopener"><img class="" src="/images/lib/as3466-3261-4738-b938-303637303133/__-18.png" alt="" loading="lazy"><span>Новый год Samsung</span><i>↗</i></a></li></ul></div><div class="mc"><h3>Контент и медианосители</h3><p>Контент для мероприятий и выставок под конкретную площадку: проекции на здание и автомобиль, изогнутые и кинетические экраны, интерактив, песочные столы.</p><ul><li><a href="https://hand-marketing.ru/3d/stavropol/" target="_blank" rel="noopener"><img class="" src="/images/lib/as6466-3635-4534-b432-353364376364/__-01.png" alt="" loading="lazy"><span>3D mapping на здании, Ставрополь</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/event/changan/" target="_blank" rel="noopener"><img class="" src="/images/lib/as3635-3436-4663-b265-633363383261/__-98.png" alt="" loading="lazy"><span>Mapping на кузове Changan CS35</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/portfolio/samara-exhibition/" target="_blank" rel="noopener"><img class="" src="/images/lib/custom-samara-exhibition/cover-main.png" alt="" loading="lazy"><span>Интерактив с Kinect, музей Алабина</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/video/silkway/" target="_blank" rel="noopener"><img class="" src="/images/lib/as6164-6432-4132-a361-613136626438/__-51.png" alt="" loading="lazy"><span>3D-маршрут и песочный стол, Silk Way</span><i>↗</i></a></li></ul></div><div class="mc"><h3>Дизайн</h3><p>Своя креативная студия: айдентика, полиграфия, упаковка и сувенирная продукция.</p><ul><li><a href="https://hand-marketing.ru/creative/metra/" target="_blank" rel="noopener"><img class="" src="/images/lib/custom-metra/cover-main.png" alt="" loading="lazy"><span>Брендбук Metra</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/creative/saintgobain/suitcase/" target="_blank" rel="noopener"><img class="" src="/images/lib/as3734-3562-4636-a636-633764353537/__-41.png" alt="" loading="lazy"><span>Чемодан Saint-Gobain</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/creative/becar/sdep/" target="_blank" rel="noopener"><img class="" src="/images/lib/as6366-6163-4338-b039-373730386163/__-74.png" alt="" loading="lazy"><span>Стиль отдела продаж Becar</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/creative/becar/vertical/" target="_blank" rel="noopener"><img class="" src="/images/lib/as6633-6662-4561-b364-303861353166/__-64.png" alt="" loading="lazy"><span>Брошюра Vertical, 24 полосы</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/creative/saintgobain/calendar/" target="_blank" rel="noopener"><img class="" src="/images/lib/custom-sgcalendar/cover-main.png" alt="" loading="lazy"><span>Календарь Saint-Gobain: креативная концепция</span><i>↗</i></a></li><li><a href="https://hand-marketing.ru/creative/rgd/suvenir/" target="_blank" rel="noopener"><img class="" src="/images/lib/as3634-3861-4239-b237-356636663535/__-60.png" alt="" loading="lazy"><span>Новогодний набор ЦМ РЖД</span><i>↗</i></a></li></ul></div></div></div></section>
<section class="arch-bar" id="archive-open"><div class="wrap arch-in"><div><p class="eyebrow"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg>Материалы от 1 октября</p><h3>Наши работы и как мы их снимали</h3><p>Кейсы, фильмы, отзывы и всё, что мы показывали до встречи. <a class="pdf-btn" href="?pdf=portfolio">Портфолио в PDF</a></p></div><button class="btn ghost-d" type="button" id="arch-btn" aria-expanded="false" aria-controls="archive">Посмотреть</button></div></section><div id="archive" hidden>
<section class="hero" id="hero"><video class="hero-bg" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="auto" poster="img/hero-loop.jpg" aria-hidden="true" tabindex="-1"><source src="img/hero-loop.mp4" type="video/mp4"></video><div class="wrap"><p class="eyebrow light"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg>ГК АЛИДИ · имиджевый фильм к 35-летию</p><h1>Наши работы<br>и как мы их снимали.</h1><p class="lead">Корпоративные и имиджевые фильмы, съёмки на заводах, складах и терминалах, серии роликов, графика. Каждый проект со ссылкой на страницу кейса с видео.</p><div class="hero-cta"><a class="btn" href="#match">Что из задачи мы уже снимали</a></div><div class="clock" id="clock"><div class="clock-n"><b id="days">330</b><span>дней до 35-летия АЛИДИ<br>26 августа 2027</span></div><div class="line" aria-hidden="true"><i class="now" id="now"></i><span class="mk" style="--p:0%"><b>сегодня</b></span><span class="mk" data-d="2027-02-01"><b>1 февраля</b>старт съёмок</span><span class="mk blue" data-d="2027-07-26"><b>26 июля</b>сдача фильма</span><span class="mk end" data-d="2027-08-26"><b>26 августа</b>юбилей</span></div></div><p class="sign">ООО «Хэнд-маркетинг» · с 2012 года · hand-marketing.ru</p></div></section>
<section class="sec" id="tz"><div class="wrap"><p class="eyebrow"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>01</b> Задача</p><h2>Как мы прочитали ТЗ.</h2><div class="tz">
<div class="tz-c"><b class="n">2</b><span class="cap">версии фильма</span><p>Презентационная 2:30-3:00 и мини-фильм 4:00-5:00. Горизонталь для зала, ТВ и ПК.</p></div>
<div class="tz-c"><b class="n">5</b><span class="cap">съёмочных площадок</span><p>Москва, Валищево, Нижний Новгород, Минск, Алматы. Офисы и склады.</p></div>
<div class="tz-c"><b class="n">3</b><span class="cap">страны в смете</span><p>Организация съёмок в РФ, РБ и РК отдельными разделами, как просит ТЗ.</p></div>
<div class="tz-c"><b class="n">2</b><span class="cap">концепции на старте</span><p>Два сценария на выбор, дальше детальная доработка выбранного.</p></div>
<div class="tz-c"><b class="n">3</b><span class="cap">круга правок</span><p>Включены в стоимость. Под ключ: идея, сценарий, съёмки, дизайн, озвучка, монтаж.</p></div>
<div class="tz-c"><b class="n">26.07</b><span class="cap">2027, сдача</span><p>Обе версии согласованы. Старт съёмок 1 февраля 2027 года.</p></div>
</div><div class="note"><b>Сверили даты с alidi.ru.</b> Компания основана в 1992 году, 34 года исполнилось 26 августа 2026. Значит, 35 лет будет 26 августа 2027, и сдача 26 июля ложится ровно за месяц до юбилея. В ТЗ указан август 2026, это стоит поправить до сценария.</div><div class="geo"><div class="geo-t"><h3>Пять площадок, три страны, одна съёмочная группа</h3><p>Фильм в трёх странах собираем с одним режиссёром и оператором-постановщиком на всех площадках, чтобы Минск, Алматы и Валищево выглядели как одна компания.</p><ul class="geo-l"><li><i class="c-rf"></i>РФ · 3 площадки</li><li><i class="c-rb"></i>РБ · Минск</li><li><i class="c-rk"></i>РК · Алматы</li></ul></div><div class="geo-m"><svg class="geo-svg" viewBox="0 0 680 330" role="img" aria-label="Пять съёмочных площадок: Москва, Валищево, Нижний Новгород, Минск, Алматы"><line class="mer" x1="105.0" y1="18" x2="105.0" y2="312"/><text class="deg" x="109.0" y="314">30°</text><line class="mer" x1="217.5" y1="18" x2="217.5" y2="312"/><text class="deg" x="221.5" y="314">40°</text><line class="mer" x1="330.0" y1="18" x2="330.0" y2="312"/><text class="deg" x="334.0" y="314">50°</text><line class="mer" x1="442.5" y1="18" x2="442.5" y2="312"/><text class="deg" x="446.5" y="314">60°</text><line class="mer" x1="554.9" y1="18" x2="554.9" y2="312"/><text class="deg" x="558.9" y="314">70°</text><line class="mer" x1="20" y1="267.5" x2="660" y2="267.5"/><text class="deg" x="22" y="263.5">45°</text><line class="mer" x1="20" y1="180.0" x2="660" y2="180.0"/><text class="deg" x="22" y="176.0">50°</text><line class="mer" x1="20" y1="92.5" x2="660" y2="92.5"/><text class="deg" x="22" y="88.5">55°</text><path class="route" style="--d:0.0s" d="M190.7,79.4 Q134.1,39.8 77.5,111.8"/><path class="route" style="--d:0.7s" d="M190.7,79.4 Q220.7,83.1 189.1,86.7"/><path class="route" style="--d:1.0499999999999998s" d="M190.7,79.4 Q226.6,34.6 262.5,69.2"/><path class="route" style="--d:1.4s" d="M190.7,79.4 Q411.9,0.3 633.1,298.3"/><g class="pt pt-РБ" style="--d:0.4s"><circle class="halo" cx="77.5" cy="111.8" r="11"/><path class="tri-pt" d="M70.5,116.8 L77.5,104.8 L84.5,116.8z"/><text x="77.5" y="141.8" text-anchor="middle"><tspan class="nm">Минск</tspan><tspan class="cc" x="77.5" dy="15">РБ · офис и склад</tspan></text></g><g class="pt pt-РФ" style="--d:0.75s"><circle class="halo" cx="190.7" cy="79.4" r="11"/><path class="tri-pt" d="M183.7,84.4 L190.7,72.4 L197.7,84.4z"/><text x="176.7" y="45.400000000000006" text-anchor="end"><tspan class="nm">Москва</tspan><tspan class="cc" x="176.7" dy="15">РФ · головной офис</tspan></text></g><g class="pt pt-РФ" style="--d:1.1s"><circle class="halo" cx="189.1" cy="86.7" r="11"/><path class="tri-pt" d="M182.1,91.7 L189.1,79.7 L196.1,91.7z"/><text x="203.1" y="116.7" text-anchor="start"><tspan class="nm">Валищево</tspan><tspan class="cc" x="203.1" dy="15">РФ · складской комплекс</tspan></text></g><g class="pt pt-РФ" style="--d:1.4499999999999997s"><circle class="halo" cx="262.5" cy="69.2" r="11"/><path class="tri-pt" d="M255.5,74.2 L262.5,62.2 L269.5,74.2z"/><text x="276.5" y="35.2" text-anchor="start"><tspan class="nm">Нижний Новгород</tspan><tspan class="cc" x="276.5" dy="15">РФ · офис и склад</tspan></text></g><g class="pt pt-РК" style="--d:1.7999999999999998s"><circle class="halo" cx="633.1" cy="298.3" r="11"/><path class="tri-pt" d="M626.1,303.3 L633.1,291.3 L640.1,303.3z"/><text x="633.1" y="272.3" text-anchor="middle"><tspan class="nm">Алматы</tspan><tspan class="cc" x="633.1" dy="15">РК · офис и склад</tspan></text></g></svg></div></div></div></section>
<section class="sec dark" id="match"><div class="wrap"><p class="eyebrow light"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>02</b> Опыт под задачу</p><h2>Что из этой задачи мы уже снимали.</h2><div class="match"><div class="m-list" role="tablist">
<button class="m-row on" type="button" role="tab" aria-selected="true" data-i="0"><span class="m-n">01</span><span class="m-need">Склад, погрузчик, отгрузка, фура в кадре</span></button>
<button class="m-row" type="button" role="tab" aria-selected="false" data-i="1"><span class="m-n">02</span><span class="m-need">Логистическая сеть в разных городах</span></button>
<button class="m-row" type="button" role="tab" aria-selected="false" data-i="2"><span class="m-n">03</span><span class="m-need">Офис и прямая речь руководителей</span></button>
<button class="m-row" type="button" role="tab" aria-selected="false" data-i="3"><span class="m-n">04</span><span class="m-need">История компании по годам</span></button>
<button class="m-row" type="button" role="tab" aria-selected="false" data-i="4"><span class="m-n">05</span><span class="m-need">Две версии одного фильма</span></button>
</div><div class="m-panes">
<div class="m-pane on" role="tabpanel" data-i="0"><div class="m-shots n3"><figure><img src="/images/sgcx/sc-pallets.jpg" alt="" loading="lazy"></figure><figure><img src="/images/sgcx/sc-truck@560.jpg" alt="" loading="lazy"></figure><figure><img src="/images/sgcx/sc-shipping-doc@560.jpg" alt="" loading="lazy"></figure></div><p class="m-need-m">Склад, погрузчик, отгрузка, фура в кадре</p><p>Saint-Gobain «Клиентский опыт»: путь одного заказа через закупку, линию, склад, отгрузку и доставку.</p><a class="m-link" href="https://hand-marketing.ru/video/saintgobain/cx" target="_blank" rel="noopener">hand-marketing.ru/video/saintgobain/cx <span>↗</span></a></div>
<div class="m-pane" role="tabpanel" data-i="1"><div class="m-shots n3"><figure><img src="/images/rgd-history/aero-station.jpg" alt="" loading="lazy"></figure><figure><img src="/images/rgd-history/baltkran.jpg" alt="" loading="lazy"></figure><figure><img src="/images/rgd-history/aero-kal.jpg" alt="" loading="lazy"></figure></div><p class="m-need-m">Логистическая сеть в разных городах</p><p>ЦМ РЖД: три группы параллельно в Москве, Петербурге и Калининграде, грузовые дворы с земли и сверху.</p><a class="m-link" href="https://hand-marketing.ru/video/rgd/history" target="_blank" rel="noopener">hand-marketing.ru/video/rgd/history <span>↗</span></a></div>
<div class="m-pane" role="tabpanel" data-i="2"><div class="m-shots n4"><figure><img src="/images/sgcx/sp-01.jpg" alt="" loading="lazy"></figure><figure><img src="/images/sgcx/sp-06.jpg" alt="" loading="lazy"></figure><figure><img src="/images/sgcx/sp-07.jpg" alt="" loading="lazy"></figure><figure><img src="/images/sgcx/sp-12.jpg" alt="" loading="lazy"></figure></div><p class="m-need-m">Офис и прямая речь руководителей</p><p>Saint-Gobain: 17 интервью руководителей всех направлений, в московском офисе и на заводе. Свет, кадр и вопросы готовили на месте под каждого спикера.</p><a class="m-link" href="https://hand-marketing.ru/video/saintgobain/cx" target="_blank" rel="noopener">hand-marketing.ru/video/saintgobain/cx <span>↗</span></a></div>
<div class="m-pane" role="tabpanel" data-i="3"><div class="m-shots n3"><figure><img src="/images/isotec/map.jpg" alt="" loading="lazy"></figure><figure><img src="/images/isotec/prod-5.jpg" alt="" loading="lazy"></figure><figure><img src="/images/isotec/prod-4.jpg" alt="" loading="lazy"></figure></div><p class="m-need-m">История компании по годам</p><p>Бренд-ролик «Изотек»: 2012-2024, девять вех, шесть площадок, цифры итога в финале.</p><a class="m-link" href="https://hand-marketing.ru/isotec" target="_blank" rel="noopener">hand-marketing.ru/isotec <span>↗</span></a></div>
<div class="m-pane" role="tabpanel" data-i="4"><div class="m-shots n2"><figure><img src="/images/powertech/poster-full.jpg" alt="" loading="lazy"></figure><figure><img src="/images/powertech/poster-short.jpg" alt="" loading="lazy"></figure></div><p class="m-need-m">Две версии одного фильма</p><p>Power Technologies: полная 11:39 для переговоров и короткая 4:27 для соцсетей и стенда.</p><a class="m-link" href="https://hand-marketing.ru/video/powertechnologies" target="_blank" rel="noopener">hand-marketing.ru/video/powertechnologies <span>↗</span></a></div>
</div></div></div></section>
<section class="sec" id="films"><div class="wrap"><p class="eyebrow"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>03</b> Корпоративные и имиджевые фильмы</p><h2>Четыре фильма, ближе всего к вашему.</h2>
<article class="film" id="f-sgcx" style="--c:#5a9a2c"><div class="film-v"><p class="part">Часть 1 · путь клиента</p><button class="vid " type="button" data-video="/media/sg-cx-part1.mp4" aria-label="Смотреть: Saint-Gobain: один заказ через всю компанию, Часть 1 · путь клиента"><img src="/images/sgcx/hero-poster.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><p class="part">Часть 2 · голоса руководителей</p><button class="vid " type="button" data-video="/media/sg-cx-part2.mp4" aria-label="Смотреть: Saint-Gobain: один заказ через всю компанию, Часть 2 · голоса руководителей"><img src="img/sg-leaders.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><p class="accent">Реклама, закупка, линия, склад, отгрузка, фура, монтаж. Без пропусков.</p></div><div class="film-t"><p class="tag">Корпоративный фильм · программа «Клиентский опыт»</p><h3>Saint-Gobain: один заказ через всю компанию</h3><p>Saint-Gobain запускал внутри компании программу «Клиентский опыт» и хотел объяснить каждому сотруднику простую вещь: путь клиента складывается из работы всех подразделений, даже тех, кто клиента ни разу не видит. Первая часть фильма проходит весь путь заказа: реклама, выбор, закупка сырья, планирование, смена на линии, склад, отгрузка, доставка, монтаж и готовый дом. Вторая собирает прямую речь руководителей всех направлений. Две смены в московском офисе, одна смена на двух заводах в Егорьевске. Руководителей из Казахстана и Беларуси сняли отдельно и собрали в общий монтаж.</p><div class="stats n4"><div><b>10 мин</b><span>две части фильма: путь клиента и голоса руководителей</span></div><div><b>17</b><span>интервью, от операционного директора до глав компании в Казахстане и Беларуси</span></div><div><b>48</b><span>сотрудников названы в кадре по имени, на своих рабочих местах</span></div><div><b>3 смены</b><span>офис в Москве и два завода в Егорьевске</span></div></div><a class="case-link" href="https://hand-marketing.ru/video/saintgobain/cx" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></div></article>
<article class="film rev" id="f-rgd" style="--c:#e2661c"><div class="film-v"><button class="vid " type="button" data-video="/media/transrzhd.mp4" aria-label="Смотреть: ЦМ РЖД: терминально-складское хозяйство за 3:54"><img src="/images/rgd-history/poster.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><p class="accent">Грузовой двор, где вагон встречается с автомобилем и складом.</p></div><div class="film-t"><p class="tag">Корпоративный фильм к десятилетию дирекции</p><h3>ЦМ РЖД: терминально-складское хозяйство за 3:54</h3><p>Центральная дирекция по управлению терминально-складским комплексом держит грузовые дворы по всей стране, от Калининграда до Находки. За 3:54 фильм показывает, что это за хозяйство, чем оно занято каждый день и что изменилось за десять лет. Три съёмочные группы вышли параллельно, снимали действующие терминалы с земли и с квадрокоптера, слайды дирекции пересобрали в экранную графику. Итог десяти лет проговаривает начальник дирекции.</p><div class="stats n3"><div><b>3 группы</b><span>параллельно: Москва, Санкт-Петербург, Калининград</span></div><div><b>117</b><span>планов в фильме, средняя длина 2 секунды</span></div><div><b>15</b><span>городов на карте сети терминалов, с запада на восток</span></div></div><a class="case-link" href="https://hand-marketing.ru/video/rgd/history/" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></div></article>
<article class="film" id="f-isotec" style="--c:#9b2a8a"><div class="film-v"><button class="vid " type="button" data-video="/media/izotek-brand-video.mp4" aria-label="Смотреть: «Изотек»: двенадцать лет бренда в одной истории"><img src="/images/isotec/poster.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><p class="accent">От образования направления до криогенной изоляции.</p></div><div class="film-t"><p class="tag">Имиджевый фильм · Saint-Gobain · ISOTEC · 2024</p><h3>«Изотек»: двенадцать лет бренда в одной истории</h3><p>Ролик показывает «Изотек» как живой бренд с историей, а не как поставщика материалов. Работает в двух контурах: для клиентов, партнёров и отраслевых событий и для внутренних коммуникаций и адаптации сотрудников. Структура: пролог, хронология, география, производство, цифровые сервисы, итоги. Съёмки на действующих производственных площадках по регламентам СИЗ.</p><div class="stats n3"><div><b>4:33</b><span>хронометраж фильма</span></div><div><b>9 вех</b><span>2012-2024, каждая вынесена в экранную графику</span></div><div><b>6</b><span>площадок с реальными кадрами производства</span></div></div><a class="case-link" href="https://hand-marketing.ru/isotec/" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></div></article>
<article class="film rev" id="f-pt" style="--c:#1f8a85"><div class="film-v"><button class="vid " type="button" data-video="/media/pt-film-short.mp4" aria-label="Смотреть: Power Technologies: фильм снят, пока шёл проект"><img src="/images/powertech/poster-short.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><p class="accent">Одиннадцать городов, двенадцать стадионов, месяц съёмок.</p></div><div class="film-t"><p class="tag">История успеха · Чемпионат мира по футболу 2018</p><h3>Power Technologies: фильм снят, пока шёл проект</h3><p>Power Technologies обеспечивала временное энергоснабжение всех объектов чемпионата. Мобильные группы (оператор, репортёр, полевой директор, техспециалист) месяц собирали материал в городах: объекты, работу смен, синхроны руководителей проекта и вещателей. По просьбе заказчика фильм собран в двух версиях.</p><div class="stats n3"><div><b>11</b><span>городов от Калининграда до Екатеринбурга и Сочи</span></div><div><b>2 версии</b><span>полная 11:39 для переговоров и короткая 4:27 для соцсетей и стенда</span></div><div><b>12</b><span>стадионов в кадре, плюс вещательный центр и фан-зоны</span></div></div><a class="case-link" href="https://hand-marketing.ru/video/powertechnologies" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></div></article>
</div></section>
<section class="sec faces" id="people"><div class="wrap faces-in"><div class="faces-t"><p class="eyebrow light"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>04</b> Люди в кадре</p><h2>48 сотрудников по имени, на своих местах.</h2><p>Так мы снимали Saint-Gobain: не массовка в коридоре, а кладовщик, водитель, технолог и менеджер, каждый подписан в кадре. Юбилейный фильм АЛИДИ тоже про людей: тысячи сотрудников в трёх странах, и зритель должен узнать в фильме своих коллег.</p><a class="m-link" href="https://hand-marketing.ru/video/saintgobain/cx/" target="_blank" rel="noopener">стена лиц на странице кейса <span>↗</span></a></div><div class="wall" aria-hidden="true"><img src="/images/sgcx/p01@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p02@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p03@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p04@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p05@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p06@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p07@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p08@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p09@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p10@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p11@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p12@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p13@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p14@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p15@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p16@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p17@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p18@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p19@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p20@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p21@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p22@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p23@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p24@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p25@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p26@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p27@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p28@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p29@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p30@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p31@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p32@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p33@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p34@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p35@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p36@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p37@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p38@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p39@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p40@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p41@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p42@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p43@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p44@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p45@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p46@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p47@280.jpg" alt="" loading="lazy" width="280" height="374"><img src="/images/sgcx/p48@280.jpg" alt="" loading="lazy" width="280" height="374"></div></div></section>
<section class="sec" id="places"><div class="wrap"><p class="eyebrow"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>05</b> Презентационные фильмы</p><h2>Фильмы о площадках для инвесторов.</h2><div class="places">
<article class="place"><button class="vid " type="button" data-video="/media/technopark-zubovo.mp4" aria-label="Смотреть: Технопарк «Зубово»"><img src="/images/zubovo/poster.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><p class="meta">Башкортостан · 3:04</p><h3>Технопарк «Зубово»</h3><p>Живая промышленная площадка под Уфой: корпуса, инженерия, облёт территории, синхроны руководства. Более 70 гектаров.</p><a class="case-link" href="https://hand-marketing.ru/zubovo/" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></article>
<article class="place"><button class="vid " type="button" data-video="/media/bekabad-hd.mp4" aria-label="Смотреть: Технопарк «Бекабад»"><img src="/images/bekabad/poster.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><p class="meta">Узбекистан · 2:34</p><h3>Технопарк «Бекабад»</h3><p>Площадка в Ташкентской области, которую Башкортостан строит вместе с Узбекистаном. Мастер-план поднимается поверх аэросъёмки реального участка.</p><a class="case-link" href="https://hand-marketing.ru/bekobod1/" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></article>
<article class="place"><button class="vid " type="button" data-video="/media/mmg-paveleckayaplaza.mp4" aria-label="Смотреть: ТРЦ «Павелецкая Плаза»"><img src="/images/mmg/poster.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><p class="meta">MMG · 5:37</p><h3>ТРЦ «Павелецкая Плаза»</h3><p>Фильм для арендаторов объекта на стройке: локация, трафик, аудитория, готовность. В первом кадре знак победителя MIPIM 2020.</p><a class="case-link" href="https://hand-marketing.ru/mmg" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></article>
</div></div></section>
<section class="sec tint" id="series"><div class="wrap"><p class="eyebrow"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>06</b> Серии</p><h2>Серии в едином языке: от десятка роликов до курса.</h2><div class="series">
<a class="ser" href="https://hand-marketing.ru/portfolio/ceramicanova" target="_blank" rel="noopener"><img src="/images/lib/custom-ceramicanova/cover-main.png" alt="" loading="lazy" width="476" height="396"><p class="ser-n"><b>17</b> роликов</p><h3>CeramicaNova</h3><p>По фильму на коллекцию санфарфора. Предметная макросъёмка, смыв на подкрашенной воде, 16:9 и 1:1.</p><span class="arr">↗</span></a>
<a class="ser" href="https://hand-marketing.ru/portfolio/obo-academy" target="_blank" rel="noopener"><img src="/images/lib/custom-obo-academy/cover-main.png" alt="" loading="lazy" width="476" height="396"><p class="ser-n"><b>10</b> роликов</p><h3>OBO Bettermann</h3><p>Съёмка в шоу-руме Академии OBO. Эксперт компании разбирает продукт: назначение, устройство, монтаж.</p><span class="arr">↗</span></a>
<a class="ser" href="https://hand-marketing.ru/video/saintgobain/training" target="_blank" rel="noopener"><img src="/images/lib/custom-sgtraining/cover-main.png" alt="" loading="lazy" width="476" height="396"><p class="ser-n"><b>19:30</b> минут курса</p><h3>Saint-Gobain, обучение</h3><p>Курс для руководителей: 28 экранов графики, 9 игровых сцен, 4 актёра, разбор поверх кадра.</p><span class="arr">↗</span></a>
<a class="ser" href="https://hand-marketing.ru/photo/saint-gobain" target="_blank" rel="noopener"><img src="/images/lib/custom-sgphoto/cover-main.png" alt="" loading="lazy" width="476" height="396"><p class="ser-n"><b>63</b> позиции за смену</p><h3>Saint-Gobain, Gyproc</h3><p>Предметная съёмка на площадке заказчика: 62 кадра в сдаче под каталог, сайт и POS.</p><span class="arr">↗</span></a>
</div></div></section>
<section class="sec" id="skills"><div class="wrap"><p class="eyebrow"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>07</b> Что мы умеем</p><h2>Всё, что нужно юбилейному фильму, в одних руках.</h2><p class="sub">Своя съёмочная группа и техника. Идею, сценарий, съёмки, графику, озвучку и монтаж делает одна команда. У каждого пункта есть кейс, где это видно.</p><div class="skills">
<div class="sk"><span class="sk-n">01</span><h3>Две концепции и сценарий</h3><p>Предлагаем два хода на выбор и доводим выбранный до покадрового сценария.</p><a href="https://hand-marketing.ru/video/gaz/" target="_blank" rel="noopener">где видно: Газель-трансформер <span>↗</span></a></div>
<div class="sk"><span class="sk-n">02</span><h3>Съёмка на складе и в цеху</h3><p>Работаем на действующих площадках по регламентам СИЗ, не останавливая смену.</p><a href="https://hand-marketing.ru/isotec/" target="_blank" rel="noopener">где видно: «Изотек» <span>↗</span></a></div>
<div class="sk"><span class="sk-n">03</span><h3>Несколько групп одновременно</h3><p>Параллельные выезды в разные города с одним режиссёрским планом.</p><a href="https://hand-marketing.ru/video/rgd/history/" target="_blank" rel="noopener">где видно: ЦМ РЖД <span>↗</span></a></div>
<div class="sk"><span class="sk-n">04</span><h3>Аэросъёмка</h3><p>Территория, терминалы и подъездные пути сверху, с квадрокоптера.</p><a href="https://hand-marketing.ru/zubovo/" target="_blank" rel="noopener">где видно: Технопарк «Зубово» <span>↗</span></a></div>
<div class="sk"><span class="sk-n">05</span><h3>Синхроны и интервью</h3><p>Ставим свет и кадр в кабинете и на рабочем месте, готовим вопросы со спикером.</p><a href="https://hand-marketing.ru/video/saintgobain/cx" target="_blank" rel="noopener">где видно: Saint-Gobain <span>↗</span></a></div>
<div class="sk"><span class="sk-n">06</span><h3>Экранная графика и 3D</h3><p>От полностью смоделированного запуска ракеты в космос до контента на все экраны стенда, плюс ежедневные репортажи и трансляции.</p><a href="https://hand-marketing.ru/portfolio/samara-stand-vdnh" target="_blank" rel="noopener">где видно: стенд Самары на ВДНХ <span>↗</span></a></div>
<div class="sk"><span class="sk-n">07</span><h3>Озвучка и языки</h3><p>Дикторский текст, английская версия, вшитые субтитры.</p><a href="https://hand-marketing.ru/video/eaton" target="_blank" rel="noopener">где видно: Eaton для выставки <span>↗</span></a></div>
<div class="sk"><span class="sk-n">08</span><h3>Версии под площадки</h3><p>Длинная для зала и переговоров, короткая для экранов и соцсетей, из одного материала.</p><a href="https://hand-marketing.ru/video/powertechnologies" target="_blank" rel="noopener">где видно: Power Technologies <span>↗</span></a></div>
</div></div></section>
<section class="sec dark" id="reviews"><div class="wrap"><p class="eyebrow light"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>08</b> Отзывы</p><h2>Что пишут клиенты в благодарственных письмах.</h2><div class="revs">
<figure class="rev big"><blockquote>«…за создание корпоративного видео ролика высокого качества, который был выполнен с высоким уровнем профессионализма в сжатые сроки. Результат оправдал и превзошёл ожидания.»</blockquote><figcaption><b>Saint-Gobain</b>Татьяна Дулуба, руководитель программы «Клиентский опыт»<a href="https://hand-marketing.ru/video/saintgobain/cx" target="_blank" rel="noopener">кейс <span>↗</span></a></figcaption></figure>
<figure class="rev"><blockquote>«За надежные партнерские отношения, эффективную работу и высокие показатели по итогам 2019 года.»</blockquote><figcaption><b>ЦМ РЖД</b>А. Ю. Бельский, начальник Центральной дирекции, 2019<a href="https://hand-marketing.ru/video/rgd/history" target="_blank" rel="noopener">кейс <span>↗</span></a></figcaption></figure>
<figure class="rev"><blockquote>«На протяжении нескольких лет совместная работа с агентством «Хэнд-Маркетинг» приносит ожидаемый положительный результат.»</blockquote><figcaption><b>Eaton</b>А. К. Бурочкин, директор по маркетингу, 2018–2019<a href="https://hand-marketing.ru/video/eaton" target="_blank" rel="noopener">кейс <span>↗</span></a></figcaption></figure>
<figure class="rev"><blockquote>«…мы рады возможности решать задачи разного уровня и направлений (от разработки и производства сувенирной продукции до оформления стендов и проведение клиентских мероприятий) в рамках взаимодействия с одной компанией.»</blockquote><figcaption><b>Becar Asset Management</b>Д. С. Сороколетов, вице-президент, 2018<a href="https://hand-marketing.ru/portfolio/becar-private-money" target="_blank" rel="noopener">кейс <span>↗</span></a></figcaption></figure>
<figure class="rev"><blockquote>«Агентством были выполнены все поставленные задачи в сжатые сроки, что свидетельствует о высоком профессионализме сотрудников.»</blockquote><figcaption><b>МФК «Саларис» (АО «ЛАУТ»)</b>Т. В. Левченко, генеральный директор, 2018<a href="https://hand-marketing.ru/event/salaris" target="_blank" rel="noopener">кейс <span>↗</span></a></figcaption></figure>
</div><p class="revs-note">Цитаты из писем без правок. Сканы писем показываем на встрече.</p></div></section>
<section class="sec tint" id="all"><div class="wrap"><p class="eyebrow"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>09</b> Все остальные проекты</p><h2>Ролики, дизайн, полиграфия и события.</h2><div class="tabs" role="tablist"><button class="on" type="button" data-f="*">Все <i>39</i></button>
<button type="button" data-f="video">Ролики <i>9</i></button>
<button type="button" data-f="design">Дизайн и 3D <i>9</i></button>
<button type="button" data-f="print">Полиграфия <i>8</i></button>
<button type="button" data-f="event">События и стенды <i>13</i></button>
</div><div class="grid">
<a class="card" data-k="video" href="https://hand-marketing.ru/video/patriot" target="_blank" rel="noopener"><img src="/images/lib/as3532-3737-4330-b333-386531636666/__-03.png" alt="" loading="lazy" width="476" height="396"><span class="cl">УАЗ и Eaton</span><h4>Рекламный ролик УАЗ Патриот, 60 секунд</h4><p>60-секундный ролик о блокировке дифференциала Eaton на УАЗ Патриот. Сценарий согласован с российской и международной компанией, три съемочных дня.</p></a>
<a class="card" data-k="video" href="https://hand-marketing.ru/video/gaz" target="_blank" rel="noopener"><img src="/images/lib/as3233-3363-4138-b265-353738653739/__-20.png" alt="" loading="lazy" width="476" height="396"><span class="cl">ГАЗ и Eaton</span><h4>Вирусный ролик «Газель-трансформер», 1:42</h4><p>Вирусный ролик «Газель-трансформер» про блокировку Eaton, 1:42. Идея родилась из запрета на прямое сравнение машин.</p></a>
<a class="card" data-k="video" href="https://hand-marketing.ru/video/vivax" target="_blank" rel="noopener"><img src="/images/lib/as6163-3132-4061-a536-363936336533/__-52.png" alt="" loading="lazy" width="476" height="396"><span class="cl">VIVAX SPORT</span><h4>Настасья Самбурская и три средства за 49 секунд</h4><p>Вирусный ролик спортивных средств VIVAX с Настасьей Самбурской: вся продуктовая линейка в одном сюжете тренировки, 49 секунд.</p></a>
<a class="card" data-k="video" href="https://hand-marketing.ru/video/eaton" target="_blank" rel="noopener"><img src="/images/lib/as3935-3832-4662-a132-383864613435/__-35.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Eaton</span><h4>Ролик для международной выставки</h4><p>Англоязычный ролик для международной выставки: монтаж из девяти исходников, досъемка в Москве, английская озвучка, вшитые русские субтитры.</p></a>
<a class="card" data-k="video" href="https://hand-marketing.ru/video/interplastika" target="_blank" rel="noopener"><img src="/images/lib/as3331-3035-4965-a439-613266363431/__-54.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Messe Düsseldorf</span><h4>«интерпластика» за 2:12, 17 компаний в кадре</h4><p>Обзорный ролик выставки полимеров на 2:12: заменяет прогулку по четырем павильонам, 17 компаний в кадре.</p></a>
<a class="card" data-k="video" href="https://hand-marketing.ru/video/mozaika" target="_blank" rel="noopener"><img src="/images/lib/as6537-6538-4133-b832-383637333832/__-45.png" alt="" loading="lazy" width="476" height="396"><span class="cl">ТРЦ «Мозаика»</span><h4>4:31 и тринадцать синхронов</h4><p>Презентационный фильм о ТРЦ на 134 000 м²: аэросъемка, галереи, цифры графикой и тринадцать синхронов арендаторов и руководства, 4:31.</p></a>
<a class="card" data-k="video" href="https://hand-marketing.ru/video/salaris" target="_blank" rel="noopener"><img src="/images/lib/as3933-3462-4563-b861-383364333966/__-15.png" alt="" loading="lazy" width="476" height="396"><span class="cl">МФК «Саларис»</span><h4>Два ролика: объект и аудитория</h4><p>Два ролика о МФК «Саларис»: первый на стадии стройки с аэросъемкой и 3D-графикой, второй к открытию про аудиторию.</p></a>
<a class="card" data-k="video" href="https://hand-marketing.ru/video/silkway" target="_blank" rel="noopener"><img src="/images/lib/as6164-6432-4132-a361-613136626438/__-51.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Silk Way Rally</span><h4>Маршрут 5 947,93 км рельефом по легенде</h4><p>3D-маршрут ралли-марафона рельефом по координатам легенды, 5 947,93 км. Песочный стол и техническая поддержка презентации.</p></a>
<a class="card" data-k="video" href="https://hand-marketing.ru/video/lingerie" target="_blank" rel="noopener"><img src="/images/lib/as3439-3739-4562-a533-616631333163/__-37.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Lingerie</span><h4>Подиумная съемка для журнала Lingerie</h4><p>Полуторачасовой показ в двухкамерной съемке, смонтированный в семиминутный ролик: все одиннадцать марок в порядке выхода.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/metra" target="_blank" rel="noopener"><img src="/images/lib/custom-metra/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Брендбук Metra Technology Group</span><h4>Пять брендов индустриальной экосистемы</h4><p>Брендбук индустриальной экосистемы: один знак на пять названий, пять палитр и паттернов на общей сетке, правила для сборки без дизайнера.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/samara" target="_blank" rel="noopener"><img src="/images/lib/custom-samara-brand/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Фирменный стиль выставки «Самара»</span><h4>28 полос и маскот в 16 образах</h4><p>Брендбук выставки «Самара»: визуальный язык стенда с ВДНХ переведен в правила для музейных залов, экранов, навигации и сувенирки. 28 полос, маскот в 16 образах.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/eaton/visual" target="_blank" rel="noopener"><img src="/images/lib/as6230-6132-4533-b633-626431633139/__-43.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Eaton</span><h4>3D визуализация «Комплексные решения компании Eaton»</h4><p>3D-модели гипермаркета, завода и ЦОД с типовой расстановкой оборудования Eaton, адаптированные под печатные плакаты.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/saintgobain/calendar" target="_blank" rel="noopener"><img src="/images/lib/custom-sgcalendar/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Новогодний календарь Saint-Gobain</span><h4>Концепция: иллюстрации из инструментов</h4><p>Концепция новогоднего календаря: материалы Saint-Gobain глазами мастера. Профиль становится небоскребом, плита утеплителя пляжем.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/skolkovo" target="_blank" rel="noopener"><img src="/images/lib/as3266-3963-4363-a239-646364383365/__-72.png" alt="" loading="lazy" width="476" height="396"><span class="cl">СКОЛКОВО</span><h4>Доклад «Цифровое производство» на 86 полос</h4><p>Дизайн и верстка доклада «Цифровое производство» на 86 полос по брендбуку СКОЛКОВО с переработанной инфографикой.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/teoxane" target="_blank" rel="noopener"><img src="/images/lib/as3538-6538-4236-b937-343132366134/__-76.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Teoxane</span><h4>Key Visual Teoxane</h4><p>Key visual научной конференции Teoxane Russia на основе образа иконописи.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/piloti" target="_blank" rel="noopener"><img src="/images/lib/as3530-6166-4831-b932-356466373932/__-70.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Пилоты Будущего</span><h4>Креативная концепция и фирменный стиль «Пилоты Будущего»</h4><p>Логотип и фирменный стиль детского технологического клуба: космический корабль внутри надписи и паттерн.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/rgd/suvenir" target="_blank" rel="noopener"><img src="/images/lib/as3634-3861-4239-b237-356636663535/__-60.png" alt="" loading="lazy" width="476" height="396"><span class="cl">РЖД</span><h4>Новогодняя сувенирная продукция ОАО РЖД</h4><p>Новогодний набор ЦМ РЖД из шести позиций в одной концепции. Каждый месяц календаря закреплен за услугой дирекции.</p></a>
<a class="card" data-k="design" href="https://hand-marketing.ru/creative/saintgobain/suitcase" target="_blank" rel="noopener"><img src="/images/lib/as3734-3562-4636-a636-633764353537/__-41.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Saint-Gobain</span><h4>Дизайн презентационного чемодана Saint-Gobain</h4><p>Чемодан образцов для проектных продаж: снаружи он выглядит как фрагмент стены с двумя сторонами и разрезом по торцу.</p></a>
<a class="card" data-k="print" href="https://hand-marketing.ru/creative/becar/sdep" target="_blank" rel="noopener"><img src="/images/lib/as6366-6163-4338-b039-373730386163/__-74.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Becar</span><h4>Фирменный стиль отдела продаж компании Becar</h4><p>Айдентика отдела продаж Becar: знак, паттерн и палитра сведены к простым правилам, по которым макеты собирают сами менеджеры.</p></a>
<a class="card" data-k="print" href="https://hand-marketing.ru/creative/becar/ramada" target="_blank" rel="noopener"><img src="/images/lib/as6534-3037-4839-a432-383536343433/__-56.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Becar</span><h4>Брошюра продукта: «Отель Ramada»</h4><p>Брошюра на 20 полос для продажи номеров отеля Ramada Encore инвесторам: менеджер открывает нужный разворот на встрече.</p></a>
<a class="card" data-k="print" href="https://hand-marketing.ru/creative/becar/vertical" target="_blank" rel="noopener"><img src="/images/lib/as6633-6662-4561-b364-303861353166/__-64.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Becar</span><h4>Брошюра Vertical BW Signature Collection</h4><p>Брошюра на 24 полосы для продажи номеров бутик-отеля на 82 номера: доход, сам отель, материал на стол после встречи.</p></a>
<a class="card" data-k="print" href="https://hand-marketing.ru/creative/becar/weampi" target="_blank" rel="noopener"><img src="/images/lib/as3532-6637-4235-a237-396563653836/__-78.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Becar</span><h4>We&amp;I: 24 полосы про кондо-отель</h4><p>Буклет на 24 полосы, который объясняет новый формат кондо-отеля We&amp;I за менеджера.</p></a>
<a class="card" data-k="print" href="https://hand-marketing.ru/creative/becar/smile" target="_blank" rel="noopener"><img src="/images/lib/custom-smile-broch/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Брошюра ТЦ «Смайл»</span><h4>22 полосы про доход с торговых метров</h4><p>Брошюра на 22 полосы для частных инвесторов в ТЦ «Смайл»: формат кондо-ТЦ, цифры работающего объекта, три доходных продукта.</p></a>
<a class="card" data-k="print" href="https://hand-marketing.ru/creative/becar/knight-house" target="_blank" rel="noopener"><img src="/images/lib/custom-knight/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Брошюра «Дом с рыцарем»</span><h4>18 полос про апартаменты в доходном доме</h4><p>Брошюра на 18 полос про апартаменты в доходном доме начала XX века: сначала история дома, потом планировки.</p></a>
<a class="card" data-k="print" href="https://hand-marketing.ru/creative/patriki" target="_blank" rel="noopener"><img src="/images/lib/as6265-3361-4465-a366-336161356638/__-68.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Patriki Times</span><h4>Дизайн и верстка журнала Patriki Times</h4><p>Дизайн и сетка ежемесячного глянцевого журнала о Патриарших прудах, ведение выпусков для печати и интернет-версии.</p></a>
<a class="card" data-k="print" href="https://hand-marketing.ru/creative/tunel" target="_blank" rel="noopener"><img src="/images/lib/as3630-6238-4266-a466-346530396234/__-58.png" alt="" loading="lazy" width="476" height="396"><span class="cl">AnVIT</span><h4>Тоннель дезинфекции с циклом до 20 секунд</h4><p>Разработка дезинфекционного тоннеля AnVIT S12T с циклом до 20 секунд и защитного лицевого экрана для персонала.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/event/eaton" target="_blank" rel="noopener"><img src="/images/lib/as6165-3534-4833-b866-366532623865/__-26.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Eaton</span><h4>Партнерская конференция в Казахстане</h4><p>Партнерская конференция в Алматы под ключ: отель, перелеты, трансферы, программа, сцена, LED, застройка, гид участника, сопровождение трое суток.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/eaton_online" target="_blank" rel="noopener"><img src="/images/lib/as6135-3563-4735-a365-643234376439/icons-112.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Eaton</span><h4>Семь часов эфира на IT-ОСЬ 2020 из офиса</h4><p>Семь часов эфира из офиса заказчика на форум OCS «IT-ОСЬ 2020»: две камеры, vMix, свет, петлички, основной и резервный мобильный канал.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/portfolio/samara-stand-vdnh" target="_blank" rel="noopener"><img src="/images/lib/custom-samara-vdnh/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Стенд Самарской области</span><h4>Выставка-форум «Россия», ВДНХ</h4><p>Стенд в форме ладьи с экраном-парусом на выставке-форуме «Россия». Девять тем региона, амфитеатр, кинетический экран, восемь тач-панелей, Naked Eye контент на изогнутом экране.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/portfolio/stavropol-stand-vdnh" target="_blank" rel="noopener"><img src="/images/lib/custom-stavropol-vdnh/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Стенд Ставропольского края</span><h4>Выставка-форум «Россия», ВДНХ</h4><p>Мультимедийная часть стенда края на выставке-форуме «Россия»: LED-короб и контент, рассчитанный под конкретную экспозицию.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/portfolio/samara-exhibition" target="_blank" rel="noopener"><img src="/images/lib/custom-samara-exhibition/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Выставка «Самара»</span><h4>Музей им. Алабина</h4><p>Продолжение проекта с ВДНХ в Музее им. П. В. Алабина: стилистика стенда перенесена в музейные залы, интерактивные панели с Kinect.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/3d/stavropol" target="_blank" rel="noopener"><img src="/images/lib/as6466-3635-4534-b432-353364376364/__-01.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Администрация Ставрополя</span><h4>27 проекторов, более 25 000 зрителей</h4><p>Восьмиминутное 3D mapping шоу на здании Парламента: 27 проекторов, лазеры, более 25 000 зрителей.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/event/samsung" target="_blank" rel="noopener"><img src="/images/lib/as3466-3261-4738-b938-303637303133/__-18.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Samsung</span><h4>Новогодний вечер 2020, зимний лес из проекций</h4><p>Новогодний вечер, собранный из проекций: зимний лес по дуге зала и интерактивный почтовый ящик Деда Мороза. Контент, оборудование, монтаж, техсопровождение.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/event/changan" target="_blank" rel="noopener"><img src="/images/lib/as3635-3436-4663-b265-633363383261/__-98.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Презентация Changan CS35</span><h4>Атриум ТЦ и финал с 3D mapping шоу</h4><p>Презентация CS35 в атриуме ТЦ с записью на тест-драйв и финальное шоу в дилерском центре с 3D mapping на кузове.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/portfolio/becar-private-money" target="_blank" rel="noopener"><img src="/images/lib/custom-becar-pm/cover-main.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Стенд You&amp;Co для Becar</span><h4>Private Money Expo Forum 2021</h4><p>Стенд генерального партнера на Private Money Expo Forum 2021 под ключ: проект, застройка, презентация для сцены, раздатка, дежурство, демонтаж.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/event/riviera" target="_blank" rel="noopener"><img src="/images/lib/as3062-3363-4134-b333-623232303134/__-22.png" alt="" loading="lazy" width="476" height="396"><span class="cl">ТРЦ «Ривьера»</span><h4>«Внутри стихии»: вечер для арендаторов на стройке</h4><p>Вечер «Внутри стихии» для почти двухсот руководителей прямо на стройке ТРЦ: передача помещения «Ашан Сити», три экрана в одной композиции.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/event/salaris" target="_blank" rel="noopener"><img src="/images/lib/as3234-6262-4231-b031-663033663939/__-16.png" alt="" loading="lazy" width="476" height="396"><span class="cl">МФК «Саларис»</span><h4>Презентация для арендаторов, 200 гостей</h4><p>Презентация строящегося МФК для 200 ритейлеров: площадка, концепция, презентация, ролик об объекте.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/event/mozaika" target="_blank" rel="noopener"><img src="/images/lib/as6263-3532-4466-b765-323663363739/__-28.png" alt="" loading="lazy" width="476" height="396"><span class="cl">ТЦ «Мозаика»</span><h4>«Пора выходить на свет»: 134 гостя зажгли знак</h4><p>Вечер для арендаторов «Пора выходить на свет»: 134 гостя собрали новый знак ТЦ из лампочек.</p></a>
<a class="card" data-k="event" href="https://hand-marketing.ru/event/marieclaire" target="_blank" rel="noopener"><img src="/images/lib/as3731-3666-4163-a661-383336646133/__-13.png" alt="" loading="lazy" width="476" height="396"><span class="cl">Marie Claire</span><h4>Кросс-мероприятия в ТЦ Москвы, 2011-2013</h4><p>Серия кросс-мероприятий в ГУМ, «Европейском», «Атриуме» и «Метрополисе»: стенды, семплинг, POS-материалы, финальный вечер с показом.</p></a>
</div></div></section>
<section class="sec" id="next"><div class="wrap"><p class="eyebrow"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg><b>10</b> Следующие шаги</p><h2>Как двигаемся дальше.</h2><div class="steps">
<div class="st"><b>01</b><h3>Онлайн-встреча</h3><p>Приоритет площадок показа, обязательные объекты, утверждённые цифры, бренды партнёров в кадре.</p></div>
<div class="st"><b>02</b><h3>Коммерческое предложение</h3><p>Две концепции, календарь до 26 июля 2027, смета построчно: концепция, РФ, РБ, РК, дизайн, пост, правки.</p></div>
<div class="st"><b>03</b><h3>Видео-скаут площадок</h3><p>Удалённый осмотр пяти объектов до фиксации сметы: окна активности, свет, маршруты, допуски.</p></div>
</div><div class="par"><span class="par-l">параллельно</span><div><h3>Проверка СБ</h3><p>С первого дня регистрируемся на tender.alidi.ru и загружаем документы для службы безопасности. Работа над фильмом при этом не ждёт.</p></div></div>
</div></section>
</div>
<section class="final" id="contacts"><div class="wrap fin"><div><p class="eyebrow light"><svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg>Контакты</p><h2>На связи.</h2><p class="lead">Пишите на почту с любыми вопросами по идеям, смете и площадкам.</p><div class="hero-cta"><a class="btn" href="mailto:anarodetsky@hand-marketing.ru?subject=%D0%90%D0%9B%D0%98%D0%94%D0%98%3A%20%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%20%D0%BA%2035-%D0%BB%D0%B5%D1%82%D0%B8%D1%8E">Написать письмо</a><a class="btn ghost" href="https://t.me/narodetskii" target="_blank" rel="noopener">Telegram</a><a class="btn ghost pdf-btn" href="?pdf=1">Скачать PDF</a></div></div><dl class="cont"><dt>Контактное лицо</dt><dd>Народецкий Александр · Client Service Director</dd><dt>Телефон</dt><dd><a href="tel:+79859998783">+7 985 999 87 83</a> · <a href="tel:+74955807537">+7 495 580 75 37</a></dd><dt>Почта</dt><dd><a href="mailto:info@hand-marketing.ru">info@hand-marketing.ru</a></dd><dt>Офис</dt><dd>123022, Москва, ул. Рочдельская, 14А</dd><dt>Все проекты</dt><dd><a href="https://hand-marketing.ru/project" target="_blank" rel="noopener">hand-marketing.ru/project</a></dd><dt>Реквизиты</dt><dd>ООО «Хэнд-маркетинг» · ИНН 7709931482 · КПП 770901001 · ОГРН 1137746525608</dd></dl></div><p class="wrap foot">Страница подготовлена для ГК АЛИДИ · доступ по личному приглашению</p></section>
<div class="modal" id="modal" hidden><button class="x" type="button" aria-label="Закрыть">×</button><div class="mv"></div></div>
<script>
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

</script>
<script id="hm-al-analytics">
// Учёт просмотра страницы для Hand Marketing: время по разделам, прокрутка, клики, шаги игры.
// Данные уходят только на наш сервер (?track=1).
(function () {
  var sid = Math.random().toString(36).slice(2, 12) + Date.now().toString(36).slice(-4);
  var t0 = Date.now(), events = [], dwell = {}, order = [], active = 0, maxScroll = 0, lastInput = Date.now(), dirty = true, sent = false;
  function cap(s) { s = (s || '').replace(/\s+/g, ' ').trim(); return s.charAt(0).toUpperCase() + s.slice(1); }
  function ev(k, d) { events.push({ k: k, d: d, at: Date.now() - t0 }); dirty = true; }

  // Разделы с понятными названиями (по надписи над заголовком)
  var secs = [].slice.call(document.querySelectorAll('section, .final')).map(function (el) {
    var name = 'Первый экран';
    if (!el.classList.contains('hero')) {
      var eb = el.querySelector('.eyebrow');
      if (eb) { var c = eb.cloneNode(true); var b = c.querySelector('b'); if (b) b.remove(); name = cap(c.textContent); }
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
    var body = JSON.stringify({ sid: sid, final: final ? 1 : 0, events: events.splice(0), dwell: dwell, order: order, active: active, scroll: maxScroll,
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
    var a = e.target.closest('a, button, .vid, .hall .st'); if (!a) return;
    var txt = cap((a.getAttribute('aria-label') || a.textContent || '').slice(0, 80));
    var href = (a.getAttribute && a.getAttribute('href')) || '';
    if (a.classList.contains('pdf-btn')) return ev('pdf', 'нажал «Скачать PDF»');
    if (a.id === 'arch-btn') return ev('archive', a.getAttribute('aria-expanded') === 'true' ? 'свернул архив' : 'открыл архив «Наши работы»');
    if (a.closest('.nav')) return ev('nav', 'меню: ' + txt);
    if (a.classList.contains('vid') || a.classList.contains('vid-inline')) return ev('video', 'включил ролик: ' + (a.dataset.video || '').split('/').pop());
    if (a.classList.contains('m-row')) return first('match' + a.dataset.i, 'match', 'опыт под задачу: «' + txt.replace(/^0\d\s*/, '') + '»');
    if (a.closest('.tabs')) return ev('tab', 'все проекты: вкладка «' + txt.replace(/\s*\d+$/, '') + '»');
    if (/^tel:/.test(href)) return ev('contact', 'нажал телефон');
    if (/^mailto:/.test(href)) return ev('contact', 'нажал почту' + (/subject/.test(href) ? ' («Назначить встречу»)' : ''));
    if (/t\.me|wa\.me/.test(href)) return ev('contact', 'нажал Telegram');
    if (/^https?:/.test(href)) { var h = a.querySelector('h4, h3'); return ev('link', 'открыл кейс: ' + cap(h ? h.textContent : txt) + ' → ' + href.replace('https://hand-marketing.ru', '')); }
    if (/^#/.test(href)) return ev('anchor', 'перешёл к разделу: ' + txt);
  }, true);
  document.addEventListener('copy', function () {
    var s = String(getSelection() || '').trim(); if (s) ev('copy', 'скопировал текст: «' + s.slice(0, 120) + (s.length > 120 ? '…' : '') + '»');
  });
})();

</script>
<script>
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym(71125393, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true, params:{ private_page:'alidi' } });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute; left:-9999px;" alt=""></div></noscript>
</body>
</html>
