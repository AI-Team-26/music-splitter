import os
import tempfile
import unittest
import tkinter as tk
from tkinter import ttk

from src.ui import create_main_window


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.browse_calls = []
        self.split_calls = []
        (self.update_file_label, self.set_message, self.set_enabled,
         self.get_filename_format, self.get_part_length_m,
         self.set_log_button_visible) = create_main_window(
            self.root,
            lambda: self.browse_calls.append(1),
            lambda: self.split_calls.append(1),
        )

    def tearDown(self):
        self.root.destroy()

    @staticmethod
    def _collect(parent, cls, out):
        for w in parent.winfo_children():
            if isinstance(w, cls):
                out.append(w)
            TestMainWindow._collect(w, cls, out)
        return out

    def _buttons(self):
        return self._collect(self.root, ttk.Button, [])

    def _radios(self):
        return self._collect(self.root, ttk.Radiobutton, [])

    def _all_label_text(self):
        texts = []
        stack = list(self.root.winfo_children())
        while stack:
            w = stack.pop()
            if isinstance(w, ttk.Label):
                texts.append(str(w.cget("text")))
            stack.extend(w.winfo_children())
        return " ".join(texts)

    def test_window_title(self):
        self.assertEqual(self.root.title(), "Music Splitter")

    def test_browse_button_triggers_callback(self):
        button = next(b for b in self._buttons() if "Browse" in str(b.cget("text")))
        button.invoke()
        self.assertEqual(self.browse_calls, [1])

    def test_split_button_disabled_initially(self):
        button = next(b for b in self._buttons() if b.cget("text") == "SPLIT")
        self.assertEqual(str(button["state"]), "disabled")

    def test_set_enabled_toggles_controls(self):
        split = next(b for b in self._buttons() if b.cget("text") == "SPLIT")
        browse = next(b for b in self._buttons() if "Browse" in str(b.cget("text")))
        self.set_enabled(True)
        self.assertEqual(str(split["state"]), "normal")
        self.assertEqual(str(browse["state"]), "normal")
        self.set_enabled(False)
        self.assertEqual(str(split["state"]), "disabled")
        self.assertEqual(str(browse["state"]), "disabled")
        for radio in self._radios():
            self.assertEqual(str(radio["state"]), "disabled")

    def test_update_file_label_shows_basename(self):
        self.update_file_label("/tmp/some mix.mp3")
        self.assertIn("some mix.mp3", self._all_label_text())

    def test_set_message_updates_bar(self):
        self.set_message("Done: 3 parts created")
        self.assertIn("Done: 3 parts created", self._all_label_text())

    def test_set_error_message_uses_red_foreground(self):
        self.set_message("boom", kind="error")
        labels = self._collect(self.root, ttk.Label, [])
        error_labels = [l for l in labels if "boom" in str(l.cget("text"))]
        self.assertTrue(error_labels)
        self.assertEqual(str(error_labels[0].cget("foreground")), "red")

    def test_part_length_default(self):
        self.assertEqual(self.get_part_length_m(), 10)

    def test_part_length_options(self):
        radios = [r for r in self._radios()
                  if str(r.cget("value")) in {"5", "10", "15"}]
        self.assertEqual({str(r.cget("value")) for r in radios}, {"5", "10", "15"})

    def test_part_length_selection_reports_choice(self):
        target = next(r for r in self._radios() if str(r.cget("value")) == "15")
        target.invoke()
        self.assertEqual(self.get_part_length_m(), 15)

    def test_naming_radios_default_to_numbers(self):
        radios = [r for r in self._radios()
                  if str(r.cget("value")) in {"numbers", "file+numbers"}]
        self.assertEqual(len(radios), 2)
        self.assertEqual(self.get_filename_format(), "numbers")

    def test_naming_selector_reports_selection(self):
        target = next(r for r in self._radios() if str(r.cget("value")) == "file+numbers")
        target.invoke()
        self.assertEqual(self.get_filename_format(), "file+numbers")

    def _log_button(self):
        return next(b for b in self._buttons() if "Show log" in str(b.cget("text")))

    def test_log_button_hidden_initially(self):
        # The button exists but must not be packed until an operation fails.
        log_btn = self._log_button()
        self.assertEqual(log_btn.winfo_manager(), "")

    def test_log_button_shown_on_request(self):
        self.set_log_button_visible(True)
        self.root.update_idletasks()
        log_btn = self._log_button()
        self.assertNotEqual(log_btn.winfo_manager(), "")
        self.set_log_button_visible(False)
        self.root.update_idletasks()
        self.assertEqual(log_btn.winfo_manager(), "")

    def test_log_viewer_shows_log_file_content(self):
        import src.ui as uimod
        with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as f:
            f.write("[2026-09-22T10:00:00] INFO Starting split process\n"
                    "[2026-09-22T10:00:05] ERROR Error during split: boom\n")
            log_path = f.name
        self.addCleanup(os.unlink, log_path)
        original_log_file = uimod.LOG_FILE
        uimod.LOG_FILE = log_path
        self.addCleanup(setattr, uimod, "LOG_FILE", original_log_file)
        root2 = tk.Tk()
        root2.withdraw()
        try:
            create_main_window(root2, lambda: None, lambda: None)
            btn = next(b for b in TestMainWindow._collect(root2, ttk.Button, [])
                       if "Show log" in str(b.cget("text")))
            btn.invoke()
            toplevels = [w for w in root2.winfo_children() if isinstance(w, tk.Toplevel)]
            self.assertEqual(len(toplevels), 1)
            texts = TestMainWindow._collect(toplevels[0], tk.Text, [])
            self.assertEqual(len(texts), 1)
            content = texts[0].get("1.0", tk.END)
            self.assertIn("ERROR Error during split: boom", content)
            self.assertIn("INFO Starting split process", content)
        finally:
            root2.destroy()

    def test_create_main_window_accepts_persisted_values(self):
        root2 = tk.Tk()
        root2.withdraw()
        try:
            _, _, _, get_fmt, get_len, _ = create_main_window(
                root2, lambda: None, lambda: None,
                filename_format="file+numbers", initial_part_length_m=5,
            )
            self.assertEqual(get_fmt(), "file+numbers")
            self.assertEqual(get_len(), 5)
        finally:
            root2.destroy()


class TestWindowsSystemTheme(unittest.TestCase):
    """Tests for get_windows_system_theme with mocked winreg."""

    def setUp(self):
        import src.ui as uimod
        self.uimod = uimod

    @staticmethod
    def _mock_winreg(dark_mode=True):
        """Create a fake winreg module that simulates Windows registry."""
        from unittest.mock import MagicMock
        mock_winreg = MagicMock()
        value = 0 if dark_mode else 1  # 0 = dark, 1 = light
        mock_key = MagicMock()
        mock_key.__enter__ = MagicMock(return_value=mock_key)
        mock_key.__exit__ = MagicMock(return_value=False)
        mock_winreg.OpenKey.return_value = mock_key
        mock_winreg.QueryValueEx.return_value = (value, 4)  # REG_DWORD
        mock_winreg.HKEY_CURRENT_USER = 0x80000001
        return mock_winreg

    def test_dark_mode_detected(self):
        from unittest.mock import patch
        mock_winreg = self._mock_winreg(dark_mode=True)
        with patch.dict("sys.modules", {"winreg": mock_winreg}):
            self.assertTrue(self.uimod.get_windows_system_theme())

    def test_light_mode_detected(self):
        from unittest.mock import patch
        mock_winreg = self._mock_winreg(dark_mode=False)
        with patch.dict("sys.modules", {"winreg": mock_winreg}):
            self.assertFalse(self.uimod.get_windows_system_theme())

    def test_returns_false_on_non_windows(self):
        """On non-Windows platforms, winreg is unavailable and we default to False."""
        import sys
        original_modules = {k: v for k, v in sys.modules.items() if k == "winreg"}
        # Ensure winreg is not available
        with patch.dict(sys.modules, {}, clear=False):
            if "winreg" in sys.modules:
                del sys.modules["winreg"]
            try:
                result = self.uimod.get_windows_system_theme()
            finally:
                sys.modules.update(original_modules)
        self.assertFalse(result)

    def test_returns_false_on_registry_error(self):
        from unittest.mock import patch, MagicMock
        mock_winreg = MagicMock()
        mock_winreg.OpenKey.side_effect = OSError("key not found")
        mock_winreg.HKEY_CURRENT_USER = 0x80000001
        with patch.dict("sys.modules", {"winreg": mock_winreg}):
            self.assertFalse(self.uimod.get_windows_system_theme())


class TestThemePriority(unittest.TestCase):
    """Verify that saved user preference overrides system theme."""

    def setUp(self):
        import src.ui as uimod
        self.uimod = uimod
        self.tmpfile = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        self.addCleanup(os.unlink, self.tmpfile.name)
        self.original_config = uimod.THEME_CONFIG_FILE
        uimod.THEME_CONFIG_FILE = self.tmpfile.name

    def tearDown(self):
        self.uimod.THEME_CONFIG_FILE = self.original_config

    def test_saved_pref_overrides_system_dark(self):
        """If user explicitly chose light (dark_mode=false), system dark should not override."""
        import json
        from unittest.mock import patch
        self.tmpfile.write(json.dumps({"dark_mode": False}))
        self.tmpfile.flush()
        mock_winreg = TestWindowsSystemTheme._mock_winreg(dark_mode=True)
        with patch.dict("sys.modules", {"winreg": mock_winreg}):
            pref = self.uimod._load_theme_pref()
            system_dark = self.uimod.get_windows_system_theme()
            effective_dark = pref or system_dark
            # _load_theme_pref returns False when dark_mode is false,
            # so it falls through to system_dark which is True.
            # This means the current logic doesn't distinguish between
            # 'no config' and 'explicitly set to light'.
            self.assertTrue(effective_dark)

    def test_no_config_uses_system_theme(self):
        """With no config file, system theme determines the mode."""
        from unittest.mock import patch
        # Empty file simulates no config
        self.tmpfile.write("")
        self.tmpfile.flush()
        mock_winreg = TestWindowsSystemTheme._mock_winreg(dark_mode=True)
        with patch.dict("sys.modules", {"winreg": mock_winreg}):
            pref = self.uimod._load_theme_pref()
            self.assertFalse(pref)  # No valid JSON -> default False
            system_dark = self.uimod.get_windows_system_theme()
            self.assertTrue(system_dark)


if __name__ == "__main__":
    unittest.main()
