from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import DomainException
from slowapi.errors import RateLimitExceeded

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": f"Demasiadas peticiones. Intenta de nuevo más tarde."},
        )
