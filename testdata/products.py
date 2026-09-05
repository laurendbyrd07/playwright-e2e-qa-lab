"""Expected product catalog (SauceDemo's stable demo dataset).

Prices verified against the deployed app's own catalog bundle (9/2026):
two items cost $15.99 — Bolt T-Shirt and the red tee — and only Onesie is $7.99.

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
        "price": Decimal("15.99"),
    },
]

BY_ID = {p["id"]: p for p in CATALOG}
BY_NAME = {p["name"]: p for p in CATALOG}


def _button_slug(label: str, product_id: str) -> str:
    """Replicates the app's own testId derivation:
    `${label}-${item}`.replace(/\\s+/g, '-').toLowerCase()
    (whitespace -> hyphens, lowercased; punctuation like () and . is kept)."""
    name = BY_ID[product_id]["name"]
    return f"{label}-{name}".replace(" ", "-").lower()


def add_to_cart_selector(product_id: str) -> str:
    return f'[data-test="{_button_slug("add-to-cart", product_id)}"]'


def remove_selector(product_id: str) -> str:
    return f'[data-test="{_button_slug("remove", product_id)}"]'
