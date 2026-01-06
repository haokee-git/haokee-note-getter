# Haokee Note Downloader - Final Fixes

## 1. Directory Tree Sorting
- **Requirement**: Sort items by Type (Folder > Markdown > Other) then Name.
- **Implementation**:
  - The current `populate_tree` processes items in path order, which naturally groups files in folders but mixes them within the folder.
  - **Refactor `populate_tree`**:
    1. Build a full nested dictionary structure from the flat path list first.
    2. Recursively populate the `QTreeWidget`.
    3. In the recursion, sort keys based on:
       - Priority 0: Is Folder (children > 0)
       - Priority 1: Is Markdown (`.md`)
       - Priority 2: Other
       - Priority 3: Name (Alphabetical)

## 2. CheckBox Icon Fix
- **Issue**: The data URI might be invalid or not rendered by Qt correctly (URL encoding issues often cause this).
- **Fix**: 
  - Save the SVG to a local file `resources/checkbox_checked.svg` (create `resources` folder if needed).
  - Use `image: url(resources/checkbox_checked.svg);` in QSS.
  - Alternatively, use a simpler, URL-encoded data URI that is known to work in Qt.

## 3. Execution
- Create `d:\haokee-note-getter\resources\checkbox_checked.svg`.
- Modify `d:\haokee-note-getter\main.py`.
