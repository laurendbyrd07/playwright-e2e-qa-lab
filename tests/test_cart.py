"""Cart behavior — add, badge counts, removal, and navigation."""
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from testdata.products import BY_ID

pytestmark = pytest.mark.regression


def test_adding_item_updates_badge_and_cart(auth_page):
    inventory = InventoryPage(auth_page).goto()
    inventory.add_to_cart("sauce-labs-backpack")

    inventory.assert_badge_count(1)
    inventory.open_cart()
    cart = CartPage(auth_page)

    cart.assert_item_count(1)
    assert cart.item_names() == [BY_ID["sauce-labs-backpack"]["name"]]


def test_remove_from_cart_updates_badge(auth_page):
    inventory = InventoryPage(auth_page).goto()
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bike-light")

    inventory.assert_badge_count(2)
    inventory.remove_from_cart("sauce-labs-backpack")
    inventory.assert_badge_count(1)

    inventory.open_cart()
    CartPage(auth_page).assert_item_count(1)


def test_continue_shopping_returns_to_inventory(auth_page):
    inventory = InventoryPage(auth_page).goto()
    inventory.add_to_cart("sauce-labs-onesie")
    inventory.open_cart()

    CartPage(auth_page).continue_shopping()

    InventoryPage(auth_page).assert_url_contains("/inventory.html")
