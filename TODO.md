# TODO

## Backlog

- Feature 6: Add an installer for Windows — **first step WITHOUT bundled FFmpeg**
  Branch: `feat/06_windows_installer` · Plan frozen by 🍋 Pi Lemon (2026-09-27)
  Decisions:
  - No FFmpeg bundling in this step: app requires FFmpeg on the system PATH; show a clear "install FFmpeg" error when missing.
  - Pipeline: PyInstaller → Inno Setup (modern best practice per web research).
  PR task list:
  - [ ] PyInstaller config for `main.py` (`--windowed`, icon from `assets/icon.ico`, bundle `localization/english.yml` as data)
  - [ ] Robust FFmpeg resolution in `src/splitter.py`: system PATH → clear user-facing error (+ tests)
  - [ ] Inno Setup script `installer/music_splitter.iss`: exe into `{autoprogramfiles}`, Start Menu shortcut, uninstaller
  - [ ] Build workflow/script on a Windows runner (PyInstaller → ISCC)
  - [ ] README build instructions + CHANGELOG entry
  - [ ] VS code task to run the installer builder locally

- Feature 6.1: Add a proposed GH workflow for the Release of he installer

- Feature 6.2: Windows installer variant that **bundles FFmpeg** (follow-up of Feature 6)
  Bundle a static `ffmpeg.exe` next to the app exe so users without FFmpeg get a self-contained install.
  Resolution order: bundled copy next to exe → system PATH → error.

- Feature 10: Smart segment post-processing — merge short (<5min), split long (>15min) segments after fixed-duration split. Optional onset-snap refinement. See `Feature_10.md` for details.

## Done (last 20 teaks)

- Feature 8: cleanup project structure — `libs/` → `src/` (+ `__init__.py`), `ui.py` moved into `src/`, `ui-text/` → `localization/`
- Feature 7: The internal log will be replaced by a log file, plus a button that shows it when an operation fails.
- Feature 9: UX – Move split result status below action button
