# routes/user.py

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, status, Depends
from config.db import get_db
from models.session import sessions  # sessions es la tabla de la base de datos
from schemas.session import Session as SessionSchema
from models.user import UserRole  # Importar el enum de roles

from sqlalchemy.exc import SQLAlchemyError  # Para manejar errores de la base de datos
from sqlalchemy import select
from middleware.auth import get_current_user  # Middleware


session = APIRouter(tags=["sessions"])


# -------------------------------------------------------------------
# Endpoint para obtener la lista de todas las sesiones de un fotógrafo
# GET /sessions
# 
# Verifica:
#   - Que el usuario esté autenticado
#   - Que el usuario tenga rol de fotógrafo
# -------------------------------------------------------------------
@session.get(
    "/sessions",
    response_model=list[SessionSchema],
    summary="Obtener sesiones del fotógrafo",
    description="Retorna la información de las sesiones del fotógrafo autenticado.",
    responses={
        200: {"description": "Lista de sesiones encontradas"},
        401: {"description": "No autenticado"},
        403: {"description": "No autorizado - Se requiere rol de fotógrafo"},
        500: {"description": "Error interno del servidor"}
    }
)
def get_sessions(current_user=Depends(get_current_user)):
    try:

        # Verificar rol de fotógrafo
        if current_user["role"] != UserRole.photographer:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los fotógrafos pueden acceder a sus sesiones",
            )
        
        print(f"\n=== Obteniendo sesiones para fotógrafo ===")
        print(f"Fotógrafo ID: {current_user['id']}")
        print(f"Email: {current_user['email']}")

        user_id = current_user["id"]  # Acceso correcto

        with get_db() as db:
            # Filtrar las sesiones por el user_id del usuario actual
            print("\n🔍 Consultando sesiones en base de datos...")
            query = select(sessions).where(sessions.c.photographer_id == user_id)            
            result = db.execute(query).fetchall() # Ejecutamos la consulta

            print(f"✅ Sesiones encontradas: {len(result)}")
            print("\n=== Operación completada con éxito ===")

            return result
    except SQLAlchemyError as e:
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las sesiones: {str(e)}",
        )
