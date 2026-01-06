# Haokee Note Downloader - Final Polish Plan

## 1. CheckBox SVG Icon Fix
- **Issue**: The current SVG data URI for the checkbox checkmark might be malformed or not rendering correctly (missing or white on white).
- **Fix**: Update the `QCheckBox::indicator:checked` image URL with a verified, clean SVG for a white checkmark on a blue background.

## 2. Help Dialog Shadow
- **Issue**: The screenshot shows the Help Dialog might be lacking depth or the shadow isn't visible enough against the light background.
- **Fix**: Ensure `QGraphicsDropShadowEffect` is correctly applied to the `HelpDialog` container. Increase blur radius or opacity if needed. The container needs to be a child of the transparent dialog for the shadow to be visible outside its bounds.

## 3. Author Name Update
- **Action**: Update the text in `HelpDialog` from "Trae AI & User" to "Gemini 3 Pro & Haokee".

## 4. App Icon Update
- **Action**: Set the application window icon to `d:\haokee-note-getter\resources\icon.ico`.
- **Implementation**: `self.setWindowIcon(QIcon(r"d:\haokee-note-getter\resources\icon.ico"))` in `MainWindow`.

## 5. Execution
- Modify `d:\haokee-note-getter\main.py`.
