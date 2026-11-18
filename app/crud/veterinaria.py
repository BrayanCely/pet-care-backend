from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.veterinaria import Veterinaria
from app.schemas.veterinaria import VeterinariaCreate, VeterinariaUpdate

def get_veterinaria_by_id(db: Session, id_veterinaria: int) -> Optional[Veterinaria]:
    return db.query(Veterinaria).filter(Veterinaria.id_veterinaria == id_veterinaria).first()

def get_veterinarias(db: Session, skip: int = 0, limit: int = 100) -> List[Veterinaria]:
    return db.query(Veterinaria).offset(skip).limit(limit).all()

def create_veterinaria(db: Session, vet_data: VeterinariaCreate) -> Veterinaria:
    db_vet = Veterinaria(**vet_data.model_dump())
    db.add(db_vet)
    db.commit()
    db.refresh(db_vet)
    return db_vet

def update_veterinaria(db: Session, db_vet: Veterinaria, vet_update: VeterinariaUpdate) -> Veterinaria:
    update_data = vet_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vet, field, value)
    
    db.commit()
    db.refresh(db_vet)
    return db_vet

def delete_veterinaria(db: Session, db_vet: Veterinaria) -> None:
    db.delete(db_vet)
    db.commit()