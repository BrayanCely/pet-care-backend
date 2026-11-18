from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate

def get_producto_by_id(db: Session, id_producto: int) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.id_producto == id_producto).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100, categoria: Optional[str] = None):
    query = db.query(Producto)
    if categoria:
        query = query.filter(Producto.categoria == categoria)
    return query.offset(skip).limit(limit).all()

def create_producto(db: Session, prod_data: ProductoCreate) -> Producto:
    db_prod = Producto(**prod_data.model_dump())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def update_producto(db: Session, db_prod: Producto, prod_update: ProductoUpdate) -> Producto:
    update_data = prod_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_prod, field, value)
    
    db.commit()
    db.refresh(db_prod)
    return db_prod

def delete_producto(db: Session, db_prod: Producto) -> None:
    db.delete(db_prod)
    db.commit()