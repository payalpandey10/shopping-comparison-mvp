"""
matching/apply_matches.py
---------------------------
Runs the matcher against all UNMATCHED raw_listings and actually
WRITES the result to the database:

    - If a match is found  -> update raw_listing.matched_product_id
    - If no match is found -> create a brand new matched_product,
                               then link the listing to it

Run with (from backend/ folder, venv active):
    python -m app.matching.apply_matches

NOTE: unlike run_matcher.py (which only prints, "dry run"), this
script actually changes your database.
"""

from ..database import SessionLocal
from ..models import RawListing, MatchedProduct
from .matcher import find_matching_product
from .quantity_parser import parse_quantity

db = SessionLocal()

unmatched_listings = db.query(RawListing).filter(
    RawListing.matched_product_id.is_(None)
).all()

print(f"Found {len(unmatched_listings)} unmatched listing(s). Applying matcher...\n")

for listing in unmatched_listings:
    all_products = db.query(MatchedProduct).all()
    result = find_matching_product(listing, all_products)

    if result:
        listing.matched_product_id = result.id
        db.commit()
        print(f"MATCHED  \"{listing.raw_title}\" -> {result.brand} - {result.product_name}")

    else:
        value, unit = parse_quantity(listing.raw_quantity_text)

        new_product = MatchedProduct(
            brand="Unknown",
            product_name=listing.raw_title,
            shade_or_color=None,
            quantity_value=value,
            quantity_unit=unit,
            pack_count=1,
            category=None,
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        listing.matched_product_id = new_product.id
        db.commit()
        print(f"NEW PRODUCT created for \"{listing.raw_title}\" -> matched_product id {new_product.id}")

print("\nDone.")

db.close()