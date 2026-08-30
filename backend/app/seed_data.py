"""
seed_data.py
------------
Inserts mock/fake retailer listings into the database so we have
something real to search and compare, WITHOUT needing live scraping yet.

This matches Stage 1 of the plan: "controlled dataset/mock retailer data
so we can develop the intelligence without depending on live scraping."

This version has MULTIPLE products, each with MULTIPLE retailer listings,
including deliberately mismatched quantities (unmatched on purpose) --
exactly like the real messy data Stage 2's matching pipeline will need
to handle later.

Run this (from backend/ folder, venv activated) with:
    python -m app.seed_data

NOTE: this script clears old rows first, so you can safely re-run it
any time without ending up with duplicates.
"""

from .database import SessionLocal, engine, Base
from .models import MatchedProduct, RawListing, PriceHistory

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Clear old data first, so re-running this script doesn't duplicate rows ---
db.query(PriceHistory).delete()
db.query(RawListing).delete()
db.query(MatchedProduct).delete()
db.commit()


def add_price_point(listing, price):
    db.add(PriceHistory(raw_listing_id=listing.id, price=price))


# =========================================================
# Product 1: Huda Beauty Mascara (your original example)
# =========================================================
huda_mascara = MatchedProduct(
    brand="Huda Beauty",
    product_name="Lash Sensational Waterproof Mascara",
    shade_or_color="Black",
    quantity_value=7.6,
    quantity_unit="ml",
    pack_count=1,
    category="Mascara",
)
db.add(huda_mascara)
db.commit()
db.refresh(huda_mascara)

huda_myntra = RawListing(
    retailer_name="Myntra",
    product_url="https://myntra.com/example-huda-mascara",
    raw_title="Huda Beauty Lash Sensational Waterproof Mascara 7.6ml",
    raw_price=2199,
    raw_quantity_text="7.6 ml",
    seller_name="Myntra Beauty Store",
    image_url="",
    matched_product_id=huda_mascara.id,
)
huda_sephora = RawListing(
    retailer_name="Sephora",
    product_url="https://sephora.com/example-huda-mascara",
    raw_title="Huda Beauty - Lash Sensational Mascara - Waterproof - 7.6 ml",
    raw_price=2299,
    raw_quantity_text="7.6 ml",
    seller_name="Sephora India",
    image_url="",
    matched_product_id=huda_mascara.id,
)
huda_nykaa_diff_qty = RawListing(
    retailer_name="Nykaa",
    product_url="https://nykaa.com/example-huda-mascara-mini",
    raw_title="HB Lash Sensational Mascara - Waterproof - 5ml (Mini)",
    raw_price=1899,
    raw_quantity_text="5 ml",
    seller_name="Nykaa Official",
    image_url="",
    matched_product_id=None,  # Deliberately unmatched -- different quantity!
)
huda_ajio_should_match = RawListing(
    retailer_name="AJIO",
    product_url="https://ajio.com/example-huda-mascara",
    raw_title="HB Lash Sensational Mascara Waterproof - 7.6 ml",
    raw_price=2149,
    raw_quantity_text="7.6 ml",
    seller_name="AJIO Beauty",
    image_url="",
    matched_product_id=None,  # Deliberately left unmatched -- SAME quantity as
                               # the 7.6ml product, but worded differently.
                               # This is the "should match" test case.
)

db.add_all([huda_myntra, huda_sephora, huda_nykaa_diff_qty, huda_ajio_should_match])
db.commit()
for l in [huda_myntra, huda_sephora, huda_nykaa_diff_qty, huda_ajio_should_match]:
    db.refresh(l)
add_price_point(huda_myntra, 2199)
add_price_point(huda_sephora, 2299)
add_price_point(huda_nykaa_diff_qty, 1899)
add_price_point(huda_ajio_should_match, 2149)


# =========================================================
# Product 2: Maybelline Mascara
# =========================================================
maybelline_mascara = MatchedProduct(
    brand="Maybelline",
    product_name="Colossal Volume Express Mascara",
    shade_or_color="Black",
    quantity_value=9.5,
    quantity_unit="ml",
    pack_count=1,
    category="Mascara",
)
db.add(maybelline_mascara)
db.commit()
db.refresh(maybelline_mascara)

mb_amazon = RawListing(
    retailer_name="Amazon",
    product_url="https://amazon.in/example-maybelline-mascara",
    raw_title="Maybelline New York Colossal Volume Express Mascara, Black, 9.5ml",
    raw_price=399,
    raw_quantity_text="9.5 ml",
    seller_name="Appario Retail (Amazon)",
    image_url="",
    matched_product_id=maybelline_mascara.id,
)
mb_nykaa = RawListing(
    retailer_name="Nykaa",
    product_url="https://nykaa.com/example-maybelline-mascara",
    raw_title="Maybelline Colossal Mascara - Volume Express - 9.5 ml",
    raw_price=375,
    raw_quantity_text="9.5 ml",
    seller_name="Nykaa Official",
    image_url="",
    matched_product_id=maybelline_mascara.id,
)
mb_ajio = RawListing(
    retailer_name="AJIO",
    product_url="https://ajio.com/example-maybelline-mascara",
    raw_title="Maybelline Colossal Volume Mascara Black 9.5 ml",
    raw_price=410,
    raw_quantity_text="9.5 ml",
    seller_name="AJIO Beauty",
    image_url="",
    matched_product_id=maybelline_mascara.id,
)
db.add_all([mb_amazon, mb_nykaa, mb_ajio])
db.commit()
for l in [mb_amazon, mb_nykaa, mb_ajio]:
    db.refresh(l)
add_price_point(mb_amazon, 399)
add_price_point(mb_nykaa, 375)
add_price_point(mb_ajio, 410)


# =========================================================
# Product 3: Lakme Mascara
# =========================================================
lakme_mascara = MatchedProduct(
    brand="Lakme",
    product_name="Eyeconic Curl Mascara",
    shade_or_color="Black",
    quantity_value=9.0,
    quantity_unit="ml",
    pack_count=1,
    category="Mascara",
)
db.add(lakme_mascara)
db.commit()
db.refresh(lakme_mascara)

lakme_myntra = RawListing(
    retailer_name="Myntra",
    product_url="https://myntra.com/example-lakme-mascara",
    raw_title="Lakme Eyeconic Curl Mascara, Black, 9ml",
    raw_price=449,
    raw_quantity_text="9 ml",
    seller_name="Myntra Beauty Store",
    image_url="",
    matched_product_id=lakme_mascara.id,
)
lakme_amazon = RawListing(
    retailer_name="Amazon",
    product_url="https://amazon.in/example-lakme-mascara",
    raw_title="Lakme Eyeconic Curl Mascara Black - 9 ml",
    raw_price=425,
    raw_quantity_text="9 ml",
    seller_name="Cloudtail India (Amazon)",
    image_url="",
    matched_product_id=lakme_mascara.id,
)
db.add_all([lakme_myntra, lakme_amazon])
db.commit()
for l in [lakme_myntra, lakme_amazon]:
    db.refresh(l)
add_price_point(lakme_myntra, 449)
add_price_point(lakme_amazon, 425)


# =========================================================
# Product 4: A DIFFERENT category, to confirm search filtering works
# =========================================================
moisturizer = MatchedProduct(
    brand="Cetaphil",
    product_name="Moisturizing Cream",
    shade_or_color=None,
    quantity_value=100.0,
    quantity_unit="g",
    pack_count=1,
    category="Moisturizer",
)
db.add(moisturizer)
db.commit()
db.refresh(moisturizer)

cetaphil_amazon = RawListing(
    retailer_name="Amazon",
    product_url="https://amazon.in/example-cetaphil-cream",
    raw_title="Cetaphil Moisturizing Cream, 100g",
    raw_price=699,
    raw_quantity_text="100 g",
    seller_name="Cloudtail India (Amazon)",
    image_url="",
    matched_product_id=moisturizer.id,
)
cetaphil_nykaa = RawListing(
    retailer_name="Nykaa",
    product_url="https://nykaa.com/example-cetaphil-cream",
    raw_title="Cetaphil Moisturising Cream - 100 g",
    raw_price=679,
    raw_quantity_text="100 g",
    seller_name="Nykaa Official",
    image_url="",
    matched_product_id=moisturizer.id,
)
db.add_all([cetaphil_amazon, cetaphil_nykaa])
db.commit()
for l in [cetaphil_amazon, cetaphil_nykaa]:
    db.refresh(l)
add_price_point(cetaphil_amazon, 699)
add_price_point(cetaphil_nykaa, 679)


db.commit()
print("Seed data inserted successfully.")
print("Products added: Huda Beauty Mascara, Maybelline Mascara, Lakme Mascara, Cetaphil Moisturizer")
db.close()