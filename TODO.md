# TODO

## Backlog

- Bug 11 | Installed .exe lack perlissions to write log file
  """
  Traceback (most recent call last):
  File "main.py", line 169, in <module>
  File "main.py", line 66, in __init__
  File "main.py", line 18, in setup_logging
  File "logging\__init__.py", line 1219, in __init__
  File "logging\__init__.py", line 1248, in _open
  PermissionError: [Errno 13] Permission denied: 'C:\\Program Files\\Music Splitter\\music_splitter.log'
  """
  I assume it will also fail to read/write the settings file.


- Feature 7: Fix `release.yml` — broken Inno Setup download
  Current step downloads `innosetup-6.5.zip` from GitHub releases which doesn't exist (releases only have compiled `.exe` installers).
  Best-practice options researched:
  - **A. Chocolatey** *(recommended)*: `choco install innosetup --no-progress -y` → ISCC at `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`
  - B. Official silent install: download `is.exe` from jrsoftware.org, run `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART`
  - C. `robin24/inno-setup-action@v1`: dedicated action, pass `.iss` path as input

- Feature 8 (low priority): Windows installer variant that **bundles FFmpeg** (follow-up of Feature 6)
  Bundle a static `ffmpeg.exe` next to the app exe so users without FFmpeg get a self-contained install.
  Resolution order: bundled copy next to exe → system PATH → error.

- Feature 12: Durable installer distribution via GitHub Releases (CalVer)
  Context: CI only uploads Actions artifacts (expire per retention setting, consume the limited Actions storage bucket); installers are not visible under *Releases* and carry no version.
  Plan:
  1. Date-based tags `vYYYY.MM.DD`. Same-day rebuilds must NOT create new releases: use `softprops/action-gh-release@v3` with `allow_existing: true` so the existing release is updated and its asset swapped in place.
  2. Release step uploads `MusicSplitter-Setup-v<date>.exe` directly from the build output (`installer/output/*.exe`) — no intermediate Actions artifact needed for this; release notes = latest `CHANGELOG.md` entry.
  3. Remove `upload-artifact` (or keep temporarily for debug copies).
  4. Set repo artifact retention to ~7 days (`PATCH /repos/{owner}/{repo}` → `actions_retention_days`, needs admin rights) so old artifacts auto-delete; Releases become the permanent channel.
  6. **Keep-last-3 cleanup**: after publishing/updating the release, delete older releases keeping only the latest 3 (counting the new one). Example:
     ```bash
     gh release list --limit 4 | tail -n +2 | cut -f1 | xargs -rn1 gh release delete --cleanup-tag
     ```
     Requires `delete-packages`/release write permission on the token. Caps cumulative asset size at ~3 × installer-size against the repo quota.
  Storage note: Actions artifacts count against the separate Actions storage quota (500 MB/repo free) and expire by retention; Release assets count against the repository size limit (default 5 GB soft cap, shared with git/LFS) and never expire until deleted manually. Monitor cumulative installer size if building daily.
  Blocker: editing `.github/workflows/release.yml` requires PAT `workflow` scope (see PR #50 `release.txt` workaround).

- Feature 10 (investigation/POC): Smart segment post-processing — merge short (<5min), split long (>15min) segments after fixed-duration split. Optional onset-snap refinement. See `Feature_10.md` for details.

## Done (last 20 teaks)

- Feature 6: Windows installer (first step, no bundled FFmpeg) — PyInstaller spec, Inno Setup script, CI build workflow, VS Code task, robust FFmpeg resolution with install-guidance error
- Feature 8: cleanup project structure — `libs/` → `src/` (+ `__init__.py`), `ui.py` moved into `src/`, `ui-text/` → `localization/`
- Feature 7: The internal log will be replaced by a log file, plus a button that shows it when an operation fails.
- Feature 9: UX – Move split result status below action button
