from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# --- VETERINARIAS ---
class VeterinariaBase(BaseModel):
    nombre_comercial: str
    direccion: str
    telefono: str
    correo_electronico: Optional[EmailStr] = None
    horario_atencion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class VeterinariaCreate(VeterinariaBase):
    pass

class VeterinariaUpdate(BaseModel):
    nombre_comercial: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    horario_atencion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    activo: Optional[bool] = None

class VeterinariaResponse(VeterinariaBase):
    id_veterinaria: int
    calificacion_promedio: float
    activo: bool

    model_config = ConfigDict(from_attributes=True)


# --- PROFESIONALES ---
class ProfesionalBase(BaseModel):
    id_veterinaria: int
    nombre_completo: str
    especialidad: Optional[str] = None
    numero_registro_profesional: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None

class ProfesionalCreate(ProfesionalBase):
    pass

class ProfesionalResponse(ProfesionalBase):
    id_profesional: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)


# --- CITAS VETERINARIAS ---
class CitaBase(BaseModel):
    id_mascota: int
    id_profesional: int
    id_veterinaria: int
    fecha_cita: datetime
    motivo: str
    notas: Optional[str] = None

class CitaCreate(CitaBase):
    pass

class CitaUpdateEstado(BaseModel):
    estado: str  # programada, completada, cancelada

class CitaResponse(CitaBase):
    id_cita: int
    estado: str
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)