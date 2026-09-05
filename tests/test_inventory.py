"""Inventory browsing and sorting — with real data verification.

Sorting tests verify the *data* (names/price sequences), not just that the
control changed — a sort bug that produces the wrong order fails loudly.
"""
from decimal import Decimal

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from testdata import users
from testdata.products import CATALOG

pytestmark = pytest.mark.regression

EXPECTED_NAMES_AZ = sorted(p["name"] for p in CATALOG)


def test_all_catalog_items_display_with_expected_prices(auth_page):
    inventory = InventoryPage(auth_page).goto()

    names = inventory.visible_names()
    prices = inventory.visible_prices()

    assert sorted(names) == EXPECTED_NAMES_AZ, "Catalog contents changed"
    assert sorted(prices) == sorted(p["price"] for p in CATALOG), "Catalog prices changed"


def test_default_sort_is_name_ascending(auth_page):
    inventory = InventoryPage(auth_page).goto()
    assert inventory.visible_names() == EXPECTED_NAMES_AZ


def test_sort_name_descending(auth_page):
    inventory = InventoryPage(auth_page).goto()
    inventory.sort_by("za")
    assert inventory.visible_names() == list(reversed(EXPECTED_NAMES_AZ))


def test_sort_price_low_to_high(auth_page):
    inventory = InventoryPage(auth_page).goto()
    inventory.sort_by("lohi")

    prices = inventory.visible_prices()
    assert prices == sorted(prices), "Prices are not in ascending order"
    assert prices == [Decimal("7.99"), Decimal("7.99"), Decimal("9.99"),
                      Decimal("15.99"), Decimal("29.99"), Decimal("49.99")]


def test_sort_price_high_to_low(auth_page):
    inventory = InventoryPage(auth_page).goto()
    inventory.sort_by("hilo")

    prices = inventory.visible_prices()
    assert prices == sorted(prices, reverse=True), "Prices are not in descending order"
    assert prices[0] == Decimal("49.99") and prices[-1] == Decimal("7.99")


@pytest.mark.smoke
def test_product_images_all_render(auth_page):
    """Every product image must actually load — not just exist in the DOM."""
    inventory = InventoryPage(auth_page).goto()
    load_states = inventory.image_load_states()
    assert len(load_states) == 6
    broken = [i for i, ok in enumerate(load_states) if not ok]
    assert all(load_states), f"Broken product images at indices: {broken}"


@pytest.mark.failure_detection
def test_problem_user_visual_defect_is_detected(page):
    """Known-defect detection: the 'problem user' persona ships broken product
    images. This test proves the suite catches visual failures, not just
    functional ones — the same check that passed for the standard user fails
    here, by design of the target app."""
    LoginPage(page).goto().login(users.PROBLEM_USER, users.PASSWORD)

    inventory = InventoryPage(page)
    load_states = inventory.image_load_states()
    broken = [i for i, ok in enumerate(load_states) if not ok]
    assert broken, "Expected problem_user broken images — visual failure not detected"
