from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductOut])
def list_products(
    db: Session = Depends(get_db_dep),
    skip: int = 0,
    limit: int = Query(50, le=200),
    sku: Optional[str] = None,
    name: Optional[str] = None,
    active: Optional[bool] = None,
    description: Optional[str] = None,
):
    items, total = product_service.list_products(
        db, skip=skip, limit=limit, sku=sku, name=name, active=active, description=description
    )
    # You can also return total in a wrapper schema if you want metadata for pagination
    return items


@router.post("/", response_model=ProductOut)
def create_product_endpoint(
    data: ProductCreate,
    db: Session = Depends(get_db_dep),
):
    product = product_service.create_product(db, data)
    return product


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db_dep)):
    product = db.query(product_service.Product).get(product_id)  # type: ignore
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product_endpoint(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db_dep),
):
    product = db.query(product_service.Product).get(product_id)  # type: ignore
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = product_service.update_product(db, product, data)
    return product


@router.delete("/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db_dep)):
    product = db.query(product_service.Product).get(product_id)  # type: ignore
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_service.delete_product(db, product)
    return {"detail": "Deleted"}


@router.delete("/bulk/all")
def bulk_delete_products_endpoint(db: Session = Depends(get_db_dep)):
    deleted = product_service.bulk_delete_products(db)
    return {"detail": f"Deleted {deleted} products"}
