# Build Script Implementation

## 1. Code Preparation (`main.py`)
- **Resource Path Helper**: Implemented a `resource_path(relative_path)` function.
  - Checks for `sys._MEIPASS` (PyInstaller temp folder) first.
  - Fallbacks to `os.path.dirname(os.path.abspath(__file__))` for development mode.
- **Path Replacement**: Replaced all hardcoded absolute paths (e.g., `d:\haokee-note-getter\resources\...`) with `resource_path("resources/...")`. This ensures the app works on any machine and inside the packed executable.

## 2. Dependency Management (`requirements.txt`)
- Added `pyinstaller` to the requirements file.

## 3. Build Script (`build.bat`)
- Created a batch file at `d:\haokee-note-getter\build.bat` that performs the following:
  1.  **Install Dependencies**: Runs `pip install -r requirements.txt`.
  2.  **Clean/Prep**: Creates the `build` directory if missing.
  3.  **Run PyInstaller**:
      - `--onefile`: Packages everything into a single `.exe`.
      - `--windowed`: Suppresses the console window (GUI mode).
      - `--icon "resources/icon.ico"`: Sets the executable icon.
      - `--add-data "resources;resources"`: Embeds the `resources` folder (containing the SVG and ICO) into the executable.
      - `--distpath "build"`: Places the final exe in the requested folder.
      - `--name "HaokeeNoteDownloader"`: Names the output file.

## 4. Execution
- You can now run `d:\haokee-note-getter\build.bat` to generate the standalone executable.
