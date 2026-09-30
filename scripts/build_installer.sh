#!/usr/bin/env bash
# Builds the Windows installer: PyInstaller app bundle -> Inno Setup compilation.
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

source "$(dirname "$0")/find_iscc.sh"

if ! iscc_path=$(find_iscc); then
    echo 'ERROR: ISCC (InnoSetup executable) not found. Run the "Install Inno Setup" task first.' >&2
    exit 1
fi
echo "Using ISCC at: $iscc_path"
"$iscc_path" /Q installer/music_splitter.iss
