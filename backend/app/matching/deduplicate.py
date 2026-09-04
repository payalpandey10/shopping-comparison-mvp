"""
matching/deduplicate.py
--------------------------
Finds and merges DUPLICATE matched_products already in your database.

Run with (from backend/ folder, venv active):
    python -m app.matching.deduplicate
"""

from ..database import SessionLocal
from ..models import MatchedProduct, RawListing
from .brand_normalizer import normalize_brand
from .text_similarity import name_similarity, NAME_SIMILARITY_THRESHOLD

db = SessionLocal()

all_products = db.query(MatchedProduct).order_by(MatchedProduct.id).all()
print(f"Checking {len(all_products)} products for duplicates...\n")

merged_away = set()
merge_count = 0

for i, product_a in enumerate(all_products):
    if product_a.id in merged_away:
        continue

    for product_b in all_products[i + 1:]:
        if product_b.id in merged_away:
            continue

        if normalize_brand(product_a.brand) != normalize_brand(product_b.brand):
            continue

        if product_a.quantity_value is None or product_b.quantity_value is None:
            continue
        if float(product_a.quantity_value) != float(product_b.quantity_value):
            continue
        if product_a.quantity_unit != product_b.quantity_unit:
            continue

        score = name_similarity(product_a.product_name, product_b.product_name)
        if score < NAME_SIMILARITY_THRESHOLD:
            continue

        print(f"DUPLICATE (score={score:.2f}):")
        print(f"  Keeping:  [{product_a.id}] {product_a.brand} - {product_a.product_name[:60]}")
        print(f"  Merging:  [{product_b.id}] {product_b.brand} - {product_b.product_name[:60]}")

        listings_to_move = db.query(RawListing).filter(
            RawListing.matched_product_id == product_b.id
        ).all()
        for listing in listings_to_move:
            listing.matched_product_id = product_a.id

        db.delete(product_b)
        db.commit()

        merged_away.add(product_b.id)
        merge_count += 1
        print()

print(f"=== Done. Merged {merge_count} duplicate product(s). ===")
db.close()