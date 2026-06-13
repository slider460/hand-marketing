#!/usr/bin/env bash
# Один шаг: коммит + пуш в GitHub. Пуш запускает GitHub Actions, который
# автоматически выкладывает сайт на хостинг (см. .github/workflows/deploy.yml).
#
# Использование:
#   scripts/ship.sh "сообщение коммита"
#
# Перед первым запуском один раз должно быть выполнено:
#   gh auth login            (или git remote add origin <url>)
#   gh repo create ...        (создание репозитория)
set -euo pipefail
cd "$(dirname "$0")/.."

MSG="${1:-Обновление сайта}"

# прогнать проверку битых ссылок перед отправкой
echo "→ Проверка ссылок…"
python3 scripts/check-links.py || { echo "✗ Найдены битые ссылки — пуш отменён"; exit 1; }

git add -A
if git diff --cached --quiet; then
  echo "Нет изменений для коммита."
else
  git commit -m "$MSG

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
fi

echo "→ Пуш в GitHub…"
git push origin main

echo "✓ Запушено. GitHub Actions разворачивает сайт на хостинге."
echo "  Статус: gh run watch  (или вкладка Actions в репозитории)"
