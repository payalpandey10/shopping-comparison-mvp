"""
matching/brand_normalizer.py
------------------------------
Cleans up brand names so different spellings/cases match correctly.
"""

BRAND_ALIASES = {
    "hb": "huda beauty",
    "mnyc": "maybelline",
}


def normalize_brand(raw_brand: str) -> str:
    if not raw_brand:
        return ""
    cleaned = raw_brand.strip().lower()
    return BRAND_ALIASES.get(cleaned, cleaned)


if __name__ == "__main__":
    tests = ["Huda Beauty", "HUDA BEAUTY", "HB", "Maybelline", "  Lakme  "]
    for t in tests:
        print(f"{t!r:20} -> {normalize_brand(t)!r}")