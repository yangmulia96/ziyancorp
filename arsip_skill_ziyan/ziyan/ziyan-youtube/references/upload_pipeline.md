# Pipeline batch upload NotebookLM → YouTube

Script: `C:\Users\arija\ziyan_drive_learn\upload_pipeline.py`
State:  `C:\Users\arija\ziyan_drive_learn\upload_state.json` (dict path→video_id, anti double-upload)

## Pakai
```
python upload_pipeline.py                # DRY-RUN (default aman, tidak upload)
python upload_pipeline.py --run          # eksekusi
python upload_pipeline.py --run --max 2  # batasi jumlah
python upload_pipeline.py --run --now    # publish langsung public, tanpa jadwal
python upload_pipeline.py --no-router    # skip 9router, template murni
```

## Tahap & keputusan desain (terverifikasi 2026-08-02)
1. **Scan** `C:\Users\arija\ziyan_videos\*.mp4`
   - skip `*.compressed.mp4` (output sendiri, kalau tidak → loop upload ganda)
   - skip file dgn mtime < 60 detik → menghindari upload file yang MASIH ditulis
     NotebookLM/ffmpeg (penyebab video korup di server).
2. **Compress** kalau > 12 MB:
   `ffmpeg -i in.mp4 -c:v copy -c:a aac -b:a 48k -ac 1 -movflags +faststart out.compressed.mp4`
   - `-c:v copy` = video tidak di-reencode → cepat, hanya audio yang dikecilkan.
   - `+faststart` penting supaya moov atom di depan (upload/streaming lancar).
   - Terbukti: 0.4 MB → 0.1 MB, probe hasil `aac (LC) mono 48 kb/s`.
   - Path ffmpeg winget:
     `C:\Users\arija\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe`
3. **Auth**: refresh token dulu dari `youtube_desktop_client.json` (`installed`|`web`),
   tulis balik `access_token` ke `youtube_token.json`. Print status saja
   ("token: refreshed OK"), TIDAK PERNAH nilai token.
4. **Guard channel**: `channels?part=snippet&mine=true`; kalau judul channel tidak
   mengandung "compound" → ABORT sebelum upload apa pun. Wajib ada di tiap script
   upload agar video tidak nyasar ke channel lain di akun yang sama.
5. **Metadata**: template ZIYAN + polish 9router (`openrouter/google/gemma-4-26b-a4b-it:free`),
   minta balasan JSON `{title, hook, bullets}`; fallback ke topik dari nama file
   (`compound_daily_agentic_ai_20260802.mp4` → "Compound Daily Agentic Ai") kalau
   router mati. Parsing respons 9router: lihat skill `llm-proxy-9router`
   (body berpadding + multi-objek JSON).
6. **Jadwal random**: `status.privacyStatus="private"` + `status.publishAt` (RFC3339 UTC,
   `%Y-%m-%dT%H:%M:%SZ`) acak 3–36 jam ke depan, dgn gap minimal 90 mnt + jitter
   terhadap `last_scheduled` di state → rilis tidak serentak.
   `--now` → `public` tanpa `publishAt`.

## Cara tes tanpa upload nyata
Bikin MP4 dummy dgn lavfi lalu mundurkan mtime supaya lolos guard 60 detik:
```bash
ffmpeg -y -f lavfi -i color=c=blue:s=640x360:d=3 -f lavfi -i anullsrc -shortest \
  -loglevel error 'C:\Users\arija\ziyan_videos\_test.mp4'
touch -d '-5 minutes' /c/Users/arija/ziyan_videos/_test.mp4
python upload_pipeline.py --max 1     # dry-run
rm -f /c/Users/arija/ziyan_videos/_test.mp4
```
CATATAN git-bash: argumen path OUTPUT untuk ffmpeg.exe harus gaya Windows
(`'C:\Users\...'`); path gaya `/c/Users/...` ditolak "No such file or directory".
