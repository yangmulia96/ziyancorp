"""
Google Colab Runner — Video #1
Topic: Deep-Sea Octopus Ultimate Mother Sacrifice
YT Title: The Heartbreaking Sacrifice of the Deep Sea's Most Devoted Mother 🐙 #Nature #Shorts #Wildlife
"""
import os
import json

# Load metadata
with open("/content/pending_meta_1.json", "r") as f:
    data = json.load(f)

print(f"STARTING VIDEO #1: {data['topic_title']}")
print(f"YT Title: {data['youtube_title']}")
print(f"Hook: {data['hook_sentence']}")

# Execute production cell
exec(open("/content/pending_colab_cell_1.py").read())

print(f"VIDEO #1 PRODUCTION COMPLETE")
