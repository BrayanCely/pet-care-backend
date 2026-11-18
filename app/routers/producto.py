from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.producto import Producto, CarritoCompras, DetalleCarrito, Pedido, DetallePedido
from app.schemas.producto import (
    ProductoCreate, ProductoUpdate, ProductoResponse,
    ItemCarritoCreate, CarritoResponse,
    PedidoCreate, PedidoResponse
)

router = APIRouter(prefix="/productos", tags=["Productos, Carrito y Pedidos"])

# ==================== PRODUCTOS ====================

@router.get("/", response_model=List[ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Producto).filter(Producto.activo == True).offset(skip).limit(limit).all()

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(prod_in: ProductoCreate, db: Session = Depends(get_db)):
    nuevo_prod = Producto(**prod_in.model_dump())
    db.add(nuevo_prod)
    db.commit()
    db.refresh(nuevo_prod)
    return nuevo_prod

@router.get("/{id_producto}", response_model=ProductoResponse)
def obtener_producto(id_producto: int, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


# ==================== CARRITO DE COMPRAS ====================

def obtener_o_crear_carrito(id_usuario: int, db: Session) -> CarritoCompras:
    carrito = db.query(CarritoCompras).filter(CarritoCompras.id_usuario == id_usuario).first()
    if not carrito:
        carrito = CarritoCompras(id_usuario=id_usuario)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
    return carrito

@router.get("/carrito/mi-carrito", response_model=CarritoResponse)
def ver_carrito(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_o_crear_carrito(current_user.id_usuario, db)

@router.post("/carrito/items", response_model=CarritoResponse)
def agregar_al_carrito(
    item_in: ItemCarritoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    prod = db.query(Producto).filter(Producto.id_producto == item_in.id_producto).first()
    if not prod or not prod.activo:
        raise HTTPException(status_code=404, detail="Producto no disponible")
    
    if prod.stock < item_in.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente para este producto")

    carrito = obtener_o_crear_carrito(current_user.id_usuario, db)
    
    # Verificar si el ítem ya existe en el carrito
    detalle = db.query(DetalleCarrito).filter(
        DetalleCarrito.id_carrito == carrito.id_carrito,
        DetalleCarrito.id_producto == item_in.id_producto
    ).first()

    if detalle:
        detalle.cantidad += item_in.cantidad
    else:
        detalle = DetalleCarrito(
            id_carrito=carrito.id_carrito,
            id_producto=item_in.id_producto,
            cantidad=item_in.cantidad
        )
        db.add(detalle)

    db.commit()
    db.refresh(carrito)
    return carrito


# ==================== PEDIDOS ====================

@router.post("/pedidos/checkout", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def realizar_pedido(
    pedido_in: PedidoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    carrito = obtener_o_crear_carrito(current_user.id_usuario, db)
    if not carrito.detalles:
        raise HTTPException(status_code=400, detail="El carrito de compras está vacío")

    total_pedido = 0.0
    detalles_pedido_crear = []

    for item in carrito.detalles:
        producto = item.producto
        if producto.stock < item.cantidad:
            raise HTTPException(
                status_code=400, 
                detail=f"Stock insuficiente para {producto.nombre}"
            )
        
        subtotal = producto.precio * item.cantidad
        total_pedido += subtotal
        
        # Descontar stock
        producto.stock -= item.cantidad

        detalles_pedido_crear.append(
            DetallePedido(
                id_producto=producto.id_producto,
                cantidad=item.cantidad,
                precio_unitario=producto.precio
            )
        )

    # Crear la cabecera del pedido
    nuevo_pedido = Pedido(
        id_usuario=current_user.id_usuario,
        id_veterinaria=pedido_in.id_veterinaria,
        total=total_pedido,
        direccion_envio=pedido_in.direccion_envio,
        detalles=detalles_pedido_crear
    )

    db.add(nuevo_pedido)
    
    # Vaciar el carrito
    db.query(DetalleCarrito).filter(DetalleCarrito.id_carrito == carrito.id_carrito).delete()
    
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido

@router.get("/pedidos/mis-pedidos", response_model=List[PedidoResponse])
def listar_mis_pedidos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Pedido).filter(Pedido.id_usuario == current_user.id_usuario).all()