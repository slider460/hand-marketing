<?php
/**
 * Панель просмотра заходов на приватную страницу-отчёт.
 * Доступ только с ключом: log.php?k=<ключ>
 */

$KEY = 'hm-2025-log-4e91';
if (!isset($_GET['k']) || !hash_equals($KEY, (string)$_GET['k'])) {
    http_response_code(404);
    exit('Not Found');
}

// ---------- обнуление статистики ----------
if (isset($_GET['reset']) && $_GET['reset'] === '1') {
    foreach (['hits.jsonl', 'hits.log', '.hit-guard.json', '.geo-cache.json'] as $f) {
        @unlink(__DIR__ . '/' . $f);
    }
    header('Location: log.php?k=' . urlencode($KEY) . '&cleared=1');
    exit;
}

header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');

$tz = new DateTimeZone('Europe/Moscow');
$events = [];
foreach ([__DIR__ . '/hits.jsonl'] as $f) {
    if (!is_readable($f)) continue;
    foreach (explode("\n", (string)file_get_contents($f)) as $l) {
        if (trim($l) === '') continue;
        $r = json_decode($l, true);
        if (is_array($r)) $events[] = $r;
    }
}
// старый формат (табуляции) — если остался
if (is_readable(__DIR__ . '/hits.log')) {
    foreach (explode("\n", (string)file_get_contents(__DIR__ . '/hits.log')) as $l) {
        if (trim($l) === '') continue;
        $p = explode("\t", $l);
        if (count($p) >= 3) {
            $events[] = ['ts' => strtotime(str_replace('.', '-', $p[0])) ?: 0,
                         'sid' => 'old', 'e' => $p[1], 'ip' => $p[2], 'ua' => $p[4] ?? '-'];
        }
    }
}

// ---------- группируем в сессии ----------
$S = [];
foreach ($events as $r) {
    $sid = $r['sid'] ?: ('ip-' . ($r['ip'] ?? '-'));
    if (!isset($S[$sid])) {
        $S[$sid] = ['first'=>$r['ts'],'last'=>$r['ts'],'ip'=>$r['ip'] ?? '-','ua'=>$r['ua'] ?? '-',
                    'geo'=>[], 'unlock'=>false,'sec'=>0,'scroll'=>0,'sections'=>[],'clicks'=>[],'screen'=>'','tz'=>''];
    }
    $s =& $S[$sid];
    $s['first'] = min($s['first'], $r['ts']);
    $s['last']  = max($s['last'], $r['ts']);
    if (!empty($r['geo'])) $s['geo'] = $r['geo'];
    if ($r['e'] === 'unlock') $s['unlock'] = true;
    if ($r['e'] === 'start' && is_array($r['v'] ?? null)) {
        $s['screen'] = $r['v']['screen'] ?? '';
        $s['tz'] = $r['v']['tz'] ?? '';
    }
    if (in_array($r['e'], ['beat','end'], true) && is_array($r['v'] ?? null)) {
        $s['sec']    = max($s['sec'], (int)($r['v']['sec'] ?? 0));
        $s['scroll'] = max($s['scroll'], (int)($r['v']['scroll'] ?? 0));
    }
    if ($r['e'] === 'scroll') $s['scroll'] = max($s['scroll'], (int)($r['v'] ?? 0));
    if ($r['e'] === 'section' && $r['v']) $s['sections'][(string)$r['v']] = true;
    if ($r['e'] === 'click' && is_array($r['v'] ?? null)) {
        $t = (string)($r['v']['t'] ?? '');
        if ($t !== '') $s['clicks'][$t] = ($s['clicks'][$t] ?? 0) + 1;
    }
    unset($s);
}
uasort($S, fn($a,$b) => $b['first'] <=> $a['first']);

$totalOpen = count($S);
$totalUnlock = count(array_filter($S, fn($s) => $s['unlock']));
$countries = [];
foreach ($S as $s) if (!empty($s['geo']['country'])) $countries[$s['geo']['country']] = true;
$maxSec = 0; foreach ($S as $s) $maxSec = max($maxSec, $s['sec']);

function dev(string $ua): string {
    if (preg_match('/iPhone|iPad/i',$ua)) return 'iPhone/iPad';
    if (preg_match('/Android/i',$ua))     return 'Android';
    if (preg_match('/Macintosh/i',$ua))   return 'Mac';
    if (preg_match('/Windows/i',$ua))     return 'Windows';
    return 'другое';
}
function mmss(int $s): string {
    if ($s < 60) return $s . ' сек';
    return intdiv($s,60) . ' мин ' . ($s%60 ? ($s%60).' сек' : '');
}
?><!DOCTYPE html>
<html lang="ru"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Заходы на отчёт</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fafaf8;color:#080000;font:15px/1.55 -apple-system,system-ui,sans-serif;padding:26px}
h1{font-size:23px}
.sub{color:#8c8c88;font-size:13px;margin:4px 0 0}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:22px}
.reset{flex:none;font-size:13px;color:#8c8c88;text-decoration:none;border:1px solid #e7e7e4;
  background:#fff;border-radius:20px;padding:7px 15px;transition:all .15s}
.reset:hover{color:#ba1e1e;border-color:#ba1e1e}
.ok{background:#eef7dd;border:1px solid #93c01f;border-radius:10px;padding:12px 16px;
  margin-bottom:18px;font-size:14px}
.cards{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:26px}
.c{background:#fff;border:1px solid #e7e7e4;border-radius:12px;padding:15px 18px;min-width:140px}
.c b{display:block;font-size:28px;line-height:1.1}
.c span{font-size:12px;color:#8c8c88}
.c.hot b{color:#609430}
.s{background:#fff;border:1px solid #e7e7e4;border-radius:14px;padding:16px 18px;margin-bottom:12px}
.s.in{border-color:#609430;box-shadow:0 0 0 1px #609430 inset}
.hdr{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:baseline}
.when{font-weight:600}
.badge{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;
  padding:3px 9px;border-radius:20px;background:#f4f4f2;color:#8c8c88}
.badge.in{background:#609430;color:#fff}
.meta{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px;font-size:13px;color:#4a4a47}
.meta b{font-weight:600}
.bar{height:6px;background:#f4f4f2;border-radius:4px;margin-top:10px;overflow:hidden}
.bar i{display:block;height:100%;background:#609430}
.tags{margin-top:10px;display:flex;flex-wrap:wrap;gap:5px}
.tag{font-size:11.5px;background:#f4f4f2;border-radius:6px;padding:3px 8px;color:#4a4a47}
.tag.k{background:#fff3cd;color:#7a5b00}
.ua{font-size:11px;color:#a8a8a4;margin-top:8px;word-break:break-word}
.empty{background:#fff;border:1px solid #e7e7e4;border-radius:12px;padding:26px;color:#8c8c88}
code{font-family:ui-monospace,monospace;font-size:12px}
</style></head><body>

<div class="top">
  <div>
    <h1>Заходы на отчёт</h1>
    <div class="sub">Голубой огонёк 2025 · время московское</div>
  </div>
  <a class="reset" href="?k=<?= urlencode($KEY) ?>&amp;reset=1"
     onclick="return confirm('Обнулить статистику? Все записи будут удалены.')">Обнулить</a>
</div>

<?php if (isset($_GET['cleared'])): ?>
  <div class="ok">Статистика обнулена. Дальше пойдут только новые заходы.</div>
<?php endif; ?>

<div class="cards">
  <div class="c"><b><?= $totalOpen ?></b><span>всего визитов</span></div>
  <div class="c hot"><b><?= $totalUnlock ?></b><span>вошли по паролю</span></div>
  <div class="c"><b><?= count($countries) ?></b><span>стран</span></div>
  <div class="c"><b><?= $maxSec ? mmss($maxSec) : '—' ?></b><span>самый долгий просмотр</span></div>
</div>

<?php if (!$S): ?>
  <div class="empty">Пока никто не заходил.</div>
<?php else: foreach ($S as $sid => $s):
  $place = trim(($s['geo']['country'] ?? '') . ($s['geo']['city'] ? ', '.$s['geo']['city'] : ''), ' ,');
?>
<div class="s <?= $s['unlock'] ? 'in' : '' ?>">
  <div class="hdr">
    <span class="when"><?= (new DateTime('@'.$s['first']))->setTimezone($tz)->format('d.m.Y H:i') ?></span>
    <span class="badge <?= $s['unlock'] ? 'in' : '' ?>">
      <?= $s['unlock'] ? 'вошли по паролю' : 'только открыли' ?>
    </span>
  </div>

  <div class="meta">
    <span>Смотрели: <b><?= $s['sec'] ? mmss($s['sec']) : 'меньше 5 сек' ?></b></span>
    <span>Домотали: <b><?= $s['scroll'] ?>%</b></span>
    <span>Откуда: <b><?= $place !== '' ? htmlspecialchars($place) : 'не определилось' ?></b></span>
    <span><?= dev($s['ua']) ?><?= $s['screen'] ? ' · '.htmlspecialchars($s['screen']) : '' ?></span>
  </div>

  <div class="bar"><i style="width:<?= max(2,(int)$s['scroll']) ?>%"></i></div>

  <?php if ($s['sections'] || $s['clicks']): ?>
  <div class="tags">
    <?php foreach (array_keys($s['sections']) as $sec): ?>
      <span class="tag"><?= htmlspecialchars($sec) ?></span>
    <?php endforeach; ?>
    <?php foreach ($s['clicks'] as $t => $n): ?>
      <span class="tag k">клик: <?= htmlspecialchars($t) ?><?= $n > 1 ? " ×$n" : '' ?></span>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>

  <div class="ua">
    IP <code><?= htmlspecialchars($s['ip']) ?></code>
    <?php if (!empty($s['geo']['isp'])): ?> · <?= htmlspecialchars($s['geo']['isp']) ?><?php endif; ?>
    <?php if (!empty($s['geo']['proxy'])): ?> · через VPN/прокси<?php endif; ?>
    <?php if ($s['tz']): ?> · часовой пояс <?= htmlspecialchars($s['tz']) ?><?php endif; ?>
    <br><?= htmlspecialchars($s['ua']) ?>
  </div>
</div>
<?php endforeach; endif; ?>

</body></html>
