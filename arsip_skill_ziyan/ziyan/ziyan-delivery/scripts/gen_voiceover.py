import pyttsx3, re, sys

# Usage: python3 scripts/gen_voiceover.py <input.md> [output.mp3]
# Baca laporan .md, strip markdown, generate voice over mp3 (pyttsx3 lokal).
inp = sys.argv[1] if len(sys.argv) > 1 else 'C:/Users/arija/ziyan_learn_batch2_report.md'
out = sys.argv[2] if len(sys.argv) > 2 else 'C:/Users/arija/ziyan_voice/laporan.mp3'

with open(inp, encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'[#*`>]', '', text)
text = re.sub(r'\n{2,}', '\n', text)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.save_to_file(text, out)
engine.runAndWait()
print('SAVED', out)
