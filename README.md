# Haokee Note Getter (媒体下载器)

这是一个现代化的、专门用于从 [Haokee Note](https://haokee-note.org/) 网站下载媒体文件（图片、音频、视频）的桌面应用程序。

## ✨ 主要特性

*   **现代化 UI 设计**: 采用 PyQt6 构建，拥有优雅的浅色主题、圆角设计、阴影效果和流畅的动画。
*   **自绘标题栏**: 完全自定义的无边框窗口，与系统完美融合。
*   **智能目录解析**: 自动解析 Haokee Note 的文章目录结构，并支持智能排序（文件夹 > 文章 > 其他）。
*   **一键下载**: 
    *   支持下载整篇文章及其包含的所有媒体资源。
    *   支持单独选择特定的媒体文件进行下载。
*   **媒体过滤**: 可随时开启/关闭显示媒体文件，专注浏览文章目录。
*   **便携式设计**: 单文件 EXE，无需安装，即点即用。

## 🛠️ 技术栈

*   **Python 3.14**
*   **PyQt6**: GUI 框架
*   **Requests**: 网络请求
*   **BeautifulSoup4**: HTML 解析
*   **Qtawesome**: 图标库
*   **PyInstaller**: 打包工具

## 🚀 如何运行

### 开发环境运行

1.  克隆或下载本项目。
2.  安装依赖:
    ```bash
    pip install -r requirements.txt
    ```
3.  运行主程序:
    ```bash
    python main.py
    ```

### 构建可执行文件

本项目包含一个一键构建脚本，可生成独立的 `.exe` 文件。

1.  双击运行根目录下的 `build.bat`。
2.  构建完成后，可在 `build/` 文件夹中找到 `Haokee Note Getter.exe`。

## 📂 项目结构

*   `main.py`: 主程序入口及 GUI 实现。
*   `scraper.py`: 爬虫核心逻辑（解析 Obsidian Publish 站点结构）。
*   `resources/`: 存放图标及 SVG 资源文件。
*   `build.bat`: PyInstaller 打包脚本。
*   `requirements.txt`: Python 依赖列表。

## 📝 许可证

本项目由 **Gemini 3 Pro** 与 **Haokee** 共同开发。
仅供学习交流使用。
