<?php
// Аналитика приватной страницы АЛИДИ: журнал событий, уведомления в Telegram, отчёт для Hand Marketing.
// Подключается из index.php, напрямую не открывается (.htaccess закрывает файлы на «_»).
//
// Журнал: JSON-строки в каталоге ВЫШЕ корня сайта (деплой его не трогает, из веба не виден).
// Если туда писать нельзя, запасной вариант: _data/ рядом со страницей (закрыт своим .htaccess).
// Отчёт: /for/alidi/?stats=<ключ>. Ключ отдельный от пароля клиента, в файле только его хеш.

if (!defined('HM_ALIDI')) { http_response_code(403); exit; }

$STATS_HASH = 'ad9ffe5117b76be78defba863761327bc14c6564847268384592af7fc0dcd3fc';

function hm_https() {
    return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https');
}

function hm_cookie($name, $value, $days) {
    setcookie($name, $value, time() + 86400 * $days, '/for/alidi/', '', hm_https(), true);
    $_COOKIE[$name] = $value;
}

function hm_dir() {
    static $dir = null;
    if ($dir !== null) return $dir;
    $root = isset($_SERVER['DOCUMENT_ROOT']) ? rtrim($_SERVER['DOCUMENT_ROOT'], '/') : '';
    $candidates = array();
    if ($root !== '') $candidates[] = dirname($root) . '/hm-analytics/alidi';
    $candidates[] = __DIR__ . '/_data';
    foreach ($candidates as $c) {
        if (!is_dir($c)) @mkdir($c, 0750, true);
        if (is_dir($c) && is_writable($c)) {
            if (strpos($c, __DIR__) === 0 && !is_file($c . '/.htaccess')) {
                @file_put_contents($c . '/.htaccess', "Require all denied\nDeny from all\n");
            }
            return $dir = $c;
        }
    }
    return $dir = '';
}

function hm_ip() {
    foreach (array('HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR') as $k) {
        if (!empty($_SERVER[$k])) { $v = trim(explode(',', $_SERVER[$k])[0]); if ($v !== '') return $v; }
    }
    return '';
}

// Постоянный идентификатор устройства: отличает телефон от ноутбука одного человека
function hm_vid() {
    if (empty($_COOKIE['hm_al_vid']) || !preg_match('/^[a-f0-9]{16}$/', $_COOKIE['hm_al_vid'])) {
        hm_cookie('hm_al_vid', bin2hex(random_bytes(8)), 400);
    }
    return $_COOKIE['hm_al_vid'];
}

function hm_owner() { return !empty($_COOKIE['hm_al_owner']); }

function hm_write($row) {
    $d = hm_dir(); if ($d === '') return;
    @file_put_contents($d . '/events.jsonl', json_encode($row, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
}

function hm_event($ev, $extra = array()) {
    $row = array(
        't' => date('c'), 'ev' => $ev, 'vid' => hm_vid(), 'owner' => hm_owner() ? 1 : 0,
        'ip' => hm_ip(), 'ua' => isset($_SERVER['HTTP_USER_AGENT']) ? substr($_SERVER['HTTP_USER_AGENT'], 0, 300) : '',
        'ref' => isset($_SERVER['HTTP_REFERER']) ? substr($_SERVER['HTTP_REFERER'], 0, 300) : '',
    );
    hm_write(array_merge($row, $extra));
}

// Город и организация по IP (ip-api.com), с кешем, чтобы не дёргать сервис на каждое событие
function hm_geo($ip) {
    if ($ip === '' || preg_match('/^(127\.|10\.|192\.168\.|::1)/', $ip)) return array('city' => 'локально');
    $d = hm_dir(); $cf = $d !== '' ? $d . '/geo.json' : '';
    $cache = ($cf && is_file($cf)) ? (json_decode((string)@file_get_contents($cf), true) ?: array()) : array();
    if (isset($cache[$ip])) return $cache[$ip];
    $ctx = stream_context_create(array('http' => array('timeout' => 2)));
    $raw = @file_get_contents('http://ip-api.com/json/' . rawurlencode($ip) . '?fields=status,country,regionName,city,org,isp,mobile&lang=ru', false, $ctx);
    $j = $raw ? json_decode($raw, true) : null;
    $g = ($j && isset($j['status']) && $j['status'] === 'success')
        ? array('country' => $j['country'], 'region' => $j['regionName'], 'city' => $j['city'], 'org' => $j['org'] ?: $j['isp'], 'isp' => $j['isp'], 'mobile' => !empty($j['mobile']))
        : array();
    if ($cf) { $cache[$ip] = $g; @file_put_contents($cf, json_encode($cache, JSON_UNESCAPED_UNICODE), LOCK_EX); }
    return $g;
}

function hm_device($ua) {
    $os = 'другое';
    if (preg_match('/iPad|Macintosh.*Mobile/i', $ua)) $os = 'iPad';
    elseif (stripos($ua, 'iPhone') !== false) $os = 'iPhone';
    elseif (stripos($ua, 'Android') !== false) $os = stripos($ua, 'Mobile') !== false ? 'Android-телефон' : 'Android-планшет';
    elseif (stripos($ua, 'Windows') !== false) $os = 'Windows';
    elseif (stripos($ua, 'Mac OS X') !== false) $os = 'Mac';
    elseif (stripos($ua, 'Linux') !== false) $os = 'Linux';
    $br = 'браузер';
    if (stripos($ua, 'YaBrowser') !== false) $br = 'Яндекс Браузер';
    elseif (stripos($ua, 'Edg/') !== false) $br = 'Edge';
    elseif (stripos($ua, 'OPR/') !== false) $br = 'Opera';
    elseif (stripos($ua, 'Firefox') !== false) $br = 'Firefox';
    elseif (stripos($ua, 'Chrome') !== false || stripos($ua, 'CriOS') !== false) $br = 'Chrome';
    elseif (stripos($ua, 'Safari') !== false) $br = 'Safari';
    if (preg_match('/Telegram|TelegramBot/i', $ua)) $br .= ' (Telegram)';
    return $os . ', ' . $br;
}

// Уведомление в Telegram через бот сайта: токены читаем из api/config.php, сам файл не меняем
function hm_tg($text) {
    if (hm_owner()) return;
    $root = isset($_SERVER['DOCUMENT_ROOT']) ? rtrim($_SERVER['DOCUMENT_ROOT'], '/') : '';
    if ($root !== '' && is_file($root . '/api/config.php')) @include_once $root . '/api/config.php';
    if (!defined('TELEGRAM_BOT_TOKEN') || !defined('TELEGRAM_CHAT_ID') || !TELEGRAM_BOT_TOKEN) return;
    $ctx = stream_context_create(array('http' => array(
        'method' => 'POST', 'timeout' => 3, 'header' => "Content-Type: application/x-www-form-urlencoded\r\n",
        'content' => http_build_query(array('chat_id' => TELEGRAM_CHAT_ID, 'text' => $text, 'parse_mode' => 'HTML', 'disable_web_page_preview' => 1)),
    )));
    @file_get_contents('https://api.telegram.org/bot' . TELEGRAM_BOT_TOKEN . '/sendMessage', false, $ctx);
}

function hm_where($g) {
    $p = array();
    if (!empty($g['city'])) $p[] = $g['city'];
    if (!empty($g['org'])) $p[] = $g['org'];
    if (!empty($g['mobile'])) $p[] = 'мобильная сеть';
    return $p ? implode(', ', $p) : 'место не определено';
}

function hm_esc($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

function hm_fmt($sec) {
    $sec = (int)round($sec);
    if ($sec < 60) return $sec . ' с';
    $m = intdiv($sec, 60); $s = $sec % 60;
    if ($m < 60) return $m . ' мин' . ($s ? ' ' . $s . ' с' : '');
    return intdiv($m, 60) . ' ч ' . ($m % 60) . ' мин';
}

// Приём событий со страницы (navigator.sendBeacon, JSON). Только для вошедших.
function hm_track() {
    $raw = file_get_contents('php://input');
    if ($raw === false || strlen($raw) > 65536) { http_response_code(413); return; }
    $j = json_decode($raw, true);
    if (!is_array($j) || empty($j['sid']) || !preg_match('/^[a-z0-9]{8,32}$/', $j['sid'])) { http_response_code(400); return; }
    $row = array(
        't' => date('c'), 'ev' => 'beacon', 'vid' => hm_vid(), 'owner' => hm_owner() ? 1 : 0, 'ip' => hm_ip(),
        'sid' => $j['sid'],
        'env' => isset($j['env']) && is_array($j['env']) ? $j['env'] : null,
        'events' => isset($j['events']) && is_array($j['events']) ? array_slice($j['events'], 0, 200) : array(),
        'dwell' => isset($j['dwell']) && is_array($j['dwell']) ? $j['dwell'] : array(),
        'order' => isset($j['order']) && is_array($j['order']) ? array_slice($j['order'], 0, 40) : array(),
        'active' => isset($j['active']) ? (int)$j['active'] : 0,
        'scroll' => isset($j['scroll']) ? (int)$j['scroll'] : 0,
        'final' => !empty($j['final']) ? 1 : 0,
    );
    hm_write($row);
    // Итог визита в Telegram: когда гость закрыл или свернул страницу, пробыв больше 20 секунд
    if ($row['final'] && $row['active'] >= 20 && !hm_owner()) {
        $d = hm_dir(); $sent = $d !== '' ? $d . '/tg-sent.json' : '';
        $done = ($sent && is_file($sent)) ? (json_decode((string)@file_get_contents($sent), true) ?: array()) : array();
        $key = $row['sid'] . ':' . intdiv($row['active'], 60); // не чаще раза в минуту активного времени
        if (empty($done[$key])) {
            arsort($row['dwell']); $top = array_slice($row['dwell'], 0, 4, true);
            $lines = array(); foreach ($top as $name => $sec) { if ($sec >= 3) $lines[] = '• ' . $name . ': ' . hm_fmt($sec); }
            $notes = array();
            foreach ($row['events'] as $e) { if (!empty($e['k']) && $e['k'] === 'game_release') $notes[] = 'прошли игру'; }
            hm_tg("📊 <b>АЛИДИ изучают страницу</b>\nактивно " . hm_fmt($row['active']) . ", прокрутка " . $row['scroll'] . "%\n"
                . ($lines ? implode("\n", $lines) : '') . ($notes ? "\n" . implode(', ', array_unique($notes)) : ''));
            $done[$key] = 1; if ($sent) @file_put_contents($sent, json_encode($done), LOCK_EX);
        }
    }
    http_response_code(204);
}

// ---------- Отчёт для Hand Marketing ----------
function hm_stats_page($key) {
    global $STATS_HASH;
    if (!is_string($key) || !hash_equals($STATS_HASH, hash('sha256', $key))) { http_response_code(404); echo 'Not found'; exit; }
    hm_cookie('hm_al_owner', '1', 400); // этот браузер больше не считается клиентом
    $d = hm_dir(); $file = $d !== '' ? $d . '/events.jsonl' : '';
    // Обнулить: текущий журнал уходит в архив с датой, счёт начинается заново
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['reset'])) {
        if ($file && is_file($file)) @rename($file, $d . '/events-archive-' . date('Ymd-His') . '.jsonl');
        if ($d !== '' && is_file($d . '/tg-sent.json')) @unlink($d . '/tg-sent.json');
        header('Location: ?stats=' . rawurlencode($key));
        exit;
    }
    if (isset($_GET['raw'])) {
        header('Content-Type: application/x-ndjson; charset=utf-8');
        header('Content-Disposition: attachment; filename="alidi-events.jsonl"');
        if ($file && is_file($file)) readfile($file);
        exit;
    }
    $rows = array();
    if ($file && is_file($file)) {
        foreach (file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $l) { $r = json_decode($l, true); if ($r) $rows[] = $r; }
    }
    $showOwner = isset($_GET['all']);

    // Сборка: устройства → визиты (sid). Серверные события привязываем к ближайшему визиту устройства.
    $devices = array(); $fails = array(); $pdf = 0; $logins = 0;
    foreach ($rows as $r) {
        if (!$showOwner && !empty($r['owner'])) continue;
        $vid = isset($r['vid']) ? $r['vid'] : '?';
        if (!isset($devices[$vid])) $devices[$vid] = array('ua' => '', 'ip' => array(), 'sessions' => array(), 'server' => array(), 'owner' => !empty($r['owner']), 'first' => $r['t'], 'last' => $r['t']);
        $D = &$devices[$vid];
        $D['last'] = $r['t'];
        if (!empty($r['ua'])) $D['ua'] = $r['ua'];
        if (!empty($r['ip'])) $D['ip'][$r['ip']] = 1;
        if ($r['ev'] === 'beacon') {
            $sid = $r['sid'];
            if (!isset($D['sessions'][$sid])) $D['sessions'][$sid] = array('start' => $r['t'], 'end' => $r['t'], 'env' => null, 'events' => array(), 'dwell' => array(), 'order' => array(), 'active' => 0, 'scroll' => 0);
            $S = &$D['sessions'][$sid];
            $S['end'] = $r['t'];
            if (!empty($r['env'])) $S['env'] = $r['env'];
            foreach ($r['events'] as $e) $S['events'][] = $e;
            foreach ($r['dwell'] as $k => $v) $S['dwell'][$k] = max(isset($S['dwell'][$k]) ? $S['dwell'][$k] : 0, (float)$v);
            if (!empty($r['order'])) $S['order'] = $r['order'];
            $S['active'] = max($S['active'], $r['active']); $S['scroll'] = max($S['scroll'], $r['scroll']);
            unset($S);
        } else {
            $D['server'][] = $r;
            if ($r['ev'] === 'login_fail') $fails[] = $r;
            if ($r['ev'] === 'pdf_download') $pdf++;
            if ($r['ev'] === 'login_ok') $logins++;
        }
        unset($D);
    }
    uasort($devices, function ($a, $b) { return strcmp($b['last'], $a['last']); });
    $totalActive = 0; $sessCount = 0; $sectionTotals = array(); $orderAll = array(); $gameDone = 0;
    foreach ($devices as $D) foreach ($D['sessions'] as $S) {
        $totalActive += $S['active']; $sessCount++;
        foreach ($S['dwell'] as $k => $v) $sectionTotals[$k] = (isset($sectionTotals[$k]) ? $sectionTotals[$k] : 0) + $v;
        foreach ($S['order'] as $o) if (!in_array($o, $orderAll, true)) $orderAll[] = $o;
        foreach ($S['events'] as $e) if (isset($e['k']) && $e['k'] === 'game_release') { $gameDone++; break; }
    }
    $maxSec = $sectionTotals ? max($sectionTotals) : 1;

    header('Content-Type: text/html; charset=utf-8');
    $kq = '?stats=' . rawurlencode($key);
    ?><!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Аналитика · АЛИДИ, фильм к 35-летию</title><link rel="stylesheet" href="/fonts/unbounded-fira.css"><link rel="stylesheet" href="/fonts/react-main.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,system-ui,sans-serif;background:#f5f5f5;color:#090714;font-size:15px;line-height:1.5;padding:28px 16px 60px}
.w{max-width:1120px;margin:0 auto}h1{font-family:Unbounded,Inter,sans-serif;font-weight:500;font-size:clamp(24px,4vw,40px);letter-spacing:-.04em}h2{font-family:Unbounded,Inter,sans-serif;font-weight:500;font-size:20px;letter-spacing:-.03em;margin:34px 0 12px}
.sub{color:#5b5d67;margin-top:6px}.bar{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}.bar a{background:#fff;border-radius:99px;padding:9px 16px;text-decoration:none;color:#090714;font-size:14px}.bar a.v{background:#754be9;color:#fff}
.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:22px}.kpi div{background:#fff;border-radius:18px;padding:16px 18px}.kpi b{display:block;font-family:Unbounded,Inter,sans-serif;font-weight:500;font-size:26px;letter-spacing:-.04em}.kpi span{font-size:13px;color:#5b5d67}
.card{background:#fff;border-radius:22px;padding:22px;margin-top:12px}.row{display:grid;grid-template-columns:210px 1fr 70px;gap:10px;align-items:center;padding:5px 0;font-size:14px}.row .t{height:12px;border-radius:6px;background:#efeafd;overflow:hidden}.row .t i{display:block;height:100%;background:#754be9;border-radius:6px}.row .s{text-align:right;color:#5b5d67;font-variant-numeric:tabular-nums}
.dev h3{font-family:Unbounded,Inter,sans-serif;font-weight:500;font-size:17px;letter-spacing:-.02em}.meta{color:#5b5d67;font-size:13.5px;margin-top:4px}.owner{opacity:.55}.tag{display:inline-block;background:#efeafd;color:#754be9;border-radius:99px;padding:3px 10px;font-size:12px;font-weight:600;margin-left:6px;vertical-align:middle}.tag.g{background:#e3f7ea;color:#1e7a45}.tag.o{background:#fff1e0;color:#b45309}
.sess{border-top:1px solid #eee;margin-top:16px;padding-top:14px}.sess h4{font-size:14.5px;font-weight:600}.tl{margin-top:10px;font-size:13.5px;color:#5b5d67;display:flex;flex-direction:column;gap:3px;max-height:340px;overflow:auto}.tl b{color:#090714;font-weight:600;font-variant-numeric:tabular-nums;display:inline-block;min-width:54px}
.fail{font-size:13.5px;color:#5b5d67}.empty{color:#8e9099;padding:30px 0;text-align:center}
@media(max-width:640px){.row{grid-template-columns:120px 1fr 56px;font-size:13px}}
</style></head><body><div class="w">
<h1>Как АЛИДИ изучают страницу</h1>
<p class="sub">/for/alidi/ · обновлено <?= date('d.m.Y H:i') ?> · <?= $showOwner ? 'показаны все визиты, включая ваши' : 'ваши визиты скрыты' ?></p>
<div class="bar"><a class="v" href="<?= hm_esc($kq . ($showOwner ? '&all=1' : '')) ?>">Обновить</a><a href="<?= hm_esc($showOwner ? $kq : $kq . '&all=1') ?>"><?= $showOwner ? 'Скрыть мои визиты' : 'Показать мои визиты' ?></a><a href="<?= hm_esc($kq . '&raw=1') ?>">Скачать сырой журнал</a><a href="./" target="_blank">Открыть страницу</a>
<form method="post" action="<?= hm_esc($kq) ?>" onsubmit="return confirm('Обнулить статистику? Текущий журнал уйдёт в архив на сервере.')" style="display:inline"><button name="reset" value="1" style="font:inherit;font-size:14px;background:#fff;border:0;border-radius:99px;padding:9px 16px;cursor:pointer;color:#c2410c">Обнулить статистику</button></form></div>
<?php if (!$rows || (!$devices && !$fails)): ?><div class="card empty">Пока никто не заходил. Уведомление о первом входе придёт в Telegram.</div><?php else: ?>
<div class="kpi">
  <div><b><?= count($devices) ?></b><span>устройств</span></div>
  <div><b><?= $logins ?></b><span>входов по паролю</span></div>
  <div><b><?= $sessCount ?></b><span>просмотров страницы</span></div>
  <div><b><?= hm_fmt($totalActive) ?></b><span>активного времени всего</span></div>
  <div><b><?= $gameDone ?></b><span>раз прошли игру</span></div>
  <div><b><?= $pdf ?></b><span>скачиваний PDF</span></div>
</div>
<?php if ($sectionTotals): ?>
<h2>Где задерживались, все визиты вместе</h2><div class="card">
<?php foreach ($orderAll as $name) { if (!isset($sectionTotals[$name])) continue; $v = $sectionTotals[$name]; ?>
  <div class="row"><span><?= hm_esc($name) ?></span><span class="t"><i style="width:<?= max(1, round($v / $maxSec * 100)) ?>%"></i></span><span class="s"><?= hm_fmt($v) ?></span></div>
<?php } ?></div><?php endif; ?>
<h2>Визиты по устройствам</h2>
<?php foreach ($devices as $vid => $D) {
    $ips = array_keys($D['ip']); $g = $ips ? hm_geo($ips[0]) : array();
    $firstSrv = $D['server'] ? $D['server'][0]['t'] : $D['first']; ?>
<div class="card dev<?= $D['owner'] ? ' owner' : '' ?>">
  <h3><?= hm_esc(hm_device($D['ua'])) ?><?= $D['owner'] ? '<span class="tag o">это вы</span>' : '' ?></h3>
  <p class="meta"><?= hm_esc(hm_where($g)) ?> · IP <?= hm_esc(implode(', ', $ips)) ?> · первый заход <?= date('d.m H:i', strtotime($firstSrv)) ?>, последний <?= date('d.m H:i', strtotime($D['last'])) ?></p>
  <p class="meta"><?php
    $srv = array(); foreach ($D['server'] as $e) {
        $lbl = array('gate_view' => 'открыл экран пароля', 'login_ok' => 'вошёл по паролю', 'login_fail' => 'ввёл неверный пароль', 'pdf_download' => 'скачал PDF', 'page_view' => 'открыл страницу');
        $srv[] = date('d.m H:i', strtotime($e['t'])) . ' ' . (isset($lbl[$e['ev']]) ? $lbl[$e['ev']] : $e['ev']);
    }
    echo hm_esc(implode(' · ', array_slice($srv, -12))); ?></p>
  <?php foreach (array_reverse($D['sessions'], true) as $sid => $S) {
      $env = $S['env'] ?: array(); ?>
  <div class="sess">
    <h4><?= date('d.m.Y H:i', strtotime($S['start'])) ?> · активно <?= hm_fmt($S['active']) ?> · прокрутка <?= (int)$S['scroll'] ?>%
      <?php foreach ($S['events'] as $e) { if (isset($e['k']) && $e['k'] === 'game_release') { echo '<span class="tag g">прошёл игру</span>'; break; } } ?>
      <?php foreach ($S['events'] as $e) { if (isset($e['k']) && $e['k'] === 'pdf') { echo '<span class="tag">нажал PDF</span>'; break; } } ?></h4>
    <p class="meta"><?= !empty($env['vw']) ? 'экран ' . (int)$env['sw'] . '×' . (int)$env['sh'] . ', окно ' . (int)$env['vw'] . '×' . (int)$env['vh'] : '' ?><?= !empty($env['tz']) ? ' · ' . hm_esc($env['tz']) : '' ?><?= !empty($env['ref']) ? ' · пришёл с ' . hm_esc($env['ref']) : '' ?></p>
    <?php $mx = $S['dwell'] ? max($S['dwell']) : 1; $ord = $S['order'] ?: array_keys($S['dwell']);
    foreach ($ord as $name) { if (empty($S['dwell'][$name])) continue; $v = $S['dwell'][$name]; ?>
    <div class="row"><span><?= hm_esc($name) ?></span><span class="t"><i style="width:<?= max(1, round($v / $mx * 100)) ?>%"></i></span><span class="s"><?= hm_fmt($v) ?></span></div>
    <?php } ?>
    <?php if ($S['events']) { ?><div class="tl"><?php foreach ($S['events'] as $e) { ?><div><b><?= isset($e['at']) ? hm_fmt($e['at'] / 1000) : '' ?></b> <?= hm_esc(isset($e['d']) ? $e['d'] : '') ?></div><?php } ?></div><?php } ?>
  </div>
  <?php } ?>
</div>
<?php } ?>
<?php if ($fails) { ?><h2>Неверные пароли</h2><div class="card fail"><?php foreach (array_slice(array_reverse($fails), 0, 30) as $f) { echo hm_esc(date('d.m H:i', strtotime($f['t'])) . ' · ' . hm_device($f['ua']) . ' · ' . hm_where(hm_geo($f['ip'])) . ' · длина ввода ' . (isset($f['len']) ? $f['len'] : '?')) . '<br>'; } ?></div><?php } ?>
<?php endif; ?>
<p class="sub" style="margin-top:30px">Журнал: <?= hm_esc($d !== '' ? (strpos($d, __DIR__) === 0 ? 'рядом со страницей (_data, закрыт)' : 'вне корня сайта') : 'НЕ ПИШЕТСЯ: нет прав на запись') ?>. Вебвизор с записью экрана: Метрика 71125393, фильтр по странице /for/alidi/.</p>
</div></body></html><?php
    exit;
}
