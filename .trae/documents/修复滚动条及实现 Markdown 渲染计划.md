我将执行以下步骤来修复滚动条显示问题并实现 Markdown 渲染：

## 1. 修复文件预览右侧滚动条显示问题
- **原因分析**: 目前全局 QSS 样式表中将 `QScrollBar:vertical` 的背景设置为灰色 (`#F0F0F0`)，宽度为 8px，但这在白色背景的 `QTextEdit` 中可能显得不协调或被截断（如截图所示，看起来像是被边框遮挡或样式冲突）。
- **解决方案**:
    - 在 [main.py](file:///d:/haokee-note-getter/main.py) 中，专门针对 `QTextEdit`（即预览框）调整滚动条样式，或者微调全局滚动条的 `margin` 和 `padding`，确保其在容器内完整显示。
    - 检查 `QTextEdit` 的样式表，移除可能导致冲突的 `padding` 设置，或者确保滚动条区域不被 `border` 覆盖。

## 2. 为文件预览框加入 Markdown 渲染
- **安装依赖**: 通过 `pip install markdown` 安装 Python 的 `markdown` 库。
- **引入库**: 在 [main.py](file:///d:/haokee-note-getter/main.py) 顶部引入 `import markdown`。
- **实现渲染逻辑**: 修改 `on_content_fetched` 方法：
    - 检查当前文件的扩展名。
    - 如果是 `.md` 文件，使用 `markdown.markdown(content, extensions=['extra', 'nl2br'])` 将文本转换为 HTML，并调用 `self.preview_text.setHtml(html)` 进行显示。
    - 如果是其他文本文件（如 `.js`, `.css`），继续使用 `setText(content)` 显示纯文本。
    - 确保 `QTextEdit` 为只读模式 (`setReadOnly(True)`)。

此方案将解决视觉上的瑕疵，并显著提升 Markdown 文档的阅读体验。