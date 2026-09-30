import unittest
from pathlib import Path

from src.splitter import LOG_FILE, get_data_dir


class TestRuntimeDataPaths(unittest.TestCase):
    """Log and settings must live in a per-user writable directory, never in
    the (read-only) install directory."""

    def test_data_dir_exists_and_is_writable(self):
        data_dir = get_data_dir()
        self.assertTrue(data_dir.is_dir())
        probe = data_dir / ".write_probe"
        try:
            probe.write_text("probe")
        finally:
            probe.unlink(missing_ok=True)

    def test_log_file_is_absolute_and_inside_data_dir(self):
        self.assertTrue(Path(LOG_FILE).is_absolute())
        self.assertEqual(Path(LOG_FILE).resolve().parent, get_data_dir().resolve())


if __name__ == "__main__":
    unittest.main()
