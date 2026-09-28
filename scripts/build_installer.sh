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
  echo "Using ISCC at: $iscc_path"
  "$iscc_path" /Q installer/music_splitter.iss
  exit $?
fi

if [ -f innosetup/ISCC.exe ]; then
  echo 'Using local ISCC at ./innosetup/ISCC.exe'
  ./innosetup/ISCC.exe /Q installer/music_splitter.iss
  exit $?
fi

echo 'ERROR: ISCC.exe not found'
exit 1