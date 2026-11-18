from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ResenaBase(BaseModel):
    id_veterinaria: int
    calificacion: int = Field(..., ge=1, le=5, description="Calificación entre 1 y 5 estrellas")
    comentario: Optional[str] = None

class ResenaCreate(ResenaBase):
    pass

class ResenaUpdate(BaseModel):
    calificacion: Optional[int] = Field(None, ge=1, le=5)
    comentario: Optional[str] = None

class ResenaResponse(ResenaBase):
    id_resena: int
    id_usuario: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)