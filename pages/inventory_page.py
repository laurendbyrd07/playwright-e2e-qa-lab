"""Inventory (products) page — browsing, sorting, and cart-badge state."""
from decimal import Decimal

from playwright.sync_api import expect

from pages.base_page import BasePage
from testdata.products import add_to_cart_selector, remove_selector


class InventoryPage(BasePage):
    path = "/inventory.html"

    ITEMS = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_IMAGE = ".inventory_item_img img"
    SORT = '[data-test="product-sort-container"]'
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    BURGER = "#react-burger-menu-button"
    LOGOUT = "#logout_sidebar_link"

    def add_to_cart(self, product_id: str) -> "InventoryPage":
        self.page.click(add_to_cart_selector(product_id))
        return self

    def remove_from_cart(self, product_id: str) -> "InventoryPage":
        self.page.click(remove_selector(product_id))
        return self

    def visible_names(self) -> list[str]:
        return self.locator(self.ITEM_NAME).all_inner_texts()

    def visible_prices(self) -> list[Decimal]:
        raw = self.locator(self.ITEM_PRICE).all_inner_texts()
        return [Decimal(t.removeprefix("$")) for t in raw]

    def sort_by(self, option: str) -> "InventoryPage":
        """option: 'az' | 'za' | 'lohi' | 'hilo'"""
        self.page.select_option(self.SORT, option)
        return self

    def assert_badge_count(self, count: int) -> None:
        badge = self.page.locator(self.CART_BADGE)
        if count == 0:
            expect(badge).to_have_count(0)
        else:
            expect(badge).to_have_text(str(count))

    def open_cart(self) -> None:
        self.page.click(self.CART_LINK)

    def image_load_states(self) -> list[bool]:
        """True for every product image that actually rendered (naturalWidth > 0).

        Requires images finished loading — wait via a DOM condition, never a sleep.
        """
        self.page.wait_for_function(
            "Array.from(document.images).every(img => img.complete)"
        )
        return self.page.eval_on_selector_all(
            self.ITEM_IMAGE, "els => els.map(e => e.naturalWidth > 0)"
        )

    def logout(self) -> None:
        self.page.click(self.BURGER)
        self.page.click(self.LOGOUT)
