import sys
import os
from pathlib import Path

# Agregar la ruta raíz (pet-care-backend) al sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# IMPORTACIONES DESDE APP DIRECTAMENTE (sin .core)
from app.database import Base
from app.config import settings

# Importar modelos para la detección de Alembic
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.models.veterinaria import Veterinaria, Profesional, CitaVeterinaria
from app.models.recordatorio import Recordatorio, Medicamento, Vacuna
from app.models.producto import Producto, CarritoCompras, DetalleCarrito, Pedido, DetallePedido
from app.models.resena import Resena
from app.models.mensaje import Mensaje

config = context.config

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()