"""Fixtures for the Playwright E2E lab.

The authentication pattern here is deliberate and different from naive
login-before-every-test: we log in ONCE per session, save the authenticated
browser state (cookies + storage) via Playwright's storage_state, and reuse
it for every test that needs a logged-in user. This is the modern approach —
fast, and it mirrors how real suites handle authenticated areas.
"""
from pathlib import Path

import pytest

from pages.login_page import LoginPage
from testdata import users

STATE_FILE = Path("test-results/auth/state.json")


@pytest.fixture(scope="session")
def auth_state(browser):
    """Log in once, persist the storage state, hand the file path to tests."""
    context = browser.new_context()
    page = context.new_page()
    LoginPage(page).goto().login(users.STANDARD_USER, users.PASSWORD)
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(STATE_FILE))
    context.close()
    return str(STATE_FILE)


@pytest.fixture
def auth_page(browser, auth_state):
    """A fresh page already authenticated via the saved storage state.

    Fresh context per test keeps isolation (cart contents don't leak between
    tests) while still reusing the session cookie.
    """
    context = browser.new_context(storage_state=auth_state)
    page = context.new_page()
    yield page
    context.close()
