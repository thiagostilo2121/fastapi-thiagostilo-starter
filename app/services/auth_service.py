from sqlmodel import Session
from app.models.user import User
from app.core.security import verify_password
from app.core.exceptions import AuthenticationError
from app.services import user_service

def authenticate(session: Session, email: str, password: str) -> User:
    user = user_service.get_user_by_email(session, email)
    if not user or not user.is_active:
        raise AuthenticationError("Email o contraseña incorrectos")
    
    if not verify_password(password, user.hashed_password):
        raise AuthenticationError("Email o contraseña incorrectos")
        
    return user
