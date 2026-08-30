"""
models.py
---------
These are our 3 tables from the schema we designed, written as Python
classes instead of raw SQL. SQLAlchemy turns each class into a table,
and each instance of the class into a row.

This matches exactly what we discussed:
  matched_product  -> the clean, normalized "real product"
  raw_listing      -> untouched retailer data, points to matched_product
  price_history    -> every price check over time, points to raw_listing
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class MatchedProduct(Base):
    __tablename__ = "matched_product"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(255), nullable=False)
    product_name = Column(String(500), nullable=False)
    shade_or_color = Column(String(100), nullable=True)
    quantity_value = Column(Numeric(10, 2), nullable=True)
    quantity_unit = Column(String(20), nullable=True)
    pack_count = Column(Integer, default=1)
    category = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # This lets us do matched_product.listings to get all raw listings
    # that point to this product (the "many" side of many-to-one).
    listings = relationship("RawListing", back_populates="matched_product")


class RawListing(Base):
    __tablename__ = "raw_listing"

    id = Column(Integer, primary_key=True, index=True)
    retailer_name = Column(String(100), nullable=False)
    product_url = Column(Text, nullable=False)
    raw_title = Column(Text, nullable=False)
    raw_price = Column(Numeric(10, 2), nullable=True)
    raw_quantity_text = Column(String(100), nullable=True)
    seller_name = Column(String(255), nullable=True)
    image_url = Column(Text, nullable=True)

    # This is the foreign key we discussed — nullable, because a listing
    # can exist before matching has run on it.
    matched_product_id = Column(Integer, ForeignKey("matched_product.id"), nullable=True)
    last_crawled_at = Column(TIMESTAMP, server_default=func.now())

    matched_product = relationship("MatchedProduct", back_populates="listings")
    price_points = relationship("PriceHistory", back_populates="listing")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    raw_listing_id = Column(Integer, ForeignKey("raw_listing.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    checked_at = Column(TIMESTAMP, server_default=func.now())

    listing = relationship("RawListing", back_populates="price_points")
