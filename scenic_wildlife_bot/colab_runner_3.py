"""
Google Colab Runner — Video #3
Topic: Octopus Mother Ultimate Sacrifice
YT Title: The Heartbreaking Ultimate Sacrifice of a Mother Octopus 💔 #wildlife #nature #ocean
"""
import os
import json

# Load metadata
with open("/content/pending_meta_3.json", "r") as f:
    data = json.load(f)

print(f"STARTING VIDEO #3: {data['topic_title']}")
print(f"YT Title: {data['youtube_title']}")
print(f"Hook: {data['hook_sentence']}")

# Execute production cell
exec(open("/content/pending_colab_cell_3.py").read())

print(f"VIDEO #3 PRODUCTION COMPLETE")
