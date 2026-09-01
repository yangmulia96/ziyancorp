---
name: ziyan-fact-validation
description: Validate ZIYAN facts via tool/terminal before reporting.
---

# ZIYAN Fact Validation

## Trigger
- Before reporting project status
- Before building/modifying workflows/templates/automation
- When user asks for validation
- Every 4 hours auto refresh

## Rules
1. Verify via direct tool/terminal/API. Never trust model claims alone.
2. After validation, update `MEMORY.md` with verified facts.
3. If conflict found between report and memory, fix memory first.
4. Keep memory entries short, factual, current.

## Commands
- n8n workflow count: `sqlite3 .n8n/database.sqlite "SELECT COUNT(*) FROM workflow_entity;"`
- List workflows: `sqlite3 .n8n/database.sqlite "SELECT id, name, active FROM workflow_entity ORDER BY active DESC, name;"`
- Process check: `ps aux | grep -E 'n8n|scheduler|9router|hermes' | grep -v grep`
- Config check: `grep -A2 '^model:' AppData/Local/hermes/config.yaml`

## Output
- Table: Item | Verified Value | Source
- If invalid, state correction clearly
- Update MEMORY.md immediately after
