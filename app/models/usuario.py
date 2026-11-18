from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    correo_electronico = Column(String(100), nullable=False, unique=True, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())
    rol = Column(String(20), server_default="cliente")
    activo = Column(Boolean, default=True)

    # Relaciones con los demás módulos
    mascotas = relationship("Mascota", back_populates="propietario", cascade="all, delete-orphan")
    carritos = relationship("CarritoCompras", back_populates="usuario")
    pedidos = relationship("Pedido", back_populates="usuario")
    resenas = relationship("Resena", back_populates="usuario")