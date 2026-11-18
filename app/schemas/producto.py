from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# --- PRODUCTOS ---
class ProductoBase(BaseModel):
    id_veterinaria: int
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio: float
    stock: int
    imagen_url: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id_producto: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)


# --- CARRITO ---
class ItemCarritoCreate(BaseModel):
    id_producto: int
    cantidad: int

class ItemCarritoResponse(BaseModel):
    id_detalle_carrito: int
    id_producto: int
    cantidad: int
    producto: ProductoResponse

    model_config = ConfigDict(from_attributes=True)

class CarritoResponse(BaseModel):
    id_carrito: int
    id_usuario: int
    fecha_creacion: datetime
    detalles: List[ItemCarritoResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- PEDIDOS ---
class PedidoCreate(BaseModel):
    id_veterinaria: int
    direccion_envio: str

class DetallePedidoResponse(BaseModel):
    id_detalle_pedido: int
    id_producto: int
    cantidad: int
    precio_unitario: float

    model_config = ConfigDict(from_attributes=True)

class PedidoResponse(BaseModel):
    id_pedido: int
    id_usuario: int
    id_veterinaria: int
    fecha_pedido: datetime
    total: float
    estado: str
    direccion_envio: str
    detalles: List[DetallePedidoResponse] = []

    model_config = ConfigDict(from_attributes=True)