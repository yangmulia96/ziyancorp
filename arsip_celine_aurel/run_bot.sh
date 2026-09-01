#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo "File .env belum ada. Salin .env.example menjadi .env lalu isi secret." >&2
  exit 1
fi
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
fi

while true; do
  .venv/bin/python -m ziyan_bot.bot
  status=$?
  echo "Bot berhenti dengan status $status. Restart dalam 5 detik..." >&2
  sleep 5
done
