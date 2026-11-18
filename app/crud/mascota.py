from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.mascota import Mascota
from app.schemas.mascota import MascotaCreate, MascotaUpdate

def get_mascota_by_id(db: Session, id_mascota: int) -> Optional[Mascota]:
    return db.query(Mascota).filter(Mascota.id_mascota == id_mascota).first()

def get_mascotas_by_usuario(db: Session, id_usuario: int, skip: int = 0, limit: int = 100) -> List[Mascota]:
    return (
        db.query(Mascota)
        .filter(Mascota.id_usuario == id_usuario)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_mascota(db: Session, mascota_data: MascotaCreate, id_usuario: int) -> Mascota:
    db_mascota = Mascota(
        **mascota_data.model_dump(),
        id_usuario=id_usuario
    )
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

def update_mascota(db: Session, db_mascota: Mascota, mascota_update: MascotaUpdate) -> Mascota:
    update_data = mascota_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_mascota, field, value)
    
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

def delete_mascota(db: Session, db_mascota: Mascota) -> None:
    db.delete(db_mascota)
    db.commit()