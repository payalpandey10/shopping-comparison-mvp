"""
matching/brand_extractor.py
------------------------------
Guesses a brand name from a raw, messy product title.
"""

KNOWN_MULTIWORD_BRANDS = [
    "Blue Heaven",
    "La Roche-Posay",
    "Huda Beauty",
    "Sugar Cosmetics",
    "Kay Beauty",
    "Beauty of Joseon",
    "The Derma Co",
    "Dr. Sheth's",
    "Maybelline New York",
    "Lakme 9-5",
    "Smart And Handsome",
]


def guess_brand(raw_title: str) -> str:
    if not raw_title:
        return "Unknown"

    title = raw_title.strip()

    sorted_brands = sorted(KNOWN_MULTIWORD_BRANDS, key=len, reverse=True)
    for brand in sorted_brands:
        if title.lower().startswith(brand.lower()):
            return brand

    first_word = title.split()[0] if title.split() else "Unknown"
    first_word = first_word.strip(",.|-")

    return first_word if first_word else "Unknown"


if __name__ == "__main__":
    test_titles = [
        "Lakme 9-5 Eyeconic Kajal, Deep Black",
        "Blue Heaven Hyper Black Gel Kajal Eyeliner",
        "La Roche-Posay Anthelios UVMUNE400 Invisible Fluid",
    ]
    for t in test_titles:
        print(f"{t[:40]!r:45} -> {guess_brand(t)}")