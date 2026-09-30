#!/usr/bin/env bash
# Builds MusicSplitter with PyInstaller, then compiles the Inno Setup installer.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -x .venv/bin/python ]; then
    PY=.venv/bin/python
elif [ -x .venv/Scripts/python.exe ]; then
    PY=.venv/Scripts/python.exe
else
    echo 'ERROR: virtualenv not found. Run the "Setup Project" task first.' >&2
    exit 1
fi

if ! "$PY" -c 'import PyInstaller' >/dev/null 2>&1; then
    echo 'PyInstaller not in venv, installing...'
    uv pip install pyinstaller
fi

"$PY" -m PyInstaller music_splitter.spec

bash scripts/build_installer.sh
