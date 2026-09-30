#!/usr/bin/env bash
# Compile the installer with Inno Setup (expects dist/MusicSplitter from PyInstaller).
set -e
source "$(dirname "$0")/find_iscc.sh"

if ! iscc_path=$(find_iscc); then
  echo 'ERROR: ISCC (InnoSetup executable) not found. Run the "Install Inno Setup" task first.'
  exit 1
fi
echo "Using ISCC at: $iscc_path"
"$iscc_path" /Q installer/music_splitter.iss
