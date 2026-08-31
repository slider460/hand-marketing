#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Локальный предпросмотр mirror/ с поддержкой Range (HTTP 206).

    python3 scripts/serve-mirror.py            # http://127.0.0.1:8080
    python3 scripts/serve-mirror.py 8090

Зачем отдельный сервер: встроенный `python3 -m http.server` не отвечает
на Range-запросы, поэтому в кейсах с перемоткой плеера currentTime
падает в ноль и все кнопки «перемотать к секунде» выглядят сломанными.
Здесь обычный SimpleHTTPRequestHandler плюс разбор Range и ответ 206.
"""
import http.server
import os
import posixpath
import re
import socketserver
import sys
import urllib.parse

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=MIRROR, **kw)

    def log_message(self, fmt, *args):
        if '404' in (fmt % args):
            sys.stderr.write('404 %s\n' % (self.path,))

    def translate_path(self, path):
        """Каталог без index.html не должен уводить на листинг: сайт статический
        и /video/vivax/ это /video/vivax/index.html."""
        p = super().translate_path(path)
        if os.path.isdir(p):
            idx = os.path.join(p, 'index.html')
            if os.path.exists(idx):
                return idx
        return p

    def send_head(self):
        rng = self.headers.get('Range')
        if not rng:
            return super().send_head()
        path = self.translate_path(self.path)
        if os.path.isdir(path) or not os.path.exists(path):
            return super().send_head()
        m = re.match(r'bytes=(\d*)-(\d*)$', rng.strip())
        if not m:
            return super().send_head()
        size = os.path.getsize(path)
        start, end = m.group(1), m.group(2)
        if start == '':                       # bytes=-N — хвост файла
            start = max(0, size - int(end or 0))
            end = size - 1
        else:
            start = int(start)
            end = int(end) if end else size - 1
        end = min(end, size - 1)
        if start > end:
            self.send_error(416, 'Requested Range Not Satisfiable')
            return None
        f = open(path, 'rb')
        f.seek(start)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        return _Slice(f, end - start + 1)

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


class _Slice:
    """Файловый объект, отдающий ровно N байт: copyfile читает до EOF."""

    def __init__(self, f, n):
        self.f, self.left = f, n

    def read(self, n=-1):
        if self.left <= 0:
            return b''
        if n < 0 or n > self.left:
            n = self.left
        b = self.f.read(n)
        self.left -= len(b)
        return b

    def close(self):
        self.f.close()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    with Server(('127.0.0.1', port), Handler) as httpd:
        print(f'mirror/ → http://127.0.0.1:{port}/  (Ctrl+C чтобы остановить)')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
