<?php
/**
 * Единый обработчик заявок с форм сайта hand-marketing.ru.
 * Принимает form-POST, urlencoded или JSON (фронтенды разные: React SPA,
 * Astro-страницы, статические страницы зеркала).
 * Сохраняет заявку в leads.csv, отправляет на e-mail и — если на сервере
 * лежит api/config.php с токенами — в Telegram.
 * Возвращает JSON с обоими флагами: {"success":true,"ok":true}.
 *
 * api/config.php (НЕ в git, исключён из деплой-синка), формат:
 *   <?php
 *   const TELEGRAM_BOT_TOKEN = '<токен от @BotFather>';
 *   const TELEGRAM_CHAT_ID   = '<ID чата для заявок>';
 */

header('Content-Type: application/json; charset=utf-8');

// --- НАСТРОЙКИ ---
$TO      = 'info@hand-marketing.ru';      // куда слать заявки
$SUBJECT = 'Заявка с сайта hand-marketing.ru';
$LOGFILE = __DIR__ . '/leads.csv';        // резервная запись заявок
// -----------------

@include __DIR__ . '/config.php'; // токены Telegram живут только на сервере

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'ok' => false, 'error' => 'method not allowed']);
    exit;
}

// простейший rate-limit: не чаще одной заявки в 10 секунд с одного IP
$rlFile = sys_get_temp_dir() . '/hm-lead-' . md5($_SERVER['REMOTE_ADDR'] ?? '');
if (file_exists($rlFile) && time() - (int)@filemtime($rlFile) < 10) {
    http_response_code(429);
    echo json_encode(['success' => false, 'ok' => false, 'error' => 'too many requests']);
    exit;
}
@touch($rlFile);

// собрать поля: обычный POST, urlencoded raw или JSON
$data = $_POST;
if (empty($data)) {
    $raw = file_get_contents('php://input');
    parse_str($raw, $data);
    if (empty($data)) {
        $json = json_decode($raw, true);
        if (is_array($json)) $data = $json;
    }
}

// honeypot: скрытое поле заполняют только боты — отвечаем «успехом», ничего не шлём
if (!empty($data['website'])) {
    echo json_encode(['success' => true, 'ok' => true]);
    exit;
}

// защита от мусора: максимум 20 полей, безопасные имена, значения до 500 символов,
// переводы строк из значений выкидываются (заодно закрывает CRLF-инъекции в заголовки)
$skip = ['formid', 'tnspec', 'form-spec-comments-value', '_ga', 'website'];
$clean = [];
foreach ($data as $k => $v) {
    if (count($clean) >= 20) break;
    if (!is_string($k) || in_array($k, $skip, true)) continue;
    if (!preg_match('/^[\w\- ]{1,40}$/u', $k)) continue;
    if (is_array($v)) $v = implode(', ', $v);
    $v = trim(mb_substr(preg_replace('/[\r\n\t]+/', ' ', (string)$v), 0, 500));
    if ($v === '') continue;
    $clean[$k] = $v;
}

// в заявке должен быть хоть один контакт: телефон (6+ цифр) или валидный e-mail
$hasContact = false;
foreach ($clean as $v) {
    if (preg_match('/\d{6,}/', preg_replace('/\D/', '', $v)) || filter_var($v, FILTER_VALIDATE_EMAIL)) {
        $hasContact = true;
        break;
    }
}
if (!$hasContact) {
    http_response_code(422);
    echo json_encode(['success' => false, 'ok' => false, 'error' => 'validation']);
    exit;
}

$lines = [];
foreach ($clean as $k => $v) {
    $lines[] = mb_strtoupper($k) . ': ' . $v;
}
$body = implode("\n", $lines);
$body .= "\n\n—\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? '') .
         "\nВремя: " . date('Y-m-d H:i:s') .
         "\nСтраница: " . ($_SERVER['HTTP_REFERER'] ?? '');

// 1) сохранить в CSV (на случай проблем с почтой);
//    ведущие =,+,-,@ экранируются от formula-injection при открытии в Excel
$row = [date('Y-m-d H:i:s')];
foreach (['name', 'phone', 'email', 'contact', 'comment', 'Name', 'Phone', 'Email'] as $f) {
    if (isset($clean[$f])) $row[] = $clean[$f];
}
$row[] = $_SERVER['HTTP_REFERER'] ?? '';
$csv = array_map(function ($x) {
    $x = str_replace('"', "'", (string)$x);
    return preg_match('/^[=+\-@]/', $x) ? "'" . $x : $x;
}, $row);
@file_put_contents($LOGFILE, '"' . implode('","', $csv) . "\"\n", FILE_APPEND | LOCK_EX);

// 2) отправить письмо; Reply-To — только провалидированный e-mail
$replyTo = 'noreply@hand-marketing.ru';
foreach (['email', 'Email'] as $f) {
    if (isset($clean[$f]) && filter_var($clean[$f], FILTER_VALIDATE_EMAIL)) {
        $replyTo = $clean[$f];
        break;
    }
}
$headers = "From: site@hand-marketing.ru\r\n" .
           "Reply-To: {$replyTo}\r\n" .
           "Content-Type: text/plain; charset=utf-8\r\n";
@mail($TO, '=?UTF-8?B?' . base64_encode($SUBJECT) . '?=', $body, $headers);

// 3) уведомление в Telegram (работает, только если на сервере есть api/config.php)
if (defined('TELEGRAM_BOT_TOKEN') && TELEGRAM_BOT_TOKEN !== ''
    && defined('TELEGRAM_CHAT_ID') && TELEGRAM_CHAT_ID !== ''
    && function_exists('curl_init')) {
    $ch = curl_init('https://api.telegram.org/bot' . TELEGRAM_BOT_TOKEN . '/sendMessage');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 10,
        CURLOPT_POSTFIELDS => http_build_query([
            'chat_id' => TELEGRAM_CHAT_ID,
            'text'    => "🟢 Заявка с hand-marketing.ru\n" . $body,
        ]),
    ]);
    curl_exec($ch);
    curl_close($ch);
}

echo json_encode(['success' => true, 'ok' => true]);
