"""Checkout flow: step one (buyer info) and step two (order overview + math)."""
import re
from decimal import Decimal

from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutStepOne(BasePage):
    path = "/checkout-step-one.html"

    FIRST_NAME = '[data-test="firstName"]'
    LAST_NAME = '[data-test="lastName"]'
    POSTAL_CODE = '[data-test="postalCode"]'
    CONTINUE = '[data-test="continue"]'
    ERROR = '[data-test="error"]'

    def fill(self, first: str | None = None, last: str | None = None,
             postal: str | None = None) -> "CheckoutStepOne":
        if first is not None:
            self.page.fill(self.FIRST_NAME, first)
        if last is not None:
            self.page.fill(self.LAST_NAME, last)
        if postal is not None:
            self.page.fill(self.POSTAL_CODE, postal)
        return self

    def continue_to_overview(self) -> None:
        self.page.click(self.CONTINUE)

    def assert_field_error(self, fragment: str) -> None:
        expect(self.page.locator(self.ERROR)).to_contain_text(fragment)


class CheckoutOverviewPage(BasePage):
    """Step two — the financial summary. The math verification lives here because
    'the totals look right' is exactly the kind of thing users trust blindly."""

    path = "/checkout-step-two.html"

    CART_ITEMS = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    SUBTOTAL_LABEL = ".summary_subtotal_label"
    TAX_LABEL = ".summary_tax_label"
    TOTAL_LABEL = ".summary_total_label"
    FINISH = '[data-test="finish"]'

    @staticmethod
    def _money(label_text: str) -> Decimal:
        match = re.search(r"\$([\d.]+)", label_text)
        assert match, f"No dollar amount found in: {label_text!r}"
        return Decimal(match.group(1))

    def item_names(self) -> list[str]:
        return self.locator(self.CART_ITEM_NAME).all_inner_texts()

    def item_prices(self) -> list[Decimal]:
        raw = self.locator(self.ITEM_PRICE).all_inner_texts()
        return [Decimal(t.removeprefix("$")) for t in raw]

    def subtotal(self) -> Decimal:
        return self._money(self.locator(self.SUBTOTAL_LABEL).inner_text())

    def tax(self) -> Decimal:
        return self._money(self.locator(self.TAX_LABEL).inner_text())

    def total(self) -> Decimal:
        return self._money(self.locator(self.TOTAL_LABEL).inner_text())

    def assert_cart_item_count(self, count: int) -> None:
        expect(self.locator(self.CART_ITEMS)).to_have_count(count)

    def finish(self) -> None:
        self.page.click(self.FINISH)


class OrderConfirmationPage(BasePage):
    path = "/checkout-complete.html"

    HEADER = ".complete-header"

    def assert_thank_you(self) -> None:
        expect(self.page.locator(self.HEADER)).to_have_text("Thank you for your order!")
