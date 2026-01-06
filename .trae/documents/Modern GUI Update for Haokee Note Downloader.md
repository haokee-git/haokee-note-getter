# Modern GUI Implementation for Haokee Note Downloader

## 1. UI Overhaul
- **Framework**: `PyQt6` with `qtawesome` for icons.
- **Window Style**:
  - Frameless window with custom title bar.
  - "Dark Mode" aesthetic with semi-transparent backgrounds and rounded corners to simulate modern app feel.
  - Drop shadow effects for depth.
- **Custom Components**:
  - `CustomTitleBar`: Implements drag-to-move, minimize, maximize, close, and help buttons.
  - `ModernWindow`: Uses `QFrame` with specific QSS styling for the main container.

## 2. Functionality Updates
- **Language**: All text translated to Simplified Chinese.
- **Help Feature**: New Help dialog with usage instructions.
- **Download Path**:
  - Added text input field for path (default: `~/Downloads`).
  - Added "Browse" button to open folder selection dialog.
- **Icons**:
  - Replaced standard icons with FontAwesome 5 Free icons via `qtawesome`.
  - Color-coded icons for different file types (Images, Audio, Video).

## 3. Code Structure
- **`main.py`**: Completely rewritten to include the new `CustomTitleBar` class, styled components, and updated logic.
- **Styles**: Embedded CSS (QSS) for easy tweaking of colors, gradients, and animations.

## 4. Dependencies
- Added `qtawesome` to `requirements.txt`.
