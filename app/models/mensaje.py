from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from app.database import Base

class Mensaje(Base):
    __tablename__ = "mensajes"

    id_mensaje = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, nullable=False)
    id_emisor = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_receptor = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)