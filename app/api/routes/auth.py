from fastapi import APIRouter, Request
from app.api.deps import SessionDep
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.core.rate_limit import limiter
from app.core.security import create_access_token
from app.services import auth_service, user_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, session: SessionDep, data: UserCreate):
    """
    Inicia sesión obteniendo un JWT. Limitado a 5 intentos por minuto.
    """
    user = auth_service.authenticate(session, data.email, data.password)
    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token)

@router.post("/register", response_model=UserResponse)
@limiter.limit("10/minute")
def create_new_user(request: Request, session: SessionDep, user_in: UserCreate):
    """
    Crea un nuevo usuario en la plataforma.
    """
    user = user_service.create_user(session, user_in)
    return user
