from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud.usuario import delete_usuario
from app.models.usuario import Usuario

from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, Token
from app.crud.usuario import get_usuario_by_correo, create_usuario
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.
    Valida que el correo no esté ya registrado antes de crear.
    """
    usuario_existente = get_usuario_by_correo(db, usuario_data.correo_electronico)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario registrado con este correo electrónico",
        )
    return create_usuario(db, usuario_data)

@router.delete("/usuarios/{id_usuario}", status_code=status.HTTP_200_OK)
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario por su ID.
    """
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con ID {id_usuario} no existe."
        )
    
    try:
        db.delete(usuario)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el usuario porque tiene registros asociados (mascotas, citas, etc.)."
        )
        
    return {"mensaje": f"Usuario con ID {id_usuario} eliminado exitosamente."}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autentica a un usuario y devuelve un token JWT.
    Usa OAuth2PasswordRequestForm: espera 'username' y 'password' (form-data),
    donde 'username' será el correo electrónico.
    """
    usuario = get_usuario_by_correo(db, form_data.username)

    if not usuario or not verify_password(form_data.password, usuario.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    access_token = create_access_token(data={"sub": str(usuario.id_usuario)})
    return Token(access_token=access_token)