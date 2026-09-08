"""
crawler/nykaa_crawler.py
---------------------------
An attempt at crawling Nykaa search results.

IMPORTANT HONEST NOTE:
Nykaa's site may be a JavaScript-rendered single-page app, meaning the
raw HTML we fetch might not contain real product data. We're testing
this directly rather than assuming either way.

Run with (from backend/ folder, venv active):
    python -m app.crawler.nykaa_crawler
"""

import re
import requests
from bs4 import BeautifulSoup

from ..database import SessionLocal
from ..models import RawListing
from ..matching.quantity_parser import parse_quantity

SEARCH_URL = "https://www.nykaa.com/search/result/?q=mascara"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
}
def fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=10)
    print(f"Status code: {response.status_code}")
    response.raise_for_status()
    return response.text


def parse_products(html: str):
    soup = BeautifulSoup(html, "html.parser")
    product_elements = soup.find_all("div", class_=re.compile("product", re.I))

    products = []
    for el in product_elements:
        title_el = el.find(class_=re.compile("title|name", re.I))
        price_el = el.find(class_=re.compile("price", re.I))

        if not title_el or not price_el:
            continue

        title = title_el.get_text(strip=True)
        price_match = re.search(r"[\d,]+", price_el.get_text())
        price = price_match.group().replace(",", "") if price_match else None

        if title and price:
            products.append({"title": title, "price": price})

    return products


if __name__ == "__main__":
    print(f"Fetching {SEARCH_URL} ...")
    html = fetch_page(SEARCH_URL)

    print(f"Page length received: {len(html)} characters")
    print("Parsing products...")
    products = parse_products(html)
    print(f"Found {len(products)} products.\n")

    for p in products[:5]:
        print(f"  {p['title']} -- Rs.{p['price']}")

    if len(products) == 0:
        print("\nNo products found. Printing a sample of the raw HTML to")
        print("diagnose whether this is JS-rendered content or just a")
        print("wrong CSS selector guess:\n")
        print(html[:1000])