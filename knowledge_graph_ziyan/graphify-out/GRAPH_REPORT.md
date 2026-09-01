# Graph Report - knowledge_graph_ziyan  (2026-08-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 201 nodes · 430 edges · 20 communities (17 shown, 3 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8524395d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- distribute_agent.py
- ArchiveService
- GoogleWorkspace
- ArchiveBot
- Database
- autotube_api_server.py
- FakeGoogle
- get_credentials
- run_distribute.sh
- youtube_studio_upload.py
- threads_reauth.py
- fb_reauth.py
- shorts_engine.py
- run_bot.sh

## God Nodes (most connected - your core abstractions)
1. `GoogleWorkspace` - 33 edges
2. `ArchiveBot` - 25 edges
3. `Database` - 25 edges
4. `ArchiveService` - 23 edges
5. `Settings` - 18 edges
6. `ProductDraft` - 14 edges
7. `FakeGoogle` - 13 edges
8. `main()` - 13 edges
9. `LocalFile` - 9 edges
10. `distribute_to_platforms()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `get_products_latest()` --uses--> `Settings`  [INFERRED]
  distribute_agent.py → ziyan_bot/config.py
- `get_pending_product()` --uses--> `Settings`  [INFERRED]
  distribute_agent.py → ziyan_bot/config.py
- `main()` --uses--> `Settings`  [INFERRED]
  distribute_agent.py → ziyan_bot/config.py
- `mark_published()` --uses--> `Settings`  [INFERRED]
  distribute_agent.py → ziyan_bot/config.py
- `mark_status()` --uses--> `Settings`  [INFERRED]
  distribute_agent.py → ziyan_bot/config.py

## Import Cycles
- None detected.

## Communities (20 total, 3 thin omitted)

### Community 0 - "distribute_agent.py"
Cohesion: 0.10
Nodes (37): Application, build_caption(), download_asset(), drive_id_from_url(), get_affiliate_json(), get_pending_product(), main(), mark_published() (+29 more)

### Community 1 - "ArchiveService"
Cohesion: 0.20
Nodes (9): main(), main(), ArchiveService, LocalFile, Path, clean_url(), parse_caption(), ProductDraft (+1 more)

### Community 2 - "GoogleWorkspace"
Cohesion: 0.17
Nodes (4): Any, get_products_latest(), GoogleWorkspace, Path

### Community 3 - "ArchiveBot"
Cohesion: 0.31
Nodes (4): DEFAULT_TYPE, Update, ArchiveBot, UploadSession

### Community 4 - "Database"
Cohesion: 0.22
Nodes (3): Connection, Database, Path

### Community 5 - "autotube_api_server.py"
Cohesion: 0.24
Nodes (8): BaseHTTPRequestHandler, fetch_image(), generate_tts(), Handler, publish_video(), AutoTube Shorts Factory — Backend HTTP API Server Dipanggil oleh n8n via HTTP…, render_short(), _tts_async()

### Community 7 - "get_credentials"
Cohesion: 0.36
Nodes (9): Credentials, Namespace, get_credentials(), get_my_channel(), main(), Path, main(), parse_args() (+1 more)

### Community 8 - "run_distribute.sh"
Cohesion: 0.25
Nodes (7): CHANNEL_CELINE, FB_PAGE_TOKEN, GOOGLE_CREDENTIALS_FILE, HERMES_CUSTOM_9ROUTER_API_KEY, INSTAGRAM_USER_TOKEN, run_distribute.sh script, THREADS_USER_TOKEN

### Community 9 - "youtube_studio_upload.py"
Cohesion: 0.71
Nodes (6): Page, click_create_and_upload(), fill_metadata(), first_visible(), main(), wait_for_manual_login()

### Community 10 - "threads_reauth.py"
Cohesion: 0.43
Nodes (4): code_to_short(), refresh(), req(), short_to_long()

### Community 11 - "fb_reauth.py"
Cohesion: 0.83
Nodes (3): get_page_token(), get_user_token_from_code(), req()

## Knowledge Gaps
- **8 isolated node(s):** `run_bot.sh script`, `CHANNEL_CELINE`, `FB_PAGE_TOKEN`, `GOOGLE_CREDENTIALS_FILE`, `HERMES_CUSTOM_9ROUTER_API_KEY` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GoogleWorkspace` connect `GoogleWorkspace` to `distribute_agent.py`, `ArchiveService`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `ArchiveService` connect `ArchiveService` to `distribute_agent.py`, `GoogleWorkspace`, `ArchiveBot`, `Database`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `Database` connect `Database` to `distribute_agent.py`, `ArchiveService`, `GoogleWorkspace`, `ArchiveBot`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `ArchiveBot` (e.g. with `ArchiveService` and `LocalFile`) actually correct?**
  _`ArchiveBot` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Database` (e.g. with `ArchiveService` and `ArchiveBot`) actually correct?**
  _`Database` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ArchiveService` (e.g. with `Database` and `GoogleWorkspace`) actually correct?**
  _`ArchiveService` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Settings` (e.g. with `get_pending_product()` and `get_products_latest()`) actually correct?**
  _`Settings` has 12 INFERRED edges - model-reasoned connections that need verification._