# Telegram Channel Post Debug (reproducible recipe)

Terbukti 2026-08-15: bot @Zynarsipbot di-angkat admin channel "Celine Aurel arsip" (-1004373452633, public @celineaurel0) tapi sendMessage/getChat tetap 404. Bot BISA baca forward (FORWARD_ORIGIN chat_id=-1004373452633).

## Probe sequence (jalankan via curl, token dari .env)
Ganti TOK dengan TELEGRAM_BOT_TOKEN dari ziyancorp/ziyan_archive_bot/.env, ID=-1004373452633.

1 getChat:        curl -s -m15 "https://api.telegram.org/bot$TOK/getChat?chat_id=$ID"
2 getChatAdmins:  curl -s -m15 "https://api.telegram.org/bot$TOK/getChatAdministrators?chat_id=$ID"
3 sendMessage:    curl -s -m15 "https://api.telegram.org/bot$TOK/sendMessage" -d "chat_id=$ID&text=TEST"
4 joinInvite:     curl -s -m15 "https://api.telegram.org/bot$TOK/joinChatByInviteLink?invite_link=https://t.me/+XXXX"
5 forward:        curl -s -m15 "https://api.telegram.org/bot$TOK/forwardMessage" -d "chat_id=$ID&from_chat_id=7349146540&message_id=1"

Semua 404 = bot gak punya membership aktif (ghost-admin).

## Dapatkan ID akurat dari forward (PTB 22.6)
Minta Bos forward 1 pesan dari channel ke PM bot. Di handler:
  msg = update.effective_message
  fo = getattr(msg, "forward_origin", None)
  if fo:
      chat = getattr(fo, "chat", None)
      channel_id = chat.id if chat else None   # ID AKURAT
JANGAN pakai ID dari bot "User Info - Get ID" (bisa salah channel).

## Root cause yang sudah ketahui
- Bot di-angkat admin LEWAT invite link, lalu link dihapus -> bot otomatis leave/kick -> jadi ghost di list admin.
- "Tambah admin" dari layar "Tambah Pengikut" != bot join sebagai member.
- joinChatByInviteLink GAGAL untuk public link t.me/xxx; butuh t.me/+XXXX eksplisit, dan bot gak bisa join dari link yang di-chat ke PM.

## Resolusi (agent GAK BISA via API)
1. Bos kick bot lalu re-add sebagai MEMBER (bukan cuma admin) - 1 aksi manusia.
2. Atau buat channel BARU, add bot, JANGAN hapus link, tes sendMessage.
3. Loop-cutoff: kalau tetap 404 setelah Bos re-add 2x -> STOP suruh klik UI, serahkan ke agent lain / buat channel baru.

## Pitfall terkait
- reject_if_unauthorized di channel: pesan channel punya effective_user=None -> bot balas "Akses ditolak". Bypass auth untuk command /distribusi.
- Jangan suruh Bos "tekan Save / klik Tambahkan sebagai admin" berulang kalau screenshot sudah nunjukin bot di list admin.
