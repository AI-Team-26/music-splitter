# TODO

## Backlog

- Feature 13 | **Modernize Tkinter UI with `ttkthemes` and Custom Styling**  
  
  **Goal**: Replace the default Tkinter look with a modern theme and improve visual consistency.

  ---
  ### **Requirements**
  1. **Integrate `ttkthemes`**:
     - Install the library: `pip install ttkthemes>=3.2.0`.
     - Apply a modern theme (e.g., `"plastik"`, `"clam"`, or `"equilux"` for dark mode) **before** creating any widgets.
     - Example:
       ```python
       from ttkthemes import ThemedStyle
       style = ThemedStyle(root)
       style.set_theme("plastik")
       ```

  2. **Custom Styling**:
     - Use `ttk.Style()` to customize:
       - **Buttons**: Font (`Arial 10`), padding (`10px`), and colors (e.g., `#4CAF50` for the "SPLIT" button).
       - **Labels**: Font (`Arial 10`), foreground color for disabled/active states.
       - **Frames**: Padding and background colors (e.g., `#f0f0f0` for the status bar).
     - Example:
       ```python
       style.configure("TButton", font=("Arial", 10), padding=10)
       style.configure("Big.TButton", font=("Arial", 14, "bold"), background="#4CAF50", foreground="white")
       style.configure("Status.TFrame", background="#f0f0f0")
       ```

  3. **Layout Improvements**:
     - Replace `pack()` with `grid()` for the following widgets:
       - `browse_frame`, `naming_frame`, `part_len_frame`, and `status_bar`.
     - Ensure widgets **expand to fill available space** and maintain consistent padding (`padx=10`, `pady=5`).
     - Example:
       ```python
       browse_frame.grid(column=0, row=0, sticky=tk.W, pady=5)
       naming_frame.grid(column=0, row=1, sticky=tk.W+tk.E, pady=5)
       root.grid_columnconfigure(0, weight=1)
       ```

  4. **Add Icons**:
     - Use `Pillow` to load and display icons for the "Browse" and "SPLIT" buttons.
     - Icons should be `16x16` pixels and placed in the `assets/` directory (`browse_icon.png`, `split_icon.png`).
     - Example:
       ```python
       from PIL import Image, ImageTk
       browse_icon = ImageTk.PhotoImage(Image.open("assets/browse_icon.png").resize((16, 16)))
       browse_button.config(image=browse_icon, compound=tk.LEFT)
       ```

  5. **Dark Mode Toggle (Stretch Goal)**:
     - Add a checkbox to toggle between light (`"plastik"`) and dark (`"equilux"`) themes.
     - Persist the theme preference in a `config.json` file.
     - Example:
       ```python
       theme_var = tk.StringVar(value="plastik")
       ttk.Checkbutton(main_frame, text="Dark Mode", command=lambda: style.set_theme("equilux" if theme_var.get() else "plastik"))
       ```

  6. **Error Handling**:
     - If `ttkthemes` is not installed, fall back to default Tkinter and show a warning in the status bar:
       `"Warning: ttkthemes not installed. Using default theme."`.

  ---
  ### **Dependencies**
  - Add to `requirements.txt`:
    ```
    ttkthemes>=3.2.0
    Pillow>=10.0.0
    ```

  ---
  ### **Files to Modify**
  - `src/ui.py` (or the file containing `create_main_window`).
  - `assets/browse_icon.png` (create if missing).
  - `assets/split_icon.png` (create if missing).

  ---
  ### **Acceptance Criteria**
  - [ ] Modern theme applied via `ttkthemes`.
  - [ ] Custom styling for all `ttk` widgets (buttons, labels, frames).
  - [ ] Icons added to "Browse" and "SPLIT" buttons.
  - [ ] Layout uses `grid()` and expands to fill available space.
  - [ ] Fallback to default Tkinter with a warning if `ttkthemes` is missing.
  - [ ] *(Stretch)* Dark/light theme toggle works and persists.

  ---
  ### **Out of Scope**
  - Functional changes to the splitting logic.
  - Migration to PyQt/CustomTkinter.


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
