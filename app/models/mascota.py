from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id_mascota = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(50), nullable=True)
    sexo = Column(String(20), nullable=True)
    edad = Column(Integer, nullable=True)
    peso = Column(String(20), nullable=True)
    peso_kg = Column(Integer, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    color_mascota = Column(String(50), nullable=True)
    numero_chip = Column(String(100), nullable=True)
    foto_url = Column(String(255), nullable=True)
    alergias = Column(Text, nullable=True)
    condiciones_medicas = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    # Relaciones
    propietario = relationship("Usuario", back_populates="mascotas")
    citas = relationship("CitaVeterinaria", back_populates="mascota", cascade="all, delete-orphan")
    medicamentos = relationship("Medicamento", back_populates="mascota", cascade="all, delete-orphan")
    vacunas = relationship("Vacuna", back_populates="mascota", cascade="all, delete-orphan")
    recordatorios = relationship("Recordatorio", back_populates="mascota", cascade="all, delete-orphan")