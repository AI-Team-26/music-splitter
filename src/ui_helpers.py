"""Reusable Tkinter/ttk helpers shared by the Music Splitter UI."""

import tkinter as tk
from tkinter import ttk

from src.logging import log_warning


def create_ttk_button(parent, text, command, image=None, compound=None, style=None, state=None):
    """Create ttk.Button safely: only pass image when it is not None."""
    kwargs = {"text": text, "command": command}
    if image is not None:
        kwargs["image"] = image
    if compound is not None:
        kwargs["compound"] = compound
    if style is not None:
        kwargs["style"] = style
    if state is not None:
        kwargs["state"] = state
    return ttk.Button(parent, **kwargs)


DEFAULT_ICON_PX = 24
SMALL_ICON_PX = 16

_ICON_SIZES = {
    "default": (DEFAULT_ICON_PX, DEFAULT_ICON_PX),
    "small": (SMALL_ICON_PX, SMALL_ICON_PX),
}


def button_image(root, path, size="default"):
    """Load button icon via Pillow; None if unavailable or missing.

    size: "default" (24x24), "small" (16x16), an int for a square,
    or a (width, height) tuple.
    """
    try:
        from PIL import Image, ImageTk
        if isinstance(size, str):
            dims = _ICON_SIZES[size]
        elif isinstance(size, int):
            dims = (size, size)
        else:
            dims = tuple(size)
        img = Image.open(path).resize(dims)
        return ImageTk.PhotoImage(img, master=root)
    except Exception as err:
        # Missing Pillow/asset must degrade gracefully (text-only button),
        # but stay visible in the log instead of failing silently.
        log_warning("Could not load icon %s (%s); continuing without image.", path, err)
        return None


def attach_tooltip(widget, text, delay_ms=500):
    """Attach a basic hover tooltip (Tkinter has none natively)."""
    tip = None
    timer = None

    def show():
        nonlocal tip, timer
        timer = None
        if tip is not None:
            return
        x = widget.winfo_rootx() + 20
        y = widget.winfo_rooty() + widget.winfo_height() + 4
        # Master the main window (not the widget) so the tooltip stays a direct
        # child of it and is destroyed together with the app.
        tip = tk.Toplevel(widget.winfo_toplevel())
        tip.wm_overrideredirect(True)
        tip.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(tip, text=text, background="#ffffe0", foreground="#1e1e1e",
                       relief=tk.SOLID, borderwidth=1, font=("Arial", 9))
        lbl.pack()

    def on_enter(_event):
        nonlocal timer
        if timer is not None:
            widget.after_cancel(timer)
        timer = widget.after(delay_ms, show)

    def on_leave(_event):
        nonlocal tip, timer
        if timer is not None:
            widget.after_cancel(timer)
            timer = None
        if tip is not None:
            tip.destroy()
            tip = None

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)
