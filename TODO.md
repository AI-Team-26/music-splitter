# TODO

## Backlog

- Feature 7: Fix `release.yml` — broken Inno Setup download
  Current step downloads `innosetup-6.5.zip` from GitHub releases which doesn't exist (releases only have compiled `.exe` installers).
  Best-practice options researched:
  - **A. Chocolatey** *(recommended)*: `choco install innosetup --no-progress -y` → ISCC at `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`
  - B. Official silent install: download `is.exe` from jrsoftware.org, run `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART`
  - C. `robin24/inno-setup-action@v1`: dedicated action, pass `.iss` path as input

- Feature 8 (low priority): Windows installer variant that **bundles FFmpeg** (follow-up of Feature 6)
  Bundle a static `ffmpeg.exe` next to the app exe so users without FFmpeg get a self-contained install.
  Resolution order: bundled copy next to exe → system PATH → error.

- Feature 10 (investigation/POC): Smart segment post-processing — merge short (<5min), split long (>15min) segments after fixed-duration split. Optional onset-snap refinement. See `Feature_10.md` for details.

## Done (last 20 teaks)

- Feature 6: Windows installer (first step, no bundled FFmpeg) — PyInstaller spec, Inno Setup script, CI build workflow, VS Code task, robust FFmpeg resolution with install-guidance error
- Feature 8: cleanup project structure — `libs/` → `src/` (+ `__init__.py`), `ui.py` moved into `src/`, `ui-text/` → `localization/`
- Feature 7: The internal log will be replaced by a log file, plus a button that shows it when an operation fails.
- Feature 9: UX – Move split result status below action button
