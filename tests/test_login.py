"""Authentication workflows — positive, negative, and session teardown."""

import pytest
from playwright.sync_api import expect

import config
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from testdata import users

pytestmark = pytest.mark.regression


def test_valid_login_lands_on_inventory(page):
    LoginPage(page).goto().login(users.STANDARD_USER, users.PASSWORD)

    inventory = InventoryPage(page)
    inventory.assert_url_contains("/inventory.html")
    assert len(inventory.visible_names()) == 6, "Expected the full 6-product catalog"


def test_locked_out_user_is_rejected_with_specific_error(page):
    login = LoginPage(page).goto()
    login.login(users.LOCKED_OUT_USER, users.PASSWORD)
    login.assert_login_failed_with(users.LOCKED_OUT_ERROR)


def test_invalid_credentials_are_rejected(page):
    login = LoginPage(page).goto()
    login.login(users.INVALID_USERNAME, users.INVALID_PASSWORD)
    login.assert_login_failed_with(users.INVALID_CREDENTIALS_ERROR)


def test_logout_ends_the_session(page):
    login = LoginPage(page).goto()
    login.login(users.STANDARD_USER, users.PASSWORD)

    InventoryPage(page).logout()

    # back at the login screen...
    expect(page.locator('[data-test="login-button"]')).to_be_visible()
    # ...and the session is truly gone: direct navigation to the protected
    # page bounces back to login rather than showing inventory content.
    page.goto(f"{config.BASE_URL}/inventory.html")
    assert "/inventory.html" not in page.url, "Session survived logout — protected page reachable"
    expect(page.locator('[data-test="login-button"]')).to_be_visible()
