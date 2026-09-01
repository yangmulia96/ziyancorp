# Kebocoran Rahasia lewat `.bashrc` → `ziyan_keys.env`

Ditemukan 4 Agu 2026 saat cron job upload YouTube: setiap panggilan `terminal` diawali baris

```
bash: password: command not found
bash: bknq ... : command not found
bash: api: command not found
bash: sk-or-...: command not found
bash: bot: command not found
bash: 8825875995:***: command not found
```

## Akar masalah
`~/.bashrc` berisi:

```bash
if [ -f "$HOME/ziyan_keys.env" ]; then
  set -a
  . "$HOME/ziyan_keys.env"
  set +a
fi
```

`.` (source) mengeksekusi file sebagai skrip bash. Baris yang bukan `KEY=VALUE` (catatan prosa,
label "api key openrouter", nilai telanjang di baris sendiri) diperlakukan sebagai PERINTAH.
Bash gagal, lalu mencetak potongan isinya ke stderr — termasuk app password Gmail, API key
OpenRouter, dan token bot Telegram — pada SETIAP sesi shell, lalu ikut tersimpan di transcript
Hermes dan log cron.

## Audit (tanpa membocorkan nilai)
```bash
cd /c/Users/arija && awk '{
  if ($0 ~ /^[[:space:]]*#/ || $0 ~ /^[[:space:]]*$/) t="ok-comment/blank";
  else if ($0 ~ /^[A-Za-z_][A-Za-z0-9_]*=/) t="ok-kv";
  else t="BAD";
  printf "%d\t%s\t%s\n", NR, t, substr($0,1,18)
}' ziyan_keys.env | grep BAD
```
`substr(...,1,18)` sengaja memotong supaya nilai rahasia tidak tercetak penuh.

## Perbaikan permanen (idempoten, aman diulang)
```bash
cd /c/Users/arija \
  && cp ziyan_keys.env ziyan_keys.env.bak2 \
  && awk '{ if ($0 ~ /^[[:space:]]*#/ || $0 ~ /^[[:space:]]*$/ || $0 ~ /^[A-Za-z_][A-Za-z0-9_]*=/) print $0; else print "# " $0 }' \
       ziyan_keys.env > ziyan_keys.env.tmp \
  && mv ziyan_keys.env.tmp ziyan_keys.env \
  && echo SANITIZED
```

Verifikasi shell sudah bersih:
```bash
bash -lc 'echo SHELL_CLEAN_TEST' 2>&1 | tail -5   # harus hanya SHELL_CLEAN_TEST
```

## Aturan lanjutan
- Semua rahasia baru masuk sebagai `KEY=VALUE` satu baris, tanpa spasi di sekitar `=`.
  Catatan/keterangan WAJIB diawali `#`.
- Nilai yang mengandung spasi WAJIB dikutip: `GMAIL_APP_PASSWORD="abcd efgh ijkl mnop"`.
- Selama audit/perbaikan, saring output: `... 2>&1 | grep -viE "command not found|job control"`.
- Kalau kebocoran sudah berjalan lama, laporkan ke Bos untuk ROTASI key (OpenRouter, app password
  Gmail, token bot Telegram) — sebut nama kredensial, JANGAN nilainya.
