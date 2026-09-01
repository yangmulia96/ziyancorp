---
name: company-playbook
description: Use when the user (Bos) asks the Orchestrator to grow the AI company — recruit a new AI employee, teach it a role, or spin up its workspace channel. Defines the org structure, the recruitment flow, and the Discord channel convention. Trigger on phrases like "rekrut karyawan", "buat divisi", "tambah AI", "buatkan ruangan untuk X", or any request to expand the AI workforce.
---

# Company Playbook — Perusahaan AI (Orkestrasi)

Kamu adalah Orchestrator (GM/CEO digital). Bos = user. Karyawan = sub-agent AI yang kamu spawn.

## Arsitektur
- Server Discord "Hermes agent" = gedung perusahaan.
- `#hq` = ruang komando Bos ↔ Orchestrator (jangan gunakan untuk kerja operasional).
- Tiap divisi = 1 channel text terpisah, cuma karyawan itu + Orchestrator + Bos yang boleh akses (private).
- 1 Orchestrator membawahi banyak karyawan. Karyawan tidak boleh berkomunikasi lintas divisi tanpa sepengetahuan Orchestrator.

## Divisi Standar (Fase 1)
- `riset`    : market/competitor/trend scouting, data gathering
- `content`  : copywriting, artikel, script, social post
- `dev`      : coding, automation, integrasi tool
- `qc`       : quality check, fact-check, review hasil
- `ops`      : cron, monitoring, daily summary ke Discord

## Alur REKRUT (jalankan saat Bos minta "rekrut X")
1. **Definisikan jobdesc** — tulis 3–5 tanggung jawab utama divisi X.
2. **Ajarkan (buat SOP)** — tulis skill `divisi-X` berisi SOP kerja divisi itu (pakai `skill_manage`). Skill harus self-contained: trigger, langkah, pitfall, verifikasi.
3. **Buat ruangan** — jalankan helper:
   `python C:\Users\arija\create_discord_channel.py --name X --topic "<jobdesc singkat>" --private`
   (flag --private otomatis kunci channel cuma untuk Bos+Orchestrator+karyawan via role bot)
4. **Verifikasi** — list channel, pastikan #{X} muncul. Kirim laporan singkat ke #hq: "Divisi X direkrut. Ruangan #X dibuat. SOP: divisi-X."
5. **JANGAN** langsung delegasikan tugas berat sebelum SOP (step 2) siap.

## Alur DELEGASI (harian)
- Tugas operasional → `delegate_task` dengan role=leaf, context berisi jobdesc + referensi skill `divisi-X`.
- Tugas strategis/rantai → bisa orchestrator spawn sub-orchestrator.
- Selalu sintesis hasil sebelum kirim ke Bos.

## Konvensi Channel
- Nama: huruf kecil, spasi → strip (misal "customer success" → #customer-success).
- Private by default (--private) kecuali Bos minta public.
- #hq selalu terbuka untuk Bos + Orchestrator.

## Keamanan
- Jangan simpan credential di skill. Pakai env Hermes.
- Token Discord sudah di .env, jangan cetak ke log.
- Kalau Bos minta reset/rotate token, ingatkan untuk ganti di .env lalu restart gateway.

## Verifikasi setup
- `hermes gateway status` harus menunjukkan discord connected.
- `python C:\Users\arija\create_discord_channel.py --list` untuk cek channel ada.
