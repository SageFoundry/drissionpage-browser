---
name: drissionpage-browser
description: |
  Browser automation for web data collection and research. Use this skill when the user needs to search the web, query information, scrape data, debug websites, or perform any task requiring a browser. DrissionPage provides fast, persistent browser control with support for user interaction during login/captcha flows. Trigger when user mentions searching, browsing, web scraping, checking websites, getting web content, or any task that requires up-to-date internet information.
---

# DrissionPage Browser Automation

Browser automation for web data collection, research, and debugging using DrissionPage.

## When to Use

- User asks to search the web or query information
- User needs to scrape or collect data from websites
- User wants to check real-time information (news, prices, etc.)
- User mentions "open browser", "visit website", "click button"
- User needs to interact with websites that require login
- User wants to debug or test web applications
- User asks about current trends, hot topics, or recent events

## Core Workflow

```
1. Start/connect browser → Chromium()
2. Get tab object → browser.latest_tab
3. Navigate to URL → tab.get(url)
4. Find elements → tab.ele() / tab.eles()
5. Interact → click(), input(), scroll
6. Extract data → .text, .attr(), run_js()
7. Handle user intervention if needed (login/captcha)
```

## Quick Reference

### Browser & Tab

```python
from DrissionPage import Chromium

browser = Chromium()              # Start/connect browser (default port 9222)
tab = browser.latest_tab          # Get active tab
tab.get('https://example.com')    # Navigate to URL
print(tab.url)                    # Current URL
print(tab.title)                  # Page title
```

### Finding Elements

```python
# By ID
tab.ele('#my-id')

# By class
tab.ele('.my-class')

# By tag
tab.ele('tag:div')
tab.eles('tag:a')                 # Get all links

# By attribute
tab.ele('@name=username')         # name="username"
tab.ele('@placeholder:Search')    # placeholder contains "Search"

# By text
tab.ele('text:Submit')            # Text contains "Submit"
tab.ele('text=Submit')            # Text equals "Submit"

# CSS selector
tab.ele('css:.container > .item')

# XPath
tab.ele('xpath://div[@class="content"]')
```

### Interacting with Elements

```python
# Click
ele.click()                       # Normal click
ele.click(by_js=True)             # JS click (bypass overlays)

# Input
ele.input('Hello World')          # Type text
ele.input('text\n')               # Type and press Enter
ele.clear()                       # Clear input

# Keyboard actions
from DrissionPage.common import Keys
tab.actions.key_down(Keys.ENTER)  # Press Enter
tab.actions.type('text')          # Type with key simulation
```

### Getting Data

```python
# Element info
ele.text                          # Visible text
ele.attr('href')                  # Attribute value
ele.html                          # Inner HTML

# Page content
tab.html                          # Full HTML
tab.run_js('return document.body.innerText')  # Page text

# Execute JavaScript
result = tab.run_js('return document.title')
```

### Scrolling

```python
tab.scroll.down(500)              # Scroll down 500px
tab.scroll.to_bottom()            # Scroll to bottom
tab.scroll.to_see(ele)            # Scroll element into view
```

## Waiting Strategies

### Smart Waiting (Recommended)

```python
# Wait for element to appear
tab.wait.ele_displayed('#result', timeout=10)

# Wait for element to disappear (loading spinner)
tab.wait.ele_hidden('.loading', timeout=10)

# Wait for element to be in DOM
tab.wait.ele_present('.content', timeout=10)

# Wait for page load
tab.wait.doc_loaded()
```

### Network Idle Wait

```python
from time import sleep

# For AJAX-heavy sites, combine waits
tab.wait.doc_loaded()
sleep(2)  # Additional wait for JS execution
tab.wait.ele_displayed('.data-loaded')
```

### Polling Pattern

```python
from time import sleep

def wait_for_data(tab, selector, max_wait=30):
    """Poll until element appears or timeout."""
    for _ in range(max_wait):
        ele = tab.ele(selector, timeout=1)
        if ele:
            return ele
        sleep(1)
    return None
```

## Network Listener (Capture API Data)

DrissionPage can intercept network responses - more reliable than parsing HTML.

```python
from DrissionPage import Chromium

browser = Chromium()
tab = browser.latest_tab

# Start listening
tab.listen.start('api/data')  # Filter by URL pattern

# Trigger the request
tab.get('https://example.com')

# Wait and get response
for packet in tab.listen.steps(timeout=10):
    if packet.url.endswith('api/data'):
        data = packet.response.body  # JSON data
        print(data)
        break

# Stop listening
tab.listen.stop()
```

### Common Network Patterns

```python
# Listen for all XHR/Fetch requests
tab.listen.start('*.json')

# Listen for specific API
tab.listen.start('api/search')

# Get all captured packets
packets = tab.listen.wait()
for p in packets:
    print(p.url, p.response.body)
```

## Screenshots & Recording

```python
# Take screenshot
tab.get_screenshot(path='screenshot.png')

# Full page screenshot
tab.get_screenshot(path='full.png', full_page=True)

# Element screenshot
ele.get_screenshot(path='element.png')

# Start recording (for debugging)
tab.set.recorder.on()
# ... perform actions ...
tab.set.recorder.off()
```

## Error Handling

### Element Not Found

```python
# Safe element access
ele = tab.ele('#maybe-exists', timeout=5)
if ele:
    ele.click()
else:
    print("Element not found, skipping...")

# Use eles() for lists (returns empty list if none)
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
    print(f"Page load failed: {e}")
    tab.get('https://fallback.com')
```

### Handle Alerts/Popups

```python
# Handle alert automatically
tab.set.auto_handle_alert(accept=True)

# Or handle manually
alert_text = tab.handle_alert(accept=True, timeout=5)
print(f"Alert: {alert_text}")
```

## User Intervention Flow

For websites requiring login or captcha:

```python
from DrissionPage import Chromium

browser = Chromium()
tab = browser.latest_tab
tab.get('https://example.com/login')

# Prompt user to intervene
print("Please log in or complete captcha in the browser window...")
input("Press Enter when done...")

# Or wait for specific element that appears after login
tab.wait.ele_displayed('text:Welcome', timeout=120)

# Continue automation
tab.get('https://example.com/dashboard')
```

## Common Website Selectors

### B站 (bilibili.com)

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

### 百度热搜 (top.baidu.com)

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

### 微博热搜 (weibo.com)

```python
tab.get('https://s.weibo.com/top/summary')

# Hot search items usually in .data table
items = tab.eles('css:.data tbody tr')
for item in items:
    text = item.ele('tag:a').text
    print(text)
```

### 知乎 (zhihu.com)

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
from DrissionPage import Chromium
from DrissionPage.common import Keys

browser = Chromium()
tab = browser.latest_tab
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
        print(f"{text}: {href}")
```

### Infinite Scroll

```python
from time import sleep

last_count = 0
while True:
    items = tab.eles('.item')
    if len(items) == last_count:
        break  # No new items loaded
    last_count = len(items)
    tab.scroll.to_bottom()
    sleep(2)
```

## Tips

1. **Browser Persistence**: The browser stays open after script ends. Re-run `Chromium()` to reconnect.

2. **Clean Browser**: Each session starts with a fresh browser profile. Users can log in manually.

3. **Network Listener First**: For API-driven sites, use network listener instead of HTML parsing - more reliable.

4. **Debugging**: Use `tab.get_screenshot()` to capture page state when debugging.

5. **Complex Selectors**: When locator syntax fails, use `run_js()` with JavaScript.

6. **AJAX Content**: Always wait for dynamic content to load using `tab.wait.*` methods.

7. **Multiple Tabs**: Use `browser.new_tab()` and `browser.get_tab()` for multi-tab scenarios.

## Dependencies

- Python 3.7+
- DrissionPage: `pip install DrissionPage`
- Chromium-based browser (Chrome, Edge, etc.)