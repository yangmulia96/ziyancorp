---
name: n8n-workflow-validation
description: Validate n8n workflow JSON before import
---
# n8n Workflow Validation Skill

## Purpose
Ensure any n8n workflow JSON file is structurally valid and ready for import into an n8n instance (e.g., localhost:5678). Prevents common import errors such as missing required fields, incorrect versionId type, broken connections, and isolated nodes.

## When to Use
- Before importing a workflow JSON into n8n.
- When creating workflow templates for sharing or selling.
- After editing a workflow manually or programmatically.

## Validation Checklist

### 1. JSON Syntax & Required Top-Level Fields
- File must be valid JSON.
- Must contain top-level keys: `name`, `nodes`, `connections`, `settings`.
- `settings` must include `"executionOrder": "v1"` (or `"v2"` if using new execution engine).

### 2. Node Structure
Each node in `nodes` array must have:
- `id` (string, unique) – **required** for n8n >= 1.0. Older workflows may use `name` as identifier; ensure `id` exists.
- `name` (string, unique within workflow).
- `type` (string, valid n8n node type, e.g., `n8n-nodes-base.scheduleTrigger`).
- `typeVersion` (number or string, matching node type version).
- `position` (array `[x, y]`).
- `parameters` (object, node-specific configuration).
- Optional: `credentials` (object mapping credential names to IDs).

### 3. versionId Field
- If present, `versionId` **must be a string** (not a number). Example: `"versionId": "1.0.0"` or `"ZIYAN-TEMPLATE"`.
- If missing, n8n will generate one on import; but for reproducibility, include a semantic version string.

### 4. Connections Logic
- `connections` object maps source node `name` to an object with `main` array.
- Each entry in `main` is an array of connection objects: `{ "node": "Target Node Name", "type": "main", "index": 0 }`.
- Verify that every referenced target node exists in `nodes`.
- Ensure there are no circular dependencies that would cause infinite loops (n8n allows cycles but they must have a trigger).

### 6. Required Node Types (for typical ZIYAN automation workflows)
The following node types are expected in a standard automation workflow:
- **Schedule Trigger** (`n8n-nodes-base.scheduleTrigger`) – starts the workflow periodically.
- **Google Sheets Read** (`n8n-nodes-base.googleSheets` with operation `read`) – fetches input data.
- **Code / Function** (`n8n-nodes-base.code` or `n8n-nodes-base.function`) – transforms data (Python/PIL, JavaScript).
- **HTTP Request** (`n8n-nodes-base.httpRequest`) – calls external APIs (9router, Facebook Graph, etc.).
- **Google Sheets Update** (`n8n-nodes-base.googleSheets` with operation `update`/`append`) – writes results back.

If any of these are missing, flag as a potential incomplete workflow.

### 6. Isolated Node Detection
- A node with no incoming **and** no outgoing connections is isolated and will never execute.
- Exception: the start node (Schedule Trigger, Webhook, Manual Trigger) may have only outgoing connections.
- Report isolated nodes as warnings.

### 7. Credentials Placeholders
- Credential references should use placeholder IDs (e.g., `"REPLACE_GSHEET_CRED_ID"`) or environment variable expressions (`{{$env.GSHEET_CRED_ID}}`).
- Actual credential IDs are instance-specific and must be configured after import.

## Validation Procedure (Automated)
Use the provided script `scripts/validate_workflow.py` (see references) to run a full check. The script:
1. Loads JSON file.
2. Runs all checks above.
3. Outputs a summary: PASS/FAIL with detailed issues.

## Manual Quick Check (if script unavailable)
1. Open JSON in a JSON-aware editor (VS Code).
2. Verify `executionOrder` exists.
3. Search for `versionId` – ensure it's a string.
4. Count nodes and connections; ensure each connection target exists.
5. Look for required node types by scanning `type` fields.

## Pitfalls & Common Errors
- **Missing `id` field** – n8n 1.0+ requires `id` on each node; workflows exported from older versions may lack it.
- **`versionId` as number** – causes import error "versionId must be a string".
- **Duplicate node names** – n8n uses names as keys in connections; duplicates break linking.
- **Incorrect `typeVersion`** – must match the node type's available versions; check n8n documentation.
- **Hardcoded credential IDs** – will not work on another instance; always use placeholders.
- **Unconnected branches** – nodes that are not reachable from any trigger will never run.

## Windows / MSYS Troubleshooting (proven 2026-08-09)
- **n8n gak bind port / "port already in use"**: instance lama gak mati bersih. Kill semua node: `ps aux | grep node` → `kill -9 <PID>` satu per satu (taskkill gak jalan di MSYS). Cek `netstat -tln | grep 5678/5679`.
- **.env n8n corrupt**: kalau baris pertama cuma hash tanpa key name (misal `c6b85...` tanpa `N8N_API_KEY=`), n8n error `Command "api" not found`. Fix: tulis `N8N_API_KEY=<hash>` di `C:\Users\arija\.n8n\.env`.
- **Import via CLI gagal `SQLITE_CONSTRAINT: NOT NULL workflow_entity.id`**: n8n 2.33 CLI import expect id auto-generate tapi column NOT NULL reject. Strip `id`, `versionId`, node `id`, `webhookId`, `credentials` dari JSON lalu import. Atau pakai API POST `/rest/workflows` (butuh owner login).
- **API Unauthorized saat import**: n8n butuh **owner account setup** dulu lewat UI (browser → Sign in). Tanpa itu, `/rest/workflows` = 401. Set `N8N_USER_MANAGEMENT_DISABLED=true` gak cukup kalau DB sudah punya user.
- **Webhook 404 "not registered"**: workflow active di DB tapi webhook gak ter-register saat n8n start (bug v2.33). Harus buka UI → toggle Active, atau jalankan via "Execute Workflow" test mode. Production webhook butuh owner login + workflow active.
- **Jalankan n8n background**: `terminal(background=true)` dengan `export N8N_PORT=5679` (hindari 5678 yang sering bentrok). Jangan pakai `&` di foreground — gunakan background=true.
- **Port pilih 5679** (bukan 5678) untuk hindari conflict dengan instance n8n lain yang nyangkut.

## Verification Steps After Import
1. Import workflow in n8n UI (Workflows → Import).
2. Open workflow, check for red error badges on nodes.
3. Run "Execute Workflow" in test mode with sample data.
4. Verify each node executes and produces expected output.
5. Check Google Sheets / external API calls succeed (use test credentials).

## References
- `references/validation_checklist.md` – detailed checklist for code reviews.
- `scripts/validate_workflow.py` – standalone validation script (run with `python validate_workflow.py <workflow.json>`).
- n8n documentation: https://docs.n8n.io/workflows/export-import/

## Related Skills
- `ziyan-n8n-workflow-builder` – for building workflows that pass validation.
- `hermes-agent-skill-authoring` – for authoring skills that include workflow templates.