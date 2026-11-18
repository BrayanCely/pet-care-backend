from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.schemas.mascota import MascotaCreate, MascotaUpdate, MascotaResponse

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])

@router.post("/", response_model=MascotaResponse, status_code=status.HTTP_201_CREATED)
def crear_mascota(
    mascota_in: MascotaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    nueva_mascota = Mascota(
        **mascota_in.model_dump(),
        id_usuario=current_user.id_usuario
    )
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota

@router.get("/mis-mascotas", response_model=List[MascotaResponse])
def listar_mis_mascotas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Mascota).filter(
        Mascota.id_usuario == current_user.id_usuario,
        Mascota.activo == True
    ).all()

@router.get("/{id_mascota}", response_model=MascotaResponse)
def obtener_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    mascota = db.query(Mascota).filter(
        Mascota.id_mascota == id_mascota,
        Mascota.id_usuario == current_user.id_usuario
    ).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

@router.patch("/{id_mascota}", response_model=MascotaResponse)
def actualizar_mascota(
    id_mascota: int,
    datos: MascotaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    mascota = db.query(Mascota).filter(
        Mascota.id_mascota == id_mascota,
        Mascota.id_usuario == current_user.id_usuario
    ).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    
    update_data = datos.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(mascota, campo, valor)
        
    db.commit()
    db.refresh(mascota)
    return mascota

@router.delete("/{id_mascota}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    mascota = db.query(Mascota).filter(
        Mascota.id_mascota == id_mascota,
        Mascota.id_usuario == current_user.id_usuario
    ).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    
    # Inactivación lógica
    mascota.activo = False
    db.commit()
    return None