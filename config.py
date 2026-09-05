"""Environment-driven configuration.

Browser selection, headless mode, tracing, screenshots, and video are handled
by pytest-playwright's CLI (--browser, --headed, --tracing, ...) rather than
custom config — one canonical mechanism, documented in the README.
"""
import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
