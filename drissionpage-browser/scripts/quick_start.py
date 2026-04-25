"""
Quick start helper for DrissionPage browser automation.

This script follows the same startup contract documented in SKILL.md:
1. Prefer an explicit browser path from the environment
2. Otherwise use a known working platform path (macOS / Windows)
3. Verify startup with example.com before running any real task
"""

import argparse
import os
import sys
from pathlib import Path
from time import sleep

from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Keys


DEFAULT_CANDIDATES_WIN = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Chromium\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

DEFAULT_CANDIDATES_MAC = [
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

    candidates = DEFAULT_CANDIDATES_WIN if sys.platform.startswith("win") else DEFAULT_CANDIDATES_MAC

    for candidate in candidates:
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
    options.auto_port()
    return Chromium(addr_or_opts=options)


def verify_startup(tab):
    """Validate browser startup before business automation continues."""
    tab.get("https://example.com")
    tab.wait.doc_loaded()
    print("Startup title:", tab.title)
    print("Startup url:", tab.url)


def test_browser(keep_open_seconds=0):
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
    if keep_open_seconds > 0:
        print(f"Keeping browser open for {keep_open_seconds} seconds...")
        sleep(keep_open_seconds)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--keep-open-seconds",
        type=int,
        default=0,
        help="Keep the browser window open for N seconds after the test finishes.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    test_browser(keep_open_seconds=args.keep_open_seconds)
