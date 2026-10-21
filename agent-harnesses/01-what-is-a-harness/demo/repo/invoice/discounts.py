"""Discount codes and how much each one takes off."""

CODES = {
    "WELCOME10": 10,
    "SPRING15": 15,
    "VIP25": 25,
}


def lookup(code):
    """Return the discount for a code as a fraction, e.g. 0.10 for 10%."""
    if not code:
        return 0.0
    return CODES.get(code.strip().upper(), 0) / 100
