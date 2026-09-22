<?php
/**
 * Просмотр заходов на приватную страницу-отчёт.
 * Открывается только с ключом: log.php?k=<ключ>
 */

$KEY = 'hm-2025-log-4e91';

if (!isset($_GET['k']) || !hash_equals($KEY, (string)$_GET['k'])) {
    http_response_code(404);
    exit('Not Found');
}

header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');

$file = __DIR__ . '/hits.log';
$rows = [];
if (is_readable($file)) {
    foreach (array_reverse(array_filter(explode("\n", (string)file_get_contents($file)))) as $l) {
        $p = explode("\t", $l);
        if (count($p) >= 3) $rows[] = $p;
    }
}

$opens = 0; $unlocks = 0; $ips = [];
foreach ($rows as $r) {
    if ($r[1] === 'open') $opens++;
    if ($r[1] === 'unlock') $unlocks++;
    $ips[$r[2]] = true;
}
?><!DOCTYPE html>
<html lang="ru"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Заходы на отчёт</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fafaf8;color:#080000;font:15px/1.5 -apple-system,system-ui,sans-serif;padding:28px}
h1{font-size:22px;margin-bottom:6px}
.sub{color:#8c8c88;font-size:13px;margin-bottom:22px}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px}
.c{background:#fff;border:1px solid #e7e7e4;border-radius:12px;padding:16px 20px;min-width:150px}
.c b{display:block;font-size:30px;line-height:1.1}
.c span{font-size:12px;color:#8c8c88}
.c.hot b{color:#609430}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e7e7e4;border-radius:12px;overflow:hidden}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#8c8c88;
  padding:10px 12px;border-bottom:1px solid #e7e7e4;background:#f4f4f2}
td{padding:9px 12px;border-bottom:1px solid #f4f4f2;font-size:13px;vertical-align:top}
tr:last-child td{border-bottom:none}
.ev{font-weight:600}
.ev.unlock{color:#609430}
.ev.open{color:#8c8c88}
.ua{color:#8c8c88;font-size:11px;max-width:420px;word-break:break-word}
.empty{background:#fff;border:1px solid #e7e7e4;border-radius:12px;padding:28px;color:#8c8c88}
code{font-family:ui-monospace,monospace;font-size:12px}
</style></head><body>

<h1>Заходы на отчёт</h1>
<div class="sub">Голубой огонёк 2025 · время московское</div>

<div class="cards">
  <div class="c"><b><?= $opens ?></b><span>открывали страницу</span></div>
  <div class="c hot"><b><?= $unlocks ?></b><span>вводили пароль</span></div>
  <div class="c"><b><?= count($ips) ?></b><span>разных устройств</span></div>
</div>

<?php if (!$rows): ?>
  <div class="empty">Пока никто не заходил.</div>
<?php else: ?>
<table>
  <tr><th>Когда</th><th>Что</th><th>IP</th><th>Устройство</th></tr>
  <?php foreach ($rows as $r): ?>
  <tr>
    <td><?= htmlspecialchars($r[0]) ?></td>
    <td class="ev <?= htmlspecialchars($r[1]) ?>">
      <?= $r[1] === 'unlock' ? 'ввели пароль' : 'открыли' ?>
    </td>
    <td><code><?= htmlspecialchars($r[2]) ?></code></td>
    <td class="ua"><?= htmlspecialchars($r[4] ?? '-') ?></td>
  </tr>
  <?php endforeach; ?>
</table>
<?php endif; ?>

</body></html>
