# Shared logger name and log path so UI and library write to one place.
import logging
from src import get_data_dir

LOG_FILE = str(get_data_dir() / "music_splitter.log")

logger = logging.getLogger("music_splitter")

def setup_logging():
    """Point the shared 'music_splitter' logger at LOG_FILE (append mode).

    Safe to call repeatedly: handlers are replaced, never stacked.
    """
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    ))
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False

def read_logs():
    try:
        with open(LOG_FILE, encoding="utf-8") as f:
            return f.read()
    except OSError as err:
        return f"Failed to read log file. ${err}"    

def log_info(msg):
    logger.info(msg)

def log_warning(msg):
    logger.warning(msg)

def log_error(msg):
    logger.error(msg)
