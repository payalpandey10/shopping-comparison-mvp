"""
matching/import_dataset.py
-----------------------------
Imports the Kaggle cosmetics CSV dataset, grouping listings from
different retailers that are the same real product.

Since this dataset's "size" field has no unit, we can't use quantity
as a safety check. Instead, we group ONLY within the same brand using
a HIGH name-similarity threshold (0.85).

PERFORMANCE: vectorizes each brand group ONCE (not per-pair), making
this run in seconds instead of many minutes.

Run with (from backend/ folder, venv active):
    python -m app.matching.import_dataset
"""

import csv
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ..database import SessionLocal
from ..models import MatchedProduct, RawListing
from .brand_normalizer import normalize_brand

CSV_PATH = "E-commerce__cosmetic_dataset.csv"
NAME_SIMILARITY_THRESHOLD_NO_QUANTITY = 0.85


def clean_price(raw_price: str):
    if not raw_price:
        return None
    cleaned = raw_price.replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def cluster_group(rows):
    n = len(rows)
    if n < 2:
        return [[i] for i in range(n)]

    titles = [r["product_name"] for r in rows]
    try:
        tfidf_matrix = TfidfVectorizer().fit_transform(titles)
        sim_matrix = cosine_similarity(tfidf_matrix)
    except ValueError:
        return [[i] for i in range(n)]

    clustered = [False] * n
    clusters = []

    for i in range(n):
        if clustered[i]:
            continue
        cluster = [i]
        clustered[i] = True
        for j in range(i + 1, n):
            if not clustered[j] and sim_matrix[i][j] >= NAME_SIMILARITY_THRESHOLD_NO_QUANTITY:
                cluster.append(j)
                clustered[j] = True
        clusters.append(cluster)

    return clusters


def run_import():
    db = SessionLocal()

    with open(CSV_PATH, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} rows from {CSV_PATH}")

    brand_groups = defaultdict(list)
    for row in rows:
        brand_groups[normalize_brand(row["brand"])].append(row)

    print(f"Found {len(brand_groups)} unique brands. Clustering within each...\n")

    products_created = 0
    listings_created = 0

    for brand, group in brand_groups.items():
        if not brand:
            continue

        clusters = cluster_group(group)

        for cluster_indices in clusters:
            representative = group[cluster_indices[0]]

            new_product = MatchedProduct(
                brand=representative["brand"].strip(),
                product_name=representative["product_name"].strip(),
                shade_or_color=None,
                quantity_value=None,
                quantity_unit=None,
                pack_count=1,
                category=representative.get("category", "").strip() or None,
            )
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            products_created += 1

            for idx in cluster_indices:
                row = group[idx]
                listing = RawListing(
                    retailer_name=row["website"].strip(),
                    product_url=row["title-href"].strip(),
                    raw_title=row["product_name"].strip(),
                    raw_price=clean_price(row["price"]),
                    raw_quantity_text=row["size"].strip() or None,
                    seller_name=row["website"].strip(),
                    image_url="",
                    matched_product_id=new_product.id,
                )
                db.add(listing)
                listings_created += 1

        db.commit()

    print(f"\n=== Done. Created {products_created} products from {listings_created} listings. ===")
    db.close()


if __name__ == "__main__":
    run_import()