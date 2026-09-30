# Changelog

## 2026-09-30
- Feature 13: modernized the Tkinter UI. The window applies a `ttkthemes` theme (`plastik` light / `equilux` dark) before widget creation, falling back to default Tkinter with a status-bar warning when `ttkthemes` is missing. Custom `ttk.Style` configuration for buttons (Arial 10, padding), the big green SPLIT button (`#4CAF50`, muted when disabled) and the status bar frame; browse/naming/part-length/status rows moved from `pack()` to `grid()`. New 16×16 Pillow icons on the Browse and SPLIT buttons (`assets/browse_icon.png`, `assets/split_icon.png`). A Dark Mode checkbox toggles the theme live and persists the choice in `config.json` (per-user data dir). Added `ttkthemes>=3.2.0` and `Pillow>=10.0.0` to requirements.
- Feature 14: fixed the *Build Windows Installer* workflow — the old step downloaded a non-existent `innosetup-6.5.zip` from GitHub releases; Inno Setup is now installed via Chocolatey (`choco install innosetup`) and ISCC invoked from its standard path. Removed the stale `release.txt` workaround copy of the workflow.
- Bug 11: log file and settings no longer live in the install directory. Installed apps under `C:\Program Files\Music Splitter\` are read-only for regular users, so startup crashed with `PermissionError` while opening `music_splitter.log` (and saving `settings.txt` silently failed). Runtime data now goes to a per-user writable location resolved by the `platformdirs` package (`%APPDATA%\MusicSplitter` on Windows, `~/.local/share/Music Splitter` on Linux) via new `get_data_dir()` in `src/splitter.py`; `LOG_FILE` and `SETTINGS_FILE` both derive from it (+ tests).

## 2026-09-29
- Feature 6: Windows installer pipeline (first step, without bundled FFmpeg). Added `music_splitter.spec` (PyInstaller onedir, windowed, app icon, bundles `localization/english.yml`), Inno Setup script `installer/music_splitter.iss` (`{autoprogfiles}` install dir, Start Menu + optional desktop shortcuts, uninstaller), a *Build Windows Installer* GitHub workflow (windows-latest: PyInstaller → ISCC, uploads the setup exe as an artifact), and a "📦 Build Windows Installer" VS Code task. `src/splitter.py` now resolves resources via `sys._MEIPASS` when frozen, and `_find_ffmpeg()` raises a user-facing error with install guidance when FFmpeg is not on PATH (+ tests).

## 2026-09-28
- Feature 8 (project cleanup): renamed `libs/` → `src/` (now a proper package with `__init__.py`) and moved `ui.py` into `src/`; only `main.py` remains at the repo root alongside `tests/`. Renamed `ui-text/` → `localization/`. All imports, path references and doc links updated.

## 2026-09-27
- Feature 10: the app now has its own icon. `assets/icon.ico` (16/32/48 px, used via `iconbitmap` on Windows) and `assets/icon.png` (64×64, `PhotoImage` fallback on other platforms); applied in `create_main_window`.

## 2026-09-22
- Feature 7: the internal in-memory log is now a real log file (`music_splitter.log`, appended, timestamped `[YYYY-MM-DDTHH:MM:SS] LEVEL message`). Splitter warnings (provenance config fallbacks, metadata copy failures) are written to the same file instead of `print()`. A **Show log…** button appears below SPLIT whenever a split operation fails; clicking it opens a read-only viewer with the current log contents.
- Fixed `test_default_output_folder`: paths are now built with `os.path.join`/`abspath` instead of hardcoded POSIX strings, so the test passes on Windows too.
- Feature 11: split parts are now named `part_01.mp3` / `<source_stem>_part_01.mp3` instead of `01.mp3` / `<source_stem>_01.mp3`; radio button examples updated accordingly.
- Feature 10: every split part now carries a provenance COMM tag (`eng`, description "Splitter provenance"). The full frame (language, description, text) is configurable via the `comm:` section of `ui-text/english.yml`; a built-in fallback with a warning covers missing/broken configuration. Duplicate detection keys on the frame identity (language + description): a matching frame from the source is preserved verbatim, even with different text.
- Fixed invalid YAML header in `ui-text/english.yml` (`|>` → `>`).
- Hardened provenance loading: targeted error handling (OSError / YAMLError / malformed shape) instead of a broad silent catch; tests derive expectations from the repo YAML and verify loading against distinct temporary files.
- Feature 8: split parts now carry a track-number frame (`TRCK`, e.g. `2/5`) indicating their position among the generated parts; if the source file already has one, it is copied as-is and never overridden.
- Reworked UI layout: fixed-height message bar on top, Browse row (button + selected file), then *File names* and *Part length* settings, and a big **SPLIT** button disabled until a source file is chosen.
- Removed the "Selected File" frame, the Status Log widget, the Close button and all alert popups; status and errors are shown in the top message bar (errors in red).
- Splitting now runs in a background thread with the UI frozen while running; result reported as "Done: N parts created".
- Logging kept internally (timestamped in-memory list); will later become a log file shown via a button on failure.
- Unified user settings into a single `settings.txt` (KEY=VALUE), replacing the split between `config.txt` and `preferences.json`; removed the stray committed `config.txt`.
- Feature 4: added a "File names" selector (radio buttons): *Numbers* (`01.mp3`) or *File+Numbers* (`<source_stem>_01.mp3`); choice is persisted in `config.txt` (`FILENAME_FORMAT`).
- Added `ID3_tag.md` documenting the ID3v2 tags written to split files; linked from README.
- Feature 1: "Split File" dialog now opens in the last directory used, persisted across app runs via `preferences.json`.

## 2026-09-21
- Added "File names" option (radio buttons): *Numbers* (`01.mp3`) or *File+Numbers* (`<source_stem>_01.mp3`); choice persisted in `config.txt`.
- Part length is now user-selectable via radio buttons: **5**, **10** or **15 minutes** (default: 10); persisted as `PART_LENGTH_MINUTES`. Removed the obsolete `SPLIT_FIXED_DURATION_MINUTES` setting.
- Split output now goes into a folder named after the source file (e.g., `My Mix.mp3` → `My Mix/01.mp3`, …), created next to the source file.
- Removed the obsolete `OUTPUT_FOLDER` setting from `config.txt`.
- Replaced unmaintained `pydub` with direct FFmpeg stream-copy (`-c copy`) splitting: fixes `audioop` ModuleNotFoundError on Python ≥3.13 and SyntaxWarning noise; splitting is now lossless (no re-encode).
- Removed `pydub` from requirements; FFmpeg is now used directly.
- Made split test robust to MP3 duration estimation padding.

## 2026-07-06
- Implement Core MP3 Splitting Engine.
- Added unit tests for the splitter module.
- Fixed test clarity and TODO casing.

## 2026-07-05
- Implemented modern UI using `tkinter.ttk`.
- Improved Layout (Header, Selected File Display, Status/Log Area).
- Integrated File Selection and Split trigger.
- Enhanced error handling and user feedback.
