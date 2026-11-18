from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.mensaje import MensajeCreate, MensajeResponse
from app.crud.mensaje import (
    get_mensaje_by_id,
    get_mensajes_by_conversacion,
    get_conversaciones_usuario,
    create_mensaje,
    marcar_mensaje_como_leido
)

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])

@router.post("/", response_model=MensajeResponse, status_code=status.HTTP_201_CREATED)
def enviar_mensaje(msg_in: MensajeCreate, db: Session = Depends(get_db)):
    """Envía un nuevo mensaje entre dos usuarios (o usuario y veterinaria)."""
    return create_mensaje(db=db, msg_data=msg_in)

@router.get("/conversacion/{id_usuario_2}", response_model=List[MensajeResponse])
def obtener_conversacion(
    id_usuario_2: int,
    id_usuario_1: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtiene el historial de mensajes entre el usuario actual y otro usuario."""
    return get_mensajes_by_conversacion(
        db=db, 
        id_user1=id_usuario_1, 
        id_user2=id_usuario_2, 
        skip=skip, 
        limit=limit
    )

@router.get("/mis-conversaciones/{id_usuario}", response_model=List[MensajeResponse])
def listar_mis_conversaciones(id_usuario: int, db: Session = Depends(get_db)):
    """Obtiene el último mensaje de cada conversación activa de un usuario."""
    return get_conversaciones_usuario(db=db, id_usuario=id_usuario)

@router.patch("/{id_mensaje}/leido", response_model=MensajeResponse)
def marcar_leido(id_mensaje: int, db: Session = Depends(get_db)):
    """Marca un mensaje específico como leído."""
    msg = get_mensaje_by_id(db, id_mensaje=id_mensaje)
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")
    return marcar_mensaje_como_leido(db=db, db_msg=msg)