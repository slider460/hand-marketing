<?php
/**
 * Обработчик формы «Перезвоните мне» для shared-хостинга (timeweb/beget/sprinthost/reg.ru).
 * Отправляет заявку в Telegram и на почту.
 * ЗАПОЛНИТЕ КОНСТАНТЫ НИЖЕ перед запуском (см. ANTIGRAVITY.md, раздел «Формы»).
 */
const TELEGRAM_BOT_TOKEN = ''; // токен бота от @BotFather
const TELEGRAM_CHAT_ID   = ''; // ID чата/группы для заявок
const MAIL_TO            = 'info@hand-marketing.ru';

header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit('{"ok":false}'); }

$raw  = file_get_contents('php://input');
$data = json_decode($raw, true) ?: $_POST;
$name  = trim(mb_substr($data['name']  ?? '', 0, 100));
$phone = trim(mb_substr($data['phone'] ?? '', 0, 30));
$page  = trim(mb_substr($data['page']  ?? '', 0, 200));
if ($name === '' || !preg_match('/\d{6,}/', preg_replace('/\D/', '', $phone))) {
  http_response_code(422); exit('{"ok":false,"error":"validation"}');
}

$text = "🟢 Заявка с hand-marketing.ru\nИмя: {$name}\nТелефон: {$phone}\nСтраница: {$page}\n" . date('d.m.Y H:i');

$ok = true;
if (TELEGRAM_BOT_TOKEN && TELEGRAM_CHAT_ID) {
  $ch = curl_init('https://api.telegram.org/bot' . TELEGRAM_BOT_TOKEN . '/sendMessage');
  curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 10,
    CURLOPT_POSTFIELDS => http_build_query(['chat_id' => TELEGRAM_CHAT_ID, 'text' => $text]),
  ]);
  $ok = curl_exec($ch) !== false && $ok;
  curl_close($ch);
}
if (MAIL_TO) {
  $headers = "From: site@hand-marketing.ru\r\nContent-Type: text/plain; charset=utf-8\r\n";
  @mail(MAIL_TO, 'Заявка с сайта hand-marketing.ru', $text, $headers);
}

echo json_encode(['ok' => $ok]);
