@echo off
REM Install dependencies
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

pyinstaller --noconfirm --onefile --windowed ^
    --icon "%~dp0resources\icon.ico" ^
    --add-data "%~dp0resources;resources" ^
    --distpath "%~dp0build" ^
    --workpath "%~dp0build\temp" ^
    --specpath "%~dp0build" ^
    --name "Haokee Note Getter" ^
    "%~dp0main.py"

echo.
echo Build complete! Output is in d:\haokee-note-getter\build\
pause
