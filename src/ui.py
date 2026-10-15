import json
import os
import sys
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

from src import get_data_dir
from src.logging import log_error, log_warning, read_logs
from src.splitter import resource_path
from src.theme import (
    BIG_BUTTON_BG,
    BIG_BUTTON_DISABLED_BG,
    BIG_BUTTON_DISABLED_FG,
    BIG_BUTTON_FG,
    LIGHT_THEME,
    LIGHT_STATUS_BG,
    DARK_THEME,
    DARK_STATUS_BG,
    FILE_LABEL_DEFAULT_FG,
    MSG_ERROR,
    MSG_SUCCESS,
    status_bg,
)

pad = 10
pad_xs = 5
pad_xl = 20

ICON_ICO = resource_path("assets/icon.ico")
ICON_PNG = resource_path("assets/icon.png")
BROWSE_ICON = resource_path("assets/browse_icon.png")
SPLIT_ICON = resource_path("assets/split_icon.png")

CONFIG_FILE = str(get_data_dir() / "config.json")


def apply_window_icon(root):
    """Set the window/taskbar icon; .ico on Windows, PNG fallback elsewhere.

    Cosmetic only: never let an icon failure break window creation.
    """
    try:
        root.iconbitmap(ICON_ICO)
        return
    except tk.TclError:
        pass
    try:
        icon_img = tk.PhotoImage(file=ICON_PNG)
        root._icon_img = icon_img  # keep a reference so Tk doesn't free it
        root.iconphoto(True, icon_img)
    except tk.TclError:
        pass


def is_system_theme_dark() -> bool:
    """Return True if the Windows system theme is set to dark mode."""
    try:
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0  # 0 = dark, 1 = light
    except Exception as err:
        log_warning(
            "Could not read Windows system theme (%s); defaulting to light.", err
        )
        return False


def _load_theme_pref():
    """Load saved theme preference. Returns None if no explicit choice was made."""
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            data = json.load(f)
            if "dark_mode" in data:
                return bool(data["dark_mode"])
    except (OSError, ValueError) as err:
        log_warning("Could not read theme config (%s); using default.", err)
    return None


def _save_theme_pref(dark):
    data = {}
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as err:
        log_warning("Could not read existing config before saving (%s).", err)
    data["dark_mode"] = dark
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except OSError as err:
        log_error("Failed to save theme preference (%s).", err)


def _button_image(root, path):
    """Load button icon via Pillow; None if unavailable or missing."""
    try:
        from PIL import Image, ImageTk
        img = Image.open(path).resize((16, 16))
        return ImageTk.PhotoImage(img, master=root)
    except Exception:
        return None


def set_titlebar_dark(root, dark):
    """Ask Windows to draw the title bar in dark or light mode (no-op elsewhere)."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        root.update_idletasks()  # make sure the native window exists
        user32 = ctypes.windll.user32
        hwnd = user32.GetParent(root.winfo_id()) or root.winfo_id()
        value = ctypes.c_int(1 if dark else 0)
        # Attribute 20 on Win10 20H1+/Win11; 19 on older Win10 builds.
        for attr in (20, 19):
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, attr, ctypes.byref(value), ctypes.sizeof(value)
            ) == 0:
                break
        # Force the non-client area (title bar) to repaint.
        # SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED = 0x27
        user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x27)
    except Exception as err:
        log_warning("Could not set title bar theme (%s).", err)


def create_main_window(root, browse_file, split_file, filename_format="numbers",
                       initial_part_length_m=10):
    """Create and configure the main application window.

    Theme priority: saved user preference > Windows system theme.
    If no explicit preference exists, follow the OS setting.
    """

    style = ThemedStyle(root)

    pref = _load_theme_pref()
    is_dark_mode = pref if pref is not None else is_system_theme_dark()
    style.set_theme(DARK_THEME if is_dark_mode else LIGHT_THEME)

    style.configure("TButton", font=("Arial", 10), padding=10)
    style.configure("Big.TButton", font=("Arial", 14, "bold"),
                    background=BIG_BUTTON_BG, foreground=BIG_BUTTON_FG)
    style.map("Big.TButton",
              background=[("disabled", BIG_BUTTON_DISABLED_BG)],
              foreground=[("disabled", BIG_BUTTON_DISABLED_FG)])
    # ttk.Frame has no -background option here, so theme it through the Style.
    style.configure("Status.TFrame", background=status_bg(is_dark_mode))

    root.title("Music Splitter")
    root.geometry("520x400")
    # Ensure the root window itself adopts the current theme's background.
    # This fixes the issue where the window frame stayed light in dark mode.
    if is_dark_mode:
        root.config(background=DARK_STATUS_BG)
    else:
        root.config(background=LIGHT_STATUS_BG)
    apply_window_icon(root)
    set_titlebar_dark(root, is_dark_mode)

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.grid_columnconfigure(0, weight=1)

    # Title label
    title_label = ttk.Label(main_frame, text="Music Splitter", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, pad))

    is_dark_mode_var = tk.BooleanVar(value=is_dark_mode)

    def toggle_theme():
        dark = is_dark_mode_var.get()
        style.set_theme(DARK_THEME if dark else LIGHT_THEME)
        # Refresh the root window background to match the new theme.
        root.config(background=DARK_STATUS_BG if dark else LIGHT_STATUS_BG)
        style.configure("Status.TFrame",
                        background=status_bg(dark))
        set_titlebar_dark(root, dark)
        _save_theme_pref(dark)

    dark_check = ttk.Checkbutton(main_frame, text="Dark Mode", variable=is_dark_mode_var, command=toggle_theme)
    dark_check.grid(row=0, column=1, sticky=tk.E)
    # Browse row: button + selected file name
    browse_frame = ttk.Frame(main_frame)
    browse_frame.grid(row=1, column=0, sticky="we", pady=(0, pad))

    browse_img = _button_image(root, BROWSE_ICON)
    if browse_img is not None:
        root._browse_img = browse_img  # keep a reference so Tk doesn't free it
    browse_button = ttk.Button(browse_frame, text="Browse...", command=browse_file,
                               image=browse_img, compound=tk.LEFT)
    browse_button.pack(side=tk.LEFT)

    file_var = tk.StringVar(value="No file selected")
    file_label = ttk.Label(browse_frame, textvariable=file_var,
                           foreground=FILE_LABEL_DEFAULT_FG)
    file_label.pack(side=tk.LEFT, padx=(pad_xs * 2, 0))

    # File names format selector
    naming_frame = ttk.LabelFrame(main_frame, text="File names", padding="10")
    naming_frame.grid(row=2, column=0, sticky="we", pady=(0, pad))

    naming_var = tk.StringVar(value=filename_format)
    ttk.Radiobutton(
        naming_frame, text="Numbers (\u201cpart_01.mp3\u201d)",
        variable=naming_var, value="numbers",
    ).pack(side=tk.LEFT, padx=(0, pad_xl))
    ttk.Radiobutton(
        naming_frame, text="File+Numbers (\u201cDJ-AAA_part_01.mp3\u201d)",
        variable=naming_var, value="file+numbers",
    ).pack(side=tk.LEFT)

    # Part length selection (minutes: 5 / 10 / 15)
    part_len_var = tk.StringVar(value=str(initial_part_length_m))
    part_len_frame = ttk.LabelFrame(main_frame, text="Part length", padding="10")
    part_len_frame.grid(row=3, column=0, sticky="we", pady=(0, pad))

    for minutes in ("5", "10", "15"):
        ttk.Radiobutton(
            part_len_frame, text=f"{minutes} min",
            variable=part_len_var, value=minutes,
        ).pack(side=tk.LEFT, padx=(0, pad_xl))

    # Big SPLIT button, disabled until a source file is selected
    split_img = _button_image(root, SPLIT_ICON)
    if split_img is not None:
        root._split_img = split_img
    split_button = ttk.Button(main_frame, text="SPLIT", style="Big.TButton",
                              state=tk.DISABLED, command=split_file,
                              image=split_img, compound=tk.LEFT)
    split_button.grid(row=4, column=0, sticky="we", pady=(pad, 0))

    # Status area: fixed height directly below the Split button
    status_bar = ttk.Frame(main_frame, style="Status.TFrame", height=28)
    status_bar.grid(row=5, column=0, sticky="we", pady=(pad_xs, 0))
    status_bar.pack_propagate(False)
    status_var = tk.StringVar(value="")
    status_label = ttk.Label(status_bar, textvariable=status_var, anchor=tk.W)
    status_label.pack(side=tk.LEFT, fill=tk.X)

    # Log viewer button: hidden until an operation fails
    def show_log_viewer():
        win = tk.Toplevel(root)
        win.title("Music Splitter Log")
        win.geometry("560x320")
        text = tk.Text(win, wrap=tk.NONE)
        scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(fill=tk.BOTH, expand=True)
        logs = read_logs()
        text.insert(tk.END, logs or "(no log available yet)")
        text.config(state=tk.DISABLED)

    log_button = ttk.Button(main_frame, text="Show log...", command=show_log_viewer)

    def set_log_button_visible(visible):
        if visible:
            log_button.grid(row=6, column=0, sticky="we", pady=(pad, 0))
        else:
            log_button.grid_remove()

    def update_file_label(path):
        if path:
            file_var.set(os.path.basename(path))
            file_label.config(foreground="")
        else:
            file_var.set("No file selected")
            file_label.config(foreground=FILE_LABEL_DEFAULT_FG)

    _MSG_COLORS = {"error": MSG_ERROR, "success": MSG_SUCCESS}

    def set_message(msg, kind="info"):
        status_var.set(msg)
        status_label.config(foreground=_MSG_COLORS.get(kind, ""))

    def set_enabled(enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        browse_button.config(state=state)
        split_button.config(state=state)
        for frame in (naming_frame, part_len_frame):
            for child in frame.winfo_children():
                if isinstance(child, ttk.Radiobutton):
                    child.config(state=state)

    def get_filename_format():
        return naming_var.get()

    def get_part_length_m():
        return int(part_len_var.get())

    return (update_file_label, set_message, set_enabled,
            get_filename_format, get_part_length_m, set_log_button_visible)
