# TODO

## Backlog

- Feature 8 (low priority): Windows installer variant that **bundles FFmpeg** (follow-up of Feature 6)
  Bundle a static `ffmpeg.exe` next to the app exe so users without FFmpeg get a self-contained install.
  Resolution order: bundled copy next to exe → system PATH → error.

- Feature 10 (investigation/POC): Smart segment post-processing — merge short (<5min), split long (>15min) segments after fixed-duration split. Optional onset-snap refinement. See `Feature_10.md` for details.

## Done (last 20 teaks)

- Feature 12: durable installer distribution via GitHub Releases (CalVer) — `release.yml` now renames the built exe to `MusicSplitter-Setup-vYYYY.MM.DD.exe` and publishes it as a date-tagged GitHub Release (`softprops/action-gh-release@v3`, which updates an existing release for the same tag in place and replaces same-named assets by default, so same-day rebuilds never create duplicates), with the latest `CHANGELOG.md` entry as release notes; replaced `upload-artifact`; keep-last-3 release cleanup caps cumulative asset size (repo Actions artifact retention still needs admin to be lowered to ~7 days).
- Feature 13: modernized Tkinter UI — `ttkthemes` plastik/equilux theming with graceful fallback warning, custom ttk styling (buttons, SPLIT green #4CAF50, status bar frame), grid layout for browse/naming/part-length/status areas, Pillow icons on Browse/SPLIT buttons (`assets/browse_icon.png`, `assets/split_icon.png`), dark-mode toggle persisted to `config.json`
- Feature 14: fixed `release.yml` Inno Setup install — replaced the broken `innosetup-6.5.zip` GitHub-release download with Chocolatey (`choco install innosetup`), verified green on CI; removed the now-stale `release.txt` workaround copy
- Feature 6: Windows installer (first step, no bundled FFmpeg) — PyInstaller spec, Inno Setup script, CI build workflow, VS Code task, robust FFmpeg resolution with install-guidance error
- Feature 8: cleanup project structure — `libs/` → `src/` (+ `__init__.py`), `ui.py` moved into `src/`, `ui-text/` → `localization/`
- Feature 7: The internal log will be replaced by a log file, plus a button that shows it when an operation fails.
- Feature 9: UX – Move split result status below action button
