from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.models.recordatorio import Recordatorio, Medicamento, Vacuna
from app.schemas.recordatorio import (
    RecordatorioCreate, RecordatorioUpdate, RecordatorioResponse,
    MedicamentoCreate, MedicamentoResponse,
    VacunaCreate, VacunaResponse
)

router = APIRouter(prefix="/recordatorios", tags=["Recordatorios, Medicamentos y Vacunas"])

# Funcionalidad auxiliar de validación
def validar_propietario_mascota(id_mascota: int, id_usuario: int, db: Session):
    mascota = db.query(Mascota).filter(
        Mascota.id_mascota == id_mascota,
        Mascota.id_usuario == id_usuario
    ).first()
    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada o no pertenece al usuario autenticado"
        )
    return mascota


# ==================== RECORDATORIOS ====================

@router.post("/", response_model=RecordatorioResponse, status_code=status.HTTP_201_CREATED)
def crear_recordatorio(
    rec_in: RecordatorioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    validar_propietario_mascota(rec_in.id_mascota, current_user.id_usuario, db)
    nuevo_rec = Recordatorio(**rec_in.model_dump())
    db.add(nuevo_rec)
    db.commit()
    db.refresh(nuevo_rec)
    return nuevo_rec

@router.get("/mascota/{id_mascota}", response_model=List[RecordatorioResponse])
def listar_recordatorios_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    validar_propietario_mascota(id_mascota, current_user.id_usuario, db)
    return db.query(Recordatorio).filter(
        Recordatorio.id_mascota == id_mascota,
        Recordatorio.activo == True
    ).all()

@router.patch("/{id_recordatorio}", response_model=RecordatorioResponse)
def actualizar_recordatorio(
    id_recordatorio: int,
    datos: RecordatorioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    rec = db.query(Recordatorio).filter(Recordatorio.id_recordatorio == id_recordatorio).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    
    validar_propietario_mascota(rec.id_mascota, current_user.id_usuario, db)

    update_data = datos.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(rec, campo, valor)

    db.commit()
    db.refresh(rec)
    return rec


# ==================== MEDICAMENTOS ====================

@router.post("/medicamentos/", response_model=MedicamentoResponse, status_code=status.HTTP_201_CREATED)
def registrar_medicamento(
    med_in: MedicamentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    validar_propietario_mascota(med_in.id_mascota, current_user.id_usuario, db)
    nuevo_med = Medicamento(**med_in.model_dump())
    db.add(nuevo_med)
    db.commit()
    db.refresh(nuevo_med)
    return nuevo_med

@router.get("/medicamentos/mascota/{id_mascota}", response_model=List[MedicamentoResponse])
def listar_medicamentos_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    validar_propietario_mascota(id_mascota, current_user.id_usuario, db)
    return db.query(Medicamento).filter(
        Medicamento.id_mascota == id_mascota,
        Medicamento.activo == True
    ).all()


# ==================== VACUNAS ====================

@router.post("/vacunas/", response_model=VacunaResponse, status_code=status.HTTP_201_CREATED)
def registrar_vacuna(
    vac_in: VacunaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    validar_propietario_mascota(vac_in.id_mascota, current_user.id_usuario, db)
    nueva_vac = Vacuna(**vac_in.model_dump())
    db.add(nueva_vac)
    db.commit()
    db.refresh(nueva_vac)
    return nueva_vac

@router.get("/vacunas/mascota/{id_mascota}", response_model=List[VacunaResponse])
def listar_vacunas_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    validar_propietario_mascota(id_mascota, current_user.id_usuario, db)
    return db.query(Vacuna).filter(Vacuna.id_mascota == id_mascota).all()