class DomainException(Exception):
    """Clase base de donde heredan todos los errores de tu dominio."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class EntityNotFoundError(DomainException):
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, status_code=404)

class BusinessLogicError(DomainException):
    def __init__(self, message: str = "Error de validación o lógica de negocio"):
        super().__init__(message, status_code=400)

class PermissionDeniedError(DomainException):
    def __init__(self, message: str = "No tiene permisos para realizar esta acción"):
        super().__init__(message, status_code=403)

class AuthenticationError(DomainException):
    def __init__(self, message: str = "Credenciales incorrectas o sesión expirada"):
        super().__init__(message, status_code=401)
