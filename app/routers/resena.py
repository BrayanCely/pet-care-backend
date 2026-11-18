from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.veterinaria import Veterinaria
from app.models.resena import Resena
from app.schemas.resena import ResenaCreate, ResenaUpdate, ResenaResponse

router = APIRouter(prefix="/resenas", tags=["Reseñas y Calificaciones"])

def recalcular_promedio_veterinaria(id_veterinaria: int, db: Session):
    """Calcula el promedio de calificaciones y actualiza la veterinaria"""
    promedio = db.query(func.avg(Resena.calificacion)).filter(
        Resena.id_veterinaria == id_veterinaria
    ).scalar() or 0.0

    vet = db.query(Veterinaria).filter(Veterinaria.id_veterinaria == id_veterinaria).first()
    if vet:
        vet.calificacion_promedio = round(float(promedio), 2)
        db.commit()


@router.post("/", response_model=ResenaResponse, status_code=status.HTTP_201_CREATED)
def crear_resena(
    resena_in: ResenaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Validar existencia de la veterinaria
    vet = db.query(Veterinaria).filter(
        Veterinaria.id_veterinaria == resena_in.id_veterinaria,
        Veterinaria.activo == True
    ).first()
    if not vet:
        raise HTTPException(status_code=404, detail="Veterinaria no encontrada")

    # Verificar si el usuario ya reseñó esta veterinaria
    resena_existente = db.query(Resena).filter(
        Resena.id_usuario == current_user.id_usuario,
        Resena.id_veterinaria == resena_in.id_veterinaria
    ).first()
    if resena_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya has publicado una reseña para esta veterinaria. Puedes actualizarla si lo deseas."
        )

    nueva_resena = Resena(
        **resena_in.model_dump(),
        id_usuario=current_user.id_usuario
    )
    db.add(nueva_resena)
    db.commit()
    db.refresh(nueva_resena)

    # Actualizar promedio de la veterinaria
    recalcular_promedio_veterinaria(resena_in.id_veterinaria, db)

    return nueva_resena


@router.get("/veterinaria/{id_veterinaria}", response_model=List[ResenaResponse])
def listar_resenas_veterinaria(
    id_veterinaria: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    return db.query(Resena).filter(
        Resena.id_veterinaria == id_veterinaria
    ).offset(skip).limit(limit).all()


@router.patch("/{id_resena}", response_model=ResenaResponse)
def actualizar_resena(
    id_resena: int,
    datos: ResenaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    resena = db.query(Resena).filter(
        Resena.id_resena == id_resena,
        Resena.id_usuario == current_user.id_usuario
    ).first()
    if not resena:
        raise HTTPException(status_code=404, detail="Reseña no encontrada o no tienes permiso para editarla")

    update_data = datos.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(resena, campo, valor)

    db.commit()
    db.refresh(resena)

    # Recalcular calificación promedio
    recalcular_promedio_veterinaria(resena.id_veterinaria, db)

    return resena


@router.delete("/{id_resena}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_resena(
    id_resena: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    resena = db.query(Resena).filter(
        Resena.id_resena == id_resena,
        Resena.id_usuario == current_user.id_usuario
    ).first()
    if not resena:
        raise HTTPException(status_code=404, detail="Reseña no encontrada o no tienes permiso para eliminarla")

    id_vet = resena.id_veterinaria
    db.delete(resena)
    db.commit()

    # Recalcular calificación promedio tras eliminar
    recalcular_promedio_veterinaria(id_vet, db)

    return None