<?php
// Персональная страница для Saint-Gobain — доступ по коду.
// В файле хранится только SHA-256 хеш кода, сам код передаётся клиенту лично.
$ACCESS_HASH = '0ab3fb03aec2b1593a74921073361ae74640a9ac747762e9c81ae6582d09ce87';
$COOKIE_NAME = 'hm_sg_access';

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: private, no-store');

$authed = isset($_COOKIE[$COOKIE_NAME]) && hash_equals($ACCESS_HASH, $_COOKIE[$COOKIE_NAME]);
$error  = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $code = strtoupper(preg_replace('/\s+/', '', $_POST['code'] ?? ''));
    if ($code !== '' && hash_equals($ACCESS_HASH, hash('sha256', $code))) {
        // классическая сигнатура — совместима с любой версией PHP на хостинге
        setcookie($COOKIE_NAME, $ACCESS_HASH, time() + 60 * 60 * 24 * 30, '/for/saint-gobain/', '', true, true);
        header('Location: ./');
        exit;
    }
    $error = true;
}

if (!$authed) {
    // ---- Экран ввода кода ----
    $errHtml = $error ? '<p class="gate-error">Неверный код. Проверьте код из письма и попробуйте ещё раз.</p>' : '';
    echo <<<GATE
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Доступ к странице — Hand Marketing × Saint-Gobain</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/react-main.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family:'Inter',system-ui,sans-serif; color:#14213d; background:#f5f7fb;
    min-height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:24px;
  }
  .gate-card {
    background:#fff; border:1px solid #e5e9f2; border-radius:20px; padding:48px 40px;
    max-width:440px; width:100%; text-align:center;
    box-shadow:0 20px 60px rgba(20,33,61,.08);
  }
  .gate-logos { display:flex; align-items:center; justify-content:center; gap:18px; margin-bottom:28px; }
  .gate-logos img.hm { height:44px; }
  .gate-logos img.sg { height:52px; }
  .gate-logos .x { font-family:'Montserrat',sans-serif; font-weight:700; color:#9aa5bd; font-size:15px; }
  .gate-rule { height:3px; border-radius:3px; margin:0 auto 28px; width:72px;
    background:linear-gradient(90deg,#4db1b3,#0195d6,#254a9a,#c0247e,#e8262d,#f26e21); }
  h1 { font-family:'Montserrat',sans-serif; font-weight:700; font-size:20px; line-height:1.35; margin-bottom:10px; }
  .gate-sub { font-size:14px; color:#5c6b8a; margin-bottom:26px; }
  form { display:flex; flex-direction:column; gap:12px; }
  input[type=text] {
    font-family:'Montserrat',sans-serif; font-weight:600; letter-spacing:.12em; text-transform:uppercase;
    font-size:16px; text-align:center; padding:14px 16px; border:1.5px solid #d6dcea; border-radius:12px; outline:none;
    transition:border-color .15s;
  }
  input[type=text]:focus { border-color:#254a9a; }
  button {
    font-family:'Montserrat',sans-serif; font-weight:700; font-size:15px; color:#fff; cursor:pointer;
    background:#254a9a; border:none; border-radius:12px; padding:14px 16px; transition:background .15s;
  }
  button:hover { background:#1b3a7a; }
  .gate-error { color:#c62828; font-size:13px; margin-top:4px; }
  .gate-note { margin-top:28px; font-size:12px; color:#9aa5bd; }
</style>
</head>
<body>
  <div class="gate-card">
    <div class="gate-logos">
      <img class="hm" src="hm-logo.svg" alt="Hand Marketing">
      <span class="x">×</span>
      <img class="sg" src="sg-logo.png" alt="Saint-Gobain">
    </div>
    <div class="gate-rule"></div>
    <h1>Персональная страница<br>для Saint-Gobain</h1>
    <p class="gate-sub">Введите код доступа из письма</p>
    <form method="post" action="./" autocomplete="off">
      <input type="text" name="code" placeholder="SG-XXXX-XXXX" maxlength="20" autofocus required>
      <button type="submit">Открыть страницу</button>
      {$errHtml}
    </form>
    <p class="gate-note">Hand Marketing · Доступ по личному приглашению</p>
  </div>
</body>
</html>
GATE;
    exit;
}
?>
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Hand Marketing × Saint-Gobain — выставочный стенд под ключ</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/react-main.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  :root {
    --ink:#14213d; --stone:#5c6b8a; --mist:#e5e9f2; --paper:#ffffff; --bg:#f5f7fb;
    --sg-blue:#254a9a; --sg-blue-dark:#1b3a7a;
    --sg-grad:linear-gradient(90deg,#4db1b3,#0195d6,#254a9a,#c0247e,#e8262d,#f26e21);
  }
  body { font-family:'Inter',system-ui,sans-serif; color:var(--ink); background:var(--paper); }
  .wrap { max-width:1080px; margin:0 auto; padding:0 24px; }
  .eyebrow { font-family:'Montserrat',sans-serif; font-weight:700; font-size:12px; letter-spacing:.22em;
    color:var(--sg-blue); text-transform:uppercase; margin-bottom:22px; }
  .sec-title { font-family:'Montserrat',sans-serif; font-weight:800; font-size:clamp(26px,3.6vw,38px);
    line-height:1.15; margin-bottom:14px; }
  .sec-sub { font-size:16.5px; line-height:1.65; color:var(--stone); max-width:44em; }

  /* Шапка */
  .top { border-bottom:1px solid var(--mist); }
  .top-in { display:flex; align-items:center; justify-content:space-between; height:76px; }
  .top-hm { display:flex; align-items:center; gap:12px; text-decoration:none; color:var(--ink); }
  .top-hm img { height:40px; }
  .top-hm span { font-family:'Montserrat',sans-serif; font-weight:700; font-size:12px; letter-spacing:.18em; }
  .top img.sg { height:44px; }
  .grad-line { height:3px; background:var(--sg-grad); }

  /* Хиро */
  .hero { padding:84px 0 60px; }
  h1 { font-family:'Montserrat',sans-serif; font-weight:800; font-size:clamp(34px,5.2vw,56px); line-height:1.08;
    letter-spacing:-.01em; max-width:17em; }
  h1 .sg { color:var(--sg-blue); }
  .hero p { margin-top:26px; font-size:18px; line-height:1.68; color:var(--stone); max-width:41em; }
  .hero p b { color:var(--ink); }

  /* Мы уже работали вместе */
  .known { padding:26px 0 66px; }
  .known-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:30px; }
  @media (max-width:760px){ .known-grid { grid-template-columns:1fr; } }
  .kcard { display:block; text-decoration:none; color:var(--ink); border:1px solid var(--mist); border-radius:18px;
    overflow:hidden; background:var(--paper); transition:transform .18s, box-shadow .18s; }
  .kcard:hover { transform:translateY(-3px); box-shadow:0 16px 44px rgba(20,33,61,.10); }
  .kcard .img { aspect-ratio:16/8; background:#f2f5fa; display:flex; align-items:center; justify-content:center; overflow:hidden; }
  .kcard .img img { width:100%; height:100%; object-fit:cover; }
  .kcard .img.fit img { object-fit:contain; padding:14px; }
  .kcard .body { padding:22px 24px 24px; }
  .kcard .tag { font-family:'Montserrat',sans-serif; font-weight:700; font-size:11px; letter-spacing:.16em;
    text-transform:uppercase; color:var(--sg-blue); }
  .kcard h3 { font-family:'Montserrat',sans-serif; font-weight:700; font-size:19px; margin:9px 0 8px; line-height:1.3; }
  .kcard p { font-size:14.5px; line-height:1.6; color:var(--stone); }
  .kcard .more { display:inline-block; margin-top:12px; font-weight:600; font-size:14px; color:var(--sg-blue); }

  /* Предложение: стенд под ключ */
  .offer { padding:64px 0; background:var(--bg); }
  .offer-grid { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:34px; }
  @media (max-width:760px){ .offer-grid { grid-template-columns:1fr; } }
  .ocard { border:1px solid var(--mist); border-radius:16px; padding:26px 26px 24px; background:var(--paper); }
  .ocard .num { font-family:'Montserrat',sans-serif; font-weight:800; font-size:14px; letter-spacing:.08em; }
  .ocard h3 { font-family:'Montserrat',sans-serif; font-weight:700; font-size:19px; margin:10px 0 8px; }
  .ocard p { font-size:14.5px; line-height:1.62; color:var(--stone); }
  .o1 .num{color:#0195d6;} .o2 .num{color:#254a9a;} .o3 .num{color:#c0247e;} .o4 .num{color:#f26e21;}

  /* Примеры проектов */
  .cases { padding:70px 0 64px; }
  .cases-grid { display:grid; grid-template-columns:1fr 1fr; gap:22px; margin-top:34px; }
  @media (max-width:760px){ .cases-grid { grid-template-columns:1fr; } }
  .ccard { display:block; text-decoration:none; color:var(--ink); border-radius:18px; overflow:hidden;
    border:1px solid var(--mist); background:var(--paper); transition:transform .18s, box-shadow .18s; }
  .ccard:hover { transform:translateY(-3px); box-shadow:0 18px 48px rgba(20,33,61,.12); }
  .ccard .img { aspect-ratio:16/10; overflow:hidden; }
  .ccard .img img { width:100%; height:100%; object-fit:cover; transition:transform .3s; }
  .ccard:hover .img img { transform:scale(1.03); }
  .ccard .body { padding:20px 24px 22px; }
  .ccard h3 { font-family:'Montserrat',sans-serif; font-weight:700; font-size:19px; line-height:1.3; }
  .ccard .meta { margin-top:6px; font-size:14px; color:var(--stone); }
  .ccard .more { display:inline-block; margin-top:10px; font-weight:600; font-size:14px; color:var(--sg-blue); }
  .cases-note { margin-top:26px; font-size:15px; color:var(--stone); }
  .cases-note a { color:var(--sg-blue); font-weight:600; text-decoration:none; }
  .cases-note a:hover { text-decoration:underline; }

  /* Форма вопросов */
  .ask { padding:64px 0 72px; background:var(--bg); }
  .ask-card { background:var(--paper); border:1px solid var(--mist); border-radius:20px; padding:38px 36px;
    max-width:640px; margin-top:32px; }
  @media (max-width:640px){ .ask-card { padding:28px 22px; } }
  .ask-card label { display:block; font-family:'Montserrat',sans-serif; font-weight:600; font-size:13.5px; margin:0 0 7px; }
  .ask-card .row { margin-bottom:18px; }
  .ask-card input[type=text], .ask-card textarea {
    width:100%; font-family:'Inter',system-ui,sans-serif; font-size:15px; color:var(--ink);
    padding:13px 15px; border:1.5px solid #d6dcea; border-radius:12px; outline:none; background:#fff;
    transition:border-color .15s;
  }
  .ask-card input:focus, .ask-card textarea:focus { border-color:var(--sg-blue); }
  .ask-card textarea { min-height:110px; resize:vertical; }
  .ask-card button {
    font-family:'Montserrat',sans-serif; font-weight:700; font-size:15px; color:#fff; cursor:pointer;
    background:var(--sg-blue); border:none; border-radius:12px; padding:15px 30px; transition:background .15s;
  }
  .ask-card button:hover { background:var(--sg-blue-dark); }
  .ask-card button[disabled] { opacity:.6; cursor:default; }
  .ask-note { margin-top:14px; font-size:12.5px; color:#9aa5bd; }
  .ask-err { display:none; margin-top:12px; font-size:14px; color:#c62828; }
  .ask-ok { display:none; text-align:center; padding:26px 6px; }
  .ask-ok .tick { width:52px; height:52px; margin:0 auto 16px; border-radius:50%; background:var(--sg-blue);
    display:flex; align-items:center; justify-content:center; }
  .ask-ok h3 { font-family:'Montserrat',sans-serif; font-weight:700; font-size:20px; margin-bottom:8px; }
  .ask-ok p { font-size:15px; color:var(--stone); line-height:1.6; }
  .hp { position:absolute; left:-9999px; opacity:0; height:0; overflow:hidden; }

  /* Контакты */
  .contact { background:linear-gradient(135deg,var(--sg-blue) 0%,var(--sg-blue-dark) 100%); color:#fff; padding:72px 0; }
  .contact .eyebrow { color:#9fc1ff; }
  .contact h2 { font-family:'Montserrat',sans-serif; font-weight:800; font-size:clamp(28px,4vw,40px); margin-bottom:8px; }
  .contact .name { font-size:17px; color:#c9d6f2; margin-bottom:34px; }
  .contact-grid { display:flex; flex-wrap:wrap; gap:14px; }
  .contact-grid a {
    display:flex; align-items:center; gap:10px; text-decoration:none; color:#fff;
    font-family:'Montserrat',sans-serif; font-weight:600; font-size:16px;
    border:1.5px solid rgba(255,255,255,.28); border-radius:14px; padding:14px 22px;
    transition:background .15s, border-color .15s;
  }
  .contact-grid a:hover { background:rgba(255,255,255,.1); border-color:rgba(255,255,255,.55); }
  .contact-grid svg { width:19px; height:19px; flex:none; }

  /* Подвал */
  footer { padding:34px 0 44px; }
  .foot-in { display:flex; align-items:center; justify-content:space-between; gap:20px; flex-wrap:wrap; }
  .foot-in img.hm { height:30px; } .foot-in img.sg { height:32px; opacity:.9; }
  .foot-note { font-size:12.5px; color:var(--stone); }
</style>
</head>
<body>

<header class="top">
  <div class="wrap top-in">
    <a class="top-hm" href="https://hand-marketing.ru/">
      <img src="hm-logo.svg" alt="Hand Marketing">
      <span>HAND&nbsp;MARKETING</span>
    </a>
    <img class="sg" src="sg-logo.png" alt="Saint-Gobain">
  </div>
  <div class="grad-line"></div>
</header>

<section class="hero">
  <div class="wrap">
    <div class="eyebrow">Персонально для команды Saint-Gobain · июль 2026</div>
    <h1>Стенд <span class="sg">Saint&#8209;Gobain</span>, мимо которого не пройдут</h1>
    <p>Эта страница — не рассылка и не шаблон, мы собрали её специально для вас.
       <b>Мы уже знакомы:</b> Hand Marketing снимал бренд-ролик для «Изотек» и придумал
       презентационный чемодан для решений Gyproc и ISOVER. Мы знаем ваши продукты и ваш бренд-бук —
       и предлагаем сделать следующий шаг вместе: выставочный стенд Saint-Gobain под ключ.</p>
  </div>
</section>

<section class="known">
  <div class="wrap">
    <div class="eyebrow">Мы уже работали вместе</div>
    <h2 class="sec-title">Два проекта для Saint-Gobain — уже в нашем портфолио</h2>
    <div class="known-grid">
      <a class="kcard" href="https://hand-marketing.ru/creative/saintgobain/suitcase/" target="_blank" rel="noopener">
        <div class="img fit"><img src="/images/lib/as3436-3631-4366-b534-633566633162/image.png" alt="Презентационный чемодан Saint-Gobain"></div>
        <div class="body">
          <div class="tag">Creative &amp; Design</div>
          <h3>Презентационный чемодан Saint-Gobain</h3>
          <p>Демо-кейс комплексных решений звукоизоляции Gyproc и ISOVER. Концепция «Две комнаты»:
             шум и тишина по разные стороны стены — весь ассортимент в одном чемодане.</p>
          <span class="more">Смотреть кейс →</span>
        </div>
      </a>
      <a class="kcard" href="https://hand-marketing.ru/isotec/" target="_blank" rel="noopener">
        <div class="img"><img src="isotec-still.jpg" alt="Бренд-ролик «Изотек»"></div>
        <div class="body">
          <div class="tag">Video Production</div>
          <h3>Бренд-ролик «Изотек»</h3>
          <p>Имиджевый фильм для бренда технической изоляции ISOTEC: история роста компании —
             для клиентов, партнёров и отраслевых мероприятий.</p>
          <span class="more">Смотреть кейс →</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="offer">
  <div class="wrap">
    <div class="eyebrow">Предложение</div>
    <h2 class="sec-title">Выставочный стенд под ключ</h2>
    <p class="sec-sub">Одна команда отвечает за всё — от первого эскиза до демонтажа.
       Вам не нужно собирать подрядчиков: дизайн, производство, мультимедиа и контент делаем сами.</p>
    <div class="offer-grid">
      <div class="ocard o1">
        <div class="num">01</div>
        <h3>Концепция и дизайн-проект</h3>
        <p>Идея, планировки, 3D-визуализация, подбор материалов. Вы увидите и согласуете стенд
           до старта производства — без сюрпризов на монтаже.</p>
      </div>
      <div class="ocard o2">
        <div class="num">02</div>
        <h3>Производство и монтаж</h3>
        <p>Конструктив, инженерия, согласования с площадкой, логистика, монтаж, супервайзинг
           на выставке и демонтаж. Опыт площадок уровня ВДНХ и Экспоцентра.</p>
      </div>
      <div class="ocard o3">
        <div class="num">03</div>
        <h3>Мультимедиа и интерактив</h3>
        <p>Видеостены, сенсорные панели, Naked Eye 3D-экраны, интерактивные игры и инсталляции —
           чтобы материалы и технологии Saint-Gobain можно было увидеть в действии, а не на полке.</p>
      </div>
      <div class="ocard o4">
        <div class="num">04</div>
        <h3>Контент и видео</h3>
        <p>Графика и анимация для экранов стенда, презентации, съёмка работы стенда и aftermovie —
           в единой айдентике и с уважением к бренд-буку Saint-Gobain.</p>
      </div>
    </div>
  </div>
</section>

<section class="cases">
  <div class="wrap">
    <div class="eyebrow">Примеры проектов</div>
    <h2 class="sec-title">Стенды, которые мы уже построили</h2>
    <p class="sec-sub">Живые фото с площадок и рабочие дизайн-проекты — посмотрите, как это выглядит в деле.</p>
    <div class="cases-grid">
      <a class="ccard" href="https://hand-marketing.ru/portfolio/samara-stand-vdnh/" target="_blank" rel="noopener">
        <div class="img"><img src="/portfolio/russia-exhibition.jpg" alt="Стенд Самарской области на выставке-форуме «Россия»"></div>
        <div class="body">
          <h3>Стенд Самарской области</h3>
          <div class="meta">Выставка-форум «Россия», ВДНХ · стенд-ладья с Naked Eye 3D-экраном · 18+ млн посетителей выставки</div>
          <span class="more">Смотреть кейс →</span>
        </div>
      </a>
      <a class="ccard" href="https://hand-marketing.ru/portfolio/stavropol-stand-vdnh/" target="_blank" rel="noopener">
        <div class="img"><img src="/portfolio/stavropol-vdnh/gallery-1.jpg" alt="Стенд Ставропольского края на выставке-форуме «Россия»"></div>
        <div class="body">
          <h3>Стенд Ставропольского края</h3>
          <div class="meta">Выставка-форум «Россия», ВДНХ · мультимедийная экспозиция «Край для жизни»</div>
          <span class="more">Смотреть кейс →</span>
        </div>
      </a>
      <a class="ccard" href="https://hand-marketing.ru/exhibition/" target="_blank" rel="noopener">
        <div class="img"><img src="/images/exhibition/samara/render-v1-a.jpg" alt="Дизайн-проект стенда «Россия — спортивная держава»"></div>
        <div class="body">
          <h3>Дизайн-проект стенда 204 м²</h3>
          <div class="meta">Форум «Россия — спортивная держава» · 15 интерактивных зон · разбор проекта с чертежами</div>
          <span class="more">Смотреть разбор →</span>
        </div>
      </a>
      <a class="ccard" href="https://hand-marketing.ru/portfolio/samara-exhibition/" target="_blank" rel="noopener">
        <div class="img"><img src="/portfolio/samara-exhibition/photos/Ekran_parus.jpg" alt="Выставка «Самара» в музее им. Алабина"></div>
        <div class="body">
          <h3>Выставка «Самара»</h3>
          <div class="meta">Музей им. Алабина · экран-парус, VR, Kinect-игры и интерактивные инсталляции</div>
          <span class="more">Смотреть кейс →</span>
        </div>
      </a>
    </div>
    <p class="cases-note">Это только стенды и экспозиции. Ещё 40+ проектов — событий, роликов и инсталляций —
       в <a href="https://hand-marketing.ru/portfolio/" target="_blank" rel="noopener">полном портфолио</a>.</p>
  </div>
</section>

<section class="ask">
  <div class="wrap">
    <div class="eyebrow">Вопросы и комментарии</div>
    <h2 class="sec-title">Спросите нас напрямую</h2>
    <p class="sec-sub">Страница персональная, поэтому и связь прямая: сообщение придёт не в общий ящик агентства,
       а лично Александру. Отвечаем в течение рабочего дня.</p>
    <div class="ask-card">
      <form id="sg-ask" novalidate>
        <div class="row">
          <label for="f-name">Как вас зовут</label>
          <input type="text" id="f-name" name="name" placeholder="Имя и фамилия">
        </div>
        <div class="row">
          <label for="f-contact">Как с вами связаться</label>
          <input type="text" id="f-contact" name="contact" placeholder="E-mail или телефон" required>
        </div>
        <div class="row">
          <label for="f-comment">Вопрос или комментарий</label>
          <textarea id="f-comment" name="comment" placeholder="Например: планируем участие в выставке, интересует стенд 50–100 м². Какие сроки и бюджет?"></textarea>
        </div>
        <div class="hp"><input type="text" name="website" tabindex="-1" autocomplete="off"></div>
        <button type="submit">Отправить сообщение</button>
        <p class="ask-err" id="ask-err">Не получилось отправить. Проверьте контакт (e-mail или телефон) или напишите нам напрямую — контакты ниже.</p>
        <p class="ask-note">Сообщение уйдёт команде Hand Marketing. Никаких рассылок — ответим только по делу.</p>
      </form>
      <div class="ask-ok" id="ask-ok">
        <div class="tick"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></div>
        <h3>Спасибо! Сообщение отправлено</h3>
        <p>Александр получил ваш вопрос и ответит лично —<br>обычно в течение рабочего дня.</p>
      </div>
    </div>
  </div>
</section>

<section class="contact">
  <div class="wrap">
    <div class="eyebrow">Контакты</div>
    <h2>Обсудим ваш проект</h2>
    <p class="name">Александр Народецкий · Hand Marketing</p>
    <div class="contact-grid">
      <a href="tel:+79859998783">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        +7 985 999-87-83
      </a>
      <a href="mailto:anarodetsky@hand-marketing.ru">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>
        anarodetsky@hand-marketing.ru
      </a>
      <a href="https://t.me/narodetskii" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 3.44a1.5 1.5 0 0 0-1.6-.23L2.7 10.57a1.4 1.4 0 0 0 .1 2.62l4.46 1.48 1.7 5.27a1.4 1.4 0 0 0 2.28.6l2.45-2.32 4.05 2.96a1.4 1.4 0 0 0 2.2-.86l2.42-15.4a1.5 1.5 0 0 0-.42-1.48zM9.6 14.1l8.13-7.11-6.53 8.32-.24 2.94-1.36-4.15z"/></svg>
        Telegram
      </a>
      <a href="https://wa.me/+79859998783?text=Здравствуйте,%20Александр!%20Пишу%20со%20страницы%20Saint-Gobain." target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.65 15L2 22l5.15-1.35A10 10 0 1 0 12 2zm5.2 14.2c-.22.62-1.28 1.18-1.78 1.22-.48.04-.93.22-3.12-.65-2.64-1.04-4.31-3.73-4.44-3.9-.13-.17-1.06-1.41-1.06-2.69s.67-1.9.91-2.16c.24-.26.52-.33.7-.33h.5c.16 0 .38-.06.59.45l.81 1.97c.07.15.12.32.02.5l-.33.5-.47.5c-.15.15-.31.31-.13.61.18.3.79 1.3 1.7 2.11 1.17 1.04 2.15 1.36 2.46 1.52.3.15.48.13.66-.08l1-1.17c.23-.3.44-.23.73-.13l1.87.88c.3.15.5.22.57.35.07.12.07.72-.15 1.4z"/></svg>
        WhatsApp
      </a>
    </div>
  </div>
</section>

<footer>
  <div class="wrap foot-in">
    <img class="hm" src="hm-logo.svg" alt="Hand Marketing">
    <p class="foot-note">Страница подготовлена Hand Marketing специально для Saint-Gobain и не предназначена для публичного распространения.</p>
    <img class="sg" src="sg-logo.png" alt="Saint-Gobain">
  </div>
</footer>

<script>
// Форма вопросов -> общий обработчик заявок /api/lead.php (JSON), как остальные формы сайта
(function () {
  var form = document.getElementById('sg-ask');
  var ok = document.getElementById('ask-ok');
  var err = document.getElementById('ask-err');
  var f = form.elements; // доступ к полям через elements — form.name конфликтует с атрибутом формы
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    err.style.display = 'none';
    var contact = f['contact'].value.trim();
    var digits = contact.replace(/\D/g, '');
    // как на сервере: нужен телефон (6+ цифр) или e-mail
    if (digits.length < 6 && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact)) {
      err.style.display = 'block';
      f['contact'].focus();
      return;
    }
    var btn = form.querySelector('button');
    btn.disabled = true;
    fetch('/api/lead.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        form: 'for-saint-gobain',
        company: 'Saint-Gobain',
        name: f['name'].value.trim(),
        contact: contact,
        comment: f['comment'].value.trim(),
        website: f['website'].value
      })
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (d && (d.ok || d.success)) {
        form.style.display = 'none';
        ok.style.display = 'block';
      } else { throw new Error('fail'); }
    }).catch(function () {
      btn.disabled = false;
      err.style.display = 'block';
    });
  });
})();
</script>

</body>
</html>
