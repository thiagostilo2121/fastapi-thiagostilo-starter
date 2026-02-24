from sqlmodel import Session, select
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.core.exceptions import EntityNotFoundError, BusinessLogicError

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if not user or not user.is_active:
        raise EntityNotFoundError("Usuario no encontrado")
    return user

def create_user(session: Session, user_in: UserCreate) -> User:
    existing_user = get_user_by_email(session, user_in.email)
    if existing_user:
        raise BusinessLogicError("El email ya está registrado")
    
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
