"""
crawler/practice_crawler.py
-----------------------------
A basic web crawler proving out the core mechanics: fetch a page,
parse HTML, extract product data, insert into our database.

Uses books.toscrape.com -- a site built for scraping practice.

Run with (from backend/ folder, venv active):
    python -m app.crawler.practice_crawler
"""


import re
import requests
from bs4 import BeautifulSoup

from ..database import SessionLocal
from ..models import RawListing

BASE_URL = "http://books.toscrape.com/"


def fetch_page(url: str) -> str:
    """Downloads the raw HTML of a page."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_products(html: str):
    """Extracts a list of products (title, price) from the page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    product_elements = soup.find_all("article", class_="product_pod")

    products = []
    for el in product_elements:
        title = el.h3.a["title"]
        price_text = el.find("p", class_="price_color").text

        price_match = re.search(r"[\d.]+", price_text)
        price = price_match.group() if price_match else None

        products.append({
            "title": title,
            "price": price,
        })
    return products


def save_to_database(products, retailer_name="BooksPracticeSite"):
    """Inserts each scraped product as a new raw_listing row."""
    db = SessionLocal()
    inserted = 0

    for product in products:
        listing = RawListing(
            retailer_name=retailer_name,
            product_url=BASE_URL,
            raw_title=product["title"],
            raw_price=product["price"],
            raw_quantity_text=None,
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
    print(f"Fetching {BASE_URL} ...")
    html = fetch_page(BASE_URL)

    print("Parsing products...")
    products = parse_products(html)
    print(f"Found {len(products)} products on the page.\n")

    for p in products[:5]:
        print(f"  {p['title']} -- £{p['price']}")

    print(f"\nInserting into database...")
    count = save_to_database(products)
    print(f"Inserted {count} new raw_listing rows.")