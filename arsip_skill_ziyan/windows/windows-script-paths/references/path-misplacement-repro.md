# Reproduction — `/c/...` absolute path misplacement in on-disk Python (2026-08-14)

## Setup
A Python script `gen_metadata.py` was written via `write_file` to the correct
absolute path `C:\Users\arija\workdir\videos\2026-08-14b\`. Inside it:

```python
WORKDIR = "/c/Users/arija/workdir/videos/2026-08-14b"   # WRONG inside .py
os.makedirs(WORKDIR, exist_ok=True)
with open(os.path.join(WORKDIR, "metadata_qc.json"), "w") as f:
    ...
print("METADATA OK")   # printed successfully
```

Run from terminal (cwd was the correct dir):
```
cd /c/Users/arija/workdir/videos/2026-08-14b && python3 gen_metadata.py
# -> METADATA OK  (no error)
```

## Symptom (confusion)
```
ls -la /c/Users/arija/workdir/videos/2026-08-14b/
# only gen_metadata.py present, NO metadata_qc.json / social_*.md
read_file("/c/Users/arija/workdir/videos/2026-08-14b/metadata_qc.json")
# "File not found"
```
Yet the script reported success.

## Root cause
Windows-native `python3` received the string `/c/Users/arija/...` and treated it
as relative to the current drive (C:) root → resolved to
`C:\c\Users\arija\workdir\videos\2026-08-14b\` (extra `c`). The shell's
git-bash `/c/...` mapping does NOT apply inside the Python process.

## Discovery
```
find /c/c -name "metadata_qc.json" 2>/dev/null
# /c/c/Users/arija/workdir/videos/2026-08-14b/metadata_qc.json   <-- misplaced twin
```

## Fix applied
```
cp /c/c/Users/arija/workdir/videos/2026-08-14b/*.md /c/c/Users/arija/workdir/videos/2026-08-14b/*.json \
   /c/Users/arija/workdir/videos/2026-08-14b/
rm -rf /c/c/Users/arija/workdir/videos/2026-08-14b
```
And the script was corrected to use `WORK = "."` (relative) since terminal was
already `cd`'d into the target dir.

## Rule of thumb
- Terminal commands (curl/ls/mkdir/cp): `/c/Users/...` ✅
- Inside `.py` `open()`/`os.path`: use `.` or `r"C:\Users\..."` ✅ ; `/c/...` ❌
- Always `ls` the correct path after a script run; never trust its "OK" print.
