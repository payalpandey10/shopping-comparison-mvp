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
script actually changes your database. Run run_matcher.py first if
you want to preview decisions before committing to them.
"""

from ..models import RawListing, MatchedProduct
from .matcher import find_matching_product
from .quantity_parser import parse_quantity
from .brand_extractor import guess_brand


def run_matching(db):
    """
    Runs matching against all unmatched raw_listings using the given
    database session, and returns a summary of what happened.

    This function is shared by:
      - apply_matches.py (manual script, run from terminal)
      - the /admin/run-matching API endpoint (automated trigger)
    Keeping the logic here in ONE place means both callers always
    behave identically -- no risk of the script and the API drifting
    apart over time.
    """
    unmatched_listings = db.query(RawListing).filter(
        RawListing.matched_product_id.is_(None)
    ).all()

    matched_count = 0
    new_product_count = 0
    results = []

    for listing in unmatched_listings:
        all_products = db.query(MatchedProduct).all()
        result = find_matching_product(listing, all_products)

        if result:
            listing.matched_product_id = result.id
            db.commit()
            matched_count += 1
            results.append({
                "listing_title": listing.raw_title,
                "action": "matched",
                "matched_product": f"{result.brand} - {result.product_name}",
            })

        else:
            value, unit = parse_quantity(listing.raw_quantity_text)
            guessed_brand = guess_brand(listing.raw_title)

            new_product = MatchedProduct(
                brand=guessed_brand,
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
            new_product_count += 1
            results.append({
                "listing_title": listing.raw_title,
                "action": "new_product_created",
                "matched_product_id": new_product.id,
            })

    return {
        "total_processed": len(unmatched_listings),
        "matched_to_existing": matched_count,
        "new_products_created": new_product_count,
        "details": results,
    }


if __name__ == "__main__":
    from ..database import SessionLocal

    db = SessionLocal()
    summary = run_matching(db)
    print(f"Processed {summary['total_processed']} unmatched listing(s).")
    print(f"  Matched to existing products: {summary['matched_to_existing']}")
    print(f"  New products created: {summary['new_products_created']}\n")
    for item in summary["details"]:
        print(item)
    db.close()