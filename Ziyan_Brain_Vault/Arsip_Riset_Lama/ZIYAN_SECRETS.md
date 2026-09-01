# ZIYAN Secrets Inventory

> File ini HANYA daftar lokasi & status credential. Nilai mentah TIDAK disimpan di sini.

## ✅ ACTIVE (Wajib untuk ZIYAN)

| Nama | Lokasi File | Fungsi |
|------|-------------|--------|
| `HERMES_CUSTOM_9ROUTER_API_KEY` | `AppData/Local/hermes/config.yaml` (key_env) | 9Router proxy auth |
| `9Router Key` | `.9remote/keys.json` | 9Router desktop app auth |
| `Google Service Account` | `ziyan_agent/credentials/service_account.json` | Sheets + Drive API |
| `Telegram Bot Token` | `ziyan_agent/config.yaml` (bot_token) | @Ziyanclipperbot polling |
| `OPENROUTER_API_KEY` | `AppData/Local/hermes/.env` | Parent model (CEO chat) |
| `TELEGRAM_BOT_TOKEN` | `AppData/Local/hermes/.env` | Hermes Telegram gateway |
| `TELEGRAM_ALLOWED_USERS` | `AppData/Local/hermes/.env` | Whitelist Telegram |

## ❌ EXPIRED / INVALID (Perlu refresh)

| Nama | Lokasi | Tindakan |
|------|--------|----------|
| `DISCORD_BOT_TOKEN` | `AppData/Local/hermes/.env` | Re-auth Discord gateway |
| `YouTube Token` | `ziyan_agent/ziyan_credentials/youtube_token_celineaurel.json` | Refresh OAuth (expired 2026-08-11) |

## ⚠️ LEGACY (Bisa dihapus jika tidak dipakai)

| Nama | Lokasi | Keterangan |
|------|--------|-----------|
| `OPENAI_API_KEY` | `AppData/Local/hermes/.env` | Tidak dipakai (pakai 9Router) |
| `GEMINI_API_KEY` | `AppData/Local/hermes/.env` | Antigravity (opsional) |
| `ROOT .env` | `.env` | File kosong, tidak terpakai |
| `n8n Encryption Key` | `.n8n/config` | n8n sudah dibuang |

## YouTube Desktop Client (OAuth client, bukan token)

Lokasi: `ziyan_agent/ziyan_credentials/youtube_desktop_client.json`
Status: ✅ Ada, dipakai untuk refresh YouTube token.

---

## CATATAN KEAMANAN

- JANGAN commit file ini ke Git public
- File credential asli tetap di lokasi masing-masing (encrypted/permission-limited)
- Jika laptop hilang: revoke semua token via dashboard masing-masing
