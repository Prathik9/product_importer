
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def list_products(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    sku: Optional[str] = None,
    name: Optional[str] = None,
    active: Optional[bool] = None,
    description: Optional[str] = None,
) -> Tuple[List[Product], int]:
    query = db.query(Product)

    if sku:
        query = query.filter(func.lower(Product.sku) == sku.lower())
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Product.description.ilike(f"%{description}%"))
    if active is not None:
        query = query.filter(Product.active == active)

    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_product(db: Session, data: ProductCreate) -> Product:
    # overwrite based on SKU (case-insensitive)
    existing = (
        db.query(Product)
        .filter(func.lower(Product.sku) == data.sku.lower())
        .one_or_none()
    )

    if existing:
        for field, value in data.dict().items():
            setattr(existing, field, value)
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, data: ProductUpdate) -> Product:
    for field, value in data.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def bulk_delete_products(db: Session) -> int:
    count = db.query(Product).delete()
    db.commit()
    return count
