"""
matching/fix_unknown_brands.py
---------------------------------
ONE-TIME cleanup: updates existing matched_products with brand="Unknown"
to use a real guessed brand instead.

Run with (from backend/ folder, venv active):
    python -m app.matching.fix_unknown_brands
"""

from ..database import SessionLocal
from ..models import MatchedProduct
from .brand_extractor import guess_brand

db = SessionLocal()

unknown_products = db.query(MatchedProduct).filter(
    MatchedProduct.brand == "Unknown"
).all()

print(f"Found {len(unknown_products)} products with brand='Unknown'. Fixing...\n")

fixed = 0
for product in unknown_products:
    new_brand = guess_brand(product.product_name)
    print(f"  '{product.product_name[:50]}...' -> {new_brand}")
    product.brand = new_brand
    fixed += 1

db.commit()
print(f"\nFixed {fixed} products.")
db.close()