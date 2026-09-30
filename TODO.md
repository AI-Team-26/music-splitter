# TODO

## Backlog

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

- Feature 10 (investigation/POC): Smart segment post-processing — merge short (<5min), split long (>15min) segments after fixed-duration split. Optional onset-snap refinement. See `Feature_10.md` for details.

- Feature 15 | UI dark mode default set as OS
  """
  import winreg

  def is_dark_mode_windows():
      try:
          with winreg.OpenKey(
              winreg.HKEY_CURRENT_USER,
              r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
          ) as key:
              value = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
              return value == 0  # 0 = dark mode, 1 = light mode
      except Exception:
          return False
  """

## Done (last 20 teaks)

- Feature 13: modernized Tkinter UI — `ttkthemes` plastik/equilux theming with graceful fallback warning, custom ttk styling (buttons, SPLIT green #4CAF50, status bar frame), grid layout for browse/naming/part-length/status areas, Pillow icons on Browse/SPLIT buttons (`assets/browse_icon.png`, `assets/split_icon.png`), dark-mode toggle persisted to `config.json`
- Feature 14: fixed `release.yml` Inno Setup install — replaced the broken `innosetup-6.5.zip` GitHub-release download with Chocolatey (`choco install innosetup`), verified green on CI; removed the now-stale `release.txt` workaround copy
- Feature 6: Windows installer (first step, no bundled FFmpeg) — PyInstaller spec, Inno Setup script, CI build workflow, VS Code task, robust FFmpeg resolution with install-guidance error
- Feature 8: cleanup project structure — `libs/` → `src/` (+ `__init__.py`), `ui.py` moved into `src/`, `ui-text/` → `localization/`
- Feature 7: The internal log will be replaced by a log file, plus a button that shows it when an operation fails.
- Feature 9: UX – Move split result status below action button
