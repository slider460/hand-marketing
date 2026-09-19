#!/usr/bin/env bash
# Перенос почты hand-marketing.ru: Яндекс -> Reg.ru.
# Креды читаются из ~/.config/hm-mail/creds.env (вне репозитория, в git не попадает).
#
#   ./imapsync-run.sh probe 1     — посчитать папки/письма/объём, ничего не переносить
#   ./imapsync-run.sh sync  1     — перенести ящик 1 (архив anarodetsky@)
#   ./imapsync-run.sh sync  2     — перенести ящик 2 (info@)
#
# Второй прогон sync должен показать 0 новых писем — это и есть подтверждение полноты.
set -euo pipefail

MODE="${1:-}"; BOX="${2:-}"
CREDS="$HOME/.config/hm-mail/creds.env"
LOGDIR="$HOME/hm-mail-logs"

[[ "$MODE" =~ ^(probe|sync)$ ]] || { echo "режим: probe | sync"; exit 1; }
[[ "$BOX"  =~ ^[12]$        ]] || { echo "ящик: 1 (anarodetsky@) | 2 (info@)"; exit 1; }
[[ -f "$CREDS" ]] || { echo "нет файла кредов $CREDS"; exit 1; }

set -a; source "$CREDS"; set +a
mkdir -p "$LOGDIR"

if [[ "$BOX" == 1 ]]; then
  U1="$BOX1_USER"; P1="$BOX1_YA_PASS"; U2="$BOX1_RU_USER"; P2="$BOX1_RU_PASS"
else
  U1="$BOX2_USER"; P1="$BOX2_YA_PASS"; U2="$BOX2_RU_USER"; P2="$BOX2_RU_PASS"
fi

[[ -n "$P1" ]] || { echo "не заполнен пароль Яндекса для ящика $BOX в $CREDS"; exit 1; }
[[ -n "$P2" ]] || { echo "не заполнен пароль Reg.ru для ящика $BOX в $CREDS"; exit 1; }

COMMON=(
  --host1 "$YA_HOST" --user1 "$U1" --password1 "$P1" --ssl1 --port1 993
  --host2 "$RU_HOST" --user2 "$U2" --password2 "$P2" --ssl2 --port2 993
  --automap
  --no-modulesversion
  --timeout 180
  --logdir "$LOGDIR/imapsync-internal"
)

if [[ "$MODE" == probe ]]; then
  # Ничего не пишет на приёмник: только опись папок и объёмов с обеих сторон.
  imapsync "${COMMON[@]}" --justfoldersizes --dry 2>&1 | tee "$LOGDIR/probe-box$BOX-$(date +%Y%m%d-%H%M).log"
else
  # Перенос. --useheader сопоставляет письма по Message-Id, поэтому повторный
  # прогон догоняет только новое и ничего не дублирует.
  imapsync "${COMMON[@]}" \
    --useheader Message-Id --useheader Date \
    --skipcrossduplicates \
    --maxbytespersecond 3000000 \
    --errorsmax 80 \
    --exclude '^(Spam|Junk|Спам)$' \
    2>&1 | tee "$LOGDIR/sync-box$BOX-$(date +%Y%m%d-%H%M).log"
fi
