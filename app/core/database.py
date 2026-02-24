import logging
from sqlmodel import SQLModel, create_engine
from app.core.config import settings

logger = logging.getLogger(__name__)

# Configuración del Engine
engine_args = {}
# Para SQLite en threads (FastAPI) es necesario esto
if "sqlite" in settings.DATABASE_URL:
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, **engine_args)

async def create_db_and_tables():
    """Para generar las tablas en SQLite al inicio de la app"""
    logger.info("Verificando/Creando tablas de la Base de Datos...")
    SQLModel.metadata.create_all(engine)
    logger.info("Inicialización de la Base de Datos finalizada.")
