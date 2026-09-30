#!/usr/bin/env bash
# Find ISCC.exe (the Inno Setup compiler) in common installation paths.
# Sourceable: defines find_iscc(). Run directly to print the found path or exit 1.

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
  if [ -f innosetup/ISCC.exe ]; then
    echo 'innosetup/ISCC.exe'
    return 0
  fi
  return 1
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  if iscc_path=$(find_iscc); then
    echo "ISCC (InnoSetup executable) found at $iscc_path"
    exit 0
  fi
  echo 'ERROR: ISCC (InnoSetup executable) not found'
  exit 1
fi
