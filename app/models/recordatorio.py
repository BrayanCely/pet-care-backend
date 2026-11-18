from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Recordatorio(Base):
    __tablename__ = "recordatorios"

    id_recordatorio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(30), nullable=False)  # Ej: 'medicamento', 'vacuna', 'desparasitacion'
    fecha_programada = Column(TIMESTAMP, nullable=False)
    frecuencia = Column(String(20), nullable=True)  # Ej: 'diaria', 'semanal', 'unica'
    notificado = Column(Boolean, default=False)
    fecha_notificacion = Column(TIMESTAMP, nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relaciones
    mascota = relationship("Mascota", back_populates="recordatorios")
    medicamentos = relationship("Medicamento", back_populates="recordatorio")
    vacunas = relationship("Vacuna", back_populates="recordatorio")


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota", ondelete="CASCADE"), nullable=False)
    id_recordatorio = Column(Integer, ForeignKey("recordatorios.id_recordatorio", ondelete="SET NULL"), nullable=True)
    nombre_medicamento = Column(String(100), nullable=False)
    dosis = Column(String(50), nullable=True)
    unidad_medida = Column(String(20), nullable=True)  # Ej: 'ml', 'pastilla', 'mg'
    frecuencia_administracion = Column(String(50), nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    observaciones = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    mascota = relationship("Mascota", back_populates="medicamentos")
    recordatorio = relationship("Recordatorio", back_populates="medicamentos")


class Vacuna(Base):
    __tablename__ = "vacunas"

    id_vacuna = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota", ondelete="CASCADE"), nullable=False)
    id_recordatorio = Column(Integer, ForeignKey("recordatorios.id_recordatorio", ondelete="SET NULL"), nullable=True)
    id_profesional = Column(Integer, ForeignKey("profesionales.id_profesional", ondelete="SET NULL"), nullable=True)
    nombre_vacuna = Column(String(100), nullable=False)
    fecha_aplicacion = Column(Date, nullable=False)
    fecha_proxima_dosis = Column(Date, nullable=True)
    numero_dosis = Column(Integer, default=1)
    lote = Column(String(50), nullable=True)
    veterinario_nombre = Column(String(100), nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relaciones
    mascota = relationship("Mascota", back_populates="vacunas")
    recordatorio = relationship("Recordatorio", back_populates="vacunas")
    profesional = relationship("Profesional", back_populates="vacunas")