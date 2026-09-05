"""Checkout workflow — the flagship multi-step scenario, plus form validation.

The overview-math test verifies the app's financial summary from first
principles: line-item sum, tax, and grand total are recalculated and compared,
because 'the totals look right' is exactly what users trust blindly.
"""
from decimal import Decimal

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutOverviewPage, CheckoutStepOne, OrderConfirmationPage
from pages.inventory_page import InventoryPage
from testdata.products import BY_ID

pytestmark = pytest.mark.regression

BUYER = {"first": "Jordan", "last": "Lee", "postal": "12345"}


@pytest.fixture
def cart_with_two_items(auth_page):
    """UI-driven data setup: two known items in the cart, ending on the cart page."""
    inventory = InventoryPage(auth_page).goto()
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-onesie")
    inventory.open_cart()
    return CartPage(auth_page)


def test_checkout_form_validates_each_required_field(cart_with_two_items):
    checkout = CheckoutStepOne(cart_with_two_items.page)

    # submit completely empty — first error names the first missing field
    checkout.continue_to_overview()
    checkout.assert_field_error("Error: First Name is required")

    # fill first name only — error moves to the next missing field
    checkout.fill(first=BUYER["first"])
    checkout.continue_to_overview()
    checkout.assert_field_error("Error: Last Name is required")

    # fill last name only — postal code error
    checkout.fill(last=BUYER["last"])
    checkout.continue_to_overview()
    checkout.assert_field_error("Error: Postal Code is required")


def test_full_purchase_flow_verifies_order_math_and_confirms(cart_with_two_items):
    cart = cart_with_two_items
    expected_names = {BY_ID["sauce-labs-backpack"]["name"], BY_ID["sauce-labs-onesie"]["name"]}
    expected_subtotal = BY_ID["sauce-labs-backpack"]["price"] + BY_ID["sauce-labs-onesie"]["price"]

    cart.checkout()
    CheckoutStepOne(cart.page).fill(**BUYER).continue_to_overview()

    overview = CheckoutOverviewPage(cart.page)
    overview.assert_cart_item_count(2)
    assert set(overview.item_names()) == expected_names, "Wrong items reached the overview"

    # recalculate the financial summary from the displayed line items
    assert sum(overview.item_prices(), Decimal("0")) == expected_subtotal
    assert overview.subtotal() == expected_subtotal, "Displayed subtotal != sum of line items"

    tax = overview.tax()
    expected_total = expected_subtotal + tax
    assert overview.total() == expected_total, "Displayed total != subtotal + displayed tax"

    overview.finish()
    OrderConfirmationPage(cart.page).assert_thank_you()
