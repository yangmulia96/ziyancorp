import sqlite3
import json
import uuid
from pathlib import Path
from datetime import datetime

db_path = Path.home() / ".n8n" / "database.sqlite"
workflows_dir = Path(r"C:\Users\arija\ziyancorp\ziyan_n8n_core\workflows")

conn = sqlite3.connect(str(db_path))
c = conn.cursor()

# 1. Clean up non-standard UUID rows
c.execute("DELETE FROM workflow_entity WHERE name LIKE 'ZAS%';")
c.execute("DELETE FROM shared_workflow WHERE workflowId NOT IN (SELECT id FROM workflow_entity);")
print("Cleaned old ZAS rows.")

# 2. Get project_id
c.execute("SELECT id FROM project LIMIT 1;")
proj_row = c.fetchone()
project_id = proj_row[0] if proj_row else None
print("Using project_id:", project_id)

json_files = sorted(list(workflows_dir.glob("*.json")))
now_iso = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.000")

for jf in json_files:
    data = json.loads(jf.read_text(encoding="utf-8"))
    wf_name = data.get("name", jf.stem)
    
    wf_id = str(uuid.uuid4())
    version_id = str(uuid.uuid4())
    nodes_json = json.dumps(data.get("nodes", []))
    connections_json = json.dumps(data.get("connections", {}))
    settings_json = json.dumps(data.get("settings", {"executionOrder": "v1"}))
    meta_json = json.dumps({"templateCredsSetupCompleted": True})
    
    c.execute("""
        INSERT INTO workflow_entity (
            id, name, active, nodes, connections, settings, staticData, pinData,
            versionId, triggerCount, meta, createdAt, updatedAt, isArchived,
            versionCounter, description, nodeGroups
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?
        )
    """, (
        wf_id, wf_name, 0, nodes_json, connections_json, settings_json, None, None,
        version_id, 0, meta_json, now_iso, now_iso, 0,
        1, f"ZAS Official Template: {jf.name}", "[]"
    ))
    
    if project_id:
        c.execute("""
            INSERT INTO shared_workflow (workflowId, projectId, role)
            VALUES (?, ?, ?)
        """, (wf_id, project_id, "workflow:owner"))
        
    print(f"[RE-INSERTED OK] {wf_name} -> {wf_id}")

conn.commit()
conn.close()
print("All workflows successfully fixed and formatted with standard UUIDs!")
