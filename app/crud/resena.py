from sqlalchemy.orm import Session
from app.models.resena import Resena
from app.schemas.resena import ResenaCreate, ResenaUpdate

def get_resena_by_id(db: Session, id_resena: int):
    return db.query(Resena).filter(Resena.id_resena == id_resena).first()

def get_resenas_by_veterinaria(db: Session, id_veterinaria: int, skip: int = 0, limit: int = 100):
    return db.query(Resena).filter(Resena.id_veterinaria == id_veterinaria).offset(skip).limit(limit).all()

def get_resenas_by_usuario(db: Session, id_usuario: int, skip: int = 0, limit: int = 100):
    return db.query(Resena).filter(Resena.id_usuario == id_usuario).offset(skip).limit(limit).all()

def create_resena(db: Session, resena: ResenaCreate, id_usuario: int):
    db_resena = Resena(
        id_veterinaria=resena.id_veterinaria,
        id_usuario=id_usuario,
        calificacion=resena.calificacion,
        comentario=resena.comentario
    )
    db.add(db_resena)
    db.commit()
    db.refresh(db_resena)
    return db_resena

def update_resena(db: Session, id_resena: int, resena_update: ResenaUpdate):
    db_resena = get_resena_by_id(db, id_resena)
    if db_resena:
        update_data = resena_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_resena, key, value)
        db.commit()
        db.refresh(db_resena)
    return db_resena

def delete_resena(db: Session, id_resena: int):
    db_resena = get_resena_by_id(db, id_resena)
    if db_resena:
        db.delete(db_resena)
        db.commit()
    return db_resena