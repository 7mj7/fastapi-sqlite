# schemas/token.py

from pydantic import BaseModel

class Token(BaseModel):
    """
    Esquema Pydantic para la respuesta del token JWT.
    
    Attributes:
        access_token (str): El token JWT generado
        token_type (str): Tipo de token, generalmente "bearer"
    
    Example:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Esquema Pydantic para los datos contenidos en el token JWT.
    
    Attributes:
        email (str | None): Email del usuario almacenado en el token.
                           Es opcional (None) por defecto.
    
    Note:
        Este esquema representa los datos que se extraen del token JWT
        después de decodificarlo. El email se almacena en el campo 'sub'
        del token.
    
    Example:
        {
            "email": "usuario@ejemplo.com"
        }
    """
    email: str | None = None  # Union type (str o None) con valor por defecto None