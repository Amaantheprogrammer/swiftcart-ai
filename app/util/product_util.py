import re

_NUMBER = r"(?:₹\s*)?(\d[\d,]*(?:\.\d+)?)"

_PRICE_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        rf"\bunder\s+{_NUMBER}",
        rf"\bbelow\s+{_NUMBER}",
        rf"\bless\s+than\s+{_NUMBER}",
        rf"\bmaximum\s+(?:price\s+)?(?:of\s+)?{_NUMBER}",
        rf"\bmax(?:imum)?\s+(?:budget|price)\s*(?:is|of|:)?\s*{_NUMBER}",
        rf"\bbudget\s*(?:is|of|:)?\s*{_NUMBER}",
    ]
]


def extract_max_price(message: str) -> float | None:
    for pattern in _PRICE_PATTERNS:
        match = pattern.search(message)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                pass
    return None


def filter_products_by_price(products: list[dict], max_price: float) -> list[dict]:
    return [
        p
        for p in products
        if isinstance(p.get("price"), (int, float)) and p["price"] <= max_price
    ]


def filter_products_by_category(products: list[dict], category: str) -> list[dict]:
    target = category.strip().lower()
    return [
        p
        for p in products
        if isinstance(p.get("categoryName"), str)
        and target in p["categoryName"].strip().lower()
    ]


def extract_category(products: list[dict], message: str) -> str | None:
    msg = message.lower()
    categories = {
        p["categoryName"].strip()
        for p in products
        if isinstance(p.get("categoryName"), str) and p["categoryName"].strip()
    }
    for category in sorted(categories, key=len, reverse=True):
        if category.lower() in msg:
            return category
    return None
