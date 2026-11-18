from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Veterinaria(Base):
    __tablename__ = "veterinarias"

    id_veterinaria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_comercial = Column(String(100), nullable=False)
    direccion = Column(Text, nullable=False)
    telefono = Column(String(20), nullable=False)
    correo_electronico = Column(String(100), nullable=True)
    horario_atencion = Column(String(100), nullable=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    calificacion_promedio = Column(Float, default=0.0)
    activo = Column(Boolean, default=True)

    # Relaciones
    profesionales = relationship("Profesional", back_populates="veterinaria", cascade="all, delete-orphan")
    citas = relationship("CitaVeterinaria", back_populates="veterinaria")
    productos = relationship("Producto", back_populates="veterinaria")
    pedidos = relationship("Pedido", back_populates="veterinaria")
    resenas = relationship("Resena", back_populates="veterinaria")


class Profesional(Base):
    __tablename__ = "profesionales"

    id_profesional = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria", ondelete="CASCADE"), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    especialidad = Column(String(50), nullable=True)
    numero_registro_profesional = Column(String(30), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo_electronico = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    veterinaria = relationship("Veterinaria", back_populates="profesionales")
    citas = relationship("CitaVeterinaria", back_populates="profesional")
    vacunas = relationship("Vacuna", back_populates="profesional")


class CitaVeterinaria(Base):
    __tablename__ = "citas_veterinarias"

    id_cita = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota", ondelete="CASCADE"), nullable=False)
    id_profesional = Column(Integer, ForeignKey("profesionales.id_profesional", ondelete="CASCADE"), nullable=False)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria", ondelete="CASCADE"), nullable=False)
    fecha_cita = Column(TIMESTAMP, nullable=False)
    motivo = Column(String(200), nullable=False)
    estado = Column(String(20), server_default="programada")
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relaciones
    mascota = relationship("Mascota", back_populates="citas")
    profesional = relationship("Profesional", back_populates="citas")
    veterinaria = relationship("Veterinaria", back_populates="citas")