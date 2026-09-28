#!/usr/bin/env bash
# Find ISCC.exe in common Inno Setup installation paths
# Returns the path to ISCC.exe on stdout, exits 0 if found, 1 if not found

find_iscc() {
  local p
  for p in \
    '/c/Program Files/Inno Setup 7/ISCC.exe' \
    '/c/Program Files (x86)/Inno Setup 7/ISCC.exe' \
    '/c/Program Files/Inno Setup 6/ISCC.exe' \
    '/c/Program Files (x86)/Inno Setup 6/ISCC.exe' \
    '/c/Program Files/Inno Setup 5/ISCC.exe' \
    '/c/Program Files (x86)/Inno Setup 5/ISCC.exe'; do
    if [ -f "$p" ]; then
      echo "$p"
      return 0
    fi
  done
  return 1
}

if iscc_path=$(find_iscc); then
  echo "ISCC found at: $iscc_path"
  exit 0
fi

if [ -f innosetup/ISCC.exe ]; then
  echo 'Inno Setup already installed locally'
  exit 0
fi

# Download and extract Inno Setup
mkdir -p innosetup
curl -L -o innosetup/innosetup.exe https://github.com/jrsoftware/issrc/releases/download/is-7_1_0/innosetup-7.1.0-x64.exe
innosetup/innosetup.exe /EXTRACT:"${workspaceFolder}/innosetup" /SP- /VERYSILENT
rm innosetup/innosetup.exe

# Ensure ISCC.exe is at innosetup/ISCC.exe
if [ ! -f innosetup/ISCC.exe ]; then
  find innosetup -name ISCC.exe -exec cp {} innosetup/ISCC.exe \;
fi