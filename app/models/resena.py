from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Resena(Base):
    __tablename__ = "resenas"

    id_resena = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria", ondelete="CASCADE"), nullable=False)
    calificacion = Column(Integer, nullable=False)  # Valor entre 1 y 5
    comentario = Column(Text, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="resenas")
    veterinaria = relationship("Veterinaria", back_populates="resenas")