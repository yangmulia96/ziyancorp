# LOG PERJALANAN ZIYAN — AGENT HANDOFF DOCUMENT
> Dokumen ini adalah "ingatan perusahaan". Jika Orchestrator (GM/CEO Digital) bermasalah di tengah jalan, suruh agent BARU membaca file ini + MEMORY Hermes, lalu lanjutkan dari bagian "STATUS PROYEK AKTIF".

---

## 1. IDENTITAS & VISI
- **Nama:** ZIYAN — perusahaan AI 100% dijalankan agent (manusia hanya sebagai Komisaris).
- **Komisaris (Bos):** Arijal Meutuwah. Bukan influencer, tidak menjual manual. Semua sales/outreach done by agent.
- **Objective:** GROWTH & menghasilkan REVENUE (bukan hobi/eksperimen).
- **Prinsip biaya:** operasional nyaris nol (inferensi gratis, tim = AI, hosting free tier).
- **Prinsip ETIK (instruksi Bos):** JANGAN jual yang bikin klien rugi. Pelajari betul produk sebelum outreach. Bangun portofolio/bukti dulu sebelum janji ke UMKM.

## 2. STRUKTUR ORGANISASI (Multi-Agent)
- **Orchestrator** = GM/CEO Digital (persona di `C:\Users\arija\AppData\Local\hermes\SOUL.md`). Delegasikan ke sub-agent, jangan kerja operasional manual.
- **Bos** = Komisaris, hanya setuju harga & review metrik.
- **Divisi live:** `#riset-mendalam` (Divisi Riset Mendalam), `#content-intel` (Divisi Analis Konten), Divisi Dev (via Antigravity), Divisi Audit.
- **Cara eksekusi:** `delegate_task` (background, output tidak masuk context Orchestrator → hemat token).

## 3. INFRASTRUKTUR (TERVERIFIKASI JALAN)
| Komponen | Status | Catatan |
|---|---|---|
| 9router proxy lokal | ✅ | `http://127.0.0.1:20128`, 71 model, 6 free jalan |
| 9router free models | ✅ | gemma-4-31b, gemma-4-26b, laguna-s-2.1, nemotron-nano-omni, nemotron-super-120b, nemotron-nano-30b + cadangan groq/llama-3.3-70b |
| 9router TTS | ✅ | `edge-tts/id-ID-ArdiNeural` (Indo) |
| 9router Image | ✅ | `cf/@cf/black-forest-labs/flux-2-klein-9b` |
| 9router STT/embeddings | ✅ | subtitle + RAG |
| 8 skill 9router | ✅ | terpasang di `AppData\Roaming\hermes\skills\` |
| Gemini (key Bos) | ✅ | via `ziyan_keys.env` → tes balas "Halo" |
| Antigravity IDE | ✅ | terinstall v2.4.3, OAuth connected (Gemini/Open Router/Kimi/Kiro) |
| NotebookLM Video | ✅ | Jalur A video ZIYAN, download via computer_use Brave |
| SOP rotasi model | ✅ | `SOP_Rotasi_Model_9router.md` + `rotasi.sh` |
| Penyimpanan key | ✅ | `C:\Users\arija\ziyan_keys.env` (loader .bashrc → $VAR) |
| Shortcut desktop | ✅ | `OneDrive\Desktop\ZIYAN_Keys.lnk` |

## 4. KEPUTUSAN STRATEGIS (tercatat)
- Video ZIYAN = **Jalur A (NotebookLM)** utama. Jalur B (gratis/FFmpeg) mass-produsi, kualitas di bawah.
- computer_use boros token → pakai sesekali & delegasikan ke sub-agent.
- 9router tidak ganti default (nous/tencent) sebagai otak; 9router buat sub-agent/teknis.
- Tidak pernah ketik/mengeksekusi API key literal di chat (keamanan mutlak).
- Jalur 1 (AI Service Agency) = fokus revenue pertama, tapi DITUNDA eksekusi sampai riset pasar + portofolio siap.

## 5. STATUS PROYEK AKTIF (per 31 Jul–1 Aug 2026)
- **Jalur 1 (AI Service Agency B2B Retainer):** DISKUSI, BELUM EKSEKUSI. Menunggu (a) riset pasar UMKM selesai, (b) portofolio sample dibangun.
- **Channel YouTube operasional ZIYAN = "Ziyan Malik"** (UCend05oI081uEVPTNa934Bg, 61 subs, 57K views) — milik Bos, token OAuth valid (setup via Hermes Desktop, tersimpan di ziyan_credentials/youtube_token.json). Compound Daily (mziyan266,0sub) TIDAK dipakai. Rencana: Shorts 3x/hari + Long 3x/minggu (prime time US), EN, sumber NotebookLM.
- **Blog ZYN AI co** = https://ziyancorp.blogspot.com/ (Blog ID 598320500315317650, token OAuth scope blogger OK). Tema simpel (ziyan_blogger_theme_simple.xml) BELUM di-restore Bos.
- **Compound Daily (YouTube, target utama)**: UCzWib2-2CPkWo315fzucaUw, 0 subs/1 view. Token OAuth aktif di youtube_token.json. Uploader: upload_youtube.py (YouTube Data API v3).
- **NotebookLM WAJIB untuk produksi video** (Bos yang generate, agent urus upload). Agent siapkan source + render cadangan lokal (make_video_pipeline.py).
- **Riset keyword selesai**: ziyan_keyword_research.md — topik prioritas: AI Tools 2026 cuan, AI side hustle pelajar, Chrome extensions, Dividen Coca-Cola passive income, AI automation jobs tanpa coding. Artikel perdana LIVE: "We Tested 15 Free AI Image Models...". SEO lemah (no meta desc, no H1) -> perlu perbaiki. Rencana: tema ala ZYN AI Corp (Outfit font, luminous, partikel) via CSS, autopost <=1/hari (daily-learning agent).
- **Website resmi ZYN AI Corp**: kode React (2 versi: App.jsx buatan agent, App_gemini.jsx versi Gemini clean) tersimpan di GitHub yangmulia96/zyn-aicorp-site. Demo GitHub Pages: https://yangmulia96.github.io/zyn-aicorp-site/. Sedang di-build ulang pakai versi Gemini sbg situs resmi. Data dashboard masih dummy (belum live API).
- **Riset monetisasi YouTube:** SELESAI → `ziyan_youtube_monetization.md`. Jalur tercepat <30 hari: affiliate (hari-1), Patreon/Ko-fi (mgg-1), funnel ke AI Service Agency (mgg-2). YPP butuh 1000 subs+4000 jam / 10jt Shorts views.
- **Riset Blogspot+AdSense full-AI:** SELESAI -> ziyan_blogspot_adsense_riski.md. AI content TIDAK dilarang AdSense, yg dilarang=scaled content abuse (banyak halaman tanpa value). Autopost via Blogger API v3 feasible+gratis. Verdict: HINDARI volume tinggi; boleh side-asset dgn akun terisolasi, <=1 post/hari, data orisinal.
- **OAuth YouTube Error 403:** SELESAI → `ziyan_youtube_oauth_fix.md`. Solusi: consent screen status "In production" + External (user cap 100 cukup). Token tidak expire 7 hari.
- **Bedah 7 video referensi** (`ziyan_learn_videos_report.md`) + bedah Gemini PDF: pola menang = hook angka/kontras <3dtk, demo layar sbg bukti, faceless+VO, angle uang, CTA komunitas (bukan jualan). Hindari: hook egosentris, video musik tanpa narasi, CTA agresif+niche sempit. Rekomendasi: 1 longform/minggu + 3-5 Shorts demo, diferensiasi "100% dijalankan agent — ini datanya".
- **Studi kasus YouTube agent** (`ziyan_research_youtube_agent_cases.md`): preseden @TheCrackedEng (content-foundry, 100% autonom). RISIKO: Jan 2026 YouTube cabut YPP 16 channel via Inauthentic Content Policy (overposting/template/slideshow statis). Wajib: Judge agent (quality gate), upload random (bukan serentak), publish Private dulu lalu flip, disclosure sintetis, ukur like-rate/retention bukan jumlah video. TTS berisiko demonetisasi (pakai Google TTS/voice asli).
- **OpenMontage DIHAPUS** (pelajaran pahit 2 Ags 2026): butuh 27 menit/video, API imagen 404, Gemini image 429, Google TTS 401, video_gen berbayar tidak ada -> hasil cuma image stills (bukan video AI). TIDAK EFISIEN untuk kita. Ganti: produksi video pakai NotebookLM (Bos/login) atau computer_use + 9router/openrouter token untuk TTS/image.
- **Riset n8n cuan** (`ziyan_riset_n8n_cuan.md`): uang terbesar = JASA (workflow $150-2000/proyek, retainer $200-1500/klien/bln, margin 85-95%), BUKAN konten. Faceless YT cuma $6-15/bln (gratis) s.d $150-250 (premium). AI CS UMKM ID: Rp3-10jt setup + Rp500k-2jt/bln. n8n=self-host gratis = OTOT, Hermes = OTAK. Prioritas monetisasi: #1 AI CS UMKM, #2 jasa workflow, #3 content-as-service, #4 channel sendiri (lead magnet). Gratis tetap cuan (n8n+Gemini free+Edge-TTS+Pexels+FFmpeg+YT API).
- **Divisi Template n8n** (deleg_73484253): 3 draf JSON SIAP (wa_cs_umkm $39, leadgen_maps $49, faceless_engine $59-99) di ziyan_n8n_templates/. Semua placeholder {{API_KEY}}, 0 hardcode. README_jual.md sudah ada (Gumroad+n8n.io+X/Twitter+grup ID+Fiverr). Status: STANDBY, BELUM JUAL. Testing butuh n8n ter-install (sedang npm install di n8n_server/, gagal ENOTEMPTY -> bersihkan -> install ulang).
- **Tempat jual**: (1) Gumroad etalase utama, (2) n8n.io Creator Hub versi lite GRATIS (SEO+lead), (3) X/Twitter+LinkedIn build in public, (4) YouTube ZIYAN tutorial, (5) Grup FB/WA/Telegram ID (Rupiah), (6) Fiverr/Upwork upsell jasa $150-2000.
- **Channel YouTube `mziyan266@gmail.com`:** hanya 1 channel "Compound Daily" (0 sub, sisa nb_proof). Channel ZIYAN BELUM ADA — butuh rename/buat baru. Video pilot: `ziyan_notebooklm_short.mp4` sudah siap.
- **Riset pasar Jalur 1:** SELESAI → `ziyan_riset_jalur1.md`. Kesimpulan: PERLU REVISI (tambah tier Pilot Rp499rb, no lock-in, bundle konten+lead report+onboarding, outreach WA/IG DM, 1-2 beta klien g...[truncated]
- **Riset tools Google (Flow/Labs/Omni Flash/Nano Banana):** SELESAI → `ziyan_riset_google_tools.md`. Temuan: Nano Banana jalan via `ag/gemini-3.1-flash-image` (9router); channel `gemini/` mati (key invalid di proxy); Flow/Labs/Google Omni Flash belum ada API publik stabil → pakai browser automation.
- **Audit nb_proof:** SELESAI → `ziyan_audit_nbproof.md` (5 aset reusable: generate_visuals.py, pipeline_full.py, nb_pipeline.py, generate_longform.py, audit_and_learn.py).
- **Blueprint monetisasi:** `ZIYAN_BLUEPRINT_MONETISASI.md` (3 jalur: Agency / Micro-SaaS / Media Affiliate).

## 6. FILE PENTING (path absolut)
- `C:\Users\arija\ZIYAN_BLUEPRINT_MONETISASI.md` — blueprint bisnis
- `C:\Users\arija\SOP_NotebookLM_Video.md` — SOP video NotebookLM
- `C:\Users\arija\ziyan_content_intel_N2DfbFfdnCs.md` — bedah video kompetitor
- `C:\Users\arija\SOP_Rotasi_Model_9router.md` + `rotasi.sh` — rotasi model
- `C:\Users\arija\models9r.json` — daftar 71 model 9router
- `C:\Users\arija\ziyan_keys.env` — **RAHASIA** key API (jangan commit/share)
- `C:\Users\arija\ziyan_credentials\google_client_secret.json` — OAuth client BOS (project `lofty-layout-504106-n4`), dipakai jika ZIYAN perlu akses Google API resmi. RAHASIA.
- `C:\Users\arija\ziyan_prinsip_etik.md` — prinsip etik
- `C:\Users\arija\ziyan_notebooklm_short.mp4` — video ZIYAN (NotebookLM, tidak dikirim ke chat)
- `C:\Users\arija\test_tts.mp3`, `test_img.png` — sample TTS/image 9router
- `C:\Users\arija\ziyan_audit_nbproof.md` — hasil audit nb_proof (5 aset reusable)
- `C:\Users\arija\ziyan_riset_jalur1.md` — riset pasar Jalur 1 (sub-agent jalan)
- `C:\Users\arija\nb_proof\` — folder eksperimen LAMA (bukan ZIYAN), sedang diaudit

## 7. RAHASIA & KEAMANAN
- **JANGAN** print/eval API key di chat. Key dibaca via env var `$VAR`.
- `ziyan_keys.env` = satu-satunya tempat key (Bos isi manual via shortcut desktop).
- `nb_proof/` punya file rahasia KADALUARSA: `client_secret*.json`, `all_google_cookies.json`, `gemini_key.txt` (key BEDA dari yang Bos revoke — masih berisiko, sebaiknya revoke juga), `token_*.json`, `yt_token.pickle`.
- Email akun ZIYAN: `mziyan266@gmail.com` (Ziyan Malik) — untuk NotebookLM.

## 8. CARA LANJUTKAN JIKA ORCHESTRATOR GAGAL
1. Baca dokumen ini (ZIYAN_COMPANY_LOG.md).
2. Baca MEMORY Hermes (sudah kompak, fokus fakta stabil).
3. Cek sub-agent live log: `AppData\Local\hermes\cache\delegation\live\`.
4. Cek status proyek di bagian 5 di atas.
5. Lanjutkan delegasi: riset → portofolio → outreach (Jalur 1). Jangan bypass prinsip etik (section 1).

---
*Dokumen ini selalu di-update oleh Orchestrator tiap ada milestone. Jika stale, cek tanggal di header & bandingkan dengan MEMORY.*
