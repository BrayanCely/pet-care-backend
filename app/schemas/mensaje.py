from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MensajeBase(BaseModel):
    id_usuario_2: int
    contenido: str

class MensajeCreate(MensajeBase):
    pass

class MensajeResponse(BaseModel):
    id_mensaje: int
    id_usuario_1: int
    id_usuario_2: int
    contenido: str
    fecha_envio: datetime
    leido: bool

    class Config:
        from_attributes = True