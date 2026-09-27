import os
import struct
import unittest


class TestIconAssets(unittest.TestCase):
    ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

    def test_assets_exist(self):
        for name in ("icon.ico", "icon.png"):
            path = os.path.join(self.ASSET_DIR, name)
            self.assertTrue(os.path.isfile(path), f"missing {name}")

    def test_png_is_valid(self):
        with open(os.path.join(self.ASSET_DIR, "icon.png"), "rb") as f:
            data = f.read()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (64, 64))

    def test_ico_has_expected_sizes(self):
        with open(os.path.join(self.ASSET_DIR, "icon.ico"), "rb") as f:
            data = f.read()
        reserved, typ, count = struct.unpack("<HHH", data[:6])
        self.assertEqual((reserved, typ), (0, 1))
        sizes = []
        for i in range(count):
            w, h = struct.unpack("<BB", data[6 + i * 16 : 8 + i * 16])
            sizes.append(w if w != 0 else 256)
        self.assertEqual(sorted(sizes), [16, 32, 48])

    def test_ui_wires_icon(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "ui.py")) as f:
            source = f.read()
        self.assertIn("apply_window_icon(root)", source)
        self.assertIn("iconbitmap", source)
        self.assertIn("PhotoImage", source)


if __name__ == "__main__":
    unittest.main()
