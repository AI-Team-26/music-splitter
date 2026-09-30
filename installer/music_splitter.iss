; Inno Setup script for Music Splitter.
; Packages the onedir output of `pyinstaller music_splitter.spec` (dist/MusicSplitter/).
; Compile with: ISCC.exe /Q installer\music_splitter.iss   (output in installer/output/)

#define MyAppName "Music Splitter"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "Alessandro Piccione"
#define MyAppExeName "MusicSplitter.exe"

[Setup]
AppId={{B7A4C2D9-3F6E-4B5A-9C1D-E8F2A6B4C7D1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputBaseFilename=MusicSplitter-Setup-{#MyAppVersion}
ArchitecturesInstallIn64BitMode=x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "..\dist\MusicSplitter\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: postinstall nowait skipifsilent
