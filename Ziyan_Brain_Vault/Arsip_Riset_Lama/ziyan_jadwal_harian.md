# ZIYAN — JADWAL KERJA HARIAN & PERSIAPAN AGENT

## Prasyarat Sebelum Mulai (Setiap Pagi)
1. **9router aktif** — jalankan: `9router -p 20128 -H 127.0.0.1 -t --skip-update`
   Cek: `curl -s http://127.0.0.1:20128/v1/models` (harus return JSON)
2. **Hermes Desktop app nyala** (bukan shutdown)
3. **NotebookLM auth valid** — cek: `notebooklm list` (storage_state.json di OneDrive/ziyan_pending)
4. **YouTube/Blogger token valid** — cek file di ziyan_credentials/

## Kapasitas Harian (NotebookLM FREE tier)
- **MAX 3 Video Overview + 3 Audio Overview / HARI**
- Artinya: **3 konten penuh/hari** (Long video + Audio + 6 artefak lain)
- Blog post: unlimited (cuma butuh draft MD, tidak makan quota video)

## Jadwal Kerja (1 Hari = 3 Konten)

| Jam | Karyawan | Tugas | Output |
|-----|----------|-------|--------|
| 08:00 | RISA | Riset topik trending X/HN (niche AI/Tech/Finance) | 1-3 topik kandidat |
| 08:30 | RISA | Pilih 1 topik + kumpul 10 URL sumber valid | 10 source URL |
| 09:00 | NOVA | Buat notebook + inject 10 sumber | Notebook siap |
| 09:30 | NOVA | Generate 8 artefak (video long, audio, slide, info, report, csv, mindmap, quiz) | 8 task started |
| 10:00 | NOVA | Poll + download artefak ke ziyan_artifacts/<topik>/ | 8 file di disk |
| 11:00 | FAZA | Upload Long ke YouTube (private, schedule besok) | Video scheduled |
| 12:00 | PANDA | Blog (Blogger) + Telegram + LinkedIn | Post live |
| 13:00 | RISA | Ulangi untuk konten ke-2 (sisa 2 quota) | Topik 2 |
| 16:00 | RISA | Konten ke-3 (quota habis) | Topik 3 |
| 18:00 | PANDA | Twitter/X (jika token valid) | Tweet |

**Bos generate Short native di HP** untuk tiap topik (CLI tidak support 9:16).

## Persiapan Kebutuhan Agent (Checklist)
- [ ] 9router jalan (port 20128)
- [ ] storage_state.json valid (NotebookLM)
- [ ] youtube_token_compound.json valid
- [ ] youtube_desktop_client.json valid
- [ ] blog_zyn_id.txt (ID Blogger)
- [ ] youtube_token_ziyanmalik.json (scope blogger)
- [ ] ~/.x_credentials (Twitter OAuth 1.0a) — PERLU REGENERATE (401)
- [ ] ziyan_keys.env (9router key, dll)
- [ ] Folder ziyan_artifacts/ siap
- [ ] Folder ziyan_pending/ (script cron)

## Role Agent
- **RISA** (Riset): trending topic, 10 sumber, validasi fakta — model 9router
- **NOVA** (NotebookLM): inject source, generate 8 artefak — CLI notebooklm-py
- **FAZA** (Video/Upload): YouTube upload, schedule — API YouTube
- **PANDA** (Distribusi): Blog, TG, LinkedIn, Twitter, monetisasi — API masing-masing
- **Orchestrator (Parent/nous)**: koordinator, tidak eksekusi operasional

## Catatan Etik
- Jangan janjikan cuan sebelum ada bukti
- Selalu verifikasi URL sebelum jadi source (jangan halu)
- Private dulu, Bos review, baru publish
