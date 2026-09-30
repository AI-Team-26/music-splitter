# Music Splitter

An utility tool designed to split large MP3 audio files into smaller segments based on a specified duration while preserving ID3 metadata (Artist, Album, Title). It ensures that the resulting files are ready for playback on various media players.

[![Build Windows Installer](https://github.com/AI-Team-26/music-splitter/actions/workflows/release.yml/badge.svg)](https://github.com/AI-Team-26/music-splitter/actions/workflows/release.yml)

## Features

- **Automated Splitting**: Segment long MP3 files into equal durations.
- **Metadata Preservation**: Automatically copies ID3 tags (Artist, Album, Title) from the source file to all generated segments.
- **User Interface**: A clean Tkinter-based GUI for easy interaction.
- **Error Handling**: Robust validation for file types and segment durations.

## Prerequisites

This application requires **FFmpeg** to split audio files (lossless stream-copy, no re-encoding).

### Installation of FFmpeg

#### Windows
1. Download the latest build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
2. Extract the archive to a permanent location (e.g., `C:\ffmpeg`).
3. Add the `bin` directory (e.g., `C:\ffmpeg\bin`) to your system's **PATH** environment variable.
4. Verify installation by running `ffmpeg -version` in a terminal.

#### macOS
Using Homebrew:
```bash
brew install ffmpeg
```

#### Linux
Using your package manager (e.g., Ubuntu/Debian):
```bash
sudo apt update && sudo apt install ffmpeg
```

## Installation

### Prerequisites

- [uv](https://docs.astral.sh/uv/) — fast Python package manager
- [FFmpeg](https://ffmpeg.org) — used directly for lossless MP3 splitting

### Setup

1. Clone this repository.
2. Create a virtual environment and install dependencies:
   ```bash
   uv venv .venv --python 3.14
   uv pip install -r requirements.txt
   ```

## Usage

> **Note:** VS Code will automatically detect and offer to activate `.venv`. You can also select the interpreter via `Ctrl+Shift+P` → `Python: Select Interpreter`.

Activate the virtual environment and run:
```bash
source .venv/bin/activate
python main.py
```

Or run directly without activating:
```bash
.venv/bin/python main.py
```

### Troubleshooting

If running the app fails with `exit code: 127` (or "virtualenv not found"), the virtual environment doesn't exist yet. Run the **"🏗️ Setup Project"** task first, then run the app again.

## Building the Windows Installer

The Windows build is a two-step pipeline: **PyInstaller** packages the app into an onedir bundle, and **Inno Setup** turns that bundle into a classic setup executable (Start Menu shortcut, desktop icon option, uninstaller).

> This build does **not** bundle FFmpeg: the installed app requires FFmpeg on the system PATH (see [Prerequisites](#prerequisites)). A clear error with install instructions is shown if it is missing.

### Requirements (Windows)

- Python 3.12+ with the project venv set up (see above) plus PyInstaller:
  ```powershell
  .venv\Scripts\python.exe -m pip install pyinstaller
  ```
- [Inno Setup 6.x](https://jrsoftware.org/isinfo.php) — extract it somewhere (e.g. `.\innosetup`) so `ISCC.exe` is available.

### Build steps

```powershell
# 1. Package the app (output in dist/MusicSplitter/)
.venv\Scripts\python.exe -m PyInstaller music_splitter.spec

# 2. Compile the installer (output in installer/output/)
.\innosetup\ISCC.exe /Q installer\music_splitter.iss
```

Or run the VS Code task **"📦 Build Windows Installer"**. The resulting `MusicSplitter-Setup-*.exe` can be shared directly; CI also builds it automatically via the *Build Windows Installer* workflow (`.github/workflows/build-installer.yml`).

## CUE file

.cue file example:
```
PERFORMER "Various Artists"
TITLE "Ambient Lounge  - Vol. 5 - CD 1"
FILE "Ambient Lounge - Vol. 5 - CD 1.mp3" MP3
  TRACK 01 AUDIO
    TITLE "1 Giant Leap feat. Ro. Williams & Maxi Jazz - My Culture "
    PERFORMER "1 Giant Leap feat. Ro. Williams & Maxi Jazz - My Culture "
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "Groove Armada - Lovebox"
    PERFORMER "Groove Armada - Lovebox"
    INDEX 01 05:24:10
  TRACK 03 AUDIO
    TITLE "4 Hero - Hold it down"
    PERFORMER "4 Hero - Hold it down"
    INDEX 01 11:01:01
```

## Documentation

- [ID3_tag.md](./ID3_tag.md) - The ID3v2 tags written to the split files.

## Project Management


- [TODO.md](./TODO.md) - Current tasks and upcoming work.
- [CHANGELOG.md](./CHANGELOG.md) - Historical record of completed features and changes.
