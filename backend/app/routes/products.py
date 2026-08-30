"""
routes/products.py
-------------------
API endpoints related to searching and comparing matched products.

This is what your React frontend will actually call, e.g.:
  GET /products/search?q=mascara
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from ..database import get_db
from ..models import MatchedProduct
from ..schemas import MatchedProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/search", response_model=List[MatchedProductOut])
def search_products(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """
    Search matched_product by brand or product_name.
    This searches our OWN catalog (not live retailer sites) --
    remember: we only find what's already been crawled + matched.
    """
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
    return results


@router.get("/{product_id}", response_model=MatchedProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get one matched product with all its raw listings --
    this is what powers the Comparison page.
    """
    return db.query(MatchedProduct).filter(MatchedProduct.id == product_id).first()
