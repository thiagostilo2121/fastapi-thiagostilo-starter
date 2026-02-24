from typing import Generator, Annotated
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session

from app.core.config import settings
from app.core.database import engine
from app.core.security import ALGORITHM
from app.core.exceptions import AuthenticationError
from app.models.user import User
from app.services.user_service import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/auth/login")

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_sub = payload.get("sub")
        if token_sub is None:
            raise AuthenticationError("No se pudo validar las credenciales")
        user_id = int(token_sub)
    except JWTError:
        raise AuthenticationError("Token inválido o expirado")
        
    return get_user(session, user_id)

CurrentUser = Annotated[User, Depends(get_current_user)]
