"""Expected product catalog (SauceDemo's stable demo dataset).

Kept in test data — not hardcoded into tests — so product changes are a
one-file update. Prices are Decimals exactly as displayed ($x.xx).
"""
from decimal import Decimal

CATALOG = [
    {
        "id": "sauce-labs-backpack",
        "name": "Sauce Labs Backpack",
        "price": Decimal("29.99"),
    },
    {
        "id": "sauce-labs-bike-light",
        "name": "Sauce Labs Bike Light",
        "price": Decimal("9.99"),
    },
    {
        "id": "sauce-labs-bolt-t-shirt",
        "name": "Sauce Labs Bolt T-Shirt",
        "price": Decimal("15.99"),
    },
    {
        "id": "sauce-labs-fleece-jacket",
        "name": "Sauce Labs Fleece Jacket",
        "price": Decimal("49.99"),
    },
    {
        "id": "sauce-labs-onesie",
        "name": "Sauce Labs Onesie",
        "price": Decimal("7.99"),
    },
    {
        "id": "test-all-the-things-t-shirt-red",
        "name": "Test.allTheThings() T-Shirt (Red)",
        "price": Decimal("7.99"),
    },
]

BY_ID = {p["id"]: p for p in CATALOG}
BY_NAME = {p["name"]: p for p in CATALOG}


def add_to_cart_selector(product_id: str) -> str:
    return f'[data-test="add-to-cart-{product_id}"]'


def remove_selector(product_id: str) -> str:
    return f'[data-test="remove-{product_id}"]'
