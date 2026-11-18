from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# En app/main.py cambia la línea 9:
from app.routers import (
    auth,
    usuarios,  # <-- Cambiar 'usuario' por 'usuarios'
    mascota,
    veterinaria,
    recordatorio,
    producto,
    resena,
    mensaje
)

# Crear tablas en la BD si no existen (útil para desarrollo rápido)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="peludOS",
    description="Backend completo con FastAPI, PostgreSQL y JWT para la gestión integral de mascotas, veterinarias, productos y recordatorios.",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplaza "*" por el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(mascota.router)
app.include_router(veterinaria.router)
app.include_router(recordatorio.router)
app.include_router(producto.router)
app.include_router(resena.router)
app.include_router(mensaje.router)

@app.get("/", tags=["Health Check"])
def status_check():
    return {
        "status": "online",
        "message": "API de Cuidado de Mascotas funcionando correctamente",
        "docs": "/docs"
    }