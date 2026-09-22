<?php
/**
 * Учёт заходов на приватную страницу-отчёт.
 *
 * Пишет строку в hits.log и, если на сервере лежит /api/config.php с токенами,
 * шлёт уведомление в тот же Telegram-чат, куда падают заявки с сайта.
 * Файл api/config.php НЕ трогается и НЕ перезаписывается — только читается.
 *
 * События:
 *   open   — страницу открыли (показалась форма пароля)
 *   unlock — ввели верный пароль, содержимое расшифровано
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$event = isset($_REQUEST['e']) ? preg_replace('/[^a-z]/', '', (string)$_REQUEST['e']) : '';
if ($event !== 'open' && $event !== 'unlock') {
    http_response_code(400);
    echo json_encode(['ok' => false]);
    exit;
}

// --- откуда пришли ---
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['HTTP_X_REAL_IP'] ?? $_SERVER['REMOTE_ADDR'] ?? '-';
$ip = trim(explode(',', $ip)[0]);
$ua = substr((string)($_SERVER['HTTP_USER_AGENT'] ?? '-'), 0, 300);
$ref = substr((string)($_SERVER['HTTP_REFERER'] ?? '-'), 0, 200);

$tz = new DateTimeZone('Europe/Moscow');
$now = new DateTime('now', $tz);
$stamp = $now->format('d.m.Y H:i:s');

// --- запись в лог ---
$line = implode("\t", [$stamp, $event, $ip, $ref, $ua]) . "\n";
@file_put_contents(__DIR__ . '/hits.log', $line, FILE_APPEND | LOCK_EX);

// --- уведомление в Telegram (не чаще раза в 10 минут на связку событие+IP) ---
$notified = false;
$guard = __DIR__ . '/.hit-guard.json';
$key = $event . '|' . $ip;
$state = [];
if (is_readable($guard)) {
    $state = json_decode((string)@file_get_contents($guard), true) ?: [];
}
$last = isset($state[$key]) ? (int)$state[$key] : 0;

if (time() - $last > 600) {
    @include $_SERVER['DOCUMENT_ROOT'] . '/api/config.php';

    if (defined('TELEGRAM_BOT_TOKEN') && defined('TELEGRAM_CHAT_ID')) {
        $title = $event === 'unlock'
            ? "Отчёт открыли паролем"
            : "Заходили на страницу отчёта";

        $text = "*{$title}*\n"
              . "Проект: Голубой огонёк 2025\n"
              . "Время: {$stamp} (МСК)\n"
              . "IP: `{$ip}`\n"
              . "Устройство: " . preg_replace('/[*_`\[\]]/', '', $ua);

        $payload = http_build_query([
            'chat_id'    => TELEGRAM_CHAT_ID,
            'text'       => $text,
            'parse_mode' => 'Markdown',
            'disable_web_page_preview' => true,
        ]);

        $url = 'https://api.telegram.org/bot' . TELEGRAM_BOT_TOKEN . '/sendMessage';
        $ctx = stream_context_create(['http' => [
            'method'  => 'POST',
            'header'  => "Content-Type: application/x-www-form-urlencoded\r\n",
            'content' => $payload,
            'timeout' => 5,
            'ignore_errors' => true,
        ]]);
        $res = @file_get_contents($url, false, $ctx);
        $notified = $res !== false;

        $state[$key] = time();
        // чистим старые записи, чтобы файл не рос
        foreach ($state as $k => $t) {
            if (time() - (int)$t > 86400) unset($state[$k]);
        }
        @file_put_contents($guard, json_encode($state), LOCK_EX);
    }
}

echo json_encode(['ok' => true, 'notified' => $notified]);
