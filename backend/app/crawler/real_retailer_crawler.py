"""
crawler/real_retailer_crawler.py
-----------------------------------
Crawls a REAL retailer (Amazon India) across MULTIPLE search terms,
so we get variety in product names/categories instead of just one
type of product every run.

Run with (from backend/ folder, venv active):
    python -m app.crawler.real_retailer_crawler
"""

import re
import time
import requests
from bs4 import BeautifulSoup

from ..database import SessionLocal
from ..models import RawListing
from ..matching.quantity_parser import parse_quantity

# List of search terms to crawl -- add/remove terms here to control
# what kinds of products your catalog grows to include.
SEARCH_TERMS = ["mascara"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
}


def build_search_url(term: str) -> str:
    return f"https://www.amazon.in/s?k={term.replace(' ', '+')}"


def fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=10)
    print(f"  Status code: {response.status_code}")
    response.raise_for_status()
    return response.text


def parse_products(html: str):
    soup = BeautifulSoup(html, "html.parser")
    product_elements = soup.find_all("div", {"data-component-type": "s-search-result"})

    products = []
    for el in product_elements:
        title_el = el.find("h2")
        price_el = el.find("span", class_="a-price-whole")

        if not title_el or not price_el:
            continue

        title = title_el.get_text(strip=True)
        price_match = re.search(r"[\d,]+", price_el.get_text())
        price = price_match.group().replace(",", "") if price_match else None

        products.append({"title": title, "price": price})

    return products


def save_to_database(products, search_url, retailer_name="Amazon"):
    db = SessionLocal()
    inserted = 0

    for product in products:
        value, unit = parse_quantity(product["title"])
        quantity_text = f"{value}{unit}" if value else None

        listing = RawListing(
            retailer_name=retailer_name,
            product_url=search_url,
            raw_title=product["title"],
            raw_price=product["price"],
            raw_quantity_text=quantity_text,
            seller_name=retailer_name,
            image_url="",
            matched_product_id=None,
        )
        db.add(listing)
        inserted += 1

    db.commit()
    db.close()
    return inserted


if __name__ == "__main__":
    total_inserted = 0

    for term in SEARCH_TERMS:
        url = build_search_url(term)
        print(f"\nSearching for '{term}' -> {url}")
        try:
            html = fetch_page(url)
            products = parse_products(html)
            print(f"  Found {len(products)} products.")

            if products:
                count = save_to_database(products, url)
                print(f"  Inserted {count} new raw_listing rows.")
                total_inserted += count
            else:
                print("  No products found (likely blocked for this term).")

        except Exception as e:
            print(f"  Failed to fetch '{term}': {e}")

        # Wait a bit between requests -- more polite, less likely to
        # trigger anti-bot rate limiting than hammering requests instantly.
        time.sleep(10)

    print(f"\n=== Done. Total inserted across all search terms: {total_inserted} ===")