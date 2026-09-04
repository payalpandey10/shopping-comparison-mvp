"""
matching/matcher.py
--------------------
The core matching decision: given a raw_listing, decide which
matched_product (if any) it belongs to.

Matching rule (all must be true to count as a match):
    1. Brand matches exactly (after normalization)          -- STRICT
    2. Quantity value + unit matches exactly                -- STRICT
    3. Product name is "similar enough" (fuzzy)              -- FLEXIBLE
"""

from .quantity_parser import parse_quantity
from .brand_normalizer import normalize_brand, BRAND_ALIASES
from .text_similarity import name_similarity, NAME_SIMILARITY_THRESHOLD


def expand_aliases_in_text(text: str) -> str:
    """
    Replaces any known short-form brand alias found INSIDE a raw title
    with its full canonical name, so brand-matching can find it.
    Example: "HB Lash Sensational..." -> "huda beauty Lash Sensational..."
    """
    lowered = text.lower()
    for alias, full_name in BRAND_ALIASES.items():
        words = lowered.split()
        words = [full_name if w.strip("-,.()") == alias else w for w in words]
        lowered = " ".join(words)
    return lowered


def find_matching_product(raw_listing, candidate_products):
    listing_value, listing_unit = parse_quantity(raw_listing.raw_quantity_text)
    if listing_value is None:
        return None

    expanded_title = expand_aliases_in_text(raw_listing.raw_title)

    for product in candidate_products:
        if normalize_brand(product.brand) not in expanded_title:
            continue

        if product.quantity_value is None:
            continue
        if float(product.quantity_value) != listing_value:
            continue
        if product.quantity_unit != listing_unit:
            continue

        score = name_similarity(raw_listing.raw_title, product.product_name)
        if score >= NAME_SIMILARITY_THRESHOLD:
            return product

    return None