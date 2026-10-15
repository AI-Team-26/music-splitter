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

# Status message colors
MSG_ERROR = "red"
MSG_SUCCESS = "green"

# File label default foreground (no file selected)
FILE_LABEL_DEFAULT_FG = "gray"


def status_bg(is_dark: bool) -> str:
    """Return the status bar background color for the given mode."""
    return DARK_STATUS_BG if is_dark else LIGHT_STATUS_BG
