"""
Google Colab Runner — Video #2
Topic: Deep Sea Octopus 4.5-Year Sacrifice
YT Title: The Most Heartbreaking Sacrifice in Nature 💔 #nature #wildlife #ocean
"""
import os
import json

# Load metadata
with open("/content/pending_meta_2.json", "r") as f:
    data = json.load(f)

print(f"STARTING VIDEO #2: {data['topic_title']}")
print(f"YT Title: {data['youtube_title']}")
print(f"Hook: {data['hook_sentence']}")

# Execute production cell
exec(open("/content/pending_colab_cell_2.py").read())

print(f"VIDEO #2 PRODUCTION COMPLETE")
