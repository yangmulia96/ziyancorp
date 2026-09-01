# n8n v2.33+ Fixes & Patterns (Session 2026-08-10)

## Root Causes Discovered

### 1. Node.js Version Incompatibility
- **Node 24.16.0** → n8n crashes silently (exit 0, no logs, healthz works then dies)
- **Fix**: Use Node 22.22 LTS explicitly
- Path: `C:/Users/arija/node22b/node-v22.22.0-win-x64/node.exe`
- Update `start-n8n.bat` to use this path

### 2. Workflow Folder Requirement (CRITICAL)
- n8n 2.33+ requires `parentFolderId` on `workflow_entity`
- Without folder → workflow `active=1` in DB but **invisible in UI** (Overview tab shows "Create your first automation")
- **Fix**:
  ```sql
  -- Create folder (needs projectId from project table)
  INSERT INTO folder (id, name, projectId, createdAt, updatedAt) 
  VALUES ('uuid', 'Default', 'D74O8wwfFsAZJTM0', datetime('now'), datetime('now'));
  
  -- Assign workflow
  UPDATE workflow_entity SET parentFolderId='folder_uuid' WHERE id='workflow_id';
  ```
- Project ID is single-row in `project` table

### 3. Telegram Credential Limitations
- **Cannot create** Telegram credential via API/DB (n8n 2.33 encrypt format)
- **Must create manually** in UI: Settings → Credentials → Add → Telegram API
- **CAN link** existing credential to workflow node via DB:
  ```sql
  UPDATE workflow_entity 
  SET nodes = json_replace(nodes, '$.<node_index>.credentials.telegramApi', 'credential_id')
  WHERE id = 'workflow_id';
  ```
- Or use Python to parse/update nodes JSON

### 4. Auto-Start Patterns
- `start-n8n.bat` in Startup folder → runs Node 22.22 + n8n in independent CMD window
- `start-9router.bat` in Startup folder → runs 9Router with API key env var
- Both survive laptop restart without Antigravity/session dependency

### 5. Health Check Reliability
- `healthz` can return 200 while web UI not actually serving (cached response?)
- **Real check**: `curl -s -o /dev/null -w "%{http_code}" http://localhost:5678/` → must be 200
- Port 5678 must be LISTENING in netstat

## Verification Checklist After Restart
- [ ] 9Router port 20128 health OK
- [ ] n8n port 5678 LISTENING + HTTP 200 on `/`
- [ ] Workflow visible in UI (Workflows tab)
- [ ] Telegram credential linked to Trigger node
- [ ] Test trigger works (send message to bot)