"""
routes/products.py
-------------------
API endpoints related to searching and comparing matched products.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from ..database import get_db
from ..models import MatchedProduct
from ..schemas import MatchedProductOut

router = APIRouter(prefix="/products", tags=["products"])


def attach_price_per_unit(product: MatchedProduct) -> MatchedProduct:
    """
    Calculates price-per-unit for every listing belonging to this
    product, and attaches it as a temporary attribute so the schema
    can pick it up in the response.
    """
    for listing in product.listings:
        if listing.raw_price is not None and product.quantity_value:
            listing.price_per_unit = round(
                listing.raw_price / product.quantity_value, 2
            )
        else:
            listing.price_per_unit = None
    return product


@router.get("/search", response_model=List[MatchedProductOut])
def search_products(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    results = (
        db.query(MatchedProduct)
        .filter(
            or_(
                MatchedProduct.brand.ilike(f"%{q}%"),
                MatchedProduct.product_name.ilike(f"%{q}%"),
            )
        )
        .all()
    )
    for product in results:
        attach_price_per_unit(product)
    return results


@router.get("/{product_id}", response_model=MatchedProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(MatchedProduct).filter(MatchedProduct.id == product_id).first()
    if product:
        attach_price_per_unit(product)
    return product