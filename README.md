# DrissionPage Browser Skill

基于 [DrissionPage](https://drissionpage.cn/) 的浏览器自动化 Skill，用于网页数据采集、搜索查询和自动化操作。

## 功能特性

- 浏览器自动化控制（启动、导航、点击、输入）
- 网页数据采集和搜索
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

## 依赖

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
- 自动化测试
- 表单自动填写

## 常用网站示例

Skill 内置了以下网站的采集示例：

- 百度热搜
- B站视频列表
- 微博热搜
- 知乎热榜

详见 [SKILL.md](drissionpage-browser/SKILL.md)

## 安装

将 `drissionpage-browser.skill` 文件安装到你的 skill 管理工具中，或将 `drissionpage-browser/` 目录放到 skills 目录下。

## 参考

- [DrissionPage 官方文档](https://drissionpage.cn/)
- [DrissionPage GitHub](https://github.com/g1879/DrissionPage)

## License

MIT