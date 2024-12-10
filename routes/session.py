# routes/user.py

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, status, Depends
from config.db import get_db
from models.session import sessions  # sessions es la tabla de la base de datos
from schemas.session import Session as SessionSchema
# from passlib.context import CryptContext  # Para bcrypt
from sqlalchemy.exc import SQLAlchemyError  # Para manejar errores de la base de datos
from sqlalchemy import select
from middleware.auth import get_current_user  # Middleware


# Configurar bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

session = APIRouter(tags=["sessions"])



# -------------------------------------------------------------------
# Endpoint para obtener la lista de todas las sesiones de un fotógrafo
# -------------------------------------------------------------------
@session.get(
        "/sessions", 
        response_model=list[SessionSchema],
        summary="Obtener sesiones",
        description="Retorna la información de las sesiones del fotógrafo autenticado actual.",
        responses={
            200: {"description": "Sesiones encontradas"},
            401: {"description": "No autenticado"}
        }
)
def get_sessions(current_user=Depends(get_current_user)):
    try:
        user_id = current_user["id"]  # Acceso correcto
        with get_db() as db:
            # Filtrar las sesiones por el user_id del usuario actual            
            query = select(sessions).where(sessions.c.photographer_id == user_id)
            # Ejecutamos la consulta
            result = db.execute(query).fetchall()
            return result
    except SQLAlchemyError as e:
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las sesiones: {str(e)}",
        )

