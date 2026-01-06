# Haokee Note Downloader - Further Refinement Plan

## 1. Custom Message Box Implementation
- **Problem**: Native `QMessageBox` is dark/native style and disrupts the modern UI.
- **Solution**: Create a `CustomMessageBox` class inheriting from `QDialog`.
  - **Style**: Light mode, frameless, custom title bar (Title + Close + Min).
  - **Layout**: Icon + Message Text + "OK" Button.
  - **Usage**: Replace all `QMessageBox` calls with this new dialog.

## 2. Tree Widget Selection Style Fix (The "Blob")
- **Problem**: The blue block on the left of the item (branch indicator area) persists.
- **Solution**: 
  - Set `show-decoration-selected: 0` in QSS for `QTreeWidget`.
  - Refine `QTreeWidget::item:selected` to use a light gray background (`#F0F0F0`) and a blue border (`1px solid #0078D4`).
  - Ensure the selection covers the whole row nicely without the artifact.

## 3. Button & Download Logic Changes
- **Rename**: "Download Selected" -> "下载文件中的选定媒体".
- **New Button**: Add "下载此文件" (Download this file) to the left panel (or bottom left).
  - **Logic**: Downloads the selected `.md` file (or whatever file is selected in the tree) directly to the download folder.
  - **State**: Enabled only when a file is selected in the tree.
- **Button Behavior**: 
  - "Download Media" button should always be clickable (not disabled).
  - If clicked with no selection, show the custom warning dialog.

## 4. "Show Media" Checkbox
- **UI**: Add a `QCheckBox` "显示媒体文件" next to the "Articles Directory" label.
- **Logic**:
  - Default: Checked.
  - Unchecked: Reload the tree, filtering out non-`.md` files (and folders that only contain non-`.md` files, though simple filtering is easier).
  - **Implementation**: Update `populate_tree` to respect this flag.

## 5. Execution
- Update `d:\haokee-note-getter\main.py` with these changes.
