# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Music Splitter (onedir build, consumed by Inno Setup).

Build with:  pyinstaller music_splitter.spec
Output lands in dist/MusicSplitter/, which installer/music_splitter.iss packages.
"""
import os

ROOT = os.path.abspath(os.path.dirname(SPEC))

a = Analysis(
    [os.path.join(ROOT, 'main.py')],
    pathex=[ROOT],
    binaries=[],
    datas=[(os.path.join(ROOT, 'localization'), 'localization')],
    hiddenimports=['src', 'src.splitter', 'src.ui'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MusicSplitter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,          # windowed app, no console window
    icon=os.path.join(ROOT, 'assets', 'icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='MusicSplitter',
)
