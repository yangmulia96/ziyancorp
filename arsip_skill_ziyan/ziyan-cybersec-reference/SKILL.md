---
name: ziyan-cybersec-reference
description: Index & panduan pakai repo mukul975/Anthropic-Cybersecurity-Skills (817 skill, agentskills.io standard, kompatibel Hermes) sebagai referensi konten defensive ZIYAN. Use when butuh mapping MITRE ATT&CK/NIST, contoh threat defense, atau ide konten cybersecurity edukatif.
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Cybersec Reference (Repo 817 Skills)

Repo: https://github.com/mukul975/Anthropic-Cybersecurity-Skills
- 817 skills, 29 domain, 6 framework (MITRE ATT&CK, NIST CSF 2.0, MITRE ATLAS, D3FEND, NIST AI RMF, MITRE F3)
- Standard: agentskills.io (SKILL.md + YAML frontmatter)
- Kompatibel: Hermes Agent, Claude Code, Codex, Gemini CLI, Cursor, 26+ platform
- License: Apache 2.0

## Struktur Skill (contoh: abusing-dpapi-for-credential-access)
```yaml
---
name: abusing-dpapi-for-credential-access
description: Extract/decrypt Windows DPAPI secrets...
domain: cybersecurity
subdomain: red-teaming
tags: [red-team, credential-access, dpapi]
version: '1.0'
author: mahipal
license: Apache-2.0
mitre_attack: [T1555.004]
---
# Instruksi + Legal Notice (authorized use only)
```

## Cara Pakai untuk ZIYAN
1. **Clone/read repo** → cari skill di domain yang relevan (misal: `analyzing-email-headers-for-phishing-investigation`)
2. **Extract poin defensive** → jadi bahan konten edukatif (bukan offense)
3. **Mapping framework** → cite MITRE/NIST di video/blog (kredibilitas)
4. **JANGAN jalankan offensive skill** tanpa authorize — hanya untuk refs konten

## Domain Relevan untuk Konten ZIYAN
- `analyzing-email-headers-for-phishing-investigation` → video "Cara deteksi phishing AI"
- `analyzing-dns-logs-for-exfiltration` → "Tanda data bocor lewat DNS"
- `analyzing-certificate-transparency-for-phishing` → "Cegah phishing dengan CT log"
- `achieving-cmmc-level-2-compliance` → "UMKM & compliance keamanan"

## Install ke Hermes (optional)
```
git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills
# copy folder skills/<nama>/ ke C:\Users\arija\AppData\Local\hermes\skills\
```

## Pitfall
- Repo ada skill OFFENSIVE (red-team) — ZIYAN hanya pakai untuk refs defensive/edu
- Selalu sertakan Legal Notice di konten (authorized use)
- Jangan klaim affiliation dengan Anthropic (community project)
