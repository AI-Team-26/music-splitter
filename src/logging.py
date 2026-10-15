import logging
from src import get_data_dir

LOG_FILE = str(get_data_dir() / "music_splitter.log")

_logger = logging.getLogger("music_splitter")

def setup_logger():
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        ))

    _logger.handlers = [handler]
    _logger.setLevel(logging.INFO)
    _logger.propagate = False

def read_logs():
    try:
        with open(LOG_FILE, encoding="utf-8") as f:
            return f.read()
    except OSError as err:
        return f"Failed to read log file. {err}"

def log_info(msg):
    _logger.info(msg)

def log_warning(msg, *args):
    _logger.warning(msg, *args)

def log_error(msg, *args):
    _logger.error(msg, *args)
