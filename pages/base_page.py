"""Base page — wraps the Playwright Page with small, intention-revealing helpers.

Playwright locators auto-wait, so unlike the Selenium lab there is no explicit
wait management here — the framework's auto-waiting IS the wait strategy, and
assertions use Playwright's expect() polling.
"""
import re
from typing import Pattern, Union

from playwright.sync_api import Locator, Page, expect

import config

UrlLike = Union[str, Pattern]


class BasePage:
    path: str = ""

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, path: str | None = None) -> "BasePage":
        self.page.goto(f"{config.BASE_URL}{path if path is not None else self.path}")
        return self

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def assert_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))
