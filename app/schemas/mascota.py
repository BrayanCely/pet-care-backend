from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    sexo: Optional[str] = None
    edad: Optional[int] = None   
    fecha_nacimiento: Optional[date] = None
    peso_kg: Optional[float] = None
    color_mascota: Optional[str] = None
    numero_chip: Optional[str] = None
    foto_url: Optional[str] = None
    alergias: Optional[str] = None
    condiciones_medicas: Optional[str] = None
    activo: Optional[bool] = True

class MascotaCreate(MascotaBase):
    pass

class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    peso_kg: Optional[float] = None
    color_mascota: Optional[str] = None
    numero_chip: Optional[str] = None
    foto_url: Optional[str] = None
    alergias: Optional[str] = None
    condiciones_medicas: Optional[str] = None
    activo: Optional[bool] = None

class MascotaResponse(MascotaBase):
    id_mascota: int
    id_usuario: int

    model_config = ConfigDict(from_attributes=True)