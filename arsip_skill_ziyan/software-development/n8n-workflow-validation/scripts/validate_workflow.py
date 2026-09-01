#!/usr/bin/env python3
import json
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_workflow.py <path/to/workflow.json>")
        sys.exit(1)
    
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        sys.exit(1)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        sys.exit(1)
    
    # Check required top-level keys
    required_top = ['name', 'nodes', 'connections', 'settings']
    missing = [k for k in required_top if k not in data]
    if missing:
        print(f"Missing top-level keys: {missing}")
        sys.exit(1)
    
    # Check executionOrder in settings
    settings = data.get('settings', {})
    if 'executionOrder' not in settings:
        print("ERROR: Missing 'executionOrder' in settings")
        sys.exit(1)
    
    # Check versionId is string if present
    version_id = data.get('versionId')
    if version_id is not None and not isinstance(version_id, str):
        print("ERROR: versionId must be a string")
        sys.exit(1)
    
    # Check nodes exist and are non-empty
    nodes = data.get('nodes', [])
    if not nodes:
        print("ERROR: No nodes found")
        sys.exit(1)
    
    # Basic node validation (quick checks)
    for node in nodes:
        if 'id' not in node:
            print("ERROR: Node missing 'id' field")
            sys.exit(1)
        if 'name' not in node:
            print("ERROR: Node missing 'name' field")
            sys.exit(1)
        if 'type' not in node:
            print("ERROR: Node missing 'type' field")
            sys.exit(1)
    
    # Basic connections check
    conn_data = data.get('connections', {})
    for src_name in conn_data.keys():
        src_exists = any(n.get('name') == src_name for n in nodes)
        if not src_exists:
            print(f"ERROR: Source node '{src_name}' not found in nodes")
            sys.exit(1)
    
    print("VALIDATION PASSED: Workflow structure OK")
    sys.exit(0)

if __name__ == "__main__":
    main()