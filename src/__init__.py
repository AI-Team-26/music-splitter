from pathlib import Path
from platformdirs import user_data_dir

def get_data_dir() -> Path:
    """Per-user writable directory for runtime data (log, settings).

    Installed apps live in Program Files which is read-only for regular
    users, so all mutable files must go elsewhere (platformdirs picks the
    per-OS convention, e.g. %APPDATA%\\MusicSplitter on Windows).
    """
    base = Path(user_data_dir(appname="Music Splitter", appauthor=False))
    base.mkdir(parents=True, exist_ok=True)
    return base

