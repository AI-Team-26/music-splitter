"""Centralized theme constants for Music Splitter UI."""

# ttkthemes theme names
LIGHT_THEME = "plastik"
DARK_THEME = "equilux"

# Status bar backgrounds must match the surrounding themed frame surface
LIGHT_STATUS_BG = "#f0f0f0"   # plastik light surface
DARK_STATUS_BG = "#464646"    # equilux frame surface (-bg)

# SPLIT button (Big.TButton)
BIG_BUTTON_BG = "#4CAF50"
BIG_BUTTON_FG = "white"
BIG_BUTTON_DISABLED_BG = "#a0a0a0"
BIG_BUTTON_DISABLED_FG = "gray"

# Per-widget palettes keyed by mode. Tuned so buttons read as raised against
# the frame surface and label text keeps enough contrast in both themes.
_PALETTES = {
    False: {  # light (plastik)
        "text": "#1e1e1e",
        "btn_face": "#d9d9d9",
        "btn_light_edge": "#ffffff",   # top/left highlight
        "btn_dark_edge": "#a8a8a8",    # bottom/right shadow
        "btn_border": "#8f8f8f",
        "file_hint": "#7a7a7a",
        "msg_error": "#c62828",
        "msg_success": "#2e7d32",
    },
    True: {   # dark (equilux)
        "text": "#f2f2f2",
        "btn_face": "#5a5a5a",
        "btn_light_edge": "#7d7d7d",
        "btn_dark_edge": "#2e2e2e",
        "btn_border": "#242424",
        "file_hint": "#bdbdbd",
        "msg_error": "#ff6b6b",
        "msg_success": "#7ee08a",
    },
}


def status_bg(is_dark: bool) -> str:
    """Return the status bar background color for the given mode."""
    return DARK_STATUS_BG if is_dark else LIGHT_STATUS_BG


def widget_palette(is_dark: bool) -> dict:
    """Return the per-widget color map for the given theme mode."""
    return _PALETTES[is_dark]
