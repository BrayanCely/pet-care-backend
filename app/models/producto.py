from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(50), nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    imagen_url = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    veterinaria = relationship("Veterinaria", back_populates="productos")
    detalles_carrito = relationship("DetalleCarrito", back_populates="producto")
    detalles_pedido = relationship("DetallePedido", back_populates="producto")


class CarritoCompras(Base):
    __tablename__ = "carritos_compras"

    id_carrito = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="carritos")
    detalles = relationship("DetalleCarrito", back_populates="carrito", cascade="all, delete-orphan")


class DetalleCarrito(Base):
    __tablename__ = "detalles_carrito"

    id_detalle_carrito = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_carrito = Column(Integer, ForeignKey("carritos_compras.id_carrito", ondelete="CASCADE"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto", ondelete="CASCADE"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)

    # Relaciones
    carrito = relationship("CarritoCompras", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_carrito")


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria", ondelete="CASCADE"), nullable=False)
    fecha_pedido = Column(TIMESTAMP, server_default=func.now())
    total = Column(Float, nullable=False)
    estado = Column(String(20), server_default="pendiente")  # pendiente, pagado, enviado, entregado, cancelado
    direccion_envio = Column(Text, nullable=False)

    # Relaciones
    usuario = relationship("Usuario", back_populates="pedidos")
    veterinaria = relationship("Veterinaria", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")


class DetallePedido(Base):
    __tablename__ = "detalles_pedido"

    id_detalle_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido", ondelete="CASCADE"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto", ondelete="CASCADE"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    # Relaciones
    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_pedido")