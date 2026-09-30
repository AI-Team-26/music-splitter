import json
import os
import tkinter as tk
from tkinter import ttk

from src.splitter import LOG_FILE, get_data_dir, resource_path

pad = 10 # common padding for UI
pad_xs = 5 
pad_xl = 20

ICON_ICO = resource_path("assets/icon.ico")
ICON_PNG = resource_path("assets/icon.png")
BROWSE_ICON = resource_path("assets/browse_icon.png")
SPLIT_ICON = resource_path("assets/split_icon.png")

LIGHT_THEME = "plastik"
DARK_THEME = "equilux"
THEME_CONFIG_FILE = str(get_data_dir() / "config.json")


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


def _load_theme_pref():
    try:
        with open(THEME_CONFIG_FILE, encoding="utf-8") as f:
            return bool(json.load(f).get("dark_mode", False))
    except (OSError, ValueError):
        return False


def _save_theme_pref(dark):
    data = {}
    try:
        with open(THEME_CONFIG_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        pass
    data["dark_mode"] = dark
    try:
        with open(THEME_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except OSError:
        pass


def _button_image(root, path):
    """Load a button icon via Pillow; None if unavailable or missing.

    master is passed explicitly because ImageTk otherwise caches its own
    (possibly destroyed) default root.
    """
    try:
        from PIL import Image, ImageTk
        img = Image.open(path).resize((16, 16))
        return ImageTk.PhotoImage(img, master=root)
    except Exception:
        return None


def create_main_window(root, browse_file, split_file, filename_format="numbers",
                       initial_part_length_m=10):
    themed = True
    try:
        from ttkthemes import ThemedStyle
        style = ThemedStyle(root)
    except ImportError:
        themed = False
        style = ttk.Style()

    dark_mode = _load_theme_pref()
    if themed:
        style.set_theme(DARK_THEME if dark_mode else LIGHT_THEME)

    style.configure("TButton", font=("Arial", 10), padding=10)
    style.configure("Big.TButton", font=("Arial", 14, "bold"),
                    background="#4CAF50", foreground="white")
    style.map("Big.TButton",
              background=[("disabled", "#a5d6a7")],
              foreground=[("disabled", "gray")])
    style.configure("Status.TFrame", background="#f0f0f0")

    root.title("Music Splitter")
    root.geometry("520x400")
    apply_window_icon(root)

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.grid_columnconfigure(0, weight=1)

    # Title label + dark mode toggle on the same row
    title_label = ttk.Label(main_frame, text="Music Splitter", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, pad))

    theme_var = tk.BooleanVar(value=dark_mode)
    if themed:
        def toggle_theme():
            style.set_theme(DARK_THEME if theme_var.get() else LIGHT_THEME)
            _save_theme_pref(theme_var.get())
        dark_check = ttk.Checkbutton(main_frame, text="Dark Mode",
                                     variable=theme_var, command=toggle_theme)
        dark_check.grid(row=0, column=1, sticky=tk.E)

    # Browse row: button + selected file name
    browse_frame = ttk.Frame(main_frame)
    browse_frame.grid(row=1, column=0, sticky="we", pady=(0, pad))

    browse_img = _button_image(root, BROWSE_ICON)
    if browse_img is not None:
        root._browse_img = browse_img  # keep a reference so Tk doesn't free it
    browse_button = ttk.Button(browse_frame, text="Browse…", command=browse_file,
                               image=browse_img, compound=tk.LEFT)
    browse_button.pack(side=tk.LEFT)

    file_var = tk.StringVar(value="No file selected")
    file_label = ttk.Label(browse_frame, textvariable=file_var, foreground="gray")
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
    split_button = ttk.Button(
        main_frame, text="SPLIT", style="Big.TButton",
        state=tk.DISABLED, command=split_file,
        image=split_img, compound=tk.LEFT,
    )
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
        content = ""
        try:
            with open(LOG_FILE, encoding="utf-8") as f:
                content = f.read()
        except OSError:
            pass
        text.insert(tk.END, content or "(no log available yet)")
        text.config(state=tk.DISABLED)

    log_button = ttk.Button(main_frame, text="Show log…", command=show_log_viewer)

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
            file_label.config(foreground="gray")

    _COLORS = {"error": "red", "success": "green"}

    def set_message(msg, kind="info"):
        status_var.set(msg)
        status_label.config(foreground=_COLORS.get(kind, ""))

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

    if not themed:
        set_message("Warning: ttkthemes not installed. Using default theme.")

    return (update_file_label, set_message, set_enabled,
            get_filename_format, get_part_length_m, set_log_button_visible)
