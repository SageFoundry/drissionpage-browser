# DrissionPage Browser Skill

[中文文档](#中文文档)

A DrissionPage-based browser automation skill for web research, scraping, and browser-driven tasks.

This repository is intentionally opinionated about browser startup. The main goal is not just to list DrissionPage APIs, but to make browser automation behave predictably in a real workspace.

## Features

- Browser automation with explicit startup validation
- Web scraping and search
- Network request listening
- Screenshot-based evidence capture
- User intervention support for login and captcha flows
- Structured research output with source tracking

## Directory Structure

```text
drissionpage-browser/
├── SKILL.md              # Main skill instructions
├── scripts/
│   └── quick_start.py    # Startup validation example
└── evals/
    └── evals.json        # Behavior-focused evals

drissionpage-browser.skill  # Packaged skill file
```

## Requirements

- Python 3.7+
- DrissionPage: `pip install DrissionPage`
- A runnable Chromium-based browser executable path

### macOS Default Browser Path

Recommended default:

```text
/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

Other common macOS candidates:

```text
/Applications/Chromium.app/Contents/MacOS/Chromium
/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge
```

### Windows Default Browser Path

Recommended default:

```text
C:\Program Files\Google\Chrome\Application\chrome.exe
```

Other common Windows candidates:

```text
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
C:\Program Files\Chromium\Application\chrome.exe
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

## Startup Contract

The skill uses this startup priority:

1. User-provided browser path, port, and launch arguments
2. Previously validated workspace settings
3. Platform default path
4. If none work, stop and report the startup problem

Do not fall back to bare `Chromium()` once a verified path or user-provided configuration exists.
Prefer `auto_port()` for default startup. Use a fixed port only when you intentionally manage a specific browser instance.

## Recommended Startup Template

```python
import sys
from pathlib import Path

from DrissionPage import Chromium, ChromiumOptions

import os
chrome_path = os.environ.get(
    'DRISSIONPAGE_BROWSER_PATH',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if sys.platform.startswith('win')
    else '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
)

if not Path(chrome_path).exists():
    raise FileNotFoundError(f'Browser not found: {chrome_path}')

co = ChromiumOptions()
co.set_browser_path(chrome_path)
co.auto_port()

browser = Chromium(addr_or_opts=co)
tab = browser.latest_tab

tab.get('https://example.com')
tab.wait.doc_loaded()

print(tab.title)
print(tab.url)
```

## Quick Start

Run the included validation script:

```bash
# macOS / Linux
python3 drissionpage-browser/scripts/quick_start.py

# Windows
python drissionpage-browser/scripts/quick_start.py
```

What it does:

- resolves a browser path using explicit priority
- enables `auto_port()` to avoid fragile fixed-port startup
- verifies startup with `https://example.com`
- opens Baidu and runs a basic search
- prints page title, URL, and result count

## Research Workflow

The default workflow for this skill is:

1. Resolve and validate browser startup
2. Open the target page
3. Extract facts, links, or structured data
4. Record source title and source URL
5. Capture screenshots for key pages
6. Return structured output

Recommended minimum output fields:

- source title
- source URL
- core finding
- slide-ready sentence
- visualization suggestion
- whether manual review is needed

## Failure Diagnosis Order

When startup fails, diagnose in this order:

1. Browser path exists
2. `ChromiumOptions` setup is correct
3. If you see a WebSocket 404 during startup, retry with `auto_port()`
4. Browser can launch manually
5. `DrissionPage` is installed correctly
6. Connection or port mismatch
7. Only then inspect page logic

## Use Cases

- Search engine queries
- News collection
- Research with evidence capture
- Link extraction
- Browser-based debugging
- Form automation

## Built-in Website Examples

The skill includes examples for:

- Baidu hot topics
- Bilibili video listing
- Weibo hot search
- Zhihu hot list

See [SKILL.md](drissionpage-browser/SKILL.md) for the full skill instructions.

## Installation

Install `drissionpage-browser.skill` into your skill manager, or place the `drissionpage-browser/` directory in your skills folder.

## References

- [DrissionPage Documentation](https://drissionpage.cn/)
- [DrissionPage GitHub](https://github.com/g1879/DrissionPage)

## License

[MIT](LICENSE)

---

# 中文文档

基于 DrissionPage 的浏览器自动化 Skill，用于网页研究、抓取和浏览器驱动任务。

这个仓库的重点不是单纯罗列 DrissionPage API，而是把浏览器启动、验证、排障和结构化输出写成可执行约束。

## 功能特性

- 显式浏览器启动与验证
- 网页搜索与抓取
- 网络请求监听
- 截图留证
- 登录与验证码场景的人工介入
- 结构化研究输出

## 目录结构

```text
drissionpage-browser/
├── SKILL.md              # Skill 主文档
├── scripts/
│   └── quick_start.py    # 启动验证示例
└── evals/
    └── evals.json        # 行为导向测试

drissionpage-browser.skill  # 打包产物
```

## 环境要求

- Python 3.7+
- DrissionPage：`pip install DrissionPage`
- 一个可执行的 Chromium 系浏览器路径

### macOS 默认浏览器路径

推荐默认值：

```text
/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

其他常见候选：

```text
/Applications/Chromium.app/Contents/MacOS/Chromium
/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge
```

### Windows 默认浏览器路径

推荐默认值：

```text
C:\Program Files\Google\Chrome\Application\chrome.exe
```

其他常见候选：

```text
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
C:\Program Files\Chromium\Application\chrome.exe
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

## 启动约定

Skill 的浏览器启动优先级如下：

1. 用户提供的路径、端口、启动参数
2. 已验证通过的工作区配置
3. 当前平台默认路径
4. 如果都不可用，直接报告启动问题并停止

一旦已经有可用路径或用户给定配置，不要再回退到裸 `Chromium()`。
默认启动优先使用 `auto_port()`；只有在你明确管理某个浏览器实例时才使用固定端口。

## 推荐启动模板

```python
import sys
from pathlib import Path

from DrissionPage import Chromium, ChromiumOptions

import os
chrome_path = os.environ.get(
    'DRISSIONPAGE_BROWSER_PATH',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if sys.platform.startswith('win')
    else '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
)

if not Path(chrome_path).exists():
    raise FileNotFoundError(f'Browser not found: {chrome_path}')

co = ChromiumOptions()
co.set_browser_path(chrome_path)
co.auto_port()

browser = Chromium(addr_or_opts=co)
tab = browser.latest_tab

tab.get('https://example.com')
tab.wait.doc_loaded()

print(tab.title)
print(tab.url)
```

## 快速开始

运行仓库自带验证脚本：

```bash
# macOS / Linux
python3 drissionpage-browser/scripts/quick_start.py

# Windows
python drissionpage-browser/scripts/quick_start.py
```

脚本会：

- 按明确优先级解析浏览器路径
- 默认启用 `auto_port()`，避免依赖固定端口
- 先用 `https://example.com` 验证启动
- 再打开百度执行一次基础搜索
- 输出标题、URL 和结果数量

## 研究任务流程

默认流程：

1. 解析并验证浏览器启动
2. 打开目标页面
3. 提取事实、链接或结构化数据
4. 记录来源标题和来源 URL
5. 对关键页面截图留证
6. 返回结构化结果

建议最少输出字段：

- 来源标题
- 来源 URL
- 核心结论
- 可上 slide 的一句话
- 可视化建议
- 是否需要人工复核

## 故障排查顺序

浏览器启动失败时按这个顺序查：

1. 浏览器路径是否存在
2. `ChromiumOptions` 是否配置正确
3. 如果启动时遇到 WebSocket 404，优先改用 `auto_port()`
4. 浏览器能否手动启动
5. `DrissionPage` 是否安装正确
6. 是否连到了错误的端口或实例
7. 只有这些都确认后，再查页面逻辑

## 使用场景

- 搜索引擎查询
- 新闻采集
- 带证据留存的研究任务
- 链接提取
- 浏览器调试
- 表单自动化

## 内置示例网站

- 百度热搜
- B 站视频列表
- 微博热搜
- 知乎热榜

完整说明见 [SKILL.md](drissionpage-browser/SKILL.md)。

## 安装方式

将 `drissionpage-browser.skill` 安装到你的 skill 管理工具中，或将 `drissionpage-browser/` 目录放到 skills 目录下。

## 参考资料

- [DrissionPage 官方文档](https://drissionpage.cn/)
- [DrissionPage GitHub](https://github.com/g1879/DrissionPage)

[![Star History Chart](https://api.star-history.com/svg?repos=SageFoundry/drissionpage-browser&type=Date)](https://star-history.com/#SageFoundry/drissionpage-browser)

## 许可证

[MIT](LICENSE)
