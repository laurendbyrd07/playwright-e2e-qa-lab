"""Login page (start page)."""
import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    USERNAME = '[data-test="username"]'
    PASSWORD = '[data-test="password"]'
    SUBMIT = '[data-test="login-button"]'
    ERROR = '[data-test="error"]'

    def login(self, username: str, password: str) -> "LoginPage":
        self.page.fill(self.USERNAME, username)
        self.page.fill(self.PASSWORD, password)
        self.page.click(self.SUBMIT)
        return self

    def assert_login_succeeded(self) -> None:
        """Successful login lands on the inventory page."""
        expect(self.page).to_have_url(re.compile(r".*/inventory\.html"))

    def assert_login_failed_with(self, message: str) -> None:
        expect(self.page.locator(self.ERROR)).to_contain_text(message)
        # and we must still be on the login screen
        expect(self.page.locator(self.SUBMIT)).to_be_visible()
