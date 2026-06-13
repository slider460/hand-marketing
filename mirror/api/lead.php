<?php
/**
 * Обработчик заявок с форм сайта hand-marketing.ru
 * Принимает POST с полей формы, сохраняет в leads.csv и отправляет на e-mail.
 * Возвращает JSON, который ожидает фронтенд (показ попапа «спасибо»).
 *
 * Настройка: укажите получателя в $TO ниже.
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

// --- НАСТРОЙКИ ---
$TO      = 'info@hand-marketing.ru';      // куда слать заявки
$SUBJECT = 'Заявка с сайта hand-marketing.ru';
$LOGFILE = __DIR__ . '/leads.csv';        // резервная запись заявок
// -----------------

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'method not allowed']);
    exit;
}

// собрать поля (Tilda шлёт name/phone/email/... как обычные POST-поля)
$data = $_POST;
if (empty($data)) {
    $raw = file_get_contents('php://input');
    parse_str($raw, $data);
    if (empty($data)) {
        $json = json_decode($raw, true);
        if (is_array($json)) $data = $json;
    }
}

// служебные поля Tilda не нужны
$skip = ['formid', 'tildaspec', 'form-spec-comments-value', '_ga'];
$lines = [];
foreach ($data as $k => $v) {
    if (in_array($k, $skip, true)) continue;
    if (is_array($v)) $v = implode(', ', $v);
    $lines[] = mb_strtoupper($k) . ': ' . trim((string)$v);
}
$body = implode("\n", $lines);
$body .= "\n\n—\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? '') .
         "\nВремя: " . date('Y-m-d H:i:s') .
         "\nСтраница: " . ($_SERVER['HTTP_REFERER'] ?? '');

// 1) сохранить в CSV (на случай проблем с почтой)
$row = [date('Y-m-d H:i:s')];
foreach (['name', 'phone', 'email', 'Name', 'Phone', 'Email'] as $f) {
    if (isset($data[$f])) $row[] = $data[$f];
}
$row[] = $_SERVER['HTTP_REFERER'] ?? '';
@file_put_contents($LOGFILE, '"' . implode('","', array_map(fn($x) => str_replace('"', "'", $x), $row)) . "\"\n", FILE_APPEND | LOCK_EX);

// 2) отправить письмо
$headers = "From: site@hand-marketing.ru\r\n" .
           "Reply-To: " . ($data['email'] ?? $data['Email'] ?? 'noreply@hand-marketing.ru') . "\r\n" .
           "Content-Type: text/plain; charset=utf-8\r\n";
@mail($TO, '=?UTF-8?B?' . base64_encode($SUBJECT) . '?=', $body, $headers);

echo json_encode(['success' => true]);
