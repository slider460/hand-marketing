#!/usr/bin/env bash
# Пережатие тяжёлых видео (>40МБ) для ручной перезаливки на хостинг.
# Итог кладётся в media-optimized/ с ТЕМИ ЖЕ именами — заливать поверх /media/*.
# 720p (без апскейла), x264 crf 24 slow, звук AAC 128k, faststart.
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p media-optimized
for f in media/*.mp4; do
  b=$(basename "$f")
  sz=$(stat -f%z "$f")
  [ "$sz" -lt 41943040 ] && continue          # только >40МБ
  out="media-optimized/$b"
  [ -f "$out" ] && continue                   # идемпотентно
  echo "== $b ($((sz/1048576))МБ)"
  ffmpeg -y -v error -i "$f" \
    -vf "scale=-2:'min(720,ih)'" \
    -c:v libx264 -crf 24 -preset slow -profile:v high -pix_fmt yuv420p \
    -c:a aac -b:a 128k -movflags +faststart "$out" \
    || { echo "FAIL $b"; rm -f "$out"; continue; }
  echo "   -> $(( $(stat -f%z "$out")/1048576 ))МБ"
done
echo "DONE"
ls -la media-optimized/ | tail -25
