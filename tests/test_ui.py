import json
import os
import tempfile
import unittest
import tkinter as tk
from tkinter import ttk

import src.ui as uimod
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
        import src.logging as logging_mod
        with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as f:
            f.write("[2026-09-22T10:00:00] INFO Starting split process\n"
                    "[2026-09-22T10:00:05] ERROR Error during split: boom\n")
            log_path = f.name
        self.addCleanup(os.unlink, log_path)
        original_log_file = logging_mod.LOG_FILE
        logging_mod.LOG_FILE = log_path
        self.addCleanup(setattr, logging_mod, "LOG_FILE", original_log_file)
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

    @staticmethod
    def _status_bg(root):
        # The status bar is themed through its Style (ttk.Frame has no -bg option).
        return str(ttk.Style(root).lookup("Status.TFrame", "background"))

    def _build_with_theme_pref(self, dark):
        cfg = os.path.join(tempfile.mkdtemp(), "config.json")
        with open(cfg, "w", encoding="utf-8") as f:
            json.dump({"dark_mode": dark}, f)
        original = uimod.CONFIG_FILE
        uimod.CONFIG_FILE = cfg
        self.addCleanup(setattr, uimod, "CONFIG_FILE", original)
        root = tk.Tk()
        root.withdraw()
        self.addCleanup(root.destroy)
        create_main_window(root, lambda: None, lambda: None)
        return root

    def test_status_bar_follows_dark_theme(self):
        # Bug 18: the panel under SPLIT must not stay a fixed light grey in dark mode.
        root = self._build_with_theme_pref(dark=True)
        self.assertEqual(self._status_bg(root), uimod.DARK_STATUS_BG)

    def test_status_bar_follows_light_theme(self):
        root = self._build_with_theme_pref(dark=False)
        self.assertEqual(self._status_bg(root), uimod.LIGHT_STATUS_BG)

    @staticmethod
    def _theme_toggle_button(root):
        # Feature 16: the theme switch is an icon-only button (no text).
        return next(b for b in TestMainWindow._collect(root, ttk.Button, [])
                    if str(b.cget("text")) == "")

    def test_theme_toggle_is_icon_button_not_checkbox(self):
        root = self._build_with_theme_pref(dark=False)
        checkboxes = self._collect(root, tk.Checkbutton, []) + \
                     self._collect(root, ttk.Checkbutton, [])
        self.assertEqual(checkboxes, [])
        toggle = self._theme_toggle_button(root)
        self.assertNotEqual(str(toggle.cget("image")), "")

    def test_theme_toggle_switches_theme_and_persists(self):
        cfg = os.path.join(tempfile.mkdtemp(), "config.json")
        with open(cfg, "w", encoding="utf-8") as f:
            json.dump({"dark_mode": False}, f)
        original = uimod.CONFIG_FILE
        uimod.CONFIG_FILE = cfg
        self.addCleanup(setattr, uimod, "CONFIG_FILE", original)
        root = tk.Tk()
        root.withdraw()
        self.addCleanup(root.destroy)
        create_main_window(root, lambda: None, lambda: None)
        toggle = self._theme_toggle_button(root)
        toggle.invoke()
        self.assertEqual(self._status_bg(root), uimod.DARK_STATUS_BG)
        with open(cfg, encoding="utf-8") as f:
            self.assertTrue(json.load(f)["dark_mode"])
        toggle.invoke()  # and back to light
        self.assertEqual(self._status_bg(root), uimod.LIGHT_STATUS_BG)


if __name__ == "__main__":
    unittest.main()
