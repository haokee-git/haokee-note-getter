# Haokee Note Downloader - UI Optimization Plan

## 1. Light Mode Transformation
- **Color Palette**:
  - Background: `#FFFFFF` (White) / `#F3F3F3` (Light Gray)
  - Text: `#333333` (Dark Gray)
  - Borders: `#E0E0E0`
  - Accents: `#0078D4` (Keep the Haokee/Microsoft Blue)
- **Stylesheet Update**: Rewrite `STYLESHEET` to reflect these light mode values.

## 2. Tree Widget Selection Fix
- **Issue**: "Blue big blob".
- **Fix**: Change `QTreeWidget::item:selected` style.
  - `background-color: transparent;` (or very light gray `#F0F0F0`)
  - `color: #0078D4;` (Blue text to indicate selection)
  - `font-weight: bold;`

## 3. Button Contrast Fix
- Ensure "Download Selected" button (`#primaryBtn`) has:
  - Background: `#0078D4`
  - Text Color: `#FFFFFF` (White)
  - Font Weight: Bold

## 4. Maximize/Fullscreen Gap Fix
- **Logic**:
  - When the window is maximized, set the main container's contents margins to `0` and border radius to `0`.
  - When restored, set margins back to `20` (for shadow) and radius to `10`.
- **Implementation**: Override `changeEvent` in `MainWindow` to detect state changes and update the style/layout dynamically.

## 5. Download Complete Notification
- **Remove**: `QMessageBox.information` popup.
- **Add**: Update the status area.
  - Use `self.status_label` to show a Checkmark Icon + "Download Complete" text.
  - Add a temporary animation or color change (e.g., Green text) to make it noticeable.

## 6. Execution
- Modify `d:\haokee-note-getter\main.py` implementing these changes.
