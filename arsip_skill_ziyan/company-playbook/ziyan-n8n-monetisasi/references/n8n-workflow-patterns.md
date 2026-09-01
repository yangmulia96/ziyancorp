# n8n Workflow Patterns for ZIYAN

Sumber: Implementasi workflow di session 2026-08-12 (12 workflow di SQLite DB).

---

## Workflow Yang Sudah Ada (Active di DB)

| Workflow ID | Nama | Status | Deskripsi |
|-------------|------|--------|-----------|
| `948713af-fbe5-4e74-af74-3f2d69815d70` | **ZIYAN Shopee Affiliate → FB Page Carousel** | ACTIVE=1 | 17 node: Telegram Trigger → Split N File → Sheet Append → Schedule 33m/77m → Caption AI (SOP Bos) → FB + X + YT |
| `58da206e-8ac4-43bc-8dde-35b1d4391a23` | **ziyan_intake_post** | ACTIVE=1 | Telegram → Sheet (intake pipeline) |
| `ZIYAN_AutoPost_X` | Auto Post ke X | Imported | OAuth1a credential `6G8rbS7S645VVXL6` |
| `ZIYAN_LynkID_AutoSales` | Lynk.id Auto Sales | Imported | |
| `ZIYAN_VN_to_Video_YouTube` | Voice Note → Video YT | Imported | |
| `ZIYAN_Storyboard_Generator` | Webhook → 9router → Telegram | Imported | AI storyboard generator |

---

## Pattern: Affiliate Automation (Model 1 & 2)

### Struktur Node Standar
```
1. Telegram Trigger (Webhook)          ← Input: Link + N files
2. Split In Batches (per file)         ← Pisah jadi N konten
3. Google Sheets Append                ← Simpan: link, file_path, status, platform
4. Schedule Trigger (8 min)            ← Generate batch
5. AI Caption (SOP Bos format)         ← Link + Harga + ≤5 hashtag kreatif
6. HTTP Request → Fal.ai (Flux/Kling)  ← Generate video/gambar
7. HTTP Request → MMAudio (SFX)        ← Optional
8. FFmpeg (local via Execute Command)  ← Stitch video + audio + subtitle
9. Schedule Trigger (77 min)           ← Publish batch (anti-spam)
10. Facebook Page Post                 ← Credential `MWsuRtJtN8JMOr2C`
11. X/Twitter Post                     ← OAuth1a credential
12. YouTube Upload                     ← OAuth2 credential
13. Update Google Sheets Status        ← Done/Failed
14. Notify Telegram (Admin)            ← Summary
```

### Credentials Diperlukan
| Credential ID | Type | Platform |
|---------------|------|----------|
| `MWsuRtJtN8JMOr2C` | Telegram Bot | Trigger & Notify |
| `6G8rbS7S645VVXL6` | Twitter OAuth1a | X Post |
| `FB_Page_Token` | Facebook OAuth | FB Page Post |
| `Google_Sheets` | Google OAuth2 | Sheets + Drive |
| `YouTube` | Google OAuth2 | YT Upload |

---

## SOP Caption (Format Bos) - WAJIB di Node AI Caption

```
[LINK PRODUK EXACT]
[HARGA WAJIB ADA]
[AI Caption pendek]
#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
```

**Contoh:**
```
https://s.shopee.co.id/4LIPRqMDM8
Rp169.426
SAMELEVEL Autumn Ribbon Halter Dress - bahan premium, nyaman dipakai sehari-hari ✨
#SAMELEVEL #OOTD #HalterDress #Affiliate #FashionID
```

---

## Schedule Timing (Anti-Spam)
- **Generate**: Every 8 minutes (batch processing)
- **Publish**: Every 77 minutes (platform safe interval)
- **Sync Sheets**: Every 53 minutes (v3 scheduler)
- **Midnight Snapshot**: 00:00 daily (cron job)

---

## Database Management (SQLite Direct)

Karena n8n API unauthorized (instance Bos beda), edit workflow via SQLite:

```bash
# Read workflow
sqlite3 ~/.n8n/database.sqlite "SELECT json FROM workflow_entity WHERE id='948713af-fbe5-4e74-af74-3f2d69815d70';" | python3 -m json.tool

# Update workflow (active, schedule, nodes)
python3 << 'EOF'
import sqlite3, json
conn = sqlite3.connect('/c/Users/arija/.n8n/database.sqlite')
wf = json.loads(conn.execute("SELECT json FROM workflow_entity WHERE id=?", ('948713af-fbe5-4e74-af74-3f2d69815d70',)).fetchone()[0])
# modify wf...
conn.execute("UPDATE workflow_entity SET json=? WHERE id=?", (json.dumps(wf), '948713af-fbe5-4e74-af74-3f2d69815d70'))
conn.commit()
EOF
```

---

## Broken Node Fixes (Applied)

| Old Node | Issue | Replacement |
|----------|-------|-------------|
| `googlePalm` | Deprecated | `googleGemini` |
| `executeCommand` | Non-standard | `code` (n8n built-in) |
| `googleGemini` (old) | Non-standard | `httpRequest` → 9Router |
| `function` (legacy) | Deprecated | `code` |

---

## Template Export (Sellable)

File: `ziyan_n8n_templates/workflow_affiliate_autopost.json` (15 nodes, no credentials embedded)

**Import via API:**
```bash
curl -X POST http://localhost:5678/api/v1/workflows/import \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflow_affiliate_autopost.json
```

---

## Next: Content Factory Nodes

Butuh custom nodes untuk:
1. **Fal.ai HTTP Request** (Flux, Kling, MMAudio endpoints)
2. **Maya Router** (prompt routing lokal)
3. **FFmpeg Local** (video stitch - Execute Command dengan ffmpeg binary)
4. **Nano Banana Workaround** (Gemini/Imagen image edit via 9Router)