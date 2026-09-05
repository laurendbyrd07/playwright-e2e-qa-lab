"""Cart page — items, removal, and navigation toward checkout."""
from playwright.sync_api import expect

from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    ITEMS = '[data-test="cart-list"] .cart_item'
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    CHECKOUT = '[data-test="checkout"]'
    CONTINUE_SHOPPING = '[data-test="continue-shopping"]'
    REMOVE_PREFIX = '[data-test^="remove-"]'

    def item_names(self) -> list[str]:
        return self.locator(self.ITEM_NAME).all_inner_texts()

    def item_prices(self) -> list[str]:
        return self.locator(self.ITEM_PRICE).all_inner_texts()

    def remove_first_item(self) -> None:
        self.locator(self.REMOVE_PREFIX).first.click()

    def assert_item_count(self, count: int) -> None:
        expect(self.locator(self.ITEMS)).to_have_count(count)

    def checkout(self) -> None:
        self.page.click(self.CHECKOUT)

    def continue_shopping(self) -> None:
        self.page.click(self.CONTINUE_SHOPPING)
