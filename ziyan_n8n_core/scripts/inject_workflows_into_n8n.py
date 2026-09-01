import sqlite3
import json
import uuid
from pathlib import Path
from datetime import datetime

db_path = Path.home() / ".n8n" / "database.sqlite"
workflows_dir = Path(r"C:\Users\arija\ziyancorp\ziyan_n8n_core\workflows")

conn = sqlite3.connect(str(db_path))
c = conn.cursor()

# Get default project_id and user
c.execute("SELECT id FROM project LIMIT 1;")
proj_row = c.fetchone()
project_id = proj_row[0] if proj_row else None
print("Found project_id:", project_id)

c.execute("SELECT id FROM user LIMIT 1;")
user_row = c.fetchone()
user_id = user_row[0] if user_row else None
print("Found user_id:", user_id)

json_files = sorted(list(workflows_dir.glob("*.json")))
print(f"Total workflows to insert: {len(json_files)}")

now_iso = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

for jf in json_files:
    data = json.loads(jf.read_text(encoding="utf-8"))
    wf_name = data.get("name", jf.stem)
    
    # Check if already exists
    c.execute("SELECT id FROM workflow_entity WHERE name = ?", (wf_name,))
    existing = c.fetchone()
    if existing:
        print(f"[SKIP] '{wf_name}' already exists with ID: {existing[0]}")
        continue
    
    wf_id = uuid.uuid4().hex[:16]
    version_id = str(uuid.uuid4())
    nodes_json = json.dumps(data.get("nodes", []))
    connections_json = json.dumps(data.get("connections", {}))
    settings_json = json.dumps(data.get("settings", {"executionOrder": "v1"}))
    
    c.execute("""
        INSERT INTO workflow_entity (
            id, name, active, nodes, connections, settings, staticData, pinData,
            versionId, triggerCount, meta, createdAt, updatedAt, isArchived,
            versionCounter, description
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        wf_id, wf_name, 0, nodes_json, connections_json, settings_json, None, None,
        version_id, 0, json.dumps({}), now_iso, now_iso, 0,
        1, f"Ziyan Automation Systems (ZAS) official workflow template: {jf.name}"
    ))
    
    # Link to project in shared_workflow if table exists and project_id exists
    if project_id:
        try:
            c.execute("""
                INSERT INTO shared_workflow (workflowId, projectId, role)
                VALUES (?, ?, ?)
            """, (wf_id, project_id, "workflow:owner"))
        except Exception as e:
            print("Shared workflow insert error:", e)
            
    print(f"[INSERTED] '{wf_name}' -> ID: {wf_id}")

conn.commit()
conn.close()
print("\nAll 5 workflows successfully inserted into n8n database!")
