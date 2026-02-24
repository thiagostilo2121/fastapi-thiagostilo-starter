from fastapi import APIRouter
from app.api.deps import CurrentUser
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: CurrentUser):
    """
    Obtiene el perfil del usuario autenticado actualmente.
    """
    return current_user
