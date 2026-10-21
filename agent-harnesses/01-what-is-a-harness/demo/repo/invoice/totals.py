"""Invoice totals: subtotal, discount, tax."""

from . import discounts

TAX_RATE = 0.18


def subtotal(items):
    return sum(price * qty for price, qty in items)


def invoice_total(items, discount_code=None):
    """Total for a list of (price, quantity) pairs, after discount and tax."""
    amount = subtotal(items)
    percent_off = discounts.lookup(discount_code)
    amount = amount * (1 - percent_off / 100)
    return round(amount * (1 + TAX_RATE), 2)
