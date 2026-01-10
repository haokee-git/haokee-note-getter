我已完成以下修复和改进：

### 1. 修复文件预览右侧滚动条显示问题
- **调整样式**: 针对 `QTextEdit`（以及全局的 `QScrollBar`）进行了样式优化。
    - 将滚动条宽度从 8px 增加到 10px，并增加了 `border-radius` (5px)，使其更圆润且不易被遮挡。
    - 移除了 `QScrollBar` 的边框和背景干扰，确保滑块在任何背景下都清晰可见。
    - 统一了 `QTextEdit` 与 `QListWidget` 的边框和内边距逻辑，确保视觉一致性。

### 2. 为文件预览框加入 Markdown 渲染
- **安装库**: 成功安装了 Python `markdown` 库 (`markdown-3.10`)。
- **引入依赖**: 在 `main.py` 中导入了 `markdown` 模块。
- **实现逻辑**: 
    - 修改了 `on_content_fetched` 方法，现在能自动检测 `.md` 文件。
    - 使用 `markdown.markdown(content, extensions=['extra', 'nl2br', 'codehilite'])` 将 Markdown 源码转换为 HTML。
    - 注入了自定义 CSS 样式（如代码块背景、引用样式、标题颜色等），使渲染后的文档看起来更美观、更像现代文档阅读器。
    - 非 Markdown 文件（如 `.txt`, `.js`）仍保持纯文本显示。

代码已通过语法检查，你可以直接运行查看效果！