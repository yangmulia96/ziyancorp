# venv Isolation + PYTHONPATH Pollution (proven 2026-08-15)

## Symptom (confusing)
A fresh project venv is created, deps installed, but imports fail with:
```
ModuleNotFoundError: No module named '_cffi_backend'
ModuleNotFoundError: No module named 'cryptography'
ModuleNotFoundError: No module named 'requests'
ModuleNotFoundError: No module named 'google.api_core'
```
`pip show google-auth` inside the venv reports a version, yet code imports Hermes's copy.

## Root cause
The host has a global `PYTHONPATH` set to the Hermes agent venv:
```
PYTHONPATH=C:\Users\arija\AppData\Local\hermes\hermes-agent;C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Lib\site-packages
```
This prepends Hermes's (often outdated/broken) `site-packages` AHEAD of the project venv.
The project venv's `python.exe` still loads Hermes packages. `pip install` without unsetting
also writes into Hermes venv (polluting it, risking `cryptography==48.0.1` vs `50.0.0` conflicts).

## Fix (always do this for project venvs on this machine)
```bash
cd /c/Users/arija/ziyancorp/ziyan_archive_bot
python3 -m venv venv
# install / run WITH PYTHONPATH stripped:
env -u PYTHONPATH ./venv/Scripts/python.exe -m pip install -r requirements.txt
env -u PYTHONPATH ./venv/Scripts/python.exe -m ziyan_bot.bot
```
For single commands: `unset PYTHONPATH && ./venv/Scripts/python.exe script.py` also works in bash.
In `cmd.exe` use `set PYTHONPATH=` first.

## Why not just `python -m venv` and go?
Because the inherited `PYTHONPATH` env var outranks the venv's own path resolution. `env -u`
removes it for the child process only (safe, no global mutation needed).

## Note
The Hermes agent itself relies on that global PYTHONPATH — never unset it for Hermes tools,
only for spawning/running separate project venvs.
