# middleware/auth.py

# Importaciones necesarias
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config.security import verify_token
from config.db import get_db
from models.user import users
from sqlalchemy import select

# Configurar el esquema OAuth2 con la ruta del endpoint de autenticación
# tokenUrl="token" indica que el endpoint para obtener el token está en /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Middleware para obtener el usuario actual desde el token JWT."""

     # Definir la excepción que se lanzará si hay problemas de autenticación
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
     # Verificar y decodificar el token JWT
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
        
     # Extraer el email del usuario del token (guardado en el campo 'sub')
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    # Buscar el usuario en la base de datos usando el email
    with get_db() as db:
        query = select(users).where(users.c.email == email)
        user = db.execute(query).mappings().first() # Usar .mappings() para obtener un diccionario

        # Si el usuario no existe, lanzar excepción
        if user is None:
            raise credentials_exception
        
        # Retornar los datos del usuario si todo es correcto
        return dict(user)  # Convertir el objeto User en un diccionario 