# DrissionPage Browser Skill

[中文文档](#中文文档)

A browser automation skill based on [DrissionPage](https://drissionpage.cn/) for web data collection, search queries, and automation tasks.

## Features

- Browser automation (launch, navigate, click, input)
- Web data scraping and search
- **Image download** (search and download images from web)
- Network request listener (direct API data capture)
- User intervention support (login, captcha scenarios)
- Screenshot and recording
- Smart waiting strategies

## Directory Structure

```
drissionpage-browser/
├── SKILL.md              # Main skill documentation
├── scripts/
│   └── quick_start.py    # Quick test script
└── evals/
    └── evals.json        # Test cases

drissionpage-browser.skill  # Packaged skill file
```

## Requirements

- Python 3.7+
- DrissionPage: `pip install DrissionPage`
- Chromium browser (Chrome, Edge, etc.)

## Quick Start

```python
from DrissionPage import Chromium
from DrissionPage.common import Keys

browser = Chromium()
tab = browser.latest_tab
tab.get('https://www.baidu.com')

# Search
tab.ele('#kw').input('search query')
tab.actions.key_down(Keys.ENTER)

# Get results
results = tab.eles('tag:h3')
for r in results:
    print(r.text)
```

## Use Cases

- Search engine queries
- Hot news collection
- Web data scraping
- Image search and download
- Automated testing
- Form auto-fill

## Built-in Website Examples

The skill includes scraping examples for:

- Baidu Hot Topics
- Bilibili video list
- Weibo Hot Search
- Zhihu Hot List

See [SKILL.md](drissionpage-browser/SKILL.md) for details.

## Installation

Install the `drissionpage-browser.skill` file to your skill manager, or place the `drissionpage-browser/` directory in your skills folder.

## References

- [DrissionPage Documentation](https://drissionpage.cn/) (Chinese)
- [DrissionPage GitHub](https://github.com/g1879/DrissionPage)

## License

[MIT](LICENSE)

---

# 中文文档

基于 [DrissionPage](https://drissionpage.cn/) 的浏览器自动化 Skill，用于网页数据采集、搜索查询和自动化操作。

## 功能特性

- 浏览器自动化控制（启动、导航、点击、输入）
- 网页数据采集和搜索
- **图片下载**（搜索并下载网络图片）
- 网络请求监听（直接获取 API 数据）
- 用户介入支持（登录、验证码场景）
- 截图和录屏
- 智能等待策略

## 目录结构

```
drissionpage-browser/
├── SKILL.md              # Skill 主文档
├── scripts/
│   └── quick_start.py    # 快速测试脚本
└── evals/
    └── evals.json        # 测试用例

drissionpage-browser.skill  # 打包好的 Skill 文件
```

## 环境要求

- Python 3.7+
- DrissionPage: `pip install DrissionPage`
- Chromium 浏览器（Chrome、Edge 等）

## 快速开始

```python
from DrissionPage import Chromium
from DrissionPage.common import Keys

browser = Chromium()
tab = browser.latest_tab
tab.get('https://www.baidu.com')

# 搜索
tab.ele('#kw').input('搜索内容')
tab.actions.key_down(Keys.ENTER)

# 获取结果
results = tab.eles('tag:h3')
for r in results:
    print(r.text)
```

## 使用场景

- 搜索引擎查询
- 热点新闻采集
- 网页数据抓取
- 图片搜索下载
- 自动化测试
- 表单自动填写

## 内置网站示例

Skill 内置了以下网站的采集示例：

- 百度热搜
- B站视频列表
- 微博热搜
- 知乎热榜

详见 [SKILL.md](drissionpage-browser/SKILL.md)

## 安装方式

将 `drissionpage-browser.skill` 文件安装到你的 skill 管理工具中，或将 `drissionpage-browser/` 目录放到 skills 目录下。

## 参考资料

- [DrissionPage 官方文档](https://drissionpage.cn/)
- [DrissionPage GitHub](https://github.com/g1879/DrissionPage)

[![Star History Chart](https://api.star-history.com/svg?repos=SageFoundry/drissionpage-browser&type=Date)](https://star-history.com/#SageFoundry/drissionpage-browser)

## 许可证

[MIT](LICENSE)
