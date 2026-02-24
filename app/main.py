from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.error_handlers import register_exception_handlers
from app.core.rate_limit import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Genera dev.db al inicio para ambiente local
    await create_db_and_tables()
    yield

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="FastAPI Boilerplate with Security, JWT, SQLModel & Clean Arch",
        version=settings.VERSION,
        lifespan=lifespan,
    )

    # Rate Limiting
    application.state.limiter = limiter
    application.add_middleware(SlowAPIMiddleware)

    # CORS
    cors_origins = [settings.FRONTEND_URL] if settings.ENVIRONMENT == "production" else ["*"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Manejo Centralizado de Excepciones del Dominio
    register_exception_handlers(application)
    
    @application.get("/health", tags=["Salud del Sistema"])
    async def health_check():
        return {"status": "ok", "version": settings.VERSION}

    application.include_router(api_router, prefix="/api")

    return application

app = create_application()
