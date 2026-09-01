import subprocess, json, time, os, sys, re, argparse

# NotebookLM video generation pipeline (generate -> poll -> download).
# Proven 2026-08-12. Encodes the CORRECT CLI syntax:
#   * `generate video "<DESCRIPTION>"`  -> ONE positional = prompt/description
#     (NOT "title" + "prompt" -> VALIDATION_ERROR unexpected extra argument)
#   * `artifact poll <task_id>` REQUIRES `notebooklm use <notebook_id>` first,
#     else it returns "not_found". task_id from generate == artifact_id.
# Run this in terminal(background=true); generation takes 30+ min.

PY = r"C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"


def run(cmd, timeout=300):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notebook-id", required=True)
    ap.add_argument("--source", default=None, help="path to source .md (added if generating)")
    ap.add_argument("--out", required=True, help="output .mp4 path")
    ap.add_argument("--format", default="explainer")
    ap.add_argument("--prompt", default="Create an engaging, fast-paced explainer video with clear visuals, an energetic but professional tone, and a strong hook in the first 10 seconds.")
    ap.add_argument("--task-id", default=None, help="reuse existing generation task (skip generate)")
    ap.add_argument("--state", default=None, help="pipeline_state.json to update on completion")
    ap.add_argument("--max-min", type=int, default=110)
    args = ap.parse_args()

    # REQUIRED: set active notebook context before artifact poll
    u = run([PY, "-m", "notebooklm", "use", args.notebook_id])
    print("USE rc=%d" % u.returncode, flush=True)

    if args.task_id:
        task = args.task_id
        print("REUSE task=%s" % task, flush=True)
    else:
        if args.source and os.path.exists(args.source):
            s = run([PY, "-m", "notebooklm", "source", "add", "-n", args.notebook_id, args.source])
            print("SOURCE ADD rc=%d %s" % (s.returncode, s.stdout[-300:]), flush=True)
        # generate: SINGLE positional = DESCRIPTION/prompt (NOT title+prompt)
        g = run([PY, "-m", "notebooklm", "generate", "video", args.prompt,
                 "-n", args.notebook_id, "--format", args.format, "--no-wait", "--json"])
        print("GEN rc=%d" % g.returncode, flush=True)
        print(g.stdout[-2000:], flush=True)
        print(g.stderr[-1000:], flush=True)
        m = re.search(r'"task_id"\s*:\s*"([^"]+)"', g.stdout)
        if not m:
            m = re.search(r'task[_\s]?id[:\s]+([0-9a-f-]{20,})', g.stdout + g.stderr, re.I)
        if not m:
            print("NO TASK ID -- abort", flush=True)
            sys.exit(2)
        task = m.group(1)
    print("TASK=%s" % task, flush=True)

    url = None
    for i in range(args.max_min):
        time.sleep(60)
        p = run([PY, "-m", "notebooklm", "artifact", "poll", task, "--json"])
        out = p.stdout
        print("POLL %d %s" % (i, out[-1000:]), flush=True)
        if '"status"' in out and 'completed' in out.lower():
            mu = re.search(r'"(https?://[^"]+\.mp4)"', out)
            if not mu:
                mu = re.search(r'"url"\s*:\s*"(https?://[^"]+)"', out)
            if mu:
                url = mu.group(1)
                break

    if not url:
        print("NO URL after polling -- exit 3", flush=True)
        sys.exit(3)
    print("URL=%s" % url, flush=True)
    dl = run(["curl", "-L", url, "-o", args.out], timeout=600)
    sz = os.path.getsize(args.out) if os.path.exists(args.out) else 0
    print("DL rc=%d size=%s" % (dl.returncode, sz), flush=True)

    if args.state and os.path.exists(args.state):
        try:
            st = json.load(open(args.state))
        except Exception:
            st = {}
        st.update({"video_file": args.out if sz > 0 else None, "video_size": sz,
                   "download_url": url, "gen_task_id": task,
                   "status": "downloaded_ready_for_upload" if sz > 0 else "gen_failed",
                   "uploaded": False})
        json.dump(st, open(args.state, "w"), indent=2)
    print("=== DONE ===", flush=True)


if __name__ == "__main__":
    main()
