# Google Colab Notebook - Production Runner
# Ini adalah file yang akan di-run di Google Colab

import os
import json

# Load data produksi
with open("/content/pending_meta.json", "r") as f:
    data = json.load(f)

print(f"TOPIK: {data['topic_title']}")
print(f"YOUTUBE TITLE: {data['youtube_title']}")

# Run cell produksi
exec(open("/content/pending_colab_cell.py").read())
