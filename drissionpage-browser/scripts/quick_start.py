"""
Quick start helper for DrissionPage browser automation.

This script follows the same startup contract documented in SKILL.md:
1. Prefer an explicit browser path from the environment
2. Otherwise use a known working macOS path
3. Verify startup with example.com before running any real task
"""

import os
from pathlib import Path
from time import sleep

from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Keys


DEFAULT_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def resolve_browser_path():
    """Resolve a browser path using explicit priority."""
    user_path = os.environ.get("DRISSIONPAGE_BROWSER_PATH")
    if user_path:
        candidate = Path(user_path).expanduser()
        if not candidate.exists():
            raise FileNotFoundError(
                f"Configured browser path does not exist: {candidate}"
            )
        return str(candidate), "user-provided"

    for candidate in DEFAULT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return str(path), "platform-default"

    raise FileNotFoundError(
        "No supported browser executable was found. "
        "Set DRISSIONPAGE_BROWSER_PATH or install Chrome/Chromium/Edge."
    )


def build_browser(browser_path):
    """Build a Chromium instance with explicit options."""
    options = ChromiumOptions()
    options.set_browser_path(browser_path)
    return Chromium(addr_or_opts=options)


def verify_startup(tab):
    """Validate browser startup before business automation continues."""
    tab.get("https://example.com")
    tab.wait.doc_loaded()
    print("Startup title:", tab.title)
    print("Startup url:", tab.url)


def test_browser():
    browser_path, source = resolve_browser_path()
    print(f"Using browser path ({source}): {browser_path}")

    browser = build_browser(browser_path)
    tab = browser.latest_tab

    print("Verifying browser startup...")
    verify_startup(tab)

    print("\nOpening Baidu...")
    tab.get("https://www.baidu.com")
    tab.wait.doc_loaded()
    sleep(1)

    print(f"Page title: {tab.title}")
    print(f"URL: {tab.url}")

    print("\nSearching for 'DrissionPage'...")
    search = tab.ele("#kw", timeout=10)
    if not search:
        raise RuntimeError("Search box not found on Baidu after startup verification.")

    search.input("DrissionPage")
    tab.actions.key_down(Keys.ENTER)
    sleep(2)

    print(f"\nResults page: {tab.url}")

    results = tab.eles("tag:h3")
    print(f"Found {len(results)} result headings")

    print("\nBrowser test complete!")
    print("If this succeeded, browser startup and task flow are both valid.")


if __name__ == "__main__":
    test_browser()
