#!/usr/bin/env bash
# Генерация WebP-версий рядом с оригиналами (<файл>.webp).
# Оригиналы НЕ трогаются (фолбэк). Сервер отдаёт .webp по Accept (см. mirror/.htaccess).
# Идемпотентно: пропускает, если .webp свежее оригинала. Удаляет .webp, если он не меньше оригинала.
set -euo pipefail
ROOT="${1:-mirror}"
Q="${WEBP_Q:-82}"
MIN_BYTES="${MIN_BYTES:-10240}"   # не конвертируем мелочь <10КБ

convert_one() {
  local src="$1" q="$2"
  local out="${src}.webp"
  # пропустить, если webp свежее исходника
  if [ -f "$out" ] && [ "$out" -nt "$src" ]; then return 0; fi
  if ! cwebp -quiet -q "$q" -m 6 -sharp_yuv -metadata none "$src" -o "$out" 2>/dev/null; then
    rm -f "$out"; return 0
  fi
  # оставить только если реально меньше оригинала
  local so wo
  so=$(stat -f%z "$src"); wo=$(stat -f%z "$out" 2>/dev/null || echo 0)
  if [ "$wo" -eq 0 ] || [ "$wo" -ge "$so" ]; then rm -f "$out"; fi
}
export -f convert_one

find "$ROOT" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) \
  -size +"$((MIN_BYTES/1024))"k \
  ! -path '*/images/team/*' \
  -print0 | xargs -0 -P 8 -I{} bash -c 'convert_one "$@" '"$Q" _ {}

echo "Готово. WebP-файлов: $(find "$ROOT" -name '*.webp' | wc -l | tr -d ' ')"
