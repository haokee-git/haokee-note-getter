import sys
import os
import requests
import qtawesome as qta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTreeWidget, QTreeWidgetItem, QListWidget, QListWidgetItem, 
                             QPushButton, QLabel, QProgressBar, QSplitter, QFileDialog, 
                             QFrame, QLineEdit, QDialog, QGraphicsDropShadowEffect, QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint, QSize, QPropertyAnimation, QEasingCurve, QEvent
from PyQt6.QtGui import QIcon, QFont, QColor, QPalette, QBrush

from scraper import HaokeeScraper

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# =============================================================================
# Modern UI Constants & Styles (Light Mode)
# =============================================================================

# Define the absolute path to the SVG resource for reliable loading
CHECKBOX_ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "checkbox_checked.svg").replace("\\", "/")

STYLESHEET = f"""
/* Global */
QWidget {{
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    font-size: 14px;
    color: #333333;
    background-color: transparent;
}}

/* ScrollBar */
QScrollBar:vertical {{
    border: none;
    background: #F0F0F0;
    width: 8px;
    margin: 0px 0px 0px 0px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: #CCCCCC;
    min-height: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{
    background: #AAAAAA;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* TreeWidget & ListWidget */
QTreeWidget, QListWidget {{
    background-color: rgba(255, 255, 255, 0.8);
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 5px;
    outline: none;
    show-decoration-selected: 0;
}}
QTreeWidget::item, QListWidget::item {{
    padding: 6px;
    border-radius: 4px;
    color: #333333;
    border: 1px solid transparent;
}}
QTreeWidget::item:hover, QListWidget::item:hover {{
    background-color: rgba(0, 0, 0, 0.05);
}}
QTreeWidget::item:selected {{
    background-color: #F0F0F0;
    color: #0078D4;
    font-weight: bold;
    border: 1px solid #0078D4;
}}
QListWidget::item:selected {{
    background-color: rgba(0, 120, 212, 0.1);
    color: #0078D4;
    font-weight: bold;
    border: 1px solid #0078D4;
}}

/* Splitter */
QSplitter::handle {{
    background-color: #E0E0E0;
    width: 1px;
}}

/* Buttons */
QPushButton {{
    background-color: #FFFFFF;
    border: 1px solid #D0D0D0;
    border-radius: 6px;
    padding: 6px 12px;
    color: #333333;
}}
QPushButton:hover {{
    background-color: #F5F5F5;
    border-color: #0078D4;
}}
QPushButton:pressed {{
    background-color: #E0E0E0;
}}
QPushButton:disabled {{
    background-color: #F0F0F0;
    color: #AAAAAA;
    border-color: #E0E0E0;
}}

/* Primary Button */
QPushButton#primaryBtn {{
    background-color: #0078D4;
    border: none;
    color: #FFFFFF;
    font-weight: bold;
}}
QPushButton#primaryBtn:hover {{
    background-color: #106EBE;
}}
QPushButton#primaryBtn:pressed {{
    background-color: #005A9E;
}}
QPushButton#primaryBtn:disabled {{
    background-color: #CCCCCC;
    color: #FFFFFF;
}}

/* LineEdit */
QLineEdit {{
    background-color: #FFFFFF;
    border: 1px solid #D0D0D0;
    border-radius: 6px;
    padding: 6px;
    color: #333333;
}}
QLineEdit:focus {{
    border: 1px solid #0078D4;
}}

/* ProgressBar */
QProgressBar {{
    border: none;
    border-radius: 4px;
    background-color: #E0E0E0;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background-color: #0078D4;
    border-radius: 4px;
}}

/* CheckBox */
QCheckBox {{
    spacing: 5px;
    color: #333333;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #D0D0D0;
    background: #FFFFFF;
}}
QCheckBox::indicator:unchecked:hover {{
    border-color: #0078D4;
}}
QCheckBox::indicator:checked {{
    background-color: #0078D4;
    border-color: #0078D4;
    image: url("{CHECKBOX_ICON_PATH}");
}}

/* Title Bar */
#TitleBar {{
    background-color: #F9F9F9;
    border-bottom: 1px solid #E0E0E0;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}}
#TitleBar QLabel {{
    color: #333333;
    font-weight: bold;
}}
#TitleBar QPushButton {{
    background-color: transparent;
    border: none;
    border-radius: 0px;
    color: #333333;
}}
#TitleBar QPushButton:hover {{
    background-color: rgba(0, 0, 0, 0.05);
}}
#TitleBar QPushButton#closeBtn:hover {{
    background-color: #E81123;
    color: white;
}}
"""

# =============================================================================
# Threads
# =============================================================================

class InitThread(QThread):
    finished_signal = pyqtSignal(object) 
    error_signal = pyqtSignal(str)

    def __init__(self, scraper):
        super().__init__()
        self.scraper = scraper

    def run(self):
        try:
            self.scraper.get_site_info()
            cache = self.scraper.get_directory()
            self.finished_signal.emit(cache)
        except Exception as e:
            self.error_signal.emit(str(e))

class FetchContentThread(QThread):
    finished_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)

    def __init__(self, scraper, path):
        super().__init__()
        self.scraper = scraper
        self.path = path

    def run(self):
        try:
            content = self.scraper.get_page_content(self.path)
            media = self.scraper.extract_media(content)
            self.finished_signal.emit(media)
        except Exception as e:
            self.error_signal.emit(str(e))

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, items, dest_folder):
        super().__init__()
        self.items = items
        self.dest_folder = dest_folder

    def run(self):
        total = len(self.items)
        if total == 0:
            self.finished_signal.emit()
            return
            
        for i, item in enumerate(self.items):
            try:
                self.progress_signal.emit(int((i / total) * 100), f"正在下载 {item['name']}...")
                
                resp = requests.get(item['url'], stream=True)
                resp.raise_for_status()
                
                file_path = os.path.join(self.dest_folder, item['name'])
                with open(file_path, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
            except Exception as e:
                print(f"Failed to download {item['name']}: {e}")
                
        self.progress_signal.emit(100, "下载完成")
        self.finished_signal.emit()

# =============================================================================
# Custom UI Components
# =============================================================================

class CustomTitleBar(QWidget):
    def __init__(self, parent=None, title="", is_dialog=False):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.is_dialog = is_dialog
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setFixedHeight(32)
        
        # Icon
        self.icon_label = QLabel()
        # Use local icon if available, otherwise fallback to qtawesome
        icon_path = r"d:\haokee-note-getter\resources\icon.ico"
        if os.path.exists(icon_path):
             self.icon_label.setPixmap(QIcon(icon_path).pixmap(16, 16))
        else:
             self.icon_label.setPixmap(qta.icon('fa5s.cloud-download-alt', color='#0078D4').pixmap(16, 16))
        
        self.layout.addWidget(self.icon_label)
        self.layout.addSpacing(10)
        
        # Title
        self.title_label = QLabel(title)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch(1)
        
        # Help Button
        if not is_dialog:
            self.help_btn = QPushButton()
            self.help_btn.setIcon(qta.icon('fa5s.question-circle', color='#333333'))
            self.help_btn.setFixedSize(46, 32)
            self.help_btn.setToolTip("帮助")
            self.help_btn.clicked.connect(self.window().show_help)
            self.layout.addWidget(self.help_btn)

        # Minimize
        self.min_btn = QPushButton()
        self.min_btn.setIcon(qta.icon('fa5s.minus', color='#333333'))
        self.min_btn.setFixedSize(46, 32)
        self.min_btn.clicked.connect(self.window().showMinimized)
        self.layout.addWidget(self.min_btn)
        
        # Maximize/Restore (Only for main window)
        if not is_dialog:
            self.max_btn = QPushButton()
            self.max_btn.setIcon(qta.icon('fa5s.window-maximize', color='#333333'))
            self.max_btn.setFixedSize(46, 32)
            self.max_btn.clicked.connect(self.toggle_max)
            self.layout.addWidget(self.max_btn)

        # Close
        self.close_btn = QPushButton()
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setIcon(qta.icon('fa5s.times', color='#333333'))
        self.close_btn.setFixedSize(46, 32)
        self.close_btn.clicked.connect(self.window().close)
        self.layout.addWidget(self.close_btn)

        # Drag Logic
        self.start_pos = None

    def toggle_max(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.max_btn.setIcon(qta.icon('fa5s.window-maximize', color='#333333'))
        else:
            self.window().showMaximized()
            self.max_btn.setIcon(qta.icon('fa5s.window-restore', color='#333333'))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.start_pos:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.window().move(self.window().pos() + delta)
            self.start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.start_pos = None

class CustomMessageBox(QDialog):
    def __init__(self, parent=None, title="提示", content="", icon_name="fa5s.info-circle", icon_color="#0078D4"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.resize(350, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Container
        container = QFrame()
        container.setObjectName("Container")
        container.setStyleSheet("""
            #Container {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)
        layout.addWidget(container)
        
        inner_layout = QVBoxLayout(container)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        
        # Title Bar
        title_bar = CustomTitleBar(self, title, is_dialog=True)
        inner_layout.addWidget(title_bar)
        
        # Content Area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Icon + Text
        msg_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color=icon_color).pixmap(48, 48))
        msg_layout.addWidget(icon_label)
        
        text_label = QLabel(content)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("font-size: 15px; color: #333333;")
        msg_layout.addWidget(text_label, 1)
        
        content_layout.addLayout(msg_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton("确定")
        ok_btn.setObjectName("primaryBtn")
        ok_btn.setFixedSize(100, 32)
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        
        content_layout.addLayout(btn_layout)
        inner_layout.addWidget(content_widget)
        inner_layout.addStretch()

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.resize(400, 300)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10) # Padding for shadow
        layout.setSpacing(0)
        
        # Container
        container = QFrame()
        container.setObjectName("Container")
        container.setStyleSheet("""
            #Container {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)
        
        layout.addWidget(container)
        
        inner_layout = QVBoxLayout(container)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        
        title_bar = CustomTitleBar(self, "帮助", is_dialog=True)
        inner_layout.addWidget(title_bar)
        
        content = QLabel(
            "<h2>Haokee Note 下载器</h2>"
            "<p>版本: 1.3.0 (Light Mode)</p>"
            "<p>这是一个用于从 Haokee Note 网站下载媒体文件的工具。</p>"
            "<ul>"
            "<li><b>左侧栏</b>: 浏览文章目录。勾选'显示媒体文件'可查看所有文件。</li>"
            "<li><b>右侧栏</b>: 查看选中文章中的媒体文件。</li>"
            "<li><b>下载此文件</b>: 直接下载选中的文件。</li>"
            "<li><b>下载选定媒体</b>: 下载文章中引用的媒体。</li>"
            "</ul>"
            "<p>作者: Gemini 3 Pro & Haokee</p>"
        )
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        content.setStyleSheet("padding: 20px; color: #333333;")
        inner_layout.addWidget(content)
        inner_layout.addStretch()

# =============================================================================
# Main Window
# =============================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Haokee Note 媒体下载器")
        self.resize(1000, 600)
        
        # Frameless Window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # App Icon
        icon_path = resource_path("resources/icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.scraper = HaokeeScraper()
        self.cache_data = {} # Store directory cache
        
        self.setup_ui()
        self.start_initialization()

    def setup_ui(self):
        # Main Container
        self.main_container = QFrame()
        self.main_container.setObjectName("MainContainer")
        self.main_container.setStyleSheet("""
            #MainContainer {
                background-color: #F9F9F9; /* Light background */
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
        """)
        self.setCentralWidget(self.main_container)
        
        # Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 50))
        self.shadow.setOffset(0, 0)
        self.main_container.setGraphicsEffect(self.shadow)
        
        # Layout
        self.main_layout = QVBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.wrapper = QWidget()
        self.wrapper_layout = QVBoxLayout(self.wrapper)
        self.wrapper_layout.setContentsMargins(20, 20, 20, 20)
        self.wrapper_layout.addWidget(self.main_container)
        self.setCentralWidget(self.wrapper)

        # Title Bar
        self.title_bar = CustomTitleBar(self, "Haokee Note 媒体下载器")
        self.main_layout.addWidget(self.title_bar)
        
        # Content Area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        self.main_layout.addWidget(content_widget)
        
        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        content_layout.addWidget(splitter, 1)
        
        # --- Left Panel ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 10, 0)
        
        # Header Row: Title + Checkbox
        header_row = QHBoxLayout()
        left_label = QLabel("文章目录")
        left_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header_row.addWidget(left_label)
        header_row.addStretch()
        
        self.show_media_chk = QCheckBox("显示媒体文件")
        self.show_media_chk.setChecked(True)
        self.show_media_chk.stateChanged.connect(self.refresh_tree)
        header_row.addWidget(self.show_media_chk)
        
        left_layout.addLayout(header_row)
        
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.itemSelectionChanged.connect(self.on_tree_selection_changed)
        self.tree_widget.setIconSize(QSize(20, 20))
        left_layout.addWidget(self.tree_widget)
        
        # Download This File Button
        self.download_file_btn = QPushButton("下载此文件")
        self.download_file_btn.setEnabled(False)
        self.download_file_btn.clicked.connect(self.on_download_file_clicked)
        left_layout.addWidget(self.download_file_btn)
        
        splitter.addWidget(left_widget)
        
        # --- Right Panel ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 0, 0, 0)
        
        right_label = QLabel("媒体文件")
        right_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        right_layout.addWidget(right_label)
        
        self.media_list = QListWidget()
        self.media_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.media_list.setIconSize(QSize(24, 24))
        right_layout.addWidget(self.media_list)
        
        # Download Path
        path_layout = QHBoxLayout()
        path_label = QLabel("保存位置:")
        path_layout.addWidget(path_label)
        
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(False)
        default_download = os.path.join(os.path.expanduser("~"), "Downloads")
        self.path_input.setText(default_download)
        path_layout.addWidget(self.path_input)
        
        self.browse_btn = QPushButton()
        self.browse_btn.setIcon(qta.icon('fa5s.folder-open', color='#333333'))
        self.browse_btn.setToolTip("选择文件夹")
        self.browse_btn.clicked.connect(self.browse_folder)
        path_layout.addWidget(self.browse_btn)
        
        right_layout.addLayout(path_layout)
        
        # Download Button
        self.download_media_btn = QPushButton("下载文件中的选定媒体")
        self.download_media_btn.setObjectName("primaryBtn")
        # Always enabled so user can click and get warning
        self.download_media_btn.setEnabled(True) 
        self.download_media_btn.clicked.connect(self.on_download_media_clicked)
        self.download_media_btn.setFixedHeight(40)
        self.download_media_btn.setIcon(qta.icon('fa5s.download', color='white'))
        right_layout.addWidget(self.download_media_btn)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 700])
        splitter.setHandleWidth(2)
        
        # Status Bar / Progress
        status_layout = QHBoxLayout()
        
        self.status_container = QWidget()
        self.status_container_layout = QHBoxLayout(self.status_container)
        self.status_container_layout.setContentsMargins(0, 0, 0, 0)
        self.status_container_layout.setSpacing(5)
        
        self.status_icon = QLabel()
        self.status_container_layout.addWidget(self.status_icon)
        
        self.status_label = QLabel("就绪")
        self.status_container_layout.addWidget(self.status_label)
        self.status_container_layout.addStretch()
        
        status_layout.addWidget(self.status_container)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setFixedWidth(200)
        status_layout.addWidget(self.progress_bar)
        
        content_layout.addLayout(status_layout)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() & Qt.WindowState.WindowMaximized:
                self.wrapper_layout.setContentsMargins(0, 0, 0, 0)
                self.main_container.setStyleSheet("""
                    #MainContainer {
                        background-color: #F9F9F9;
                        border: none;
                        border-radius: 0px;
                    }
                """)
                self.title_bar.setStyleSheet("""
                    #TitleBar {
                        background-color: #F9F9F9;
                        border-bottom: 1px solid #E0E0E0;
                        border-radius: 0px;
                    }
                """)
            else:
                self.wrapper_layout.setContentsMargins(20, 20, 20, 20)
                self.main_container.setStyleSheet("""
                    #MainContainer {
                        background-color: #F9F9F9;
                        border: 1px solid #E0E0E0;
                        border-radius: 10px;
                    }
                """)
                self.title_bar.setStyleSheet("""
                    #TitleBar {
                        background-color: #F9F9F9;
                        border-bottom: 1px solid #E0E0E0;
                        border-top-left-radius: 10px;
                        border-top-right-radius: 10px;
                    }
                """)
        super().changeEvent(event)

    def show_help(self):
        dlg = HelpDialog(self)
        dlg.exec()

    def show_message(self, title, content, is_error=False):
        icon = "fa5s.times-circle" if is_error else "fa5s.info-circle"
        color = "#E81123" if is_error else "#0078D4"
        dlg = CustomMessageBox(self, title, content, icon, color)
        dlg.exec()

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择下载保存文件夹", self.path_input.text())
        if folder:
            self.path_input.setText(folder)

    def start_initialization(self):
        self.status_label.setText("正在连接 Haokee Note...")
        self.status_icon.clear()
        self.tree_widget.setEnabled(False)
        
        self.init_thread = InitThread(self.scraper)
        self.init_thread.finished_signal.connect(self.on_init_finished)
        self.init_thread.error_signal.connect(self.on_init_error)
        self.init_thread.start()

    def on_init_finished(self, cache_data):
        self.status_label.setText("目录加载完成。")
        self.tree_widget.setEnabled(True)
        self.cache_data = cache_data
        self.populate_tree(cache_data)

    def on_init_error(self, error_msg):
        self.status_label.setText("连接失败。")
        self.status_icon.setPixmap(qta.icon('fa5s.exclamation-circle', color='#E81123').pixmap(16, 16))
        self.show_message("连接错误", f"无法连接到服务器: {error_msg}", is_error=True)

    def refresh_tree(self):
        self.populate_tree(self.cache_data)

    def populate_tree(self, cache_data):
        self.tree_widget.clear()
        
        # Build hierarchical structure first
        tree_structure = {}
        
        show_media = self.show_media_chk.isChecked()
        
        for path in cache_data.keys():
            # Filter Logic
            is_md = path.endswith('.md')
            if not show_media and not is_md:
                continue

            parts = path.split('/')
            current_level = tree_structure
            for i, part in enumerate(parts):
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        
        # Recursive function to add items with sorting
        def add_items_recursive(parent_item, structure, current_path_prefix=""):
            # Sort keys: Folder > MD > Other, then Alphabetical
            def sort_key(name):
                is_folder = bool(structure[name])
                is_md = name.endswith('.md')
                
                # Priority: 
                # 0: Folder
                # 1: MD File
                # 2: Other File
                type_priority = 2
                if is_folder:
                    type_priority = 0
                elif is_md:
                    type_priority = 1
                    
                return (type_priority, name.lower())

            sorted_keys = sorted(structure.keys(), key=sort_key)
            
            folder_icon = qta.icon('fa5s.folder', color='#FFD700')
            file_icon = qta.icon('fa5s.file-alt', color='#4FC1FF')
            media_icon = qta.icon('fa5s.image', color='#B48EAD')

            for key in sorted_keys:
                full_path = f"{current_path_prefix}/{key}" if current_path_prefix else key
                item = QTreeWidgetItem([key])
                item.setData(0, Qt.ItemDataRole.UserRole, full_path)
                
                is_folder = bool(structure[key])
                if is_folder:
                    item.setIcon(0, folder_icon)
                    add_items_recursive(item, structure[key], full_path)
                else:
                    if key.endswith('.md'):
                        item.setIcon(0, file_icon)
                    else:
                        item.setIcon(0, media_icon)
                
                if parent_item:
                    parent_item.addChild(item)
                else:
                    self.tree_widget.addTopLevelItem(item)

        add_items_recursive(None, tree_structure)

    def on_tree_selection_changed(self):
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            self.download_file_btn.setEnabled(False)
            return
            
        item = selected_items[0]
        path = item.data(0, Qt.ItemDataRole.UserRole)
        
        # Check if it's a file (leaf node logic simplified)
        # Actually checking if it's in cache keys is better
        is_file = path in self.cache_data
        self.download_file_btn.setEnabled(is_file)
        
        if path.endswith('.md'):
            self.fetch_content(path)
        else:
            self.media_list.clear()
            self.status_label.setText(f"已选择: {path}")
            self.status_icon.clear()

    def fetch_content(self, path):
        self.status_label.setText(f"正在获取: {path}...")
        self.status_icon.setPixmap(qta.icon('fa5s.spinner', color='#0078D4', animation=qta.Spin(self.status_icon)).pixmap(16, 16))
        self.media_list.clear()
        
        self.fetch_thread = FetchContentThread(self.scraper, path)
        self.fetch_thread.finished_signal.connect(self.on_content_fetched)
        self.fetch_thread.error_signal.connect(self.on_content_error)
        self.fetch_thread.start()

    def on_content_fetched(self, media_files):
        self.status_label.setText(f"发现 {len(media_files)} 个媒体文件。")
        self.status_icon.setPixmap(qta.icon('fa5s.check-circle', color='#107C10').pixmap(16, 16))
        self.media_list.clear()
        
        img_icon = qta.icon('fa5s.image', color='#B48EAD')
        audio_icon = qta.icon('fa5s.music', color='#A3BE8C')
        video_icon = qta.icon('fa5s.video', color='#BF616A')
        file_icon = qta.icon('fa5s.file', color='#88C0D0')

        for media in media_files:
            item = QListWidgetItem(f"{media['name']} ({media['type']})")
            item.setData(Qt.ItemDataRole.UserRole, media)
            
            if media['type'] == 'image':
                item.setIcon(img_icon)
            elif media['type'] == 'audio':
                item.setIcon(audio_icon)
            elif media['type'] == 'video':
                item.setIcon(video_icon)
            else:
                item.setIcon(file_icon)
                
            self.media_list.addItem(item)

    def on_content_error(self, error_msg):
        self.status_label.setText("获取内容失败。")
        self.status_icon.setPixmap(qta.icon('fa5s.times-circle', color='#E81123').pixmap(16, 16))
        self.show_message("获取错误", f"无法获取文章内容: {error_msg}", is_error=True)

    def on_download_file_clicked(self):
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return
            
        path = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
        # Construct item dict for DownloadThread
        # We need URL. 
        # For .md files, URL is access URL. For others, it's file URL.
        # Scraper has construct_url
        url = self.scraper.construct_url(path)
        name = path.split('/')[-1]
        
        item = {
            'name': name,
            'url': url
        }
        
        self.start_download([item])

    def on_download_media_clicked(self):
        selected_items = self.media_list.selectedItems()
        if not selected_items:
            self.show_message("提示", "请先在右侧列表中选择要下载的媒体文件。")
            return
            
        items_to_download = [item.data(Qt.ItemDataRole.UserRole) for item in selected_items]
        self.start_download(items_to_download)

    def start_download(self, items):
        dest_folder = self.path_input.text()
        if not os.path.exists(dest_folder):
            try:
                os.makedirs(dest_folder)
            except OSError:
                self.show_message("路径错误", "目标文件夹不存在且无法创建。", is_error=True)
                return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.download_media_btn.setEnabled(False)
        self.download_file_btn.setEnabled(False)
        self.status_icon.setPixmap(qta.icon('fa5s.spinner', color='#0078D4', animation=qta.Spin(self.status_icon)).pixmap(16, 16))
        
        self.download_thread = DownloadThread(items, dest_folder)
        self.download_thread.progress_signal.connect(self.on_download_progress)
        self.download_thread.finished_signal.connect(self.on_download_finished)
        self.download_thread.start()

    def on_download_progress(self, percent, message):
        self.progress_bar.setValue(percent)
        self.status_label.setText(message)

    def on_download_finished(self):
        self.download_media_btn.setEnabled(True)
        # Re-enable file btn if selection is valid
        if self.tree_widget.selectedItems():
            self.download_file_btn.setEnabled(True)
            
        self.progress_bar.setVisible(False)
        self.status_label.setText("下载任务已完成！")
        self.status_label.setStyleSheet("color: #107C10; font-weight: bold;")
        self.status_icon.setPixmap(qta.icon('fa5s.check-circle', color='#107C10').pixmap(16, 16))
        
        QThread.msleep(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
