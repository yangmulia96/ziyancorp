---
name: ziyan-agent-skills
description: Panduan membuat, mengelola, dan menggunakan AI Agent Skills (format terbuka SKILL.md) untuk monetisasi ZIYAN. Use when Bos ingin membuat skill otomatisasi, mengubah workflow n8n/NotebookLM menjadi skill siap-pakai, atau memahami ekosistem skill (Antigravity, Claude, Codex, Gemini Spark, agentskills.io).
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Agent Skills — Panduan & Standar

Agent Skills = format terbuka (standard agentskills.io) untuk memberi AI kemampuan
baru lewat file `SKILL.md`. Kompatibel lintas platform: Hermes, Antigravity (Google),
Claude Code, OpenAI Codex, Gemini Spark, VS Code Copilot.

## Format Wajib (SKILL.md)

```markdown
---
name: nama-skill          # lowercase, angka, hyphen. Max 64 char.
description: Apa yang dilakukan & kapan dipakai. Max 1024 char.
license: MIT             # opsional
compatibility: Node 18+, Python 3.11  # opsional
---

# Judul Skill
Instruksi Markdown bebas di sini.
```

Struktur folder:
```
skill-name/
├── SKILL.md          # wajib
├── scripts/          # kode eksekusi (opsional)
├── references/       # dokumentasi pendukung (opsional)
└── assets/           # template/file (opsional)
```

## Lokasi Skill di ZIYAN
- Hermes: `C:\Users\arija\AppData\Local\hermes\skills\`
- Antigravity: `.gemini/antigravity/scratch/<nama>/`
- Claude/Codex: `.agents/skills/` atau `.claude/skills/`
- Gemini Spark: paste isi SKILL.md ke area setup Spark

## Alur Buat Skill (5 Langkah)
1. **Identifikasi kapabilitas** — apa yang ingin diotomatisasi? (contoh: TikTok UGC, review kode, baca email)
2. **Tulis SKILL.md** — frontmatter + instruksi step-by-step (directive, bukan naratif)
3. **Tambah scripts/** kalau butuh eksekusi kode (Python/Node)
4. **Test** dengan task kecil, keep approval ON untuk aksi berisiko (posting, delete)
5. **Packaging** — zip/README kalau mau jual (Gumroad/template n8n)

## Best Practices (dari agentskills.io)
- Description harus spesifik → trigger tepat sasaran
- Satu skill = satu kapabilitas (jangan terlalu lebar)
- Pakai `references/` untuk konteks panjang, jangan masukkan ke SKILL.md
- `allowed-tools` untuk batasi tools (keamanan)
- Jangan hardcode secret → pakai env/credential

## Contoh Skill Monetisasi ZIYAN (sudah ada)
- `ziyan-n8n-monetisasi` — jual template/jasa n8n
- `ziyan-youtube` — upload YouTube otomatis
- `ziyan-notebooklm-automation` — 8 artefak NotebookLM
- `ziyan-blog-seo` — SOP blog SEO

## Integrasi Skill → Cuan
| Skill | Platform | Hasil |
|---|---|---|
| tiktok-affiliate-ugc | Gemini Spark / Hermes | Naskah affiliate (lead magnet) |
| wa-cs-umkm | n8n + skill | Jasa Rp 3-10jt setup |
| faceless-content | NotebookLM + skill | YouTube adsense |

## Pitfall
- Jangan buat skill yang cuma "generate teks" (Bos sudah punya Hermes/9router)
- Skill yang akses API berbayar (X/Twitter) harus ada approval Bos — jangan auto-post ngabisin saldo
- Validasi di platform target sebelum listing jual

## Referensi
- Spec: https://agentskills.io/specification
- Showcase: https://agentskills.io/clients
- Antigravity: https://antigravity.google/docs/skills
- addyosmani/agent-skills (GitHub) — contoh nyata
