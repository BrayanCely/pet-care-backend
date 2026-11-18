from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate

def get_mensaje_by_id(db: Session, id_mensaje: int):
    return db.query(Mensaje).filter(Mensaje.id_mensaje == id_mensaje).first()

def get_mensajes_by_conversacion(db: Session, id_usuario_1: int, id_usuario_2: int, skip: int = 0, limit: int = 100):
    return db.query(Mensaje).filter(
        ((Mensaje.id_usuario_1 == id_usuario_1) & (Mensaje.id_usuario_2 == id_usuario_2)) |
        ((Mensaje.id_usuario_1 == id_usuario_2) & (Mensaje.id_usuario_2 == id_usuario_1))
    ).offset(skip).limit(limit).all()

def get_conversaciones_usuario(db: Session, id_usuario: int):
    return db.query(Mensaje).filter(
        or_(Mensaje.id_usuario_1 == id_usuario, Mensaje.id_usuario_2 == id_usuario)
    ).all()

def create_mensaje(db: Session, mensaje: MensajeCreate, id_usuario_remitente: int):
    db_mensaje = Mensaje(
        id_usuario_1=id_usuario_remitente,
        id_usuario_2=mensaje.id_usuario_2,
        contenido=mensaje.contenido
    )
    db.add(db_mensaje)
    db.commit()
    db.refresh(db_mensaje)
    return db_mensaje

def marcar_mensaje_como_leido(db: Session, id_mensaje: int):
    db_mensaje = get_mensaje_by_id(db, id_mensaje)
    if db_mensaje:
        db_mensaje.leido = True
        db.commit()
        db.refresh(db_mensaje)
    return db_mensaje