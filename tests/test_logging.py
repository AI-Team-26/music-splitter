import os
import tempfile
import unittest
import src.logging


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        # Close handlers before tmpdir cleanup; Windows cannot delete open files.
        self.addCleanup(self._close_handlers)
        self.original_log_file = src.logging.LOG_FILE
        src.logging.LOG_FILE = os.path.join(self.tmpdir.name, "logs.txt")
        self.some_dir = os.path.join(self.tmpdir.name, "music")
        os.makedirs(self.some_dir)

        src.logging.setup_logger()

    @staticmethod
    def _close_handlers():
        log = src.logging._logger
        for h in list(log.handlers):
            h.close()
            log.removeHandler(h)

    def tearDown(self):
        src.logging.LOG_FILE = self.original_log_file

    def test_log_info(self):
            src.logging.log_info("info a")

    def test_log_warning(self):
        src.logging.log_warning("warning a")

    def test_log_error(self):
            src.logging.log_error("error a")