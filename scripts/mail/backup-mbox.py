#!/usr/bin/env python3
"""Локальная офлайн-копия ящика с IMAP в mbox-файлы.

Вторая (независимая от Reg.ru) копия архива: даже если что-то пойдёт не так с
переносом или с Яндексом, письма лежат на диске и открываются Thunderbird'ом.

    python3 backup-mbox.py 1                    # ящик 1 (anarodetsky@) в ~/hm-mail-backup
    python3 backup-mbox.py 1 --out /Volumes/HD  # свой каталог, например внешний диск

Прерванную выгрузку можно запускать повторно: уже скачанные письма
пропускаются (состояние по UID лежит рядом с mbox в .state.json).
Креды берутся из ~/.config/hm-mail/creds.env — в git ничего не попадает.
"""
import argparse, base64, imaplib, json, mailbox, re, sys, time
from pathlib import Path

imaplib._MAXLINE = 10_000_000


def load_creds():
    path = Path.home() / ".config/hm-mail/creds.env"
    if not path.exists():
        sys.exit(f"нет файла кредов {path}")
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            v = v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                v = v[1:-1]          # значения можно брать в кавычки: пароль с $ или #
            env[k.strip()] = v
    return env


def imap_utf7_decode(name):
    """Имена папок IMAP приходят в modified UTF-7: &BB0EQA- вместо кириллицы."""
    def sub(m):
        chunk = m.group(1)
        if not chunk:          # "&-" кодирует сам символ "&"
            return "&"
        b64 = chunk.replace(",", "/") + "===" * (-len(chunk) % 4)
        return base64.b64decode(b64).decode("utf-16-be", "replace")
    return re.sub(r"&([^-]*)-", sub, name)


def list_folders(conn):
    typ, data = conn.list()
    if typ != "OK":
        sys.exit("не удалось получить список папок")
    out = []
    for raw in data:
        line = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else raw
        m = re.match(r'\((?P<flags>[^)]*)\)\s+"(?P<sep>[^"]*)"\s+(?P<name>.*)$', line)
        if not m:
            continue
        if "\\Noselect" in m.group("flags"):
            continue
        name = m.group("name").strip().strip('"')
        out.append(name)
    return out


def safe_filename(name):
    return re.sub(r"[^\w.\-]+", "_", name, flags=re.UNICODE).strip("_") or "folder"


def backup_folder(conn, folder, outdir):
    typ, data = conn.select(f'"{folder}"', readonly=True)
    if typ != "OK":
        print(f"  пропуск (не открывается): {imap_utf7_decode(folder)}")
        return 0, 0

    typ, data = conn.uid("SEARCH", None, "ALL")
    if typ != "OK":
        print(f"  пропуск (search failed): {imap_utf7_decode(folder)}")
        return 0, 0
    uids = data[0].split()

    human = imap_utf7_decode(folder)
    base = outdir / safe_filename(human)
    state_path = base.with_suffix(".state.json")
    state = json.loads(state_path.read_text()) if state_path.exists() else {"done": []}
    done = set(state["done"])

    todo = [u for u in uids if u.decode() not in done]
    print(f"  {human}: всего {len(uids)}, к загрузке {len(todo)}")
    if not todo:
        return len(uids), 0

    box = mailbox.mbox(str(base) + ".mbox")
    saved = 0
    try:
        box.lock()
        for i, uid in enumerate(todo, 1):
            typ, msg_data = conn.uid("FETCH", uid, "(BODY.PEEK[])")
            if typ != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
                continue
            box.add(msg_data[0][1])
            done.add(uid.decode())
            saved += 1
            if i % 50 == 0:
                box.flush()
                state_path.write_text(json.dumps({"done": sorted(done)}))
                print(f"    {i}/{len(todo)}", flush=True)
        box.flush()
    finally:
        box.unlock()
        box.close()
        state_path.write_text(json.dumps({"done": sorted(done)}))
    return len(uids), saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("box", choices=["1", "2"], help="1 = anarodetsky@, 2 = info@")
    ap.add_argument("--out", default=str(Path.home() / "hm-mail-backup"))
    args = ap.parse_args()

    env = load_creds()
    user = env[f"BOX{args.box}_USER"]
    pw = env[f"BOX{args.box}_YA_PASS"]
    host = env.get("YA_HOST", "imap.yandex.ru")
    if not pw:
        sys.exit(f"не заполнен BOX{args.box}_YA_PASS в ~/.config/hm-mail/creds.env")

    outdir = Path(args.out) / user
    outdir.mkdir(parents=True, exist_ok=True)
    print(f"ящик {user} -> {outdir}")

    conn = imaplib.IMAP4_SSL(host, 993)
    conn.login(user, pw)
    try:
        folders = list_folders(conn)
        print(f"папок: {len(folders)}")
        total = total_saved = 0
        t0 = time.time()
        for folder in folders:
            n, saved = backup_folder(conn, folder, outdir)
            total += n
            total_saved += saved
        print(f"\nготово: писем в ящике {total}, скачано за этот прогон {total_saved}, "
              f"{time.time() - t0:.0f} с")
        print(f"каталог: {outdir}")
    finally:
        try:
            conn.logout()
        except Exception:
            pass


if __name__ == "__main__":
    main()
