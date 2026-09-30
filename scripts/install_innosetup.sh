#!/usr/bin/env bash
# Ensure Inno Setup is available: reuse an existing install, otherwise download it.
set -e
source "$(dirname "$0")/find_iscc.sh"

if iscc_path=$(find_iscc); then
  echo "ISCC (InnoSetup executable) found at $iscc_path, InnoSetup already installed"
  exit 0
fi

echo 'Downloading Inno Setup...'
mkdir -p innosetup
curl -L -o innosetup/innosetup.exe https://github.com/jrsoftware/issrc/releases/download/is-7_1_0/innosetup-7.1.0-x64.exe
innosetup/innosetup.exe /EXTRACT:"$(pwd)/innosetup" /SP- /VERYSILENT
rm innosetup/innosetup.exe

if [ ! -f innosetup/ISCC.exe ]; then
  find innosetup -name ISCC.exe -exec cp {} innosetup/ISCC.exe \;
fi
echo "ISCC (InnoSetup executable) ready at $(find_iscc)"
