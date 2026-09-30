<?php
// Персональная страница для MR: стенды C7.2 и C8.1 на фестивале «Наша школа» 2026. Доступ по паролю.
// В файле хранится только SHA-256 хеш пароля. Аналитика визитов: _analytics.php, отчёт по ?stats=<ключ>.
define('HM_MR', 1);
date_default_timezone_set('Europe/Moscow');
require __DIR__ . '/_analytics.php';

$ACCESS_HASH = '8f21071c71c5643578da9abd6332c0eef760058c98154b0704516167b352e059';
$COOKIE_NAME = 'hm_mr_access';

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
        setcookie($COOKIE_NAME, $ACCESS_HASH, time() + 60 * 60 * 24 * 30, '/for/mr-group/', '', hm_https(), true);
        $g = hm_geo(hm_ip());
        hm_event('login_ok', array('geo' => $g));
        hm_tg("🔓 <b>MR открыли страницу</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where($g) . "\n" . date('d.m H:i'));
        header('Location: ./');
        exit;
    }
    // введённый текст не сохраняем: это может оказаться чужой пароль
    hm_event('login_fail', array('len' => function_exists('mb_strlen') ? mb_strlen($input) : strlen($input)));
    $error = true;
}

if (!$authed) {
    // ---- Экран ввода кода ----
    if ($_SERVER['REQUEST_METHOD'] === 'GET') hm_event('gate_view');
    $errHtml = $error ? '<p class="gate-error">Пароль не подошёл. Попробуйте ещё раз.</p>' : '';
    echo <<<GATE
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Доступ к странице · MR × Hand Marketing</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/unbounded-fira.css">
<link rel="stylesheet" href="/fonts/react-main.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Inter',system-ui,sans-serif; color:#090714; background:#f5f5f5;
    min-height:100vh; display:flex; align-items:center; justify-content:center; padding:20px; }
  .gate { background:#fff; border-radius:32px; padding:44px 36px 36px; max-width:430px; width:100%; }
  .logos { display:flex; align-items:center; gap:16px; margin-bottom:34px; }
  .logos img { height:36px; }
  .logos svg { height:26px; width:auto; color:#090714; }
  .logos i { width:1px; height:26px; background:#d0d1d7; }
  h1 { font-family:'Unbounded',sans-serif; font-weight:500; font-size:22px; line-height:1.25; letter-spacing:-.02em; margin-bottom:10px; }
  .sub { font-size:15px; color:#8e9099; margin-bottom:26px; }
  form { display:flex; flex-direction:column; gap:10px; }
  input { font-family:'Unbounded',sans-serif; font-size:16px; letter-spacing:.06em; text-align:center;
    padding:16px; border:1.5px solid #e3e3e8; border-radius:16px; outline:none; background:#f5f5f5; }
  input:focus { border-color:#754be9; background:#fff; }
  button { font-family:'Inter',sans-serif; font-weight:500; font-size:15px; color:#fff; background:#754be9; border:0;
    border-radius:999px; padding:16px; cursor:pointer; }
  button:hover { background:#5e36d0; }
  .gate-error { color:#e5484d; font-size:13px; margin-top:4px; text-align:center; }
  .note { margin-top:26px; font-size:12px; color:#8e9099; text-align:center; }
</style>
</head>
<body>
  <div class="gate">
    <div class="logos">
      <svg viewBox="0 0 43 28" aria-label="MR"><path fill="currentColor" d="M6.40114 2.62744L13.8561 19.0357L21.1274 2.62744H33.2125C35.6477 2.62761 37.6628 3.30835 39.2863 4.67292C40.9437 6.00574 41.7558 7.69525 41.7559 9.70888C41.7559 11.7227 40.9438 13.4123 39.2863 14.7772C38.0071 15.8265 36.4856 16.4704 34.7067 16.6974H37.7436L42.6322 25.368H37.1439L32.318 16.6974H26.5329V25.368H21.5615V6.92235L13.3897 25.368H11.0514L2.59893 6.76485V25.368H0.486816V2.62744H6.40114ZM26.5329 4.83244V14.5873H31.5527C34.2322 14.5873 36.0071 12.6641 36.0071 9.70888C36.007 6.7539 34.2321 4.83245 31.5527 4.83244H26.5329Z"/></svg>
      <i></i>
      <img src="hm-logo.svg" alt="Hand Marketing">
    </div>
    <h1>MR × Hand Marketing<br>«Наша школа» 2026</h1>
    <p class="sub">Введите пароль</p>
    <form method="post" action="./" autocomplete="off">
      <input type="text" name="code" placeholder="пароль" maxlength="30" autocapitalize="none" spellcheck="false" autofocus required>
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
// Выгрузка PDF только после входа: файл лежит рядом, прямой доступ закрыт в .htaccess
if (isset($_GET['pdf'])) {
    $f = __DIR__ . '/mr-proposal.pdf';
    if (!is_file($f)) { http_response_code(404); exit; }
    hm_event('pdf_download');
    hm_tg("📄 <b>MR скачали PDF</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where(hm_geo(hm_ip())) . "\n" . date('d.m H:i'));
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="MR_Nasha_shkola_2026_Hand_Marketing.pdf"');
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
<title>MR × Hand Marketing · «Наша школа» 2026</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/unbounded-fira.css">
<link rel="stylesheet" href="/fonts/react-main.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  :root {
    --bg:#f5f5f5; --card:#fff; --ink:#090714; --grey:#8e9099; --grey2:#5b5d67; --line:#e6e6ea;
    --violet:#754be9; --violet-d:#5e36d0; --violet-l:#efeafd; --sky:#5ec4f7; --sky-l:#e7f6fe; --mint:#2dbe6c;
    --r-xl:40px; --r-l:32px; --r-m:22px; --r-s:16px;
    --head:'Unbounded','Inter',sans-serif;
  }
  html { scroll-behavior:smooth; }
  body { font-family:'Inter',system-ui,sans-serif; color:var(--ink); background:var(--bg); font-size:16px; line-height:1.55;
    -webkit-font-smoothing:antialiased; overflow-x:hidden; }
  img { display:block; max-width:100%; }
  a { color:inherit; }
  button { font:inherit; color:inherit; }
  .wrap { max-width:1280px; margin:0 auto; padding:0 28px; }
  @media (max-width:640px){ .wrap { padding:0 16px; } }
  section { padding-top:96px; }
  @media (max-width:640px){ section { padding-top:64px; } }

  .eyebrow { display:flex; align-items:center; gap:10px; font-family:var(--head); font-size:12px; letter-spacing:.04em; color:var(--grey); text-transform:lowercase; }
  .eyebrow b { color:var(--violet); font-weight:500; }
  .h2 { font-family:var(--head); font-weight:500; font-size:clamp(28px,4.2vw,58px); line-height:1.02; letter-spacing:-.045em; margin-top:16px; }
  .h2 em { font-style:normal; color:var(--violet); }
  .h2 i { font-style:normal; color:var(--sky); }
  .h3 { font-family:var(--head); font-weight:500; font-size:clamp(19px,1.8vw,24px); line-height:1.2; letter-spacing:-.03em; }
  .lead { font-size:clamp(16px,1.35vw,19px); line-height:1.6; color:var(--grey2); max-width:44em; margin-top:18px; }
  .lead b { color:var(--ink); font-weight:600; }
  .pill { display:inline-flex; align-items:center; gap:8px; border-radius:999px; font-size:13px; line-height:1; padding:9px 14px;
    background:var(--card); border:1px solid var(--line); white-space:nowrap; }
  .pill.v { background:var(--violet); border-color:var(--violet); color:#fff; }
  .pill.s { background:var(--sky-l); border-color:var(--sky-l); color:#0b6c9c; }
  .card { background:var(--card); border-radius:var(--r-l); padding:36px; }
  @media (max-width:640px){ .card { padding:22px 18px; border-radius:26px; } }
  .gem { display:inline-block; width:14px; height:18px; background:var(--violet); clip-path:polygon(50% 0,100% 38%,50% 100%,0 38%); }

  /* Шапка */
  .top { position:absolute; top:0; left:0; right:0; z-index:10; color:#fff; }
  .top-in { display:flex; align-items:center; justify-content:space-between; height:84px; gap:20px; }
  .brand { display:flex; align-items:center; gap:14px; text-decoration:none; }
  .brand svg { height:24px; width:auto; }
  .brand i { width:1px; height:24px; background:rgba(255,255,255,.4); }
  .brand img { height:34px; }
  .nav { display:flex; gap:24px; font-size:14px; }
  .nav a { text-decoration:none; opacity:.85; } .nav a:hover { opacity:1; }
  @media (max-width:1020px){ .nav { display:none; } }

  /* Хиро */
  .hero { position:relative; min-height:max(680px,100vh); color:#fff; background:#090714; border-radius:0 0 var(--r-xl) var(--r-xl); overflow:hidden; padding:0; display:flex; align-items:flex-end; }
  .hero > img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:50% 30%; transform:scale(1.04); animation:heroZoom 18s ease-out forwards; }
  @keyframes heroZoom { to { transform:scale(1); } }
  .hero::after { content:''; position:absolute; inset:0; background:linear-gradient(180deg,rgba(9,7,20,.5) 0%,rgba(9,7,20,0) 30%,rgba(9,7,20,.35) 55%,rgba(9,7,20,.92) 100%); }
  .hero-in { position:relative; z-index:2; width:100%; padding-top:112px; padding-bottom:56px; }
  .hero .pill { background:rgba(255,255,255,.12); border-color:rgba(255,255,255,.22); color:#fff; backdrop-filter:blur(10px); }
  @media (max-width:640px){ .hero .pill { white-space:normal; line-height:1.35; max-width:100%; } .hero .pill .gem { flex:none; } }
  .hero h1 { font-family:var(--head); font-weight:500; font-size:clamp(40px,7.4vw,112px); line-height:.96; letter-spacing:-.055em; margin:22px 0 0; }
  .hero h1 span { color:#b9a3ff; }
  .hero-row { display:flex; justify-content:space-between; align-items:flex-end; gap:32px; margin-top:30px; flex-wrap:wrap; }
  .hero p { font-size:clamp(16px,1.35vw,19px); line-height:1.6; max-width:36em; color:rgba(255,255,255,.84); }
  .hero-stands { display:flex; gap:10px; flex-wrap:wrap; }
  .hs { display:block; text-decoration:none; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.2); backdrop-filter:blur(12px);
    border-radius:var(--r-m); padding:16px 20px; min-width:200px; transition:background .2s; }
  .hs:hover { background:rgba(255,255,255,.2); }
  .hs small { display:block; font-size:12px; color:rgba(255,255,255,.6); }
  .hs b { display:block; font-family:var(--head); font-weight:500; font-size:20px; letter-spacing:-.03em; margin-top:6px; }
  .hs span { font-size:13px; color:rgba(255,255,255,.75); }

  /* Задача: MR Образование */
  .task { display:grid; grid-template-columns:1.1fr 1fr; gap:12px; margin-top:36px; }
  @media (max-width:960px){ .task { grid-template-columns:1fr; } }
  .task .ph { border-radius:var(--r-l); overflow:hidden; position:relative; min-height:340px; }
  .task .ph img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .task .ph .pill { position:absolute; left:18px; bottom:18px; }
  .aud { display:flex; flex-wrap:wrap; gap:8px; margin-top:18px; }
  .aud span { font-size:14px; background:var(--bg); border-radius:999px; padding:9px 14px; }
  .kpis { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-top:22px; }
  .kpis div { background:var(--bg); border-radius:var(--r-s); padding:16px; }
  .kpis b { display:block; font-family:var(--head); font-weight:500; font-size:26px; letter-spacing:-.04em; }
  .kpis span { font-size:13px; color:var(--grey2); line-height:1.35; display:block; margin-top:4px; }

  /* Схема зала */
  .hall { display:grid; grid-template-columns:1.2fr 1fr; gap:36px; align-items:center; }
  @media (max-width:960px){ .hall { grid-template-columns:1fr; } }
  .hall svg { width:100%; height:auto; display:block; }
  .hall .st { cursor:pointer; transition:filter .2s; }
  .hall .st:hover { filter:brightness(1.08); }
  .legend-list { display:flex; flex-direction:column; gap:10px; margin-top:24px; }
  .li { display:flex; gap:14px; align-items:flex-start; padding:16px 18px; border-radius:var(--r-m); background:var(--bg); text-decoration:none; transition:background .2s; }
  .li:hover { background:var(--violet-l); }
  .li .n { font-family:var(--head); font-size:13px; padding:7px 10px; border-radius:10px; color:#fff; flex:none; }
  .li b { display:block; font-weight:600; }
  .li span { font-size:14px; color:var(--grey2); }
  .dash { stroke-dasharray:7 6; animation:dash 1.6s linear infinite; }
  @keyframes dash { to { stroke-dashoffset:-26; } }

  /* Подкаст-куб */
  .cube-wrap { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:36px; }
  @media (max-width:960px){ .cube-wrap { grid-template-columns:1fr; } }
  .stage { position:relative; border-radius:var(--r-l); background:radial-gradient(120% 90% at 50% 20%,#1e1840 0%,#090714 70%); min-height:520px; overflow:hidden;
    perspective:1100px; cursor:grab; touch-action:pan-y; user-select:none; }
  .stage:active { cursor:grabbing; }
  .stage .hint { position:absolute; left:20px; top:18px; font-size:12.5px; color:rgba(255,255,255,.5); }
  .stage .floor-shadow { position:absolute; left:50%; top:74%; width:360px; height:60px; margin-left:-180px; border-radius:50%; background:radial-gradient(closest-side,rgba(117,75,233,.45),transparent); filter:blur(6px); }
  .cube { position:absolute; left:50%; top:50%; width:0; height:0; transform-style:preserve-3d; }
  .cube .f { position:absolute; width:240px; height:240px; left:-120px; top:-120px; transform-style:preserve-3d; }
  .glass { background:linear-gradient(135deg,rgba(200,230,255,.16),rgba(200,230,255,.05) 60%,rgba(255,255,255,.14)); border:6px solid #111; box-shadow:inset 0 0 0 1px rgba(255,255,255,.15);
    transition:background .35s, box-shadow .35s; }
  .glass::after { content:''; position:absolute; left:0; right:0; top:44%; height:26px; background:rgba(255,255,255,.14); }
  .glass .brandband { position:absolute; left:0; right:0; top:44%; height:26px; display:flex; align-items:center; justify-content:center; gap:8px;
    font-family:var(--head); font-size:11px; color:#fff; letter-spacing:.08em; z-index:1; }
  .roof { background:#15121f; border:6px solid #111; }
  .floorp { background:repeating-linear-gradient(90deg,#b98a5c 0 22px,#a87a4e 22px 24px); border:6px solid #111; }
  .cube .obj { position:absolute; transform-style:preserve-3d; }
  .table-top { width:110px; height:64px; left:-55px; top:-32px; background:#e9e4dd; border-radius:6px; box-shadow:0 0 0 2px #cfc8bf; }
  .mic { width:8px; height:34px; left:-4px; top:-34px; background:#333; border-radius:4px; }
  .lamp { width:36px; height:14px; left:-18px; top:-7px; background:#222; border-radius:0 0 18px 18px; box-shadow:0 12px 40px 12px rgba(255,214,140,.35); }
  .pp { width:34px; height:70px; left:-17px; top:-70px; border-radius:17px 17px 6px 6px; }
  .vent { width:120px; height:26px; left:-60px; top:-13px; background:#2a2638; border:2px solid #3a3550; transition:background .3s, box-shadow .3s; }
  .cam { width:16px; height:12px; left:-8px; top:-6px; background:#444; border-radius:3px; transition:background .3s, box-shadow .3s; }
  .hp-stand { width:10px; height:90px; left:-5px; top:-90px; background:#2b2640; transition:background .3s, box-shadow .3s; }
  .hp-stand::before { content:''; position:absolute; left:-12px; top:-16px; width:34px; height:24px; border:5px solid #6b6388; border-bottom:none; border-radius:18px 18px 0 0; }
  .stage.h-glass .glass { background:linear-gradient(135deg,rgba(94,196,247,.35),rgba(94,196,247,.12)); box-shadow:inset 0 0 40px rgba(94,196,247,.5); }
  .stage.h-air .vent { background:var(--sky); box-shadow:0 0 30px var(--sky); }
  .stage.h-sound .hp-stand { background:var(--violet); box-shadow:0 0 30px var(--violet); }
  .stage.h-sound .hp-stand::before { border-color:#b9a3ff; }
  .stage.h-rec .cam { background:#ff4c4c; box-shadow:0 0 18px #ff4c4c; }
  .feat { display:flex; flex-direction:column; gap:8px; }
  .fb { text-align:left; background:var(--card); border:1.5px solid transparent; border-radius:var(--r-m); padding:20px 22px; cursor:pointer; transition:border-color .2s, background .2s; }
  .fb:hover { border-color:var(--line); }
  .fb.on { border-color:var(--violet); }
  .fb b { display:flex; align-items:center; gap:10px; font-family:var(--head); font-weight:500; font-size:17px; letter-spacing:-.02em; }
  .fb b i { width:10px; height:10px; border-radius:50%; flex:none; }
  .fb p { font-size:14.5px; color:var(--grey2); margin-top:8px; }
  .rule { margin-top:12px; background:#fff4f0; color:#6b2b18; border-radius:var(--r-m); padding:16px 20px; font-size:14.5px; }
  .rule b { color:#c2410c; }

  /* Механизм подкаста */
  .mech { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-top:12px; }
  @media (max-width:960px){ .mech { grid-template-columns:1fr 1fr; } }
  @media (max-width:520px){ .mech { grid-template-columns:1fr; } }
  .mc { background:var(--card); border-radius:var(--r-m); padding:22px; }
  .mc .n { width:40px; height:40px; border-radius:50%; background:var(--sky); color:#fff; font-family:var(--head); display:flex; align-items:center; justify-content:center; font-size:15px; }
  .mc h4 { font-family:var(--head); font-weight:500; font-size:16px; letter-spacing:-.02em; margin:16px 0 6px; }
  .mc p { font-size:14px; color:var(--grey2); }
  .quoteband { margin-top:12px; border:2px solid var(--sky); border-radius:var(--r-l); padding:28px 32px; font-family:var(--head); font-weight:400; font-size:clamp(18px,2.2vw,28px); line-height:1.25; letter-spacing:-.03em; color:#0b8fd0; }
  .quoteband small { display:block; font-family:'Inter',sans-serif; font-size:13px; letter-spacing:0; color:var(--grey); margin-top:12px; }

  /* Город MR: стенд */
  .city-hero { position:relative; border-radius:var(--r-l); overflow:hidden; margin-top:36px; min-height:520px; display:flex; align-items:flex-end; color:#fff; }
  .city-hero img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .city-hero::after { content:''; position:absolute; inset:0; background:linear-gradient(0deg,rgba(9,7,20,.88),rgba(9,7,20,0) 55%); }
  .city-hero .in { position:relative; z-index:2; padding:32px; display:flex; justify-content:space-between; gap:24px; width:100%; flex-wrap:wrap; align-items:flex-end; }
  .city-hero .in p { max-width:34em; color:rgba(255,255,255,.85); }
  .city-hero .tag { position:absolute; right:18px; top:18px; z-index:2; font-size:12px; color:rgba(255,255,255,.75); background:rgba(9,7,20,.4); border-radius:999px; padding:6px 12px; }
  .layout { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px; }
  @media (max-width:960px){ .layout { grid-template-columns:1fr; } }
  .layout svg { width:100%; height:auto; display:block; }
  .zl { display:flex; flex-direction:column; gap:6px; margin-top:6px; }
  .zi { display:flex; gap:14px; padding:14px 16px; border-radius:var(--r-s); cursor:default; transition:background .2s; }
  .zi:hover, .zi.on { background:var(--bg); }
  .zi i { width:12px; height:12px; border-radius:4px; margin-top:6px; flex:none; }
  .zi b { display:block; font-weight:600; }
  .zi span { font-size:14px; color:var(--grey2); }
  .zone { transition:opacity .2s; }
  .layout.hov .zone { opacity:.25; } .layout.hov .zone.on { opacity:1; }

  /* Играбельный прототип */
  .play { margin-top:36px; background:#090714; border-radius:var(--r-xl); padding:40px; color:#fff; }
  @media (max-width:640px){ .play { padding:18px 12px 22px; border-radius:28px; } }
  .play-head { display:flex; justify-content:space-between; gap:20px; flex-wrap:wrap; align-items:flex-end; margin-bottom:26px; }
  .play-head .h2 { color:#fff; }
  .play-head p { color:rgba(255,255,255,.65); max-width:30em; }
  .play-grid { display:grid; grid-template-columns:minmax(0,1.05fr) minmax(0,1fr); gap:18px; align-items:start; }
  @media (max-width:1060px){ .play-grid { grid-template-columns:1fr; } }
  .tablet { background:#1b1726; border-radius:34px; padding:14px; box-shadow:0 30px 80px rgba(117,75,233,.25); }
  .screen { background:#faf8ff; color:var(--ink); border-radius:22px; overflow:hidden; aspect-ratio:4/3.1; min-height:440px; position:relative; }
  @media (max-width:640px){ .screen { aspect-ratio:auto; min-height:560px; } .tablet { padding:8px; border-radius:24px; } }
  .scr { position:absolute; inset:0; display:none; flex-direction:column; padding:20px 22px; overflow:auto; }
  @media (max-width:640px){ .scr { position:relative; padding:16px; } }
  .scr.on { display:flex; animation:scrIn .35s ease; }
  @keyframes scrIn { from { opacity:0; transform:translateY(8px); } }
  .scr-top { display:flex; justify-content:space-between; align-items:center; font-family:var(--head); font-size:12px; color:var(--violet); }
  .dots { display:flex; gap:5px; } .dots i { width:7px; height:7px; border-radius:50%; background:#dcd3fb; } .dots i.on { background:var(--violet); }
  .start { background:linear-gradient(135deg,#6a3fe0,#8a5cf5 60%,#5e36d0); color:#fff; }
  .start .diamonds { position:absolute; inset:0; opacity:.22; background:
     conic-gradient(from 45deg at 50% 50%, #fff 0 25%, transparent 0 50%, #fff 0 75%, transparent 0) 0 0/44px 44px; mask:linear-gradient(180deg,#000,transparent 70%); -webkit-mask:linear-gradient(180deg,#000,transparent 70%); }
  .start .scr-top { color:#fff; position:relative; }
  .start .body { position:relative; margin:auto 0; display:grid; grid-template-columns:1.3fr 1fr; gap:16px; align-items:center; }
  @media (max-width:640px){ .start .body { grid-template-columns:1fr; margin:24px 0 0; } }
  .start h3 { font-family:var(--head); font-weight:500; font-size:clamp(22px,2.4vw,32px); line-height:1.05; letter-spacing:-.04em; margin:12px 0 12px; }
  .start p { font-size:14.5px; color:rgba(255,255,255,.85); }
  .badge-y { display:inline-block; background:#ffd84d; color:var(--ink); font-family:var(--head); font-size:11px; border-radius:999px; padding:6px 10px; }
  .gbtn { display:inline-flex; align-items:center; justify-content:center; gap:8px; border:0; border-radius:999px; padding:14px 26px; font-weight:600; font-size:15px; cursor:pointer; transition:transform .15s, background .15s; }
  .gbtn:active { transform:scale(.97); }
  .gbtn.go { background:var(--mint); color:#fff; } .gbtn.go:hover { background:#25a95e; }
  .gbtn.v { background:var(--violet); color:#fff; } .gbtn.v:hover { background:var(--violet-d); }
  .gbtn.o { background:#fff; color:var(--violet); box-shadow:inset 0 0 0 2px var(--violet); }
  .gbtn[disabled] { opacity:.4; pointer-events:none; }
  .consent { font-size:11.5px; color:rgba(255,255,255,.65); margin-top:14px; }
  .ctor { flex:1; display:grid; grid-template-columns:.8fr 1.2fr; gap:16px; margin-top:12px; min-height:0; }
  @media (max-width:640px){ .ctor { grid-template-columns:1fr; } }
  .preview { background:linear-gradient(180deg,#efe9ff,#e2f5ec); border-radius:18px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:10px; position:relative; }
  .preview svg { width:78%; max-width:170px; height:auto; }
  .namebox { width:100%; background:#fff; border-radius:12px; padding:8px 10px; display:flex; gap:8px; align-items:center; margin-top:6px; }
  .namebox small { display:block; font-size:10px; color:var(--grey); }
  .namebox input { border:0; outline:none; font:inherit; font-weight:700; font-size:15px; width:100%; background:transparent; }
  .opts h4 { font-family:var(--head); font-weight:500; font-size:18px; letter-spacing:-.03em; }
  .tabs { display:flex; flex-wrap:wrap; gap:5px; margin:10px 0 12px; }
  .tabs button { border:0; background:var(--violet-l); color:var(--violet); border-radius:999px; font-size:11.5px; font-weight:600; padding:6px 10px; cursor:pointer; text-transform:uppercase; letter-spacing:.04em; }
  .tabs button.on { background:var(--violet); color:#fff; }
  .choices { display:flex; flex-wrap:wrap; gap:8px; }
  .choices button { width:48px; height:48px; border-radius:12px; border:2px solid transparent; background:#fff; box-shadow:0 1px 0 #e6e0f5; cursor:pointer; padding:4px; display:flex; align-items:center; justify-content:center; }
  .choices button.on { border-color:var(--violet); }
  .choices button svg { width:100%; height:100%; }
  .choices button.sw { border-radius:50%; width:38px; height:38px; }
  .ctor-foot { display:flex; justify-content:flex-end; gap:8px; margin-top:auto; padding-top:12px; }
  .q-title { font-family:var(--head); font-weight:500; font-size:clamp(18px,2.2vw,26px); letter-spacing:-.035em; line-height:1.15; margin:14px 0 16px; max-width:18em; }
  .q-badge { display:inline-block; background:var(--violet-l); color:var(--violet); border-radius:999px; font-size:11px; font-weight:700; padding:5px 10px; letter-spacing:.04em; }
  .answers { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
  @media (max-width:640px){ .answers { grid-template-columns:1fr 1fr; } }
  .ans { background:#fff; border:2px solid #ece6fb; border-radius:16px; padding:14px 8px 12px; cursor:pointer; display:flex; flex-direction:column; align-items:center; gap:10px; font-weight:600; font-size:13px; text-align:center; transition:border-color .15s, transform .15s; }
  .ans:hover { transform:translateY(-2px); }
  .ans.on { border-color:var(--mint); }
  .ans svg { width:54px; height:54px; }
  .q-mini { position:absolute; right:18px; bottom:14px; width:64px; }
  @media (max-width:640px){ .q-mini { display:none; } }
  .result { flex:1; display:grid; grid-template-columns:.75fr 1.25fr; gap:14px; margin-top:10px; align-items:center; }
  @media (max-width:640px){ .result { grid-template-columns:1fr; } }
  .result .av { background:radial-gradient(circle at 50% 45%,#fff 0 55%,transparent 56%),linear-gradient(180deg,#efe9ff,#e2f5ec); border-radius:18px; display:flex; align-items:center; justify-content:center; padding:10px; min-height:200px; }
  .result .av svg { width:70%; max-width:150px; }
  .ok-badge { display:inline-block; background:var(--mint); color:#fff; font-size:11px; font-weight:700; border-radius:999px; padding:5px 10px; letter-spacing:.04em; }
  .result h3 { font-family:var(--head); font-weight:500; font-size:clamp(18px,1.9vw,24px); letter-spacing:-.04em; line-height:1.1; margin:8px 0 10px; }
  .rgrid { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
  .rgrid div { background:#fff; border-radius:12px; padding:8px 11px; box-shadow:0 1px 0 #ece6fb; }
  .rgrid b { font-size:13.5px; line-height:1.3; display:block; }
  .rgrid .w { grid-column:span 2; }
  .rgrid small { display:block; font-size:10.5px; color:var(--grey); }
  .rgrid b { font-size:14px; }
  .rgrid p { font-size:12.5px; color:var(--grey2); margin-top:4px; }

  /* Карта города */
  .map { position:relative; border-radius:24px; overflow:hidden; background:#cde; }
  .map-in { position:relative; transition:transform 1.1s cubic-bezier(.4,0,.2,1); }
  .map img { width:100%; height:auto; display:block; }
  @media (max-width:640px){ .map .tag { display:none; } }
  .map .tag { position:absolute; left:12px; top:12px; font-size:11.5px; color:#fff; background:rgba(9,7,20,.55); border-radius:999px; padding:6px 11px; z-index:3; }
  .res { position:absolute; transform:translate(-50%,-100%) scale(var(--inv,1)); transform-origin:50% 100%; transition:transform 1.1s cubic-bezier(.4,0,.2,1); display:flex; flex-direction:column; align-items:center; z-index:2; pointer-events:none; }
  .res .g { width:14px; height:20px; clip-path:polygon(50% 0,100% 38%,50% 100%,0 38%); animation:bob 2.2s ease-in-out infinite; }
  @keyframes bob { 50% { transform:translateY(-4px); } }
  .res .chip { margin-top:3px; color:var(--ink); background:#fff; border-radius:999px; font-size:11px; font-weight:700; padding:3px 9px; box-shadow:0 2px 8px rgba(0,0,0,.2); white-space:nowrap; }
  .res.me { z-index:4; }
  .res.me .chip { background:var(--violet); color:#fff; font-size:12.5px; padding:5px 11px; }
  .res.me .g { width:20px; height:28px; }
  .res.me::after { content:''; position:absolute; bottom:-10px; left:50%; width:70px; height:26px; margin-left:-35px; border-radius:50%; border:3px solid #fff; animation:ring 1.4s ease-out infinite; }
  @keyframes ring { from { transform:scale(.4); opacity:1; } to { transform:scale(1.6); opacity:0; } }
  .res.drop { animation:drop .9s cubic-bezier(.2,1.4,.4,1); }
  @keyframes drop { from { transform:translate(-50%,-400%) scale(var(--inv,1)); opacity:0; } }
  .map-count { position:absolute; right:12px; top:12px; z-index:3; color:var(--ink); background:#fff; border-radius:14px; padding:8px 12px; font-size:12px; box-shadow:0 4px 14px rgba(0,0,0,.15); }
  .map-count b { font-family:var(--head); font-size:18px; display:block; line-height:1.1; transition:color .3s; }
  .map-count.bump b { color:var(--violet); }
  .map-count .plus { position:absolute; right:10px; top:-6px; font-family:var(--head); font-size:14px; color:var(--mint); opacity:0; pointer-events:none; }
  .map-count.bump .plus { animation:plus 1.2s ease-out; }
  @keyframes plus { 0% { opacity:0; transform:translateY(10px); } 25% { opacity:1; } 100% { opacity:0; transform:translateY(-22px); } }
  .res.other .chip { background:#f2eefe; }

  /* Открытка 10×15 */
  .pc-wrap { margin-top:14px; display:grid; grid-template-columns:1fr auto; gap:14px; align-items:center; }
  @media (max-width:640px){ .pc-wrap { grid-template-columns:1fr; } }
  .postcard { display:grid; grid-template-columns:1fr 1.15fr; aspect-ratio:3/2; border-radius:10px; overflow:hidden; background:#fff; color:var(--ink); box-shadow:0 18px 50px rgba(0,0,0,.4); transform:rotate(-1.2deg); transition:transform .4s; }
  .postcard:hover { transform:rotate(0); }
  .postcard.print { animation:print 1.3s ease; }
  @keyframes print { from { clip-path:inset(0 0 100% 0); } to { clip-path:inset(0 0 0 0); } }
  .pc-l { background:radial-gradient(circle at 50% 56%,rgba(255,255,255,.92) 0 34%,rgba(255,255,255,.18) 35% 44%,transparent 45%),linear-gradient(160deg,#6a3fe0,#8a5cf5); position:relative; display:flex; align-items:center; justify-content:center; padding:10px; }
  .pc-l::before { content:'MR · город'; position:absolute; left:10px; top:8px; font-family:var(--head); font-size:9.5px; color:#fff; }
  .pc-l svg { width:74%; max-width:130px; }
  .pc-r { padding:12px 14px; display:flex; flex-direction:column; }
  .pc-r .no { align-self:flex-start; background:var(--violet-l); color:var(--violet); font-size:9px; font-weight:700; border-radius:999px; padding:3px 8px; }
  .pc-r h5 { font-family:var(--head); font-weight:500; font-size:clamp(18px,2.2vw,26px); letter-spacing:-.04em; margin-top:6px; line-height:1; }
  .pc-r .pr { color:var(--violet); font-weight:700; font-size:11px; margin-top:4px; }
  .pc-r p { font-size:10.5px; margin-top:6px; }
  .pc-r .ft { margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end; }
  .pc-r .ft b { color:var(--mint); font-family:var(--head); font-weight:500; font-size:11px; }
  .pc-r .ft svg { width:44px; height:44px; }
  .pc-note { font-size:13px; color:rgba(255,255,255,.6); max-width:15em; }
  .pc-note .gbtn { margin-top:10px; }
  .play-foot { margin-top:18px; font-size:12.5px; color:rgba(255,255,255,.45); }

  /* Путь гостя */
  .path { display:grid; grid-template-columns:repeat(8,1fr); gap:8px; margin-top:36px; }
  @media (max-width:1100px){ .path { grid-template-columns:repeat(4,1fr); } }
  @media (max-width:560px){ .path { grid-template-columns:1fr 1fr; } }
  .ps { background:var(--card); border-radius:var(--r-m); padding:18px 16px; display:flex; flex-direction:column; min-height:190px; }
  .ps .n { font-family:var(--head); font-size:30px; line-height:1; color:var(--violet); letter-spacing:-.04em; }
  .ps:nth-child(even) .n { color:var(--sky); }
  .ps b { font-family:var(--head); font-weight:500; font-size:14.5px; letter-spacing:-.02em; margin-top:18px; }
  .ps span { font-size:13px; color:var(--grey2); margin-top:4px; }
  .ps em { font-style:normal; margin-top:auto; padding-top:12px; font-size:12px; font-weight:700; color:var(--violet); }
  .timebar { margin-top:10px; display:flex; height:10px; border-radius:999px; overflow:hidden; background:var(--line); }
  .timebar i { display:block; height:100%; }
  .timecap { display:flex; justify-content:space-between; font-size:12.5px; color:var(--grey); margin-top:8px; }

  /* Ромбы */
  .gems { display:grid; grid-template-columns:1.6fr 1fr; gap:12px; margin-top:36px; }
  @media (max-width:960px){ .gems { grid-template-columns:1fr; } }
  .gems .big { position:relative; border-radius:var(--r-l); overflow:hidden; min-height:460px; }
  .gems .big img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .gems .big::after { content:''; position:absolute; inset:0; background:linear-gradient(0deg,rgba(9,7,20,.85),transparent 50%); }
  .gems .big .in { position:absolute; left:28px; right:28px; bottom:26px; z-index:2; color:#fff; }
  .gems .big .in .h3 { font-size:clamp(22px,2.6vw,34px); }
  .gems .col { display:grid; grid-template-rows:1fr 1fr; gap:12px; }
  .gems .col div { position:relative; border-radius:var(--r-l); overflow:hidden; min-height:220px; }
  .gems .col img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .gems .col span { position:absolute; left:16px; bottom:14px; right:16px; color:#fff; font-size:14px; z-index:2; text-shadow:0 1px 10px rgba(0,0,0,.6); }
  .viz { position:absolute; right:14px; top:14px; z-index:2; font-size:11.5px; color:#fff; background:rgba(9,7,20,.45); border-radius:999px; padding:5px 10px; }

  /* Колонки данных и надёжности */
  .cols3 { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:36px; }
  .cols4 { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:12px; }
  @media (max-width:960px){ .cols3, .cols4 { grid-template-columns:1fr 1fr; } }
  @media (max-width:560px){ .cols3, .cols4 { grid-template-columns:1fr; } }
  .cl { background:var(--card); border-radius:var(--r-m); padding:24px; }
  .cl h4 { font-family:var(--head); font-weight:500; font-size:17px; letter-spacing:-.02em; margin-bottom:14px; }
  .cl ul { list-style:none; display:flex; flex-direction:column; gap:9px; }
  .cl li { font-size:14.5px; color:var(--grey2); padding-left:20px; position:relative; }
  .cl li::before { content:''; position:absolute; left:2px; top:7px; width:9px; height:11px; background:var(--violet); clip-path:polygon(50% 0,100% 38%,50% 100%,0 38%); }
  .cl.dark { background:#090714; color:#fff; }
  .cl.dark p { color:rgba(255,255,255,.7); font-size:14.5px; }
  .cl.dark h4 { color:#b9a3ff; }
  .note { margin-top:14px; font-size:14.5px; color:var(--grey2); }

  /* Правила площадки */
  .rules { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:36px; }
  @media (max-width:960px){ .rules { grid-template-columns:1fr 1fr; } }
  @media (max-width:560px){ .rules { grid-template-columns:1fr; } }
  .ru { background:var(--card); border-radius:var(--r-m); padding:22px 22px 20px; display:flex; flex-direction:column; gap:8px; }
  .ru .src { font-size:12.5px; color:var(--grey); }
  .ru h4 { font-family:var(--head); font-weight:500; font-size:16.5px; letter-spacing:-.02em; line-height:1.3; }
  .ru p { font-size:14.5px; color:var(--grey2); }
  .ru p b { color:var(--ink); }
  .ru.hot { background:var(--violet); color:#fff; } .ru.hot p, .ru.hot .src { color:rgba(255,255,255,.8); } .ru.hot p b { color:#fff; }

  /* График */
  .tl { margin-top:36px; background:var(--card); border-radius:var(--r-l); padding:28px 32px; }
  @media (max-width:640px){ .tl { padding:20px 16px; } }
  .tl-bar { position:relative; height:64px; margin:0 6px; }
  .tl-bar .axis { position:absolute; left:0; right:0; top:30px; height:4px; background:var(--line); border-radius:4px; }
  .tl-bar .seg { position:absolute; top:26px; height:12px; border-radius:6px; }
  .tl-bar .mk { position:absolute; top:0; transform:translateX(-50%); font-size:11.5px; color:var(--grey); white-space:nowrap; }
  .tl-bar .today { position:absolute; top:18px; width:2px; height:30px; background:var(--ink); }
  .tl-bar .today::after { content:'сегодня'; position:absolute; top:32px; left:50%; transform:translateX(-50%); font-size:11px; font-weight:700; }
  .tl-rows { margin-top:26px; display:flex; flex-direction:column; }
  .tr { display:grid; grid-template-columns:200px 1fr; gap:18px; padding:14px 0; border-top:1px solid var(--line); align-items:baseline; }
  @media (max-width:640px){ .tr { grid-template-columns:1fr; gap:4px; } }
  .tr b { font-family:var(--head); font-weight:500; font-size:15px; letter-spacing:-.02em; display:flex; gap:10px; align-items:center; }
  .tr b i { width:10px; height:10px; border-radius:50%; }
  .tr span { font-size:15px; color:var(--grey2); }

  /* Кто что делает */
  .split { display:grid; grid-template-columns:1.4fr 1fr; gap:12px; margin-top:36px; }
  @media (max-width:900px){ .split { grid-template-columns:1fr; } }
  .split .cl li { color:var(--ink); }
  .split .mr { background:var(--sky-l); }
  .split .mr li::before { background:var(--sky); }
  .split .mr .deadline { margin-top:18px; font-family:var(--head); font-weight:500; font-size:15px; }

  /* Доказательства */
  .proof { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:36px; }
  @media (max-width:960px){ .proof { grid-template-columns:1fr; } }
  .pf { background:var(--card); border-radius:var(--r-m); overflow:hidden; text-decoration:none; display:flex; flex-direction:column; transition:transform .2s; }
  .pf:hover { transform:translateY(-4px); }
  .pf img { width:100%; aspect-ratio:16/10; object-fit:cover; }
  .pf .bd { padding:20px 22px 22px; }
  .pf .k { font-size:12.5px; color:var(--violet); font-weight:600; }
  .pf h4 { font-family:var(--head); font-weight:500; font-size:17px; letter-spacing:-.02em; margin:6px 0 8px; line-height:1.25; }
  .pf p { font-size:14px; color:var(--grey2); }
  .quotes { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:12px; }
  @media (max-width:960px){ .quotes { grid-template-columns:1fr; } }
  .qt { background:var(--card); border-radius:var(--r-m); padding:24px; font-size:15.5px; }
  .qt.v { background:var(--violet); color:#fff; }
  .qt span { display:block; margin-top:14px; font-size:13px; color:var(--grey); }
  .qt.v span { color:rgba(255,255,255,.7); }


  /* Креатив и видео */
  .crg { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:36px; }
  @media (max-width:960px){ .crg { grid-template-columns:1fr 1fr; } }
  @media (max-width:560px){ .crg { grid-template-columns:1fr; } }
  .cr { background:var(--card); border-radius:var(--r-m); overflow:hidden; text-decoration:none; display:flex; flex-direction:column; transition:transform .25s; }
  .cr:hover { transform:translateY(-4px); }
  .cr .im { aspect-ratio:4/3; overflow:hidden; background:#eee; }
  .cr .im img { width:100%; height:100%; object-fit:cover; transition:transform .5s; }
  .cr:hover .im img { transform:scale(1.04); }
  .cr .bd, .vcard .bd { padding:20px 22px 22px; }
  .cr .k, .vcard .k { font-size:12.5px; color:var(--violet); font-weight:600; }
  .cr h4, .vcard h4 { font-family:var(--head); font-weight:500; font-size:17px; letter-spacing:-.02em; margin:6px 0 8px; line-height:1.25; }
  .cr p, .vcard p { font-size:14px; color:var(--grey2); }
  @media (min-width:961px){ .cr.w { grid-column:span 2; } .cr.w .im { aspect-ratio:auto; height:100%; max-height:340px; } }
  .vids { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:36px; }
  @media (max-width:900px){ .vids { grid-template-columns:1fr; } }
  .vcard { background:var(--card); border-radius:var(--r-l); overflow:hidden; }
  .vid { position:relative; aspect-ratio:16/9; background:#000; cursor:pointer; }
  .vid img, .vid video { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .vid::after { content:''; position:absolute; inset:0; background:linear-gradient(0deg,rgba(9,7,20,.55),transparent 55%); pointer-events:none; }
  .vid .vplay { position:absolute; left:20px; bottom:18px; z-index:2; display:flex; align-items:center; gap:12px; color:#fff; font-weight:600; }
  .vid .vplay i { width:54px; height:54px; border-radius:50%; background:#fff; display:flex; align-items:center; justify-content:center; transition:transform .2s; }
  .vid:hover .vplay i { transform:scale(1.08); }
  .vid.playing::after, .vid.playing .vplay { display:none; }
  .link { display:inline-block; margin-top:12px; color:var(--violet); font-weight:600; font-size:14.5px; text-decoration:none; }

  /* Кнопка PDF */
  .pdf-btn { display:inline-flex; align-items:center; gap:14px; background:var(--violet); color:#fff; text-decoration:none; border-radius:999px;
    padding:20px 34px 20px 28px; font-weight:600; font-size:18px; box-shadow:0 14px 40px rgba(117,75,233,.45); transition:background .15s, transform .15s; }
  .pdf-btn:hover { background:var(--violet-d); transform:translateY(-2px); }
  .pdf-btn small { display:block; font-weight:400; font-size:12.5px; opacity:.75; margin-top:2px; }
  .hero-pdf { margin-top:26px; }
  @media (max-width:640px){ .pdf-btn { width:100%; justify-content:center; font-size:17px; padding:18px 22px; } }

  /* Печать и PDF: всё раскрыто, без анимаций и навигации, блоки не рвутся */
  @media print {
    @page { margin:0; }
    html, body { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
    .rv-in { opacity:1 !important; transform:none !important; }
    .top .nav, .pdf-btn, .hero-pdf, .city-hero .gbtn, .stage .hint, .play-foot + *, #again { display:none !important; }
    .hero { min-height:880px; }
    .hero > img, .res .g, .final .big-gem, .dash, .res.me::after { animation:none !important; }
    .card, .cl, .ru, .mc, .ps, .cr, .vcard, .pf, .qt, .fb, .li, .zi, .task, .cube-wrap, .city-hero, .layout, .play, .gems, .tl, .split, .rules, .proof, .quotes, .crg, .vids, .mech, .quoteband, .path { break-inside:avoid; }
    section { break-inside:avoid; padding-top:72px; }
    .eyebrow, .h2, .lead { break-after:avoid; }
    .final { break-inside:avoid; margin-top:72px; }
  }
  /* Финал */
  .final { margin-top:96px; background:#090714; color:#fff; border-radius:var(--r-xl) var(--r-xl) 0 0; padding:88px 0 40px; position:relative; overflow:hidden; }
  .final .big-gem { position:absolute; right:-40px; top:40px; width:360px; height:480px; background:linear-gradient(160deg,#9d7cff,#754be9 45%,#3b1fa0); clip-path:polygon(50% 0,100% 38%,50% 100%,0 38%); opacity:.9; animation:bob 5s ease-in-out infinite; }
  @media (max-width:900px){ .final .big-gem { width:180px; height:240px; right:-30px; top:20px; opacity:.5; } }
  .final h2 { font-family:var(--head); font-weight:500; font-size:clamp(34px,6vw,84px); line-height:.98; letter-spacing:-.05em; max-width:10em; position:relative; }
  .final .lead { color:rgba(255,255,255,.72); position:relative; }
  .person { display:flex; gap:16px; align-items:center; margin-top:40px; position:relative; }
  .person .av { width:60px; height:60px; border-radius:50%; background:var(--violet); display:flex; align-items:center; justify-content:center; font-family:var(--head); font-size:18px; }
  .person b { display:block; font-size:18px; font-weight:600; } .person span { color:rgba(255,255,255,.6); font-size:14px; }
  .cts { display:flex; flex-wrap:wrap; gap:8px; margin-top:24px; position:relative; }
  .cts a { display:inline-flex; gap:10px; align-items:center; text-decoration:none; border:1.5px solid rgba(255,255,255,.22); border-radius:999px; padding:14px 20px; font-size:15px; transition:background .15s, color .15s; }
  .cts a:hover { background:#fff; color:var(--ink); }
  .cts svg { width:17px; height:17px; }
  .foot { margin-top:64px; padding-top:24px; border-top:1px solid rgba(255,255,255,.12); display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; font-size:12.5px; color:rgba(255,255,255,.5); position:relative; }

  .rv-in { opacity:0; transform:translateY(22px); transition:opacity .7s ease, transform .7s ease; }
  .rv-in.vis { opacity:1; transform:none; }
  @media (prefers-reduced-motion:reduce){ .rv-in { opacity:1; transform:none; transition:none; } .hero > img, .res .g, .final .big-gem, .dash { animation:none; } html { scroll-behavior:auto; } }
</style>
</head>
<body>

<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="https://hand-marketing.ru/" target="_blank" rel="noopener">
      <svg viewBox="0 0 43 28" aria-label="MR"><path fill="currentColor" d="M6.40114 2.62744L13.8561 19.0357L21.1274 2.62744H33.2125C35.6477 2.62761 37.6628 3.30835 39.2863 4.67292C40.9437 6.00574 41.7558 7.69525 41.7559 9.70888C41.7559 11.7227 40.9438 13.4123 39.2863 14.7772C38.0071 15.8265 36.4856 16.4704 34.7067 16.6974H37.7436L42.6322 25.368H37.1439L32.318 16.6974H26.5329V25.368H21.5615V6.92235L13.3897 25.368H11.0514L2.59893 6.76485V25.368H0.486816V2.62744H6.40114ZM26.5329 4.83244V14.5873H31.5527C34.2322 14.5873 36.0071 12.6641 36.0071 9.70888C36.007 6.7539 34.2321 4.83245 31.5527 4.83244H26.5329Z"/></svg>
      <i></i>
      <img src="hm-logo.svg" alt="Hand Marketing">
    </a>
    <nav class="nav">
      <a href="#hall">Зал</a>
      <a href="#podcast">Подкаст-куб</a>
      <a href="#city">Город MR</a>
      <a href="#play">Сыграть</a>
      <a href="#venue">Площадка</a>
      <a href="#plan">График</a>
      <a href="#creative">Работы</a>
      <a href="#contact">Контакты</a>
    </nav>
  </div>
</header>

<section class="hero">
  <img src="img/stand-city.jpg" alt="Визуализация стенда «Город MR»">
  <div class="wrap hero-in">
    <span class="pill"><span class="gem"></span>MR · «Наша школа» 2026 · Гостиный двор · 24–26 ноября</span>
    <h1>Два стенда,<br>одна история <span>MR</span></h1>
    <div class="hero-row">
      <p>Подкаст-студия в прозрачном кубе и игра, после которой гость живёт в проекте MR. Стоят через проход друг от друга и работают как одна экспозиция. Здесь то, как мы их построим, нарисуем и запустим. Игру можно пройти прямо на этой странице.</p>
      <div class="hero-stands">
        <a class="hs" href="#podcast"><small>стенд C7.2</small><b>Подкаст-куб</b><span>разговоры с лидерами отрасли</span></a>
        <a class="hs" href="#city"><small>стенд C8.1</small><b>Город MR</b><span>игра на 5 минут</span></a>
      </div>
    </div>
    <div class="hero-pdf"><a class="pdf-btn" href="?pdf=1" download><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5M4 19h16"/></svg><span>Скачать PDF<small>чтобы распечатать или открыть без интернета</small></span></a></div>
  </div>
</section>

<!-- Задача -->
<section>
  <div class="wrap">
    <div class="eyebrow"><b>01</b> задача MR</div>
    <h2 class="h2">MR, генеральный спонсор <em>X фестиваля</em> «Наша школа»</h2>
    <div class="task">
      <div class="ph rv-in"><img src="img/mr-edu.jpg" alt="MR Образование"><span class="pill s">MR Образование</span></div>
      <div class="card rv-in">
        <h3 class="h3">Кто придёт на стенды</h3>
        <p class="lead" style="font-size:16px;margin-top:10px">Фестиваль о проектировании и строительстве школ, садов и образовательной среды. Гостям не нужна реклама квартир. Им нужна история, в которой MR строит не только дома, но и то, где учатся.</p>
        <div class="aud">
          <span>органы власти</span><span>архитекторы и бюро</span><span>проектные институты</span><span>студенты профильных вузов</span><span>девелоперы</span><span>edtech и оснащение школ</span>
        </div>
        <div class="kpis">
          <div><b>3 дня</b><span>24–26 ноября, 10:00–20:00</span></div>
          <div><b>2 × 11 м²</b><span>стенды C7.2 и C8.1 через проход</span></div>
          <div><b>400</b><span>историй жителей, цель MR на фестиваль</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Схема зала -->
<section id="hall">
  <div class="wrap">
    <div class="eyebrow"><b>02</b> идея</div>
    <h2 class="h2">Два стенда через проход работают <em>как одна экспозиция</em></h2>
    <div class="card rv-in" style="margin-top:36px">
      <div class="hall">
        <svg viewBox="0 0 620 460" role="img" aria-label="Схема стендов C7.2 и C8.1 в зале Гостиного двора">
          <defs>
            <pattern id="gridp" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#ecebf0" stroke-width="1"/></pattern>
          </defs>
          <rect width="620" height="460" rx="24" fill="#f7f7f9"/>
          <rect width="620" height="460" rx="24" fill="url(#gridp)"/>
          <!-- проходы под 45°, как на плане фестиваля -->
          <g transform="translate(310 230) rotate(45)">
            <rect x="-400" y="-26" width="800" height="52" fill="#fff"/>
            <rect x="-26" y="-400" width="52" height="800" fill="#fff"/>
            <!-- соседние стенды -->
            <rect x="-150" y="-150" width="110" height="110" fill="#e9e7ef"/>
            <rect x="40" y="40" width="110" height="110" fill="#e9e7ef"/>
            <rect x="-150" y="40" width="54" height="110" fill="#e9e7ef"/>
            <!-- C7.2: подкаст-куб -->
            <g class="st" data-go="podcast">
              <rect x="-94" y="40" width="54" height="110" rx="4" fill="#5ec4f7"/>
              <rect x="-86" y="62" width="38" height="38" rx="3" fill="#fff" fill-opacity=".35" stroke="#fff" stroke-width="2"/>
            </g>
            <!-- C8.1: город MR -->
            <g class="st" data-go="city">
              <rect x="40" y="-150" width="110" height="110" rx="4" fill="#754be9"/>
              <rect x="50" y="-144" width="90" height="10" rx="2" fill="#fff" fill-opacity=".9"/>
              <rect x="50" y="-120" width="14" height="14" rx="3" fill="#2dbe6c"/><rect x="126" y="-120" width="14" height="14" rx="3" fill="#2dbe6c"/>
              <rect x="50" y="-90" width="14" height="14" rx="3" fill="#2dbe6c"/><rect x="126" y="-90" width="14" height="14" rx="3" fill="#2dbe6c"/>
              <rect x="78" y="-62" width="34" height="14" rx="3" fill="#ffb020"/>
            </g>
          </g>
          <!-- линия взгляда: экран города виден из куба -->
          <path class="dash" d="M250 300 C 300 250, 340 200, 395 150" fill="none" stroke="#754be9" stroke-width="2.5"/>
          <circle cx="395" cy="150" r="5" fill="#754be9"/>
          <g font-family="Inter,sans-serif" font-size="13" font-weight="600">
            <rect x="120" y="330" width="150" height="46" rx="12" fill="#090714"/>
            <text x="134" y="351" fill="#5ec4f7">C7.2</text><text x="134" y="367" fill="#fff" font-weight="500" font-size="12">подкаст-куб</text>
            <rect x="420" y="70" width="150" height="46" rx="12" fill="#090714"/>
            <text x="434" y="91" fill="#b9a3ff">C8.1</text><text x="434" y="107" fill="#fff" font-weight="500" font-size="12">город MR</text>
            <text x="360" y="265" fill="#8e9099" font-weight="500" font-size="12" transform="rotate(-45 360 265)">проход</text>
          </g>
          <text x="24" y="440" font-family="Inter,sans-serif" font-size="11.5" fill="#8e9099">Схема по плану фестиваля «Наша школа 2026», стенды по 11 м²</text>
        </svg>
        <div>
          <p class="lead" style="margin-top:0">Экран города виден из куба. Гости подкаста тоже проходят игру и появляются в городе с отметкой. Одна айдентика, один ромб, одна история MR на обе стороны прохода.</p>
          <div class="legend-list">
            <a class="li" href="#podcast"><span class="n" style="background:#5ec4f7">C7.2</span><div><b>Подкаст-студия</b><span>Прозрачный куб, где идут разговоры с лидерами отрасли. Гость уходит с готовым выпуском.</span></div></a>
            <a class="li" href="#city"><span class="n" style="background:#754be9">C8.1</span><div><b>Город MR</b><span>Гость создаёт жителя и переезжает в проект MR. Уходит с открыткой и ободком с ромбом.</span></div></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Подкаст-куб -->
<section id="podcast">
  <div class="wrap">
    <div class="eyebrow"><b>03</b> стенд C7.2 · подкаст-студия</div>
    <h2 class="h2">Прозрачный куб, <i>в котором тихо</i></h2>
    <p class="lead">Люди останавливаются посмотреть, кто в кубе. Разговор слышно в наушниках у стенда. Гость уходит с видео, аудио и короткими роликами для своих соцсетей.</p>
    <div class="cube-wrap">
      <div class="stage rv-in" id="stage">
        <span class="hint">потяните, чтобы повернуть · схема, не рендер</span>
        <div class="floor-shadow"></div>
        <div class="cube" id="cube">
          <div class="f floorp" style="transform:rotateX(90deg) translateZ(-120px)"></div>
          <div class="f roof" style="transform:rotateX(90deg) translateZ(120px)"></div>
          <div class="f glass" style="transform:translateZ(120px)"><div class="brandband"><span class="gem" style="width:9px;height:12px;background:#fff"></span>MR · ПОДКАСТ</div></div>
          <div class="f glass" style="transform:rotateY(180deg) translateZ(120px)"></div>
          <div class="f glass" style="transform:rotateY(90deg) translateZ(120px)"><div class="brandband">НАША ШКОЛА</div></div>
          <div class="f glass" style="transform:rotateY(-90deg) translateZ(120px)"></div>
          <!-- внутри -->
          <div class="obj" style="transform:translateY(50px) rotateX(90deg)"><div class="obj table-top"></div></div>
          <div class="obj" style="transform:translateY(50px) translateZ(0)"><div class="obj mic"></div></div>
          <div class="obj" style="transform:translate3d(-62px,118px,0) rotateY(90deg)"><div class="obj pp" style="background:#754be9"></div></div>
          <div class="obj" style="transform:translate3d(62px,118px,0) rotateY(90deg)"><div class="obj pp" style="background:#5ec4f7"></div></div>
          <div class="obj" style="transform:translateY(-104px)"><div class="obj lamp"></div></div>
          <!-- камеры в углах -->
          <div class="obj" style="transform:translate3d(-105px,-95px,105px) rotateY(45deg)"><div class="obj cam"></div></div>
          <div class="obj" style="transform:translate3d(105px,-95px,105px) rotateY(-45deg)"><div class="obj cam"></div></div>
          <div class="obj" style="transform:translate3d(0,-95px,-110px)"><div class="obj cam"></div></div>
          <!-- вентиляция за задней стенкой -->
          <div class="obj" style="transform:translate3d(0,-100px,-130px)"><div class="obj vent"></div></div>
          <!-- стойка с наушниками у стенда -->
          <div class="obj" style="transform:translate3d(170px,120px,120px)"><div class="obj hp-stand"></div></div>
          <div class="obj" style="transform:translate3d(-170px,120px,120px)"><div class="obj hp-stand"></div></div>
        </div>
      </div>
      <div class="feat rv-in">
        <button class="fb on" data-h="glass"><b><i style="background:#5ec4f7"></i>Стекло и тишина</b><p>Двойное остекление, закрытый потолок, плавающий пол. Внутри тихо настолько, что запись звучит как студийная, а снаружи куб остаётся прозрачным.</p></button>
        <button class="fb" data-h="air"><b><i style="background:#2dbe6c"></i>Воздух без шума</b><p>Вентиляция вынесена за стенку куба и идёт через глушители. Внутри свежо весь день, в микрофонах вентиляторов не слышно.</p></button>
        <button class="fb" data-h="sound"><b><i style="background:#754be9"></i>Звук для зрителей</b><p>Разговор идёт в беспроводные наушники у стенда: слышно каждое слово, соседи не мешают.</p></button>
        <button class="fb" data-h="rec"><b><i style="background:#ff4c4c"></i>Выпуск в тот же день</b><p>Три камеры, эфирные микрофоны, монтажёр на стенде. Гость уходит с видео, аудио и короткими роликами.</p></button>
        <div class="rule"><b>Правило Гостиного двора:</b> мероприятия со звуком на стендах запрещены, штраф 25 000 ₽. Поэтому звук только в наушниках. Такую схему мы уже ставили на стенде Самарской области на ВДНХ, где на одной площади шли разные программы.</div>
      </div>
    </div>
    <div class="mech">
      <div class="mc rv-in"><div class="n">1</div><h4>Программа заранее</h4><p>Приглашаем спикеров, утверждаем темы и расписание. Записи в часы пик по трафику зала, без импровизации.</p></div>
      <div class="mc rv-in"><div class="n">2</div><h4>Запись с героем</h4><p>Ведущие из «Москвы глазами инженера» меняются по графику. Зрители слушают в наушниках.</p></div>
      <div class="mc rv-in"><div class="n">3</div><h4>Файлы сразу</h4><p>После записи гость получает аудио, видео из брендированного куба и короткие ролики.</p></div>
      <div class="mc rv-in"><div class="n">4</div><h4>Гость публикует сам</h4><p>Telegram, соцсети, сайт компании. Контент расходится по 10–15 каналам участников.</p></div>
    </div>
    <div class="quoteband rv-in">Мы не распространяем контент сами. Мы создаём площадку, а участники распространяют его на своих платформах.<small>Из концепции MR для стенда C7.2</small></div>
  </div>
</section>

<!-- Город MR -->
<section id="city">
  <div class="wrap">
    <div class="eyebrow"><b>04</b> стенд C8.1 · город MR</div>
    <h2 class="h2">Игра, после которой гость <em>живёт в проекте MR</em></h2>
    <p class="lead">Гость не читает про проекты, а получает свой: дом, школу, сад или факультет ВШЭ и историю жизни в них. Пять минут у стенда заканчиваются предметом, который он уносит с собой.</p>
    <div class="city-hero rv-in">
      <img src="img/family.jpg" alt="Гости у игровой станции-домика" loading="lazy">
      <span class="tag">Визуализация</span>
      <div class="in">
        <div><div class="h3">Весь стенд работает как один игровой город</div><p style="margin-top:10px">Экран с живой картой, четыре станции-домика, стойка выдачи у прохода и светящийся ромб, который видно с другого конца зала.</p></div>
        <a class="gbtn go" href="#play">Сыграть сейчас ↓</a>
      </div>
    </div>
    <div class="layout" id="layout">
      <div class="card rv-in">
        <svg viewBox="0 0 440 420" role="img" aria-label="Планировка стенда Город MR, 3,7 на 3,0 метра">
          <polygon points="220,8 232,26 220,44 208,26" fill="#754be9"/>
          <text x="240" y="30" font-family="Inter,sans-serif" font-size="12" fill="#5b5d67">светящийся ромб над стендом</text>
          <rect x="40" y="56" width="360" height="300" rx="6" fill="#f3f0ff" stroke="#754be9" stroke-width="2"/>
          <rect x="40" y="52" width="360" height="8" fill="#090714"/>
          <g class="zone" data-z="screen"><rect x="130" y="70" width="180" height="40" rx="10" fill="#754be9"/><text x="220" y="95" text-anchor="middle" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="#fff">экран 86″ · карта</text></g>
          <g class="zone" data-z="st"><rect x="60" y="135" width="56" height="56" rx="10" fill="#2dbe6c"/><rect x="60" y="215" width="56" height="56" rx="10" fill="#2dbe6c"/><rect x="324" y="135" width="56" height="56" rx="10" fill="#2dbe6c"/><rect x="324" y="215" width="56" height="56" rx="10" fill="#2dbe6c"/>
            <g font-family="Unbounded,sans-serif" font-size="18" fill="#fff" text-anchor="middle"><text x="88" y="170">1</text><text x="88" y="250">2</text><text x="352" y="170">3</text><text x="352" y="250">4</text></g></g>
          <g class="zone" data-z="center"><rect x="140" y="135" width="160" height="136" rx="12" fill="none" stroke="#5ec4f7" stroke-width="2" stroke-dasharray="7 6"/><text x="220" y="200" text-anchor="middle" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="#0b8fd0">центр свободен</text><text x="220" y="218" text-anchor="middle" font-family="Inter,sans-serif" font-size="11.5" fill="#5b5d67">очередь и фото на фоне карты</text></g>
          <g class="zone" data-z="desk"><rect x="160" y="292" width="120" height="44" rx="10" fill="#ffb020"/><text x="220" y="319" text-anchor="middle" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="#fff">стойка выдачи</text></g>
          <line x1="40" y1="382" x2="400" y2="382" stroke="#8e9099"/><text x="220" y="402" text-anchor="middle" font-family="Inter,sans-serif" font-size="12" fill="#8e9099">3,7 м · проход, открытая сторона</text>
          <line x1="20" y1="56" x2="20" y2="356" stroke="#8e9099"/><text x="14" y="210" text-anchor="middle" font-family="Inter,sans-serif" font-size="12" fill="#8e9099" transform="rotate(-90 14 210)">3,0 м</text>
        </svg>
      </div>
      <div class="card rv-in">
        <h3 class="h3">Четыре станции, экран и выдача на 11 м²</h3>
        <div class="zl" style="margin-top:14px">
          <div class="zi" data-z="screen"><i style="background:#754be9"></i><div><b>Экран 86 дюймов</b><span>На задней стене. Карту видно из прохода и с подкаст-стенда напротив.</span></div></div>
          <div class="zi" data-z="st"><i style="background:#2dbe6c"></i><div><b>4 игровые станции</b><span>Стойки-домики барной высоты по бокам, лицом к центру. Пятый iPad в резерве.</span></div></div>
          <div class="zi" data-z="desk"><i style="background:#ffb020"></i><div><b>Стойка выдачи</b><span>У прохода: принтер открыток, ободки, промоутер. Внутри тумбы сервер игры.</span></div></div>
          <div class="zi" data-z="center"><i style="background:#5ec4f7"></i><div><b>Центр свободен</b><span>Очередь по разметке и фото на фоне карты. Проход между станциями от 1,5 м.</span></div></div>
        </div>
        <p class="note">Станция принимает 8–10 гостей в час, четыре станции 30–40. Цель MR в 400 историй за три дня закрывается с запасом.</p>
      </div>
    </div>
  </div>
</section>

<!-- Прототип игры -->
<section id="play" style="padding-top:48px">
  <div class="wrap">
    <div class="play">
      <div class="play-head">
        <div>
          <div class="eyebrow" style="color:rgba(255,255,255,.5)"><b style="color:#b9a3ff">05</b> прототип · можно пройти</div>
          <h2 class="h2">Создайте жителя <em style="color:#b9a3ff">города MR</em></h2>
        </div>
        <p>Это рабочий прототип экранов планшета. Соберите жителя, ответьте на пять вопросов, и он появится на карте. Графику, вопросы и веса согласуем с MR и социологами.</p>
      </div>
      <div class="play-grid">
        <div class="tablet">
          <div class="screen" id="screen">
            <!-- 1. старт -->
            <div class="scr start on" data-s="0">
              <div class="diamonds"></div>
              <div class="scr-top"><span>MR · город</span></div>
              <div class="body">
                <div>
                  <span class="badge-y">5 минут · 5 вопросов</span>
                  <h3>Создайте жителя города MR</h3>
                  <p>Соберите персонажа, ответьте на вопросы, и он переедет в один из проектов MR. Вы увидите его на большом экране.</p>
                  <div style="margin-top:20px"><button class="gbtn go" data-next="1">Начать</button></div>
                  <p class="consent">Ответы сохраняются анонимно и используются для исследования</p>
                </div>
                <div id="start-chars" style="display:flex;justify-content:center;gap:4px"></div>
              </div>
            </div>
            <!-- 2. конструктор -->
            <div class="scr" data-s="1">
              <div class="scr-top"><span>MR · город</span><span class="dots" data-dots="1"></span></div>
              <div class="ctor">
                <div class="preview">
                  <div id="char-live"></div>
                  <div class="namebox"><div style="flex:1"><small>Имя жителя</small><input id="rname" maxlength="14" value="Мира" aria-label="Имя жителя"></div></div>
                </div>
                <div class="opts">
                  <h4>Соберите жителя</h4>
                  <div class="tabs" id="tabs"></div>
                  <div class="choices" id="choices"></div>
                  <div class="ctor-foot">
                    <button class="gbtn o" id="rnd">Случайно</button>
                    <button class="gbtn v" data-next="2">Дальше</button>
                  </div>
                </div>
              </div>
            </div>
            <!-- 3. вопросы -->
            <div class="scr" data-s="2">
              <div class="scr-top"><span>MR · город</span><span class="dots" data-dots="2"></span></div>
              <div style="margin-top:14px"><span class="q-badge" id="qn">ВОПРОС 1 ИЗ 5</span></div>
              <div class="q-title" id="qt"></div>
              <div class="answers" id="qa"></div>
              <div class="q-mini" id="q-mini"></div>
            </div>
            <!-- 4. результат -->
            <div class="scr" data-s="3">
              <div class="scr-top"><span>MR · город</span><span class="dots" data-dots="3"></span></div>
              <div class="result">
                <div class="av" id="res-av"></div>
                <div>
                  <span class="ok-badge">ГОТОВО</span>
                  <h3 id="res-h"></h3>
                  <div class="rgrid">
                    <div><small>Дом</small><b id="res-home"></b></div>
                    <div><small>Учёба</small><b id="res-edu"></b></div>
                    <div class="w"><small>Профессия и история</small><b id="res-prof"></b><p id="res-story"></p></div>
                  </div>
                  <div style="margin-top:10px;text-align:right"><button class="gbtn v" id="release" style="padding:12px 22px">Выпустить в город</button></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="map" id="map">
            <div class="map-in" id="map-in"><img src="img/city-map.jpg" alt="Карта города MR на большом экране, эскиз"></div>
            <span class="tag">Большой экран · эскиз графики</span>
            <div class="map-count" id="mcountbox"><span class="plus" id="mplus">+1</span><b id="mcount">247</b>жителей в городе</div>
          </div>
          <div class="pc-wrap">
            <div class="postcard" id="postcard"></div>
            <div class="pc-note" id="pc-note">Открытка 10 × 15 печатается за 10–15 секунд. Житель, имя, профессия, дом и учёба, QR на историю.</div>
          </div>
        </div>
      </div>
      <p class="play-foot">Прототип экранов для обсуждения. Условные кварталы на эскизе заменим на реальные жилые и образовательные проекты MR. Графика своя, в цветах MR, элементов чужих игр не используем.</p>
    </div>
  </div>
</section>

<!-- Путь гостя -->
<section>
  <div class="wrap">
    <div class="eyebrow"><b>06</b> путь гостя</div>
    <h2 class="h2">Восемь шагов и пять минут <em>от прохода до открытки</em></h2>
    <div class="path">
      <div class="ps rv-in"><span class="n">1</span><b>Притяжение</b><span>видит город и ромбы, промоутер зовёт к свободной станции</span><em>из прохода</em></div>
      <div class="ps rv-in"><span class="n">2</span><b>Старт</b><span>что будет и сколько займёт, согласие одной строкой</span><em>20 с</em></div>
      <div class="ps rv-in"><span class="n">3</span><b>Житель</b><span>7 параметров, больше 20 тысяч сочетаний</span><em>1,5–2 мин</em></div>
      <div class="ps rv-in"><span class="n">4</span><b>Вопросы</b><span>пять вопросов о жизни в городе, ответ в один тап</span><em>1–1,5 мин</em></div>
      <div class="ps rv-in"><span class="n">5</span><b>Переезд</b><span>проект MR, учёба и история в 3–4 предложениях</span><em>40 с</em></div>
      <div class="ps rv-in"><span class="n">6</span><b>В город</b><span>житель приземляется в свой квартал на экране</span><em>15 с</em></div>
      <div class="ps rv-in"><span class="n">7</span><b>Открытка</b><span>печать и ободок с ромбом на голову</span><em>30 с</em></div>
      <div class="ps rv-in"><span class="n">8</span><b>После</b><span>по QR история и живая карта в телефоне</span><em>дома</em></div>
    </div>
    <div class="timebar rv-in"><i style="width:7%;background:#5ec4f7"></i><i style="width:36%;background:#754be9"></i><i style="width:26%;background:#9d7cff"></i><i style="width:14%;background:#2dbe6c"></i><i style="width:6%;background:#5ec4f7"></i><i style="width:11%;background:#ffb020"></i></div>
    <div class="timecap"><span>0:00</span><span>около 5 минут у стенда</span></div>
  </div>
</section>

<!-- Ромбы -->
<section>
  <div class="wrap">
    <div class="eyebrow"><b>07</b> эффект</div>
    <h2 class="h2">Ромбы <em>по всему фестивалю</em></h2>
    <div class="gems">
      <div class="big rv-in"><img src="img/crowd.jpg" alt="Гости фестиваля в ободках с ромбом" loading="lazy"><span class="viz">Визуализация</span>
        <div class="in"><div class="h3">К концу первого дня ободки MR видно в каждом зале</div><p style="margin-top:8px;color:rgba(255,255,255,.8)">Люди спрашивают, где такой взять, и приходят на стенд. Каждый ромб ведёт к MR.</p></div></div>
      <div class="col">
        <div class="rv-in"><img src="img/handout.jpg" alt="Выдача открытки на стойке" loading="lazy"><span class="viz">Визуализация</span><span>Промоутер надевает ободок сразу, у стойки просятся фото</span></div>
        <div class="rv-in"><img src="img/headbands.jpg" alt="Ободки с объёмным ромбом" loading="lazy"><span class="viz">Визуализация</span><span>Ободок с объёмным ромбом в цветах MR</span></div>
      </div>
    </div>
  </div>
</section>

<!-- Данные и надёжность -->
<section>
  <div class="wrap">
    <div class="eyebrow"><b>08</b> данные для MR</div>
    <h2 class="h2">Каждое прохождение <em>становится строкой</em> для социологов</h2>
    <div class="cols3">
      <div class="cl rv-in"><h4>Что сохраняем</h4><ul><li>время и номер станции</li><li>ответы на все вопросы</li><li>параметры жителя</li><li>дом, учёба, профессия</li><li>длительность прохождения</li></ul></div>
      <div class="cl rv-in"><h4>Как отдаём</h4><ul><li>Excel в любой момент из админки</li><li>листы: ответы, распределение, по часам</li><li>CSV для SPSS и R</li><li>финальная выгрузка с актом</li></ul></div>
      <div class="cl rv-in"><h4>Без персональных данных</h4><ul><li>имя жителя вымышленное</li><li>контакты, фото и ФИО не собираем</li><li>152-ФЗ не затрагивается</li><li>нужны контакты: отдельное согласие</li></ul></div>
    </div>
    <div class="cols4">
      <div class="cl dark rv-in"><h4>Сервер на стенде</h4><p>Мини-ПК в стойке выдачи держит игру, базу и очередь печати. Планшеты и экран в своей сети.</p></div>
      <div class="cl dark rv-in"><h4>Облако только зеркало</h4><p>Копия базы и страницы по QR. Пропал интернет площадки, стенд работает, данные досылаются позже.</p></div>
      <div class="cl dark rv-in"><h4>Админка</h4><p>Статистика по часам, модерация имён, повторная печать, выгрузка ответов.</p></div>
      <div class="cl dark rv-in"><h4>Резерв</h4><p>Пятый iPad, запасной принтер и копия базы каждые 15 минут.</p></div>
    </div>
    <p class="note">Таблицу весов MR заполняет в Excel, мы загружаем её без пересборки игры и можем поменять хоть в день фестиваля. Игра остаётся у MR: её можно ставить в офисах продаж, на днях открытых дверей и на других событиях.</p>
  </div>
</section>

<!-- Правила площадки -->
<section id="venue">
  <div class="wrap">
    <div class="eyebrow"><b>09</b> Гостиный двор</div>
    <h2 class="h2">Руководство участника <em>уже учли в проекте</em></h2>
    <p class="lead">Прочитали все 31 страницу. Вот что из правил площадки влияет на оба стенда и как мы это закрываем.</p>
    <div class="rules">
      <div class="ru hot rv-in"><span class="src">Аккредитация застройщика</span><h4>До 8 октября у ООО «Экспо-Сервис»</h4><p>Сторонний застройщик допускается только после экспертизы документации. После срока услуга дорожает. <b>Этот срок заложен в график.</b></p></div>
      <div class="ru rv-in"><span class="src">Звук на стендах</span><h4>Запрещён, штраф 25 000 ₽</h4><p>В кубе звук только в беспроводных наушниках для зрителей. Игра без звука, привлекает картинкой и ромбом.</p></div>
      <div class="ru rv-in"><span class="src">Монтаж</span><h4>22–23 ноября и до 06:00 24 ноября</h4><p>Куб и конструктив собираем на складе заранее, на площадке только сборка и настройка. <b>Полный прогон в середине ноября.</b></p></div>
      <div class="ru rv-in"><span class="src">Стены и крепёж</span><h4>Панели 3,5 м, сверлить нельзя, гипсокартон запрещён</h4><p>Куб самонесущий. Экран 86″ и брендинг ставим на свои конструкции или крепим за верхний торец панели.</p></div>
      <div class="ru rv-in"><span class="src">Электричество</span><h4>Подключение до 2,5 кВт на стенд</h4><p>Считаем мощность заранее: экран, пять iPad, принтер и мини-ПК укладываются. Свет и вентиляцию куба закладываем в его бюджет мощности.</p></div>
      <div class="ru rv-in"><span class="src">Демонтаж</span><h4>26 ноября с 20:00 до 08:00 27 ноября</h4><p>Разбираем и вывозим за ночь, мусор вывозим сами: за оставленный площадка штрафует на 15 000 ₽.</p></div>
    </div>
  </div>
</section>

<!-- График -->
<section id="plan">
  <div class="wrap">
    <div class="eyebrow"><b>10</b> следующие шаги</div>
    <h2 class="h2">Как дойдём до открытия <em>24 ноября</em></h2>
    <div class="tl rv-in">
      <div class="tl-bar" id="tlbar"></div>
      <div class="tl-rows">
        <div class="tr"><b><i style="background:#754be9"></i>до 8 октября</b><span>Решение MR, аккредитация застройщика в Гостином дворе, первые эскизы стендов</span></div>
        <div class="tr"><b><i style="background:#5ec4f7"></i>до 10 октября</b><span>От MR: список жилых и образовательных проектов, вопросы для игры, брендбук</span></div>
        <div class="tr"><b><i style="background:#9d7cff"></i>октябрь</b><span>Концепция и 3D обоих стендов, согласование, график спикеров подкаста</span></div>
        <div class="tr"><b><i style="background:#2dbe6c"></i>октябрь – ноябрь</b><span>Производство куба и стендов, разработка игры, графика города и жителей</span></div>
        <div class="tr"><b><i style="background:#ffb020"></i>середина ноября</b><span>Полный прогон на складе: сборка, замеры тишины в кубе, игра с печатью</span></div>
        <div class="tr"><b><i style="background:#ff4c4c"></i>22–23 ноября</b><span>Монтаж на площадке и настройка</span></div>
        <div class="tr"><b><i style="background:#090714"></i>24–26 ноября</b><span>Фестиваль: команда на стендах все три дня, выгрузка данных после закрытия</span></div>
      </div>
    </div>
    <div class="split">
      <div class="cl rv-in"><h4>Hand Marketing</h4><ul>
        <li>Концепция и 3D обоих стендов</li><li>Рабочий проект, аккредитация, работа с площадкой</li><li>Производство куба и конструктива</li><li>Звук, видео, свет, вентиляция</li><li>Разработка игры и графика города</li><li>Печать открыток, ободки, брендинг</li><li>Команда на стендах все дни фестиваля</li><li>Монтаж, демонтаж, вывоз</li><li>Выпуски подкаста и выгрузка ответов</li></ul></div>
      <div class="cl mr rv-in"><h4>MR</h4><ul><li>Спикеры и расписание подкаста</li><li>Проекты MR и вопросы для игры</li><li>Брендбук и согласования</li></ul>
        <p class="deadline">Всё остальное делаем мы, с одним ответственным продюсером на связи каждый день.</p>
        <p class="note">Драфт бюджета по двум стендам у вас отдельным файлом. Под любой ориентир покажем, что оставить, а что упростить без потери идеи.</p></div>
    </div>
  </div>
</section>

<!-- Доказательства -->
<section>
  <div class="wrap">
    <div class="eyebrow"><b>11</b> мы это уже делали</div>
    <h2 class="h2">Стенды, игры и звук <em>в наушниках</em></h2>
    <div class="proof">
      <a class="pf rv-in" href="https://hand-marketing.ru/portfolio/samara-stand-vdnh/" target="_blank" rel="noopener"><img src="/images/lib/custom-samara-vdnh/stand-hero.jpg" alt="Стенд Самарской области на ВДНХ" loading="lazy"><div class="bd"><div class="k">ВДНХ · 248 дней</div><h4>Стенд Самарской области</h4><p>Проект, застройка, 20+ мультимедийных систем, игры и софт для восьми тач-панелей, звук в ИК-наушниках. 16 млн посетителей стенда, приз оргкомитета.</p></div></a>
      <a class="pf rv-in" href="https://hand-marketing.ru/portfolio/becar-private-money/" target="_blank" rel="noopener"><img src="/images/becar-pm/photo-stand-full.jpg" alt="Министенд You&amp;Co для Becar" loading="lazy"><div class="bd"><div class="k">Девелопер · министенд</div><h4>Министенд Becar на Private Money Expo</h4><p>Маленькая площадь, как у ваших 11 м²: узкая полоса галереи и семь брендов. Работала каждая поверхность. Два эскиза и финал в 3D, застройка в ночь до открытия, дежурство все дни, демонтаж и фотоотчёт.</p></div></a>
      <a class="pf rv-in" href="https://hand-marketing.ru/portfolio/samara-exhibition/" target="_blank" rel="noopener"><img src="/portfolio/samara-exhibition/photos/VR_Samara.jpg" alt="VR на выставке «Самара»" loading="lazy"><div class="bd"><div class="k">Музей Алабина · интерактив</div><h4>Выставка «Самара»</h4><p>Пять комплектов VR с виртуальной сборкой ракеты «Союз», Kinect-игры, тач-панели с голосованиями. Разработка и поставка наши.</p></div></a>
    </div>
    <div class="quotes">
      <div class="qt v rv-in">«…мы рады возможности решать задачи разного уровня и направлений (от разработки и производства сувенирной продукции до оформления стендов и проведение клиентских мероприятий) в рамках взаимодействия с одной компанией.»<span>Д. С. Сороколетов, вице-президент Becar Asset Management</span></div>
      <div class="qt rv-in">«Агентством были выполнены все поставленные задачи в сжатые сроки, что свидетельствует о высоком профессионализме сотрудников.»<span>Т. В. Левченко, генеральный директор МФК «Саларис»</span></div>
      <div class="qt rv-in">«Нас впечатлила Ваша эффективная манера работы, творческий подход к разработке концепции мероприятия, терпение и желание выполнять все, даже самые неожиданные, пожелания заказчика.»<span>Томас Штенцель, генеральный директор Messe Düsseldorf Moscow</span></div>
    </div>
  </div>
</section>

<!-- Креатив -->
<section id="creative">
  <div class="wrap">
    <div class="eyebrow"><b>12</b> креатив и дизайн</div>
    <h2 class="h2">Айдентика, книги и объекты, <em>которые держат в руках</em></h2>
    <p class="lead">Для «Нашей школы» это открытки, ободки, брендинг куба и графика города. Вот лучшее, что мы придумали и сделали для других клиентов.</p>
    <div class="crg">
      <a class="cr rv-in" href="https://hand-marketing.ru/creative/samara/" target="_blank" rel="noopener"><div class="im"><img src="img/samara-mascot.jpg" alt="Маскот Ладушка из фирменного стиля выставки «Самара»" loading="lazy"></div><div class="bd"><div class="k">Правительство Самарской области</div><h4>Фирменный стиль выставки «Самара»</h4><p>Брендбук на 28 полос: знак-парус, маскот Ладушка в 16 образах, навигация по модулю, стены зон, экраны и приложение.</p></div></a>
      <a class="cr rv-in" href="https://hand-marketing.ru/creative/saintgobain/suitcase/" target="_blank" rel="noopener"><div class="im"><img src="/images/sgsuitcase/view-front.jpg" alt="Проектный чемодан Saint-Gobain" loading="lazy"></div><div class="bd"><div class="k">Saint-Gobain</div><h4>Проектный чемодан «Две комнаты»</h4><p>Звукоизоляция Gyproc и ISOVER, которую можно показать руками: шум и тишина по разные стороны стены.</p></div></a>
      <a class="cr rv-in" href="https://hand-marketing.ru/creative/skolkovo/" target="_blank" rel="noopener"><div class="im"><img src="/images/skolkovo/mock-spread.png" alt="Доклад «Цифровое производство» для Сколково" loading="lazy" style="object-fit:contain;background:#f1f1f3"></div><div class="bd"><div class="k">СКОЛКОВО</div><h4>Доклад «Цифровое производство»</h4><p>Книга на 86 полос: вёрстка, инфографика и модели зрелости, которые читаются без пояснений.</p></div></a>
      <a class="cr rv-in" href="https://hand-marketing.ru/creative/metra/" target="_blank" rel="noopener"><div class="im"><img src="/images/metra/m-mtg-city.jpg" alt="Брендбук Metra Technology Group" loading="lazy"></div><div class="bd"><div class="k">Metra Technology Group</div><h4>Брендбук на пять брендов</h4><p>Одна система для всей экосистемы: знаки, паттерны, носители от визитки до сити-формата.</p></div></a>
      <a class="cr rv-in" href="https://hand-marketing.ru/creative/saintgobain/calendar/" target="_blank" rel="noopener"><div class="im"><img src="img/sg-calendar.jpg" alt="Концепция новогоднего календаря Saint-Gobain" loading="lazy"></div><div class="bd"><div class="k">Saint-Gobain · концепция</div><h4>Новогодний календарь</h4><p>Каждый месяц продукт Gyproc или ISOVER в авторской линейной графике. Календарь на 2021 год, от идеи до мокапов.</p></div></a>
      <a class="cr rv-in" href="https://hand-marketing.ru/creative/patriki/" target="_blank" rel="noopener"><div class="im"><img src="img/patriki.jpg" alt="Журнал Patriki Times, два номера" loading="lazy"></div><div class="bd"><div class="k">Patriki Times</div><h4>Журнал Patriki Times</h4><p>Дизайн и вёрстка двух номеров на 52 и 68 полос: обложки, модульная сетка, интервью и рекламные полосы.</p></div></a>
    </div>
  </div>
</section>

<!-- Видео -->
<section id="video">
  <div class="wrap">
    <div class="eyebrow"><b>13</b> видеопродакшн</div>
    <h2 class="h2">Снимаем <em>своей группой</em></h2>
    <p class="lead">Камеры, свет и операторы свои. Та же команда запишет выпуски в кубе и снимет ролик о стендах MR на фестивале.</p>
    <div class="vids">
      <div class="vcard rv-in">
        <div class="vid" data-video="/media/vivax-samburskaya.mp4"><img src="/images/vivax/rest-smile.jpg" alt="" loading="lazy" style="transform:scale(1.14)"><div class="vplay"><i><svg width="18" height="18" viewBox="0 0 24 24" fill="#090714"><path d="M7 4v16l13-8z"/></svg></i>Смотреть ролик</div></div>
        <div class="bd"><div class="k">VIVAX SPORT · реклама</div><h4>Ролик с Настасьей Самбурской</h4><p>Три средства линейки внутри одной тренировки. Звезда в кадре, продукт в каждой сцене.</p><a class="link" href="https://hand-marketing.ru/video/vivax/" target="_blank" rel="noopener">Кейс →</a></div>
      </div>
      <div class="vcard rv-in">
        <div class="vid" data-video="/media/eaton-yaz.mp4"><img src="/images/patriot/poster.jpg" alt="" loading="lazy" style="transform:scale(1.14)"><div class="vplay"><i><svg width="18" height="18" viewBox="0 0 24 24" fill="#090714"><path d="M7 4v16l13-8z"/></svg></i>Смотреть ролик</div></div>
        <div class="bd"><div class="k">УАЗ × Eaton · реклама</div><h4>УАЗ Патриот с блокировкой Eaton</h4><p>Грязь, брод и бездорожье. Ролик показывает, что даёт блокировка дифференциала, без технической лекции.</p><a class="link" href="https://hand-marketing.ru/video/patriot/" target="_blank" rel="noopener">Кейс →</a></div>
      </div>
    </div>
  </div>
</section>

<div class="final" id="contact">
  <div class="big-gem"></div>
  <div class="wrap">
    <div class="eyebrow" style="color:rgba(255,255,255,.5)"><b style="color:#b9a3ff">14</b> контакты</div>
    <h2 style="margin-top:16px">Готовы начать</h2>
    <p class="lead">Команда под MR собрана, сроки площадки заложены в график.</p>
    <div class="person"><div class="av">АН</div><div><b>Александр Народецкий</b><span>Client Service Director, Hand Marketing</span></div></div>
    <div class="cts">
      <a href="tel:+79859998783"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>+7 985 999-87-83</a>
      <a href="mailto:anarodetsky@hand-marketing.ru"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>anarodetsky@hand-marketing.ru</a>
      <a href="https://t.me/narodetskii" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 3.44a1.5 1.5 0 0 0-1.6-.23L2.7 10.57a1.4 1.4 0 0 0 .1 2.62l4.46 1.48 1.7 5.27a1.4 1.4 0 0 0 2.28.6l2.45-2.32 4.05 2.96a1.4 1.4 0 0 0 2.2-.86l2.42-15.4a1.5 1.5 0 0 0-.42-1.48zM9.6 14.1l8.13-7.11-6.53 8.32-.24 2.94-1.36-4.15z"/></svg>Telegram</a>
    </div>
    <div style="margin-top:36px;position:relative"><a class="pdf-btn" href="?pdf=1" download><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5M4 19h16"/></svg><span>Скачать PDF<small>чтобы распечатать или открыть без интернета</small></span></a></div>
    <div class="foot">
      <span>Страница подготовлена Hand Marketing для MR и не предназначена для публичного распространения.</span>
      <span>Визуализации и эскиз города: черновики для обсуждения, не финальная графика.</span>
    </div>
  </div>
</div>

<script>
// Проявление блоков при скролле
(function () {
  var els = document.querySelectorAll('.rv-in');
  if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('vis'); }); return; }
  var io = new IntersectionObserver(function (en) {
    en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  els.forEach(function (e) { if (e.getBoundingClientRect().top < innerHeight) e.classList.add('vis'); else io.observe(e); });
})();

// Видео по клику: грузим файл только когда попросили
document.querySelectorAll('[data-video]').forEach(function (box) {
  box.addEventListener('click', function () {
    if (box.classList.contains('playing')) return;
    var v = document.createElement('video'); v.src = box.dataset.video; v.controls = true; v.playsInline = true; v.autoplay = true;
    box.appendChild(v); box.classList.add('playing'); v.play().catch(function () {});
  });
});

// Схема зала: клик по стенду ведёт к его разделу
document.querySelectorAll('.hall .st').forEach(function (g) {
  g.addEventListener('click', function () { document.getElementById(g.dataset.go).scrollIntoView({ behavior: 'smooth' }); });
});

// Подкаст-куб: вращение перетаскиванием, автоповорот, подсветка решений
(function () {
  var stage = document.getElementById('stage'), cube = document.getElementById('cube'); if (!cube) return;
  var ry = -32, rx = -16, drag = false, sx = 0, sy = 0, auto = true, vis = false;
  var scale = Math.min(1, stage.clientWidth / 520);
  function apply() { cube.style.transform = 'translateY(-10px) scale(' + scale + ') rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)'; }
  function down(e) { var p = e.touches ? e.touches[0] : e; drag = true; auto = false; sx = p.clientX; sy = p.clientY; }
  function move(e) {
    if (!drag) return; var p = e.touches ? e.touches[0] : e;
    ry += (p.clientX - sx) * .45; rx = Math.max(-40, Math.min(8, rx - (p.clientY - sy) * .25)); sx = p.clientX; sy = p.clientY; apply();
  }
  stage.addEventListener('mousedown', down); addEventListener('mousemove', move); addEventListener('mouseup', function () { drag = false; });
  stage.addEventListener('touchstart', down, { passive: true }); stage.addEventListener('touchmove', move, { passive: true }); stage.addEventListener('touchend', function () { drag = false; });
  addEventListener('resize', function () { scale = Math.min(1, stage.clientWidth / 520); apply(); });
  new IntersectionObserver(function (e) { vis = e[0].isIntersecting; }).observe(stage);
  (function loop() { if (auto && vis) { ry += .18; apply(); } requestAnimationFrame(loop); })();
  apply();
  var btns = document.querySelectorAll('.fb');
  function hl(h) { stage.className = 'stage rv-in vis h-' + h; btns.forEach(function (b) { b.classList.toggle('on', b.dataset.h === h); }); }
  btns.forEach(function (b) { b.addEventListener('click', function () { hl(b.dataset.h); }); });
  hl('glass');
})();

// Планировка «Города MR»: наведение на пункт подсвечивает зону
(function () {
  var lay = document.getElementById('layout');
  lay.querySelectorAll('.zi').forEach(function (z) {
    z.addEventListener('mouseenter', function () {
      lay.classList.add('hov'); z.classList.add('on');
      lay.querySelectorAll('.zone').forEach(function (g) { g.classList.toggle('on', g.dataset.z === z.dataset.z); });
    });
    z.addEventListener('mouseleave', function () { lay.classList.remove('hov'); z.classList.remove('on'); });
  });
})();

// График до открытия: шкала 1 октября → 27 ноября с отметкой «сегодня»
(function () {
  var bar = document.getElementById('tlbar'); if (!bar) return;
  var t0 = new Date(2026, 8, 28), t1 = new Date(2026, 10, 28), span = t1 - t0;
  function x(d) { return Math.max(0, Math.min(100, (d - t0) / span * 100)); }
  var h = '<div class="axis"></div>';
  [[new Date(2026,8,30), new Date(2026,9,8), '#754be9'], [new Date(2026,9,8), new Date(2026,9,31), '#9d7cff'], [new Date(2026,9,15), new Date(2026,10,14), '#2dbe6c'],
   [new Date(2026,10,14), new Date(2026,10,18), '#ffb020'], [new Date(2026,10,22), new Date(2026,10,24), '#ff4c4c'], [new Date(2026,10,24), new Date(2026,10,27), '#090714']]
    .forEach(function (s) { h += '<div class="seg" style="left:' + x(s[0]) + '%;width:' + (x(s[1]) - x(s[0])) + '%;background:' + s[2] + '"></div>'; });
  [[new Date(2026,9,1), '1 окт'], [new Date(2026,9,8), '8 окт'], [new Date(2026,10,1), '1 ноя'], [new Date(2026,10,22), '22 ноя'], [new Date(2026,10,26), '26']]
    .forEach(function (m) { h += '<div class="mk" style="left:' + x(m[0]) + '%">' + m[1] + '</div>'; });
  var now = new Date(); if (now >= t0 && now <= t1) h += '<div class="today" style="left:' + x(now) + '%"></div>';
  bar.innerHTML = h;
})();

// ================= Прототип игры «Город MR» =================
(function () {
  var SKIN = ['#f6d3b5', '#e8b48f', '#c98b62', '#8d5a3b'];
  var HAIRC = ['#2b1d16', '#6b3e22', '#c9954c', '#1d1a2e', '#b8431f', '#9aa0aa'];
  var TOP = ['#2dbe6c', '#754be9', '#5ec4f7', '#ffb020', '#ff5d7a', '#090714'];
  var GEM = ['#754be9', '#2dbe6c', '#5ec4f7', '#ffb020'];
  var HAIRS = ['bun', 'short', 'long', 'curly', 'cap'];
  var ACC = ['none', 'glasses', 'book', 'scooter', 'phones'];
  var NAMES = ['Мира', 'Лев', 'Ася', 'Тимур', 'Ника', 'Марк', 'Ева', 'Глеб', 'Варя', 'Артём', 'Соня', 'Илья'];
  var st = { skin: 0, hair: 0, hairc: 0, top: 0, acc: 1, gem: 0 };

  // Житель: плоская графика в цветах MR
  function charSVG(s, opt) {
    opt = opt || {};
    var sk = SKIN[s.skin], hc = HAIRC[s.hairc], tp = TOP[s.top], gm = GEM[s.gem], h = HAIRS[s.hair], a = ACC[s.acc];
    var o = '<svg viewBox="0 0 120 190" xmlns="http://www.w3.org/2000/svg">';
    o += '<ellipse cx="60" cy="182" rx="34" ry="7" fill="#090714" opacity=".12"/>';
    if (!opt.noGem) o += '<g><polygon points="60,2 72,16 60,34 48,16" fill="' + gm + '"/><polygon points="60,2 72,16 60,16" fill="#fff" opacity=".35"/></g>';
    if (h === 'long') o += '<path d="M33 70 Q30 118 44 124 L76 124 Q90 118 87 70 Z" fill="' + hc + '"/>';
    o += '<rect x="46" y="140" width="12" height="38" rx="6" fill="#1d1a2e"/><rect x="62" y="140" width="12" height="38" rx="6" fill="#1d1a2e"/>';
    o += '<rect x="38" y="100" width="44" height="48" rx="16" fill="' + tp + '"/>';
    o += '<rect x="28" y="104" width="12" height="34" rx="6" fill="' + tp + '"/><rect x="80" y="104" width="12" height="34" rx="6" fill="' + tp + '"/>';
    o += '<circle cx="34" cy="140" r="6" fill="' + sk + '"/><circle cx="86" cy="140" r="6" fill="' + sk + '"/>';
    o += '<circle cx="60" cy="72" r="28" fill="' + sk + '"/>';
    if (h === 'bun') o += '<circle cx="60" cy="38" r="10" fill="' + hc + '"/><path d="M32 70 Q34 44 60 44 Q86 44 88 70 Q80 56 60 56 Q40 56 32 70Z" fill="' + hc + '"/>';
    if (h === 'short') o += '<path d="M31 72 Q30 42 60 42 Q90 42 89 72 Q84 58 70 55 Q64 62 50 58 Q38 60 31 72Z" fill="' + hc + '"/>';
    if (h === 'long') o += '<path d="M31 76 Q28 42 60 42 Q92 42 89 76 Q84 58 60 54 Q38 58 31 76Z" fill="' + hc + '"/>';
    if (h === 'curly') o += '<g fill="' + hc + '"><circle cx="40" cy="54" r="11"/><circle cx="54" cy="46" r="11"/><circle cx="68" cy="46" r="11"/><circle cx="81" cy="55" r="11"/><circle cx="34" cy="66" r="8"/><circle cx="87" cy="66" r="8"/></g>';
    if (h === 'cap') o += '<path d="M31 66 Q32 42 60 42 Q88 42 89 66 Z" fill="' + tp + '"/><rect x="58" y="60" width="40" height="7" rx="3.5" fill="' + tp + '"/><circle cx="60" cy="44" r="3" fill="#fff"/>';
    o += '<circle cx="50" cy="75" r="3.4" fill="#1d1a2e"/><circle cx="70" cy="75" r="3.4" fill="#1d1a2e"/>';
    o += '<circle cx="44" cy="84" r="4" fill="#ff8fa3" opacity=".45"/><circle cx="76" cy="84" r="4" fill="#ff8fa3" opacity=".45"/>';
    o += '<path d="M53 87 Q60 93 67 87" stroke="#1d1a2e" stroke-width="2.4" fill="none" stroke-linecap="round"/>';
    if (a === 'glasses') o += '<g fill="none" stroke="#1d1a2e" stroke-width="2.6"><circle cx="50" cy="75" r="8"/><circle cx="70" cy="75" r="8"/><path d="M58 75h4"/></g>';
    if (a === 'phones') o += '<path d="M33 72 Q33 40 60 40 Q87 40 87 72" fill="none" stroke="#1d1a2e" stroke-width="4"/><rect x="27" y="66" width="10" height="16" rx="4" fill="' + gm + '"/><rect x="83" y="66" width="10" height="16" rx="4" fill="' + gm + '"/>';
    if (a === 'book') o += '<rect x="84" y="118" width="16" height="22" rx="2" fill="#5ec4f7"/><rect x="86" y="120" width="2" height="18" fill="#fff" opacity=".6"/>';
    if (a === 'scooter') o += '<g stroke="#1d1a2e" stroke-width="3" fill="none"><path d="M30 178h58M88 178 L96 120"/></g><circle cx="30" cy="180" r="5" fill="#1d1a2e"/><circle cx="90" cy="180" r="5" fill="#1d1a2e"/><rect x="90" y="116" width="14" height="4" rx="2" fill="#1d1a2e"/>';
    return o + '</svg>';
  }
  function randState() { return { skin: r(SKIN.length), hair: r(HAIRS.length), hairc: r(HAIRC.length), top: r(TOP.length), acc: r(ACC.length), gem: r(GEM.length) }; }
  function r(n) { return Math.floor(Math.random() * n); }

  // Стартовый экран: пара жителей
  document.getElementById('start-chars').innerHTML =
    '<div style="width:46%">' + charSVG({ skin: 0, hair: 0, hairc: 0, top: 0, acc: 1, gem: 3 }) + '</div>' +
    '<div style="width:38%;margin-top:30px">' + charSVG({ skin: 1, hair: 1, hairc: 2, top: 3, acc: 0, gem: 2 }) + '</div>';

  // Экраны
  var screens = document.querySelectorAll('.scr');
  function show(i) {
    screens.forEach(function (s) { s.classList.toggle('on', +s.dataset.s === i); });
    document.querySelectorAll('[data-dots]').forEach(function (d) {
      var k = +d.dataset.dots, h = ''; for (var j = 1; j <= 5; j++) h += '<i class="' + (j <= k + (i === 2 ? qi : 0) ? 'on' : '') + '"></i>'; d.innerHTML = h;
    });
  }
  document.querySelectorAll('[data-next]').forEach(function (b) {
    b.addEventListener('click', function () { var n = +b.dataset.next; if (n === 2) { qi = 0; answers = []; renderQ(); } show(n); });
  });

  // Конструктор
  var TABS = [['skin', 'лицо'], ['hair', 'причёска'], ['hairc', 'волосы'], ['top', 'одежда'], ['acc', 'аксессуар'], ['gem', 'ромб']];
  var tab = 'hair', tabsEl = document.getElementById('tabs'), chEl = document.getElementById('choices'), live = document.getElementById('char-live');
  function renderLive() { live.innerHTML = charSVG(st); document.getElementById('q-mini').innerHTML = charSVG(st); }
  function renderTabs() {
    tabsEl.innerHTML = TABS.map(function (t) { return '<button class="' + (t[0] === tab ? 'on' : '') + '" data-t="' + t[0] + '">' + t[1] + '</button>'; }).join('');
    var list = { skin: SKIN, hair: HAIRS, hairc: HAIRC, top: TOP, acc: ACC, gem: GEM }[tab];
    chEl.innerHTML = list.map(function (v, i) {
      var on = st[tab] === i ? ' on' : '';
      if (tab === 'hair' || tab === 'acc') { var s2 = Object.assign({}, st); s2[tab] = i; return '<button class="' + on + '" data-i="' + i + '">' + charSVG(s2, { noGem: true }) + '</button>'; }
      if (tab === 'gem') return '<button class="' + on + '" data-i="' + i + '"><svg viewBox="0 0 24 30"><polygon points="12,1 23,11 12,29 1,11" fill="' + v + '"/></svg></button>';
      return '<button class="sw' + on + '" data-i="' + i + '" style="background:' + v + '" aria-label="цвет ' + (i + 1) + '"></button>';
    }).join('');
  }
  tabsEl.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; tab = b.dataset.t; renderTabs(); });
  chEl.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; st[tab] = +b.dataset.i; renderTabs(); renderLive(); });
  document.getElementById('rnd').addEventListener('click', function () {
    st = randState(); document.getElementById('rname').value = NAMES[r(NAMES.length)]; renderTabs(); renderLive();
  });
  renderTabs(); renderLive();

  // Иконки ответов
  var IC = {
    run: '<circle cx="36" cy="12" r="6" fill="#ff5d7a"/><path d="M20 58l10-18 10 6 6 12M30 40l6-16 12 8h10M36 24l-14 4-6 10" stroke="#1d1a2e" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    cup: '<rect x="12" y="22" width="30" height="30" rx="6" fill="#ffb020"/><path d="M42 28h6a7 7 0 010 14h-6" stroke="#ffb020" stroke-width="5" fill="none"/><path d="M20 8q4 6 0 10M30 8q4 6 0 10" stroke="#8e9099" stroke-width="3" fill="none"/>',
    ball: '<circle cx="32" cy="32" r="22" fill="#2dbe6c"/><path d="M12 26q20 8 40 0M14 42q18-6 36 0M32 10v44" stroke="#fff" stroke-width="3" fill="none"/>',
    pen: '<rect x="8" y="10" width="40" height="44" rx="4" fill="#efeafd"/><path d="M18 22h20M18 32h20M18 42h12" stroke="#754be9" stroke-width="4"/><path d="M44 50l12-26 6 3-12 26z" fill="#754be9"/>',
    house: '<path d="M10 30L32 12l22 18v24H10z" fill="#ffb020"/><rect x="26" y="38" width="12" height="16" fill="#754be9"/><path d="M6 32L32 10l26 22" stroke="#ff5d7a" stroke-width="5" fill="none" stroke-linejoin="round"/>',
    park: '<rect x="4" y="46" width="56" height="10" rx="4" fill="#5ec4f7"/><circle cx="22" cy="26" r="14" fill="#2dbe6c"/><circle cx="42" cy="30" r="11" fill="#6dd99a"/><rect x="20" y="36" width="4" height="12" fill="#6b3e22"/><rect x="40" y="38" width="4" height="10" fill="#6b3e22"/>',
    metro: '<rect x="14" y="8" width="36" height="40" rx="10" fill="#754be9"/><rect x="20" y="16" width="24" height="12" rx="3" fill="#fff"/><circle cx="23" cy="38" r="3" fill="#fff"/><circle cx="41" cy="38" r="3" fill="#fff"/><path d="M20 48l-6 10M44 48l6 10" stroke="#1d1a2e" stroke-width="4" stroke-linecap="round"/>',
    yard: '<rect x="8" y="18" width="18" height="38" rx="3" fill="#ff5d7a"/><rect x="38" y="8" width="18" height="48" rx="3" fill="#ffb020"/><circle cx="32" cy="50" r="6" fill="#2dbe6c"/>',
    arch: '<path d="M10 54V26L32 10l22 16v28" stroke="#754be9" stroke-width="5" fill="none" stroke-linejoin="round"/><path d="M22 54V36h20v18" stroke="#5ec4f7" stroke-width="5" fill="none"/><path d="M6 58h52" stroke="#1d1a2e" stroke-width="4"/>',
    teach: '<rect x="8" y="10" width="48" height="32" rx="4" fill="#1d1a2e"/><path d="M16 22h20M16 30h28" stroke="#2dbe6c" stroke-width="4"/><path d="M22 42l-6 16M42 42l6 16" stroke="#8e9099" stroke-width="4"/>',
    gear: '<circle cx="32" cy="32" r="14" fill="none" stroke="#5ec4f7" stroke-width="8"/><g stroke="#5ec4f7" stroke-width="8"><path d="M32 6v8M32 50v8M6 32h8M50 32h8M14 14l6 6M44 44l6 6M14 50l6-6M44 20l6-6"/></g>',
    paint: '<path d="M32 8a24 22 0 100 44c6 0 6-6 2-9s-2-9 5-9h7c8 0 10-6 10-10C56 16 46 8 32 8z" fill="#ffb020"/><circle cx="22" cy="24" r="4" fill="#754be9"/><circle cx="34" cy="18" r="4" fill="#ff5d7a"/><circle cx="20" cy="36" r="4" fill="#2dbe6c"/>',
    code: '<rect x="6" y="12" width="52" height="38" rx="6" fill="#090714"/><path d="M22 24l-8 7 8 7M42 24l8 7-8 7M35 22l-6 18" stroke="#2dbe6c" stroke-width="4" fill="none" stroke-linecap="round"/>',
    build: '<rect x="10" y="36" width="18" height="18" fill="#ffb020"/><rect x="30" y="36" width="18" height="18" fill="#754be9"/><rect x="20" y="18" width="18" height="18" fill="#5ec4f7"/><path d="M48 12l8 8-18 18" stroke="#1d1a2e" stroke-width="4" fill="none"/>',
    talk: '<rect x="6" y="10" width="36" height="26" rx="10" fill="#754be9"/><path d="M14 36l-4 10 12-10" fill="#754be9"/><rect x="26" y="26" width="32" height="22" rx="9" fill="#5ec4f7"/><path d="M50 48l4 8-10-8" fill="#5ec4f7"/>',
    scooter: '<path d="M14 50h32M46 50l6-34M46 16h10" stroke="#1d1a2e" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="14" cy="52" r="6" fill="#754be9"/><circle cx="48" cy="52" r="6" fill="#754be9"/>',
    car: '<path d="M8 40l6-16h36l6 16v10H8z" fill="#5ec4f7"/><rect x="18" y="28" width="28" height="10" rx="2" fill="#fff"/><circle cx="18" cy="50" r="6" fill="#1d1a2e"/><circle cx="46" cy="50" r="6" fill="#1d1a2e"/>',
    walk: '<circle cx="32" cy="10" r="6" fill="#2dbe6c"/><path d="M32 18v20M32 38l-8 18M32 38l8 18M32 24l-10 10M32 24l10 8" stroke="#1d1a2e" stroke-width="5" fill="none" stroke-linecap="round"/>'
  };
  // Вопросы из черновика; веса по кварталам: river, center, school, garden, uni
  var Q = [
    ['Как проходит ваше субботнее утро?', [['run', 'Пробежка вдоль воды', { river: 3 }], ['cup', 'Кофе в тихом дворе', { center: 2, garden: 1 }], ['ball', 'Секция с детьми', { school: 3 }], ['pen', 'Лекция или мастерская', { uni: 3 }]]],
    ['Что должно быть в 10 минутах от дома?', [['house', 'Школа и сад', { school: 2, garden: 2 }], ['park', 'Набережная и парк', { river: 3 }], ['metro', 'Метро', { center: 3 }], ['yard', 'Тихий двор', { garden: 3 }]]],
    ['Кем хотели стать в детстве?', [['arch', 'Архитектором', { uni: 1 }, 'arch'], ['teach', 'Учителем', { school: 1 }, 'teach'], ['gear', 'Инженером', { center: 1 }, 'eng'], ['paint', 'Художником', { garden: 1 }, 'art']]],
    ['Чему хотите научиться в этом году?', [['code', 'Программировать', { uni: 2 }], ['paint', 'Рисовать', { garden: 2 }], ['build', 'Строить своими руками', { school: 1, river: 1 }], ['talk', 'Выступать', { center: 2 }]]],
    ['Как удобнее ездить по городу?', [['scooter', 'На самокате', { river: 2 }, null, 'едет на самокате вдоль воды'], ['metro', 'На метро', { center: 2 }, null, 'спускается в метро у дома'], ['car', 'На машине', { uni: 1, school: 1 }, null, 'выезжает на машине, пока пусто'], ['walk', 'Пешком', { garden: 2 }, null, 'идёт пешком через дворы']]]
  ];
  var DIST = {
    river:  { home: 'Квартал MR у набережной', edu: 'Факультет девелопмента ВШЭ', x: 48, y: 78, sx: 64, sy: 8 },
    center: { home: 'Квартал MR у метро', edu: 'Факультет девелопмента ВШЭ', x: 50, y: 42, sx: 26, sy: 22 },
    school: { home: 'Квартал MR у новой школы', edu: 'Школа в квартале MR', x: 20, y: 50, sx: 22, sy: 30 },
    garden: { home: 'Семейный квартал MR', edu: 'Детский сад в квартале MR', x: 76, y: 64, sx: 24, sy: 20 },
    uni:    { home: 'Квартал MR у университета', edu: 'Факультет девелопмента ВШЭ', x: 84, y: 38, sx: 18, sy: 20 }
  };
  var PROF = {
    arch: ['Архитектор общественных пространств', 'придумывает, какими будут дворы через десять лет'],
    teach: ['Учитель проектной школы', 'ведёт у старшеклассников курс про то, как устроен город'],
    eng: ['Инженер умного дома', 'настраивает, чтобы дом сам экономил тепло и свет'],
    art: ['Дизайнер детских пространств', 'рисует площадки, на которые дети бегут сами']
  };
  var qi = 0, answers = [];
  function renderQ() {
    var q = Q[qi];
    document.getElementById('qn').textContent = 'ВОПРОС ' + (qi + 1) + ' ИЗ 5';
    document.getElementById('qt').textContent = q[0];
    document.getElementById('qa').innerHTML = q[1].map(function (a, i) { return '<button class="ans" data-i="' + i + '"><svg viewBox="0 0 64 64">' + IC[a[0]] + '</svg>' + a[1] + '</button>'; }).join('');
    show(2);
  }
  document.getElementById('qa').addEventListener('click', function (e) {
    var b = e.target.closest('.ans'); if (!b) return;
    b.classList.add('on'); answers[qi] = +b.dataset.i;
    setTimeout(function () { qi++; if (qi < Q.length) renderQ(); else finish(); }, 260);
  });
  var result = null;
  function finish() {
    var sc = { river: 0, center: 0, school: 0, garden: 0, uni: 0 };
    answers.forEach(function (ai, k) { var w = Q[k][1][ai][2]; for (var d in w) sc[d] += w[d]; });
    var best = Object.keys(sc).sort(function (a, b) { return sc[b] - sc[a]; })[0];
    var name = (document.getElementById('rname').value || 'Мира').trim().slice(0, 14);
    var prof = PROF[Q[2][1][answers[2]][3]], move = Q[4][1][answers[4]][4];
    result = { name: name, d: best, home: DIST[best].home, edu: DIST[best].edu, prof: prof[0],
      story: name + ' каждое утро ' + move + ', а днём ' + prof[1] + '.', no: population + 1 };
    document.getElementById('release').disabled = false;
    document.getElementById('res-av').innerHTML = charSVG(st);
    document.getElementById('res-h').textContent = name + ' переезжает в город MR';
    document.getElementById('res-home').textContent = result.home;
    document.getElementById('res-edu').textContent = result.edu;
    document.getElementById('res-prof').textContent = result.prof;
    document.getElementById('res-story').textContent = result.story;
    show(3);
  }

  // Карта: житель приземляется в свой квартал, рядом печатается открытка
  var map = document.getElementById('map'), mapIn = document.getElementById('map-in'), population = 247, spots = [];
  // счётчик жителей: растёт с каждым выпуском, с подсветкой и «+1»
  function grow() {
    population++;
    var box = document.getElementById('mcountbox'); document.getElementById('mcount').textContent = population;
    box.classList.remove('bump'); void box.offsetWidth; box.classList.add('bump');
  }
  // свободное место в квартале, подальше от уже приземлившихся жителей
  function spot(D) {
    var px = D.x, py = D.y, bestGap = -1;
    for (var k = 0; k < 40; k++) {
      var cx = D.x + (Math.random() - .5) * D.sx, cy = D.y + (Math.random() - .5) * D.sy, gap = 99;
      spots.forEach(function (q) { gap = Math.min(gap, Math.hypot(q[0] - cx, (q[1] - cy) * 1.8)); });
      if (gap > bestGap) { bestGap = gap; px = cx; py = cy; }
    }
    px = Math.max(6, Math.min(94, px)); py = Math.max(12, Math.min(94, py)); spots.push([px, py]);
    return [px, py];
  }
  function pin(x, y, name, gem, me) {
    var d = document.createElement('div'); d.className = 'res' + (me ? ' me drop' : '');
    d.style.left = x + '%'; d.style.top = y + '%';
    d.innerHTML = '<span class="g" style="background:' + gem + '"></span><span class="chip">' + name.replace(/[<>&]/g, '') + '</span>';
    mapIn.appendChild(d); return d;
  }
  document.getElementById('release').addEventListener('click', function () {
    if (this.disabled) return; this.disabled = true;
    mapIn.querySelectorAll('.res.me').forEach(function (m) { m.classList.remove('me', 'drop'); });
    var D = DIST[result.d], xy = spot(D), px = xy[0], py = xy[1];
    pin(px, py, result.name, GEM[st.gem], true);
    // экран «наезжает» на квартал нового жителя и через пару секунд отъезжает
    mapIn.style.transformOrigin = px + '% ' + py + '%'; mapIn.style.transform = 'scale(1.9)'; mapIn.style.setProperty('--inv', (1 / 1.9).toFixed(3));
    clearTimeout(mapIn._t); mapIn._t = setTimeout(function () { mapIn.style.transform = ''; mapIn.style.removeProperty('--inv'); }, 2600);
    grow(); result.no = population;
    renderCard();
    if (innerWidth < 1060) map.scrollIntoView({ behavior: 'smooth', block: 'center' });
    var note = document.getElementById('pc-note');
    note.innerHTML = '<b style="color:#fff">' + result.name.replace(/[<>&]/g, '') + ' уже в городе.</b> Найдите жителя на большом экране. Открытка № 0' + result.no + ' печатается у стойки.<br><button class="gbtn go" id="again">Собрать ещё одного</button>';
    document.getElementById('again').addEventListener('click', function () { st = randState(); document.getElementById('rname').value = NAMES[r(NAMES.length)]; renderTabs(); renderLive(); show(1); document.getElementById('play').scrollIntoView({ behavior: 'smooth' }); });
  });
  function qr(seed) { // узор под QR, не настоящий код
    var o = '<svg viewBox="0 0 21 21"><rect width="21" height="21" fill="#fff"/>', s = seed * 9301 + 49297;
    function rnd() { s = (s * 9301 + 49297) % 233280; return s / 233280; }
    for (var y = 0; y < 21; y++) for (var x = 0; x < 21; x++) {
      var f = (x < 7 && y < 7) || (x > 13 && y < 7) || (x < 7 && y > 13);
      if (f) { var fx = x > 13 ? x - 14 : x, fy = y > 13 ? y - 14 : y; if (fx === 0 || fx === 6 || fy === 0 || fy === 6 || (fx > 1 && fx < 5 && fy > 1 && fy < 5)) o += '<rect x="' + x + '" y="' + y + '" width="1" height="1" fill="#090714"/>'; }
      else if (rnd() > .52) o += '<rect x="' + x + '" y="' + y + '" width="1" height="1" fill="#090714"/>';
    }
    return o + '</svg>';
  }
  function renderCard() {
    var c = document.getElementById('postcard'), R = result || { name: 'Мира', prof: 'Архитектор общественных пространств', home: 'Квартал MR у набережной', edu: 'Факультет девелопмента ВШЭ', no: 247 };
    c.innerHTML = '<div class="pc-l">' + charSVG(result ? st : { skin: 0, hair: 0, hairc: 0, top: 0, acc: 1, gem: 3 }) + '</div>' +
      '<div class="pc-r"><span class="no">ЖИТЕЛЬ № 0' + R.no + '</span><h5></h5><div class="pr"></div><p><b>Дом:</b> <span class="h"></span></p><p><b>Учёба:</b> <span class="e"></span></p>' +
      '<div class="ft"><b>Растём с MR</b>' + qr(R.no) + '</div></div>';
    c.querySelector('h5').textContent = R.name; c.querySelector('.pr').textContent = R.prof;
    c.querySelector('.h').textContent = R.home; c.querySelector('.e').textContent = R.edu;
    c.classList.remove('print'); void c.offsetWidth; if (result) c.classList.add('print');
  }
  // Живой город: пока карта на экране, с трёх других станций прилетают жители
  var mapVis = false, OTHER = ['Лиза', 'Павел', 'Кира', 'Денис', 'Алиса', 'Макс', 'Злата', 'Егор', 'Полина', 'Руслан', 'Таня', 'Олег', 'Даша', 'Слава', 'Вика', 'Никита'];
  new IntersectionObserver(function (e) { mapVis = e[0].isIntersecting; }, { threshold: .3 }).observe(map);
  function ambient() {
    if (mapVis && !document.hidden) {
      var keys = Object.keys(DIST), D = DIST[keys[r(keys.length)]], xy = spot(D);
      var d = pin(xy[0], xy[1], OTHER[r(OTHER.length)], GEM[r(GEM.length)], false);
      d.classList.add('other', 'drop'); grow();
      if (spots.length > 26) { var old = mapIn.querySelector('.res.other'); if (old) { old.remove(); spots.shift(); } }
    }
    setTimeout(ambient, 5000 + Math.random() * 5000);
  }
  setTimeout(ambient, 3500);
  renderCard();
  show(0);
})();
</script>
<script id="hm-mr-analytics">
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
    if (a.closest('.nav')) return ev('nav', 'меню: ' + txt);
    if (a.classList.contains('vid')) return ev('video', 'включил ролик: ' + (a.dataset.video || '').split('/').pop());
    if (a.matches('.hall .st')) return ev('hall', 'схема зала: перешёл к стенду ' + (a.dataset.go === 'city' ? 'C8.1' : 'C7.2'));
    if (/^tel:/.test(href)) return ev('contact', 'нажал телефон');
    if (/^mailto:/.test(href)) return ev('contact', 'нажал почту');
    if (/t\.me|wa\.me/.test(href)) return ev('contact', 'нажал ' + (/t\.me/.test(href) ? 'Telegram' : 'WhatsApp'));
    if (/^https?:/.test(href)) { var h = a.querySelector('h4, h3, b'); return ev('link', 'открыл кейс: ' + cap(h ? h.textContent : txt) + ' → ' + href.replace('https://hand-marketing.ru', '')); }
    if (/^#/.test(href)) return ev('anchor', 'перешёл к разделу: ' + txt);
    if (a.classList.contains('fb')) return ev('cube', 'куб: ' + cap(a.querySelector('b').textContent));
    if (a.dataset.next === '1') return ev('game', 'игра: начал');
    if (a.dataset.next === '2') return ev('game', 'игра: собрал жителя «' + (document.getElementById('rname').value || '') + '»');
    if (a.id === 'rnd') return ev('game', 'игра: случайный житель');
    if (a.closest('#tabs')) return first('tab' + txt, 'game', 'игра: вкладка «' + txt.toLowerCase() + '»');
    if (a.closest('#choices')) return first('choice', 'game', 'игра: меняет внешность жителя');
    if (a.classList.contains('ans')) { var q = document.getElementById('qt'); return ev('game', 'игра: ' + (q ? q.textContent : '') + ' → ' + txt); }
    if (a.id === 'release') return ev('game_release', 'игра: выпустил жителя «' + (document.getElementById('rname').value || '') + '» → ' +
      (document.getElementById('res-home').textContent || '') + ', ' + (document.getElementById('res-prof').textContent || ''));
    if (a.id === 'again') return ev('game', 'игра: собирает ещё одного жителя');
  }, true);
  var stage = document.getElementById('stage');
  if (stage) ['mousedown', 'touchstart'].forEach(function (t) { stage.addEventListener(t, function () { first('cubeDrag', 'cube', 'крутил 3D-куб'); }, { passive: true }); });
  document.querySelectorAll('.zi').forEach(function (z) {
    z.addEventListener('mouseenter', function () { first('zone' + z.dataset.z, 'zone', 'план 11 м²: смотрел «' + cap(z.querySelector('b').textContent) + '»'); });
  });
  document.addEventListener('copy', function () {
    var s = String(getSelection() || '').trim(); if (s) ev('copy', 'скопировал текст: «' + s.slice(0, 120) + (s.length > 120 ? '…' : '') + '»');
  });
})();
</script>
<script>
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym(71125393, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true, params:{ private_page:'mr-group' } });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute; left:-9999px;" alt=""></div></noscript>
</body>
</html>
