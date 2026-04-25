---
name: drissionpage-browser
description: |
  Browser automation for web data collection and research. Use this skill when the user needs to search the web, query information, scrape data, debug websites, or perform any task requiring a browser. DrissionPage provides persistent browser control with support for user interaction during login and captcha flows. In this skill, browser startup must be validated before business automation continues.
---

# DrissionPage Browser Automation

Browser automation for web data collection, research, and debugging using DrissionPage.

## When to Use

- User asks to search the web or query information
- User needs to scrape or collect data from websites
- User wants to check real-time information such as news or prices
- User mentions "open browser", "visit website", "click button"
- User needs to interact with websites that require login
- User wants to debug or test web applications
- User needs structured research output with sources

## Environment Rules

- Use the user-provided browser path, port, and startup parameters first.
- Reuse previously validated settings in the same workspace before guessing new values.
- Default macOS Chrome executable path:
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Supported fallback executables on macOS:
  `/Applications/Chromium.app/Contents/MacOS/Chromium`
  `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`
- Default Windows Chrome executable path:
  `C:\Program Files\Google\Chrome\Application\chrome.exe`
- Supported fallback executables on Windows:
  `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
  `C:\Program Files\Chromium\Application\chrome.exe`
  `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- Do not fall back to bare `Chromium()` when a path, port, or launch configuration has already been provided.
- Prefer `ChromiumOptions().auto_port()` for default startup unless the user explicitly requires a fixed port.
- Before automation, verify the browser executable path exists and launch a minimal page.
- If startup fails, stop and diagnose startup first. Do not continue into business logic.

## Browser Startup Priority

Use this order every time:

1. User-provided browser path, port, and launch arguments
2. Previously validated workspace settings
3. Platform default path for the current machine
4. If none work, report the startup problem clearly and stop

## Core Workflow

```
1. Resolve browser configuration
2. Verify browser path exists
3. Start browser with ChromiumOptions
4. Open https://example.com
5. Confirm tab.title or tab.url
6. Continue with the real task
7. Capture sources, screenshots, and structured output
```

## Default Startup Template

Use this template unless the user has already given a different verified configuration.

```python
import sys
from pathlib import Path

from DrissionPage import Chromium, ChromiumOptions

# Cross-platform browser path resolution
# Override via DRISSIONPAGE_BROWSER_PATH env var or set chrome_path directly
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

## Startup Verification

Always verify startup before any real work:

```python
tab.get('https://example.com')
tab.wait.doc_loaded()

print('Startup title:', tab.title)
print('Startup url:', tab.url)
```

Proceed only after this succeeds.

## Failure Diagnosis Order

If browser startup or connection fails, diagnose in this order:

1. Browser executable path exists
2. `ChromiumOptions` is configured with the intended path and arguments
3. If you see a WebSocket handshake 404, retry with `ChromiumOptions().auto_port()`
4. The browser can be launched manually on the machine
5. `DrissionPage` is installed correctly
6. Connection or port mismatch with another browser instance
7. Only then investigate page selectors or business logic

## Parameter Reuse Rules

- If the user provides a path, port, URL, login step, or startup option, reuse it on all retries.
- Do not silently replace a user-provided path with a guessed path.
- If you retry with the user-provided configuration, say that explicitly.
- If the provided configuration is invalid, explain what failed and which value was used.

## Quick Reference

### Browser and Tab

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
    raise FileNotFoundError(chrome_path)

co = ChromiumOptions()
co.set_browser_path(chrome_path)
co.auto_port()

browser = Chromium(addr_or_opts=co)
tab = browser.latest_tab

print(tab.url)
print(tab.title)
```

### Finding Elements

```python
tab.ele('#my-id')
tab.ele('.my-class')
tab.ele('tag:div')
tab.eles('tag:a')
tab.ele('@name=username')
tab.ele('@placeholder:Search')
tab.ele('text:Submit')
tab.ele('text=Submit')
tab.ele('css:.container > .item')
tab.ele('xpath://div[@class="content"]')
```

### Interacting with Elements

```python
ele.click()
ele.click(by_js=True)

ele.input('Hello World')
ele.input('text\n')
ele.clear()

from DrissionPage.common import Keys
tab.actions.key_down(Keys.ENTER)
tab.actions.type('text')
```

### Getting Data

```python
ele.text
ele.attr('href')
ele.html

tab.html
tab.run_js('return document.body.innerText')
result = tab.run_js('return document.title')
```

### Scrolling

```python
tab.scroll.down(500)
tab.scroll.to_bottom()
tab.scroll.to_see(ele)
```

## Waiting Strategies

### Smart Waiting

```python
tab.wait.ele_displayed('#result', timeout=10)
tab.wait.ele_hidden('.loading', timeout=10)
tab.wait.ele_present('.content', timeout=10)
tab.wait.doc_loaded()
```

### Network Idle Wait

```python
from time import sleep

tab.wait.doc_loaded()
sleep(2)
tab.wait.ele_displayed('.data-loaded')
```

### Polling Pattern

```python
from time import sleep

def wait_for_data(tab, selector, max_wait=30):
    for _ in range(max_wait):
        ele = tab.ele(selector, timeout=1)
        if ele:
            return ele
        sleep(1)
    return None
```

## Network Listener

DrissionPage can intercept network responses, which is often more reliable than parsing HTML.

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
    raise FileNotFoundError(chrome_path)

co = ChromiumOptions()
co.set_browser_path(chrome_path)
co.auto_port()

browser = Chromium(addr_or_opts=co)
tab = browser.latest_tab

tab.get('https://example.com')
tab.wait.doc_loaded()

tab.listen.start('api/data')
tab.refresh()

for packet in tab.listen.steps(timeout=10):
    if packet.url.endswith('api/data'):
        print(packet.response.body)
        break

tab.listen.stop()
```

## Screenshots and Evidence Capture

Take screenshots on important pages by default, especially when the content will be used in research or slides.

```python
tab.get_screenshot(path='evidence/page.png')
tab.get_screenshot(path='evidence/full.png', full_page=True)
ele.get_screenshot(path='evidence/element.png')
```

For key findings, capture:

- source title
- source URL
- extraction time
- screenshot path if the page is visually important or unstable

## Image Download

DrissionPage can save images from page elements directly.

### Download Single Image

```python
img = tab.ele('tag:img')
img.save(path='./images', name='image.jpg')
img_bytes = img.src()
```

### Download Multiple Images

```python
import os

imgs = tab.eles('tag:img')
save_dir = './images'
os.makedirs(save_dir, exist_ok=True)

for i, img in enumerate(imgs):
    src = img.attr('src')
    if src and src.startswith('http'):
        try:
            path = img.save(path=save_dir, name=f'image_{i + 1}.jpg', timeout=10)
            print(f'Saved: {path}')
        except Exception as e:
            print(f'Failed: {e}')
```

## Error Handling

### Element Not Found

```python
ele = tab.ele('#maybe-exists', timeout=5)
if ele:
    ele.click()
else:
    print('Element not found, skipping...')

links = tab.eles('tag:a')
if links:
    for link in links:
        print(link.text)
```

### Page Load Timeout

```python
try:
    tab.get('https://slow-site.com', timeout=30)
except Exception as e:
    print(f'Page load failed: {e}')
```

### Handle Alerts and Popups

```python
tab.set.auto_handle_alert(accept=True)
alert_text = tab.handle_alert(accept=True, timeout=5)
print(f'Alert: {alert_text}')
```

## User Intervention Flow

For sites requiring login or captcha:

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
    raise FileNotFoundError(chrome_path)

co = ChromiumOptions()
co.set_browser_path(chrome_path)
co.auto_port()

browser = Chromium(addr_or_opts=co)
tab = browser.latest_tab

tab.get('https://example.com/login')
print('Please log in or complete captcha in the browser window...')
from time import sleep
sleep(60)

tab.wait.ele_displayed('text:Welcome', timeout=120)
tab.get('https://example.com/dashboard')
```

If the environment is non-interactive, do not use `input()` to hold the browser open. Prefer a fixed `sleep()` window or let a CLI flag control the wait time.

## Research Workflow

Use this default sequence for browser-based research:

1. Resolve browser settings and verify startup with `example.com`
2. Open the target page
3. Extract page facts, links, or structured data
4. Record the source title and source URL
5. Save a screenshot for key pages or unstable content
6. Return structured output

## Structured Output Template

For research and collection tasks, prefer this minimum output structure:

```text
Title: <source title>
URL: <source url>
Core finding: <one-paragraph summary>
Slide-ready line: <one sentence suitable for a presentation>
Visualization idea: <chart, screenshot, quote, or diagram suggestion>
Needs manual review: <yes/no and why>
```

## Common Website Examples

### Bilibili

```python
tab.get('https://www.bilibili.com')

videos = tab.run_js('''
var result = [];
var cards = document.querySelectorAll('.bili-video-card');
cards.forEach(function(card) {
    var titleEl = card.querySelector('.bili-video-card__info--tit');
    var linkEl = card.querySelector('a[href*="/video/"]');
    var authorEl = card.querySelector('.bili-video-card__info--author');
    if (titleEl && linkEl) {
        result.push({
            title: titleEl.innerText.trim(),
            href: linkEl.href,
            author: authorEl ? authorEl.innerText.trim() : ''
        });
    }
});
return result;
''')
```

### 百度热搜

```python
tab.get('https://top.baidu.com/board?tab=realtime')

items = tab.run_js('''
var items = document.querySelectorAll(".category-wrap_iQLoo .content_1YWBm");
var result = [];
items.forEach(function(item, i) {
    var title = item.querySelector(".title_dIF3B");
    if (title) {
        result.push({ rank: i + 1, title: title.innerText.trim() });
    }
});
return result;
''')
```

### 微博热搜

```python
tab.get('https://s.weibo.com/top/summary')

items = tab.eles('css:.data tbody tr')
for item in items:
    text = item.ele('tag:a').text
    print(text)
```

### 知乎热榜

```python
tab.get('https://www.zhihu.com/hot')

items = tab.eles('css:.HotList-item')
for item in items:
    title = item.ele('css:.HotItem-title').text
    print(title)
```

## Common Patterns

### Search Engine Query

```python
from DrissionPage.common import Keys

tab.get('https://www.baidu.com')
search_box = tab.ele('#kw')
search_box.input('search query')
tab.actions.key_down(Keys.ENTER)

tab.wait.ele_displayed('#content_left', timeout=10)
results = tab.eles('tag:h3')
for r in results:
    print(r.text)
```

### Form Submission

```python
tab.ele('@name=username').input('user@example.com')
tab.ele('@name=password').input('password123')
tab.ele('text:Login').click()
```

### Scrape Links

```python
links = tab.eles('tag:a')
for link in links:
    text = link.text.strip()
    href = link.attr('href')
    if text and href:
        print(f'{text}: {href}')
```

### Infinite Scroll

```python
from time import sleep

last_count = 0
while True:
    items = tab.eles('.item')
    if len(items) == last_count:
        break
    last_count = len(items)
    tab.scroll.to_bottom()
    sleep(2)
```

## Tips

1. Treat browser startup validation as part of the task, not as optional setup.
2. Prefer explicit `ChromiumOptions` and `auto_port()` over implicit defaults.
3. For API-driven sites, network listeners are often more reliable than DOM scraping.
4. Use screenshots to preserve evidence for key pages.
5. When selectors are unstable, use `run_js()` to extract data.
6. For dynamic pages, always wait for the right state before reading data.
7. In non-interactive environments, use timed waits instead of `input()`.
8. Reuse validated settings inside the same workspace.

## Dependencies

- Python 3.7+
- DrissionPage: `pip install DrissionPage`
- A runnable Chromium-based browser executable path
