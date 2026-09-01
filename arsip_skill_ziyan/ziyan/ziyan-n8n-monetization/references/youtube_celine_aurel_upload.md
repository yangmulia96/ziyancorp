# YouTube Shorts Upload — Channel CELINE AUREL (BUKTI 2026-08-07)

## Fakta Terverifikasi
- Channel LAMA: CELINE AUREL, ID `UCzY1VDdRBSpDDHzBn_NcSLg` (TikTok `@celineaurel` redistribute) — DITOLAK sebagai target upload (akun consent default-nya bukan ini).
- **Channel BARU (target final)**: "Celine Aurel" `UC8Lzhi5_SvJZcecD79xIiog` — dibuat Bos karena channel lama ribet (no Owner option). OAuth consent terakhir (code `4/0AXEQxIB7B4n...`) balik `mine=true` = "Celine Aurel" (`UC8Lzhi5_SvJZcecD79xIiog`). **INI channel yang benar untuk upload.**
- Akun manager yang JALAN: `The Visually Satisfying` (`UC2Z2COmJtCphYAkQ_M_wLFg`) — juga manager CELINE AUREL lama, tapi default-nya channel itu → upload nyasar ke sana (test `QCySbhFvu-k`, `KW8BAtoDFPA` dihapus).
- Token: `ziyan_youtube_token.json` (field `channel_id`, `refresh_token` tersimpan). Setelah OAuth terakhir, `channel_id` HARUS = `UC8Lzhi5_SvJZcecD79xIiog`.
- Upload test ke channel lama SUKSES teknis: video `QCySbhFvu-k` → https://youtube.com/shorts/QCySbhFvu-k (tapi SALAH channel → dihapus).

## KEPUTUSAN AKHIR (2026-08-07) — BUAT CHANNEL BARU
- Bos lihat Settings → Permissions CELINE AUREL: **TIDAK ADA opsi "Owner"** (channel pribadi cuma bisa invite Manager/Editor/Viewer). Transfer ownership TIDAK bisa.
- Bos putuskan: **"ribet, buat channel baru aja"** (bukan pakai CELINE AUREL lama).
- Rencana:
  1. Bos buka YouTube Studio → avatar → buat **channel BARU** (nama "Celine Aurel Official" / "ZIYAN Affiliate"). Channel baru = channel utama akun manager → OAuth upload otomatis ke sini.
  2. Ulang OAuth (Incognito, akun manager) → tukar code → token `ziyan_youtube_token.json` (channel_id = ID channel baru).
  3. Saya pasang node YouTube Shorts + set `privacyStatus: public`.
- STATUS: PENDING (Bos belum buat channel baru). Token lama masih valid tapi terikat akun "The Visually Satisfying" → wajib diulang.

## CARA UPLOAD (Python, tested jalan)
```python
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
tok=json.load(open('C:/Users/arija/AppData/Local/hermes/ziyan_youtube_token.json'))
creds=Credentials(token=tok['access_token'], refresh_token=tok['refresh_token'],
    client_id=tok['client_id'], client_secret=tok['client_secret'], token_uri=tok['token_uri'],
    scopes=['https://www.googleapis.com/auth/youtube.upload','https://www.googleapis.com/auth/youtube'])
svc=build('youtube','v3',credentials=creds)
VID=r"C:\Users\arija\Downloads\fashion_assets\Man_walking_on_street_202608071926.mp4"
body={'snippet':{'title':'TITLE','description':'DESC','tags':['fashion','shopee'],'categoryId':'22'},
      'status':{'privacyStatus':'private','madeForKids':False}}
req=svc.videos().insert(part='snippet,status', body=body,
    media_body=MediaFileUpload(VID, chunksize=-1, resumable=True))
resp=req.execute()
print('Video ID:', resp['id'])
```

## PITFALL (jangan ulang)
- SA `apikey@ziyancorp.iam.gserviceaccount.com` → `401 youtubeSignupRequired` saat `videos().insert`. SA TIDAK BISA upload ke channel manager biasa. GUNAKAN OAuth user.
- `channels?mine=true` cuma balik 1 primary channel akun yg login saat consent. Kalau balik channel lain → akun salah, ulang OAuth di Incognito.
- Code OAuth valid ~5 menit. Tukar dalam 1 blok Python (jangan pipa curl→python terpisah).
- Refresh token di `ziyan_youtube_token.json` → tidak expired berbulan-bulan (Production app).
- **JANGAN upload ke channel yang bukan tujuan** — selalu cek `mine=true` = channel target sebelum `videos().insert`.

## n8n Node (workflow `8a30e6f0-bb49-404f-98db-ff6b309fcd65`)
- Node `YouTube: Upload Shorts` (type `n8n-nodes-base.executeCommand`) — **DICABUT SEMENTARA** (menunggu channel baru). Tinggal tambah lagi setelah OAuth ulang.
- Env n8n `settings` key=`env`: `YT_TOKEN_FILE`, `YT_CHANNEL_ID` sudah set.
- Video test masih private — set `privacyStatus:public` di node kalau mau otomatis tayang.
