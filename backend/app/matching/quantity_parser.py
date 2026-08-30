"""
matching/quantity_parser.py
----------------------------
Extracts a clean (value, unit) pair from messy retailer quantity text.

Examples this needs to handle:
    "7.6 ml"    -> (7.6, "ml")
    "7.6ml"     -> (7.6, "ml")
    "100g"      -> (100.0, "g")
    "100 g"     -> (100.0, "g")
    "1 kg"      -> (1.0, "kg")
    "5 ml"      -> (5.0, "ml")
"""

import re

KNOWN_UNITS = ["ml", "l", "kg", "g", "gb", "tb"]


def parse_quantity(raw_text: str):
    """
    Takes raw quantity text (e.g. "7.6 ml") and returns a tuple:
        (value: float, unit: str) e.g. (7.6, "ml")
    Returns (None, None) if nothing could be parsed.
    """
    if not raw_text:
        return None, None

    text = raw_text.lower().strip()
    match = re.search(r"(\d+(?:\.\d+)?)\s*([a-z]+)", text)
    if not match:
        return None, None

    value_str, unit_str = match.groups()
    if unit_str not in KNOWN_UNITS:
        return None, None

    return float(value_str), unit_str


if __name__ == "__main__":
    test_cases = ["7.6 ml", "7.6ml", "100g", "100 g", "1 kg", "5 ml", "garbage text"]
    for case in test_cases:
        print(f"{case!r:20} -> {parse_quantity(case)}")
        