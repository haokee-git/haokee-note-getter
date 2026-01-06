# Python GUI Web Downloader for Haokee Note

## 1. Project Structure
- `main.py`: Entry point and GUI implementation using PyQt6.
- `scraper.py`: Logic for interacting with the Obsidian Publish API (fetching directory, parsing content, resolving URLs).
- `requirements.txt`: Dependencies (`requests`, `PyQt6`, `beautifulsoup4`).

## 2. Implementation Steps

### Step 1: Scraper Logic (`scraper.py`)
- **Initialization**:
  - Connect to `https://haokee-note.org/%E4%B8%BB%E9%A1%B5` to extract `siteInfo` (host, uid) from `<script>` tags.
  - Fetch the directory structure (cache) from `https://<host>/cache/<uid>`.
- **Directory Parsing**:
  - Parse the cache JSON keys to build a hierarchical directory tree of articles (`.md` files).
- **Content Fetching**:
  - Fetch article content (Markdown) from `https://<host>/access/<uid>/<encoded_path>`.
- **Media Extraction**:
  - Use Regex to find media links in Markdown: `![[filename]]` and `![...](filename)`.
  - Resolve these filenames to full paths using the cache keys.
  - Construct download URLs: `https://<host>/access/<uid>/<full_path>`.

### Step 2: GUI Implementation (`main.py`)
- **Main Window**: A modern `QMainWindow` with a split view.
- **Left Panel (Directory)**:
  - A `QTreeWidget` displaying the folder structure and articles.
  - Implements keyboard navigation (Up/Down) and mouse selection.
  - Signals the backend to fetch content upon selection.
- **Right Panel (Media List)**:
  - A `QListWidget` displaying found media files (images, audio, video).
  - A "Download" button at the bottom.
  - A `QProgressBar` to show download status.
- **Download Flow**:
  - User selects media files -> Clicks Download.
  - `QFileDialog` asks for destination folder.
  - A background thread (`QThread`) handles the downloading to prevent freezing the UI.
  - Updates progress bar and status label.

### Step 3: Refinement
- Ensure URLs are correctly encoded (handling Chinese characters).
- Add error handling for network requests.
- Apply a clean, modern stylesheet (QSS) to the UI.

## 3. Technical Details
- **Libraries**: `PyQt6` for GUI, `requests` for HTTP, `re` for parsing.
- **URL Construction**: Dynamic prefix resolution based on the `siteInfo` found on the home page.
