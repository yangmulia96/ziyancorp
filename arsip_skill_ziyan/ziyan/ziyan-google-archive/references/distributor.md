# Distributor — archive project output layer

The archive bot (input/storage) writes to Drive + Sheets `ARSIP_MASTER`. The **distributor**
is the output layer: read products from Sheets, generate a natural caption via 9Router,
and push to platforms. Built 2026-08-15.

## Architecture
```
Sheets ARSIP_MASTER (PRODUCT_MASTER tab)
   -> read latest products
   -> 9Router (kr/claude-sonnet-4.5) generates NATURAL, non-robotic caption
   -> post to Telegram channel (bot must be channel admin)
   -> (future) FB / IG / Threads / YouTube -- need Bos tokens
```

## File
`ziyancorp/ziyan_archive_bot/distributor.py`
Run: `env -u PYTHONPATH GOOGLE_CREDENTIALS_FILE=client_secret.json HERMES_CUSTOM_9ROUTER_API_KEY="$HERMES_CUSTOM_9ROUTER_API_KEY" ./venv/Scripts/python.exe distributor.py`

## Caption style (Bos rule: "bukan yang robotik")
Prompt asks for: natural Bahasa Indonesia, "kayak orang rekomendasiin ke temen", max 1 emoji,
affiliate links on separate line. Output example:
> "Gue suka banget sama celana pendek jeans ini, modelnya high waist jadi bikin kaki
> keliatan panjang... Tokopedia: [link] Shopee: [link]"

## Telegram channel setup (agent builds code, Bos does the UI part)
1. Bos creates channel (e.g. `@ZiyanArsipChannel`).
2. Bos adds bot `@Zynarsipbot` as **admin**.
3. Bos gives agent the channel username/ID.
4. Agent wires a `/distribusi PROD-ID` command / broadcast module in the bot.

## Platform status (2026-08-15)
- Telegram channel: code-ready, needs Bos to create channel + add bot.
- FB / IG / Threads / YouTube: NOT built — require Bos-provided tokens. YouTube (Compound
  Daily) is a SEPARATE project (see session history: `youtube_token_compound.json` missing).

## Celine Aurel channel (real case 2026-08-15)
Bos arsip ke akun AI influencer "Celine Aurel": YT, IG, Threads, FB, + Telegram channel
`t.me/celineaurel0` (public, name "Celine Aurel arsip", channel ID `-1004373452633`).
Caption format Bos: `[link Shopee]` blank `[deskripsi 1-2 kalimat]` blank `[link lain]`
blank `[5 hashtag]` — **DILARANG sebut harga**. Caption AI natural (9Router) sudah jalan.

## Pitfalls — Telegram channel admin (MAHAL, jangan ulangi 2026-08-15)
Simptom: `getChat`/`sendMessage` ke channel ID balik `{"ok":false,"error_code":404,"Not Found"}`
padahal Bos sudah "jadikan admin" + screenshot nunjukin bot di list admin dengan hak post ON.
Penyebab sebenarnya (bukan ID salah): bot **belum jadi MEMBER channel**. Di Telegram, bot
harus di-invite sebagai member DULU — admin rights tanpa membership = 404 di API write/read.
Forward dari channel ke PM bot MASIH bisa dibaca (update lewat ke bot), tapi `getChat`/`sendMessage`
butuh membership. Urutan yang BENER (jangan skip):
1. Channel → 3 titik → Manage → **Administrators** → "Tambah admin" → cari `@Zynarsipbot`.
2. Dialog "Tambah bot sebagai admin?" muncul → **TEKAN "Tambahkan sebagai admin" (biru kanan)**.
   (Ini yang bikin bot jadi member+admin sekaligus. Cuma buka layar Hak Admin + toggle ON
   TANPA tekan tombol ini = pending, tetap 404.)
3. Pastikan "Posting Pesan" ON → tekan ✅ Save.
4. Tes: `curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" -d "chat_id=-100...&text=TEST"`
   → `{"ok":true,...}` berarti beres.
- **JANGAN verifikasi lewat `t.me/celineaurel0` public link + `joinChatByInviteLink`** →
  public channel link gak joinable via API (404 juga). Bot harus di-add lewat UI admin, bukan link.
- **JANGAN nebak ID channel salah** kalau 404. Dapet ID AKURAT dari FORWARD: Bos forward 1
  pesan channel ke PM bot → bot log `FORWARD_ORIGIN chat_id=...`. (Bukan ngetik "Test" di channel —
  itu cuma trigger `reject_if_unauthorized`, gak kasih ID.) Forward = quote "Diteruskan dari ...".
- **PTB 22.6 attribute name**: `Message.forward_from_chat` TIDAK ADA → AttributeError. Pakai
  `msg.forward_origin` (type `MessageOriginChannel`), lalu `forward_origin.chat.id`.

## Pitfalls — general
- Distributor reads `PRODUCT_MASTER!A2:K`; column order = product_id,title,description,
  shopee_url,tiktok_url,... (matches google_workspace.PRODUCT_HEADERS).
- Always pass both `GOOGLE_CREDENTIALS_FILE=client_secret.json` (OAuth) and the 9Router key
  env, plus `env -u PYTHONPATH`, or imports/auth fail.
- `reject_if_unauthorized` nolak pesan channel (effective_user=None) dgn "Akses ditolak" — itu
  normal untuk pesan di channel, BUKAN bug. Bypass auth untuk command `/distribusi` (aman, cuma
  Bos yang tau Product ID).
