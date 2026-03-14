"""
Quick start helper for DrissionPage browser automation.
Run this to test your installation and see basic usage.
"""

from DrissionPage import Chromium
from DrissionPage.common import Keys
from time import sleep


def test_browser():
    print("Starting browser...")
    browser = Chromium()
    tab = browser.latest_tab
    
    print("Opening Baidu...")
    tab.get('https://www.baidu.com')
    sleep(1)
    
    print(f"Page title: {tab.title}")
    print(f"URL: {tab.url}")
    
    print("\nSearching for 'DrissionPage'...")
    search = tab.ele('#kw')
    search.input('DrissionPage')
    tab.actions.key_down(Keys.ENTER)
    sleep(2)
    
    print(f"\nResults page: {tab.url}")
    
    results = tab.eles('tag:h3')
    print(f"Found {len(results)} result headings")
    
    print("\nBrowser test complete!")
    print("The browser will stay open. Run Chromium() again to reconnect.")


if __name__ == '__main__':
    test_browser()