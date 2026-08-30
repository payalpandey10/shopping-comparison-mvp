"""
schemas.py
----------
While models.py defines our DATABASE tables, this file defines the
shape of data going IN and OUT of our API (JSON that the frontend sends/receives).

Why separate from models.py?
Because the API response often needs a different shape than the raw table
-- e.g. we might want to include nested listings inside a product response,
or hide certain internal fields. Keeping them separate avoids confusion later.
"""

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class RawListingOut(BaseModel):
    id: int
    retailer_name: str
    product_url: str
    raw_title: str
    raw_price: Optional[Decimal]
    raw_quantity_text: Optional[str]
    seller_name: Optional[str]
    image_url: Optional[str]

    class Config:
        orm_mode = True


class MatchedProductOut(BaseModel):
    id: int
    brand: str
    product_name: str
    shade_or_color: Optional[str]
    quantity_value: Optional[Decimal]
    quantity_unit: Optional[str]
    pack_count: int
    category: Optional[str]
    listings: List[RawListingOut] = []

    class Config:
        orm_mode = True


class PriceHistoryOut(BaseModel):
    id: int
    price: Decimal
    checked_at: datetime

    class Config:
        orm_mode = True
