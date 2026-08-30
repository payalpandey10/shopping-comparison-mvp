"""
matching/run_matcher.py
------------------------
Runs the matcher against all UNMATCHED raw_listings in the database
and reports what it decides -- without actually saving anything yet.
"""

from ..database import SessionLocal
from ..models import RawListing, MatchedProduct
from .matcher import find_matching_product

db = SessionLocal()

unmatched_listings = db.query(RawListing).filter(
    RawListing.matched_product_id.is_(None)
).all()

all_products = db.query(MatchedProduct).all()

print(f"Found {len(unmatched_listings)} unmatched listing(s). Testing matcher...\n")

for listing in unmatched_listings:
    result = find_matching_product(listing, all_products)
    print(f"Listing: \"{listing.raw_title}\" ({listing.raw_quantity_text})")
    if result:
        print(f"  -> WOULD MATCH: {result.brand} - {result.product_name} "
              f"({result.quantity_value}{result.quantity_unit})")
    else:
        print("  -> NO MATCH (would become a new product)")
    print()

db.close()