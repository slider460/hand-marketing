<?php
/**
 * Учёт заходов и поведения на приватной странице-отчёте.
 *
 * Принимает два вида обращений:
 *   GET  hit.php?e=open|unlock          — открыли страницу / ввели верный пароль
 *   POST hit.php  {sid,e,v}  (JSON)     — телеметрия: start, beat, scroll, section, click, end
 *
 * Пишет события построчно в hits.jsonl.
 * Страну и город определяет по IP через ip-api.com, результат кэширует.
 * Уведомления шлёт в тот же Telegram-чат, что и заявки: токены берутся
 * из /api/config.php — файл только читается, не изменяется.
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$DIR   = __DIR__;
$LOG   = $DIR . '/hits.jsonl';
$GEO   = $DIR . '/.geo-cache.json';
$GUARD = $DIR . '/.hit-guard.json';

// ---------- кто пришёл ----------
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['HTTP_X_REAL_IP'] ?? $_SERVER['REMOTE_ADDR'] ?? '-';
$ip = trim(explode(',', $ip)[0]);
$ua = substr((string)($_SERVER['HTTP_USER_AGENT'] ?? '-'), 0, 300);

// ---------- разбор запроса ----------
$raw = file_get_contents('php://input');
$in  = $raw ? json_decode($raw, true) : null;

if (is_array($in)) {
    $event = preg_replace('/[^a-z]/', '', (string)($in['e'] ?? ''));
    $sid   = preg_replace('/[^a-z0-9]/i', '', substr((string)($in['sid'] ?? ''), 0, 40));
    $val   = $in['v'] ?? null;
} else {
    $event = preg_replace('/[^a-z]/', '', (string)($_REQUEST['e'] ?? ''));
    $sid   = preg_replace('/[^a-z0-9]/i', '', substr((string)($_REQUEST['sid'] ?? ''), 0, 40));
    $val   = null;
}

$allowed = ['open','unlock','start','beat','scroll','section','click','end'];
if (!in_array($event, $allowed, true)) {
    http_response_code(400);
    echo json_encode(['ok' => false]);
    exit;
}

// ---------- гео по IP (с кэшем) ----------
function geo_for(string $ip, string $cacheFile): array {
    if ($ip === '-' || $ip === '' || strpos($ip, '127.') === 0) return [];
    $cache = is_readable($cacheFile)
        ? (json_decode((string)@file_get_contents($cacheFile), true) ?: [])
        : [];
    if (isset($cache[$ip]) && (time() - (int)($cache[$ip]['ts'] ?? 0) < 2592000)) {
        return $cache[$ip];
    }
    $url = 'http://ip-api.com/json/' . urlencode($ip)
         . '?fields=status,country,regionName,city,isp,mobile,proxy&lang=ru';
    $ctx = stream_context_create(['http' => ['timeout' => 3, 'ignore_errors' => true]]);
    $res = @file_get_contents($url, false, $ctx);
    $g = $res ? json_decode($res, true) : null;
    if (!is_array($g) || ($g['status'] ?? '') !== 'success') return [];
    $rec = [
        'country' => $g['country'] ?? '',
        'region'  => $g['regionName'] ?? '',
        'city'    => $g['city'] ?? '',
        'isp'     => $g['isp'] ?? '',
        'mobile'  => !empty($g['mobile']),
        'proxy'   => !empty($g['proxy']),
        'ts'      => time(),
    ];
    $cache[$ip] = $rec;
    @file_put_contents($cacheFile, json_encode($cache), LOCK_EX);
    return $rec;
}

// гео запрашиваем только на «тяжёлых» событиях, чтобы не дёргать сервис на каждый тик
$geo = in_array($event, ['open','unlock','start'], true) ? geo_for($ip, $GEO) : [];

// ---------- запись ----------
$rec = [
    'ts'  => time(),
    'sid' => $sid,
    'e'   => $event,
    'ip'  => $ip,
    'ua'  => $ua,
];
if ($val !== null) $rec['v'] = $val;
if ($geo)          $rec['geo'] = $geo;

@file_put_contents($LOG, json_encode($rec, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);

// ---------- уведомление в Telegram ----------
$notified = false;
if ($event === 'open' || $event === 'unlock') {
    $state = is_readable($GUARD)
        ? (json_decode((string)@file_get_contents($GUARD), true) ?: [])
        : [];
    $key  = $event . '|' . $ip;
    $last = (int)($state[$key] ?? 0);

    if (time() - $last > 600) {
        @include $_SERVER['DOCUMENT_ROOT'] . '/api/config.php';

        if (defined('TELEGRAM_BOT_TOKEN') && defined('TELEGRAM_CHAT_ID')) {
            $stamp = (new DateTime('now', new DateTimeZone('Europe/Moscow')))->format('d.m.Y H:i');
            $title = $event === 'unlock' ? 'Отчёт открыли паролем' : 'Заходили на страницу отчёта';

            $place = '';
            if ($geo) {
                $place = trim(($geo['country'] ?? '') . ', ' . ($geo['city'] ?? ''), ' ,');
                if (!empty($geo['isp'])) $place .= ' · ' . $geo['isp'];
            }

            $text = "*{$title}*\n"
                  . "Голубой огонёк 2025\n"
                  . "{$stamp} МСК\n"
                  . ($place ? "Откуда: {$place}\n" : '')
                  . "IP: `{$ip}`\n"
                  . 'Устройство: ' . preg_replace('/[*_`\[\]]/', '', $ua);

            $ctx = stream_context_create(['http' => [
                'method'  => 'POST',
                'header'  => "Content-Type: application/x-www-form-urlencoded\r\n",
                'content' => http_build_query([
                    'chat_id' => TELEGRAM_CHAT_ID,
                    'text' => $text,
                    'parse_mode' => 'Markdown',
                    'disable_web_page_preview' => true,
                ]),
                'timeout' => 5,
                'ignore_errors' => true,
            ]]);
            $notified = @file_get_contents(
                'https://api.telegram.org/bot' . TELEGRAM_BOT_TOKEN . '/sendMessage', false, $ctx
            ) !== false;

            $state[$key] = time();
            foreach ($state as $k => $t) {
                if (time() - (int)$t > 86400) unset($state[$k]);
            }
            @file_put_contents($GUARD, json_encode($state), LOCK_EX);
        }
    }
}

echo json_encode(['ok' => true, 'notified' => $notified]);
