from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.recordatorio import Recordatorio
from app.schemas.recordatorio import RecordatorioCreate, RecordatorioUpdate

def get_recordatorio_by_id(db: Session, id_recordatorio: int) -> Optional[Recordatorio]:
    return db.query(Recordatorio).filter(Recordatorio.id_recordatorio == id_recordatorio).first()

def get_recordatorios_by_mascota(db: Session, id_mascota: int, skip: int = 0, limit: int = 100) -> List[Recordatorio]:
    return (
        db.query(Recordatorio)
        .filter(Recordatorio.id_mascota == id_mascota)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_recordatorio(db: Session, rec_data: RecordatorioCreate) -> Recordatorio:
    db_rec = Recordatorio(**rec_data.model_dump())
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    return db_rec

def update_recordatorio(db: Session, db_rec: Recordatorio, rec_update: RecordatorioUpdate) -> Recordatorio:
    update_data = rec_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_rec, field, value)
    
    db.commit()
    db.refresh(db_rec)
    return db_rec

def delete_recordatorio(db: Session, db_rec: Recordatorio) -> None:
    db.delete(db_rec)
    db.commit()