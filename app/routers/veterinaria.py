from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.models.veterinaria import Veterinaria, Profesional, CitaVeterinaria
from app.schemas.veterinaria import (
    VeterinariaCreate, VeterinariaUpdate, VeterinariaResponse,
    ProfesionalCreate, ProfesionalResponse,
    CitaCreate, CitaUpdateEstado, CitaResponse
)

router = APIRouter(prefix="/veterinarias", tags=["Veterinarias"])

# ==================== VETERINARIAS ====================

@router.get("/", response_model=List[VeterinariaResponse])
def listar_veterinarias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Veterinaria).filter(Veterinaria.activo == True).offset(skip).limit(limit).all()

@router.post("/", response_model=VeterinariaResponse, status_code=status.HTTP_201_CREATED)
def registrar_veterinaria(vet_in: VeterinariaCreate, db: Session = Depends(get_db)):
    nueva_vet = Veterinaria(**vet_in.model_dump())
    db.add(nueva_vet)
    db.commit()
    db.refresh(nueva_vet)
    return nueva_vet

@router.get("/{id_veterinaria}", response_model=VeterinariaResponse)
def obtener_veterinaria(id_veterinaria: int, db: Session = Depends(get_db)):
    vet = db.query(Veterinaria).filter(Veterinaria.id_veterinaria == id_veterinaria).first()
    if not vet:
        raise HTTPException(status_code=404, detail="Veterinaria no encontrada")
    return vet

@router.patch("/{id_veterinaria}", response_model=VeterinariaResponse)
def actualizar_veterinaria(
    id_veterinaria: int,
    datos: VeterinariaUpdate,
    db: Session = Depends(get_db)
):
    vet = db.query(Veterinaria).filter(Veterinaria.id_veterinaria == id_veterinaria).first()
    if not vet:
        raise HTTPException(status_code=404, detail="Veterinaria no encontrada")

    update_data = datos.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(vet, campo, valor)

    db.commit()
    db.refresh(vet)
    return vet


# ==================== PROFESIONALES ====================

@router.post("/profesionales/", response_model=ProfesionalResponse, status_code=status.HTTP_201_CREATED)
def registrar_profesional(prof_in: ProfesionalCreate, db: Session = Depends(get_db)):
    vet = db.query(Veterinaria).filter(Veterinaria.id_veterinaria == prof_in.id_veterinaria).first()
    if not vet:
        raise HTTPException(status_code=404, detail="La veterinaria especificada no existe")

    nuevo_prof = Profesional(**prof_in.model_dump())
    db.add(nuevo_prof)
    db.commit()
    db.refresh(nuevo_prof)
    return nuevo_prof

@router.get("/{id_veterinaria}/profesionales", response_model=List[ProfesionalResponse])
def listar_profesionales_por_veterinaria(id_veterinaria: int, db: Session = Depends(get_db)):
    return db.query(Profesional).filter(
        Profesional.id_veterinaria == id_veterinaria,
        Profesional.activo == True
    ).all()


# ==================== CITAS VETERINARIAS ====================

@router.post("/citas/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def agendar_cita(
    cita_in: CitaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Validar que la mascota pertenezca al usuario autenticado
    mascota = db.query(Mascota).filter(
        Mascota.id_mascota == cita_in.id_mascota,
        Mascota.id_usuario == current_user.id_usuario
    ).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada o no te pertenece")

    # Validar existencia de profesional y veterinaria
    prof = db.query(Profesional).filter(Profesional.id_profesional == cita_in.id_profesional).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")

    nueva_cita = CitaVeterinaria(**cita_in.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

@router.patch("/citas/{id_cita}/estado", response_model=CitaResponse)
def cambiar_estado_cita(
    id_cita: int,
    estado_in: CitaUpdateEstado,
    db: Session = Depends(get_db)
):
    cita = db.query(CitaVeterinaria).filter(CitaVeterinaria.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    cita.estado = estado_in.estado
    db.commit()
    db.refresh(cita)
    return cita