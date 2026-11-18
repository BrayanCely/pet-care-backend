from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date

# --- RECORDATORIOS ---
class RecordatorioBase(BaseModel):
    id_mascota: int
    titulo: str
    descripcion: Optional[str] = None
    tipo: str
    fecha_programada: datetime
    frecuencia: Optional[str] = None

class RecordatorioCreate(RecordatorioBase):
    pass

class RecordatorioUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    fecha_programada: Optional[datetime] = None
    frecuencia: Optional[str] = None
    notificado: Optional[bool] = None
    activo: Optional[bool] = None

class RecordatorioResponse(RecordatorioBase):
    id_recordatorio: int
    notificado: bool
    fecha_notificacion: Optional[datetime] = None
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)


# --- MEDICAMENTOS ---
class MedicamentoBase(BaseModel):
    id_mascota: int
    id_recordatorio: Optional[int] = None
    nombre_medicamento: str
    dosis: Optional[str] = None
    unidad_medida: Optional[str] = None
    frecuencia_administracion: Optional[str] = None
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    observaciones: Optional[str] = None

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)


# --- VACUNAS ---
class VacunaBase(BaseModel):
    id_mascota: int
    id_recordatorio: Optional[int] = None
    id_profesional: Optional[int] = None
    nombre_vacuna: str
    fecha_aplicacion: date
    fecha_proxima_dosis: Optional[date] = None
    numero_dosis: Optional[int] = 1
    lote: Optional[str] = None
    veterinario_nombre: Optional[str] = None

class VacunaCreate(VacunaBase):
    pass

class VacunaResponse(VacunaBase):
    id_vacuna: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)