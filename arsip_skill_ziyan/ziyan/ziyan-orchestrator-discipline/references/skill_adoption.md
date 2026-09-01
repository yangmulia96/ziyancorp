# Adopsi Skill Eksternal (terbukti 2026-08-08)

Bos setuju install repo `addyosmani/agent-skills` (83k★, 24 engineering skills) ke ZIYAN.

## Jalur (terbukti jalan)
1. Clone: `git clone --depth 1 https://github.com/addyosmani/agent-skills.git addyosmani-agent-skills`
2. Loop `skills/<name>/` → copy ke `C:\Users\arija\AppData\Local\hermes\skills\ziyan-addon-<name>`
   (prefix `ziyan-addon-*` agar TIDAK menimpa skill ZIYAN yang sudah ada).
3. Format `SKILL.md` standar → langsung ke-load tanpa modifikasi.

## 24 skill yang masuk (ziyan-addon-*)
api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation,
code-review-and-quality, code-simplification, context-engineering,
debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs,
doubt-driven-development, frontend-ui-engineering, git-workflow-and-versioning,
idea-refine, incremental-implementation, interview-me, observability-and-instrumentation,
performance-optimization, planning-and-task-breakdown, security-and-hardening,
shipping-and-launch, source-driven-development, spec-driven-development,
test-driven-development, using-agent-skills.

## QC Workflow (pakai ini sebelum merge/launch)
- `skill_view(name='ziyan-addon-code-review-and-quality')` → 5-axis review
  (correctness / readability / architecture / security / performance).
- Terbukti 2026-08-08: berhasil bedah workflow n8n `wa_order_notif` dan nemukan
  (a) phone tidak divalidasi (security Critical), (b) tidak ada error handling Fonnte.
- `ziyan-addon-spec-driven-development` + `ziyan-addon-planning-and-task-breakdown`
  untuk build fitur baru (spec dulu, baru code).
