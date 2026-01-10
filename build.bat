@echo off
setlocal

REM Switch to the script's directory to ensure relative paths work correctly
cd /d "%~dp0"

REM Force PyQt6 to avoid conflicts with PyQt5 if both are installed
set QT_API=pyqt6

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create build directory if it doesn't exist
if not exist "build" mkdir build

REM Run PyInstaller
REM --noconfirm: overwrite existing
REM --onefile: package into single exe
REM --windowed: no console window
REM --icon: use the icon
REM --add-data: include resources folder (format: source;destination)
REM --distpath: output directory
REM --workpath: temp directory
REM --specpath: spec file directory
REM --exclude-module: prevent PyQt5 from being bundled

echo Starting build process...
REM Use %~dp0 to provide full paths dynamically, ensuring portability while avoiding relative path issues with spec file location
pyinstaller --noconfirm --onefile --windowed ^
    --icon "%~dp0resources\icon.ico" ^
    --add-data "%~dp0resources;resources" ^
    --distpath "build" ^
    --workpath "build\temp" ^
    --specpath "build" ^
    --name "Haokee Note Getter" ^
    --exclude-module PyQt5 ^
    "main.py"

echo.
echo Build complete! Output is in .\build\
pause
endlocal