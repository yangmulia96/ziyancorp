# Compound Daily — Off-Window Cron Pipeline (verified run 2026-08-11)

Snapshot operasional pipeline YouTube "Compound Daily" saat dijalankan sebagai cron
(job tunggal, tanpa user). Tujuannya menyelaraskan SKILL.md (yang berisi protokol
window-gating) dengan apa yang BENAR-BENAR jalan di disk.

## Jendela (clock = UTC, dari skill ziyan-video-production)
- Short (brief, ≤60s): generate/upload HANYA `UTC 15:00–23:00`.
- Long (explainer): HANYA `Senin/Rabu/Jumat 19:00–22:00 ET` = `UTC 23:00–02:00`,
  hari dihitung dari ET (bukan UTC).
- OFF-WINDOW (keduanya tutup) → STEP generate/upload/QC **SKIP**. Kerjakan prep saja.

## Urutan yang TERBUKTI JALAN (off-window run)
1. **Riset** (deterministik, tanpa LLM):
   - Copy `parse_trending.py` + `fetch_hn.py` dari skill
     `research/trending-topics-research/scripts/` ke `research/` (parser pakai path
     relatif `WORK="."`, jadi jalankan dari `research/`).
   - `fetch_run.sh`: `rm -f` stale `gn_*.xml tc.xml at.xml hn_*.json`, lalu curl HN top
     + 4 query GN (`artificial+intelligence`, `semiconductor`, `stock+market`,
     `business+technology`, semua `when:2d`) + `techcrunch.com/feed` + `arstechnica.com/feed`.
     JANGAN pakai `&`/`xargs -P` di foreground terminal (ditolak/hanya 1 file).
   - `python3 fetch_hn.py` (ThreadPoolExecutor 8-worker) → 25 `hn_*.json`.
   - `python3 parse_trending.py` → `research/trending_topics.md` (15 topik rank, URL nyata).
   - The Verge & Reddit dilewati (host block) — otomatis di parser.
2. **Pilih rank-#1** → staging ke `research/videos/<TANGGAL>/`:
   - `notebooklm_source_rank1.md` — naskah Short (English, ~60s) utk di-paste ke
     NotebookLM "Copied text". Tulis via 9Router model **`channel-researcher`**
     (bukan `google/*` yang 404 di proxy). Prompt: jangan fabrikasi angka, hook 3 dtk, CTA.
   - `metadata_qc.json` — SEO (title/tags/categoryId 28) + QC flags.
   - `social_twitter_thread.md`, `social_linkedin_post.md`, `social_tiktok_snippet.md` — draft.
3. **State**: `research/video_pipeline_state.json` → `status:"off_window_prep"`,
   `next_action` = generate pada run in-window berikutnya.

## CATATAN ASSET (cek tiap run, bukan aturan permanen)
- `notebooklm-py` auth: `storage_state.json` ada ≠ session hidup. Generate butuh
  background process >30 mnt + poll (cron wait clamp 60 dtk → tidak bisa atomik).
- `ziyan_videos/` sering berisi file LAMA (bukan dari run ini) → `upload_pipeline.py`
  akan anggap "baru" & upload ganda. Bersihkan / mark di `upload_state.json` sebelum upload.
- Token upload = `youtube_token.json` (lihat SKILL.md, sudah di-koreksi dari `_compound`).
