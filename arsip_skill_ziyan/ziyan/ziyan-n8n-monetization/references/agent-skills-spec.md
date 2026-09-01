# Agent Skills — Spec Ringkas (dari riset 2026-08)

Sumber: antigravity.google/docs/skills, binus.ac.id, addyosmani/agent-skills (GitHub),
Claude Agent Skills, Firebase AI Assistance, agentskills.io

## Format Wajib (SKILL.md)
```markdown
---
name: nama-skill          # lowercase, angka, hyphen. Max 64 char.
description: Apa yg dilakukan & kapan dipakai. Max 1024 char.
license: MIT             # opsional
compatibility: Node 18+  # opsional
---
# Judul
Instruksi Markdown.
```
Struktur folder:
```
skill-name/
├── SKILL.md          # wajib
├── scripts/          # kode eksekusi (opsional)
├── references/       # dokumentasi (opsional)
└── assets/           # template (opsional)
```

## Platform Kompatibel
Hermes, Antigravity (Google), Claude Code, OpenAI Codex, Gemini Spark, VS Code Copilot.

## Contoh Nyata
- github.com/addyosmani/agent-skills: code-reviewer.md, security-auditor.md
  Frontmatter: `name` + `description` (1 baris, jelas kapan trigger).
- agentskills.io/specification = spec resmi terbuka.

## Best Practices (agentskills.io)
- Description spesifik -> trigger tepat sasaran
- 1 skill = 1 kapabilitas (jangan terlalu lebar)
- `references/` untuk konteks panjang, jangan di SKILL.md
- `allowed-tools` untuk batasi tools (keamanan)
- Jangan hardcode secret -> env/credential

## Pitfall ZIYAN
- Skill yg cuma generate teks = redundant (Bos sudah punya Hermes/9router/Spark)
- Jangan auto-post API berbayar tanpa approval Bos (kasus Twitter 2026-08)
- Validasi di platform target sebelum listing jual
