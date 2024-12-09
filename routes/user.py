# routes/user.py

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, status
from config.db import get_db
from models.user import users  # users es la tabla de la base de datos
from schemas.user import User, UserCreate, UserUpdate  # Clase User
from passlib.context import CryptContext  # Para bcrypt
from sqlalchemy.exc import SQLAlchemyError  # Para manejar errores de la base de datos


# Configurar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user = APIRouter()


# -------------------------------------------------------------------
# Endpoint para crear un nuevo usuario. Recibe los datos del usuario,
# encripta la contraseña y devuelve el usuario creado con su ID
# -------------------------------------------------------------------
@user.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        # Preparar los datos del nuevo usuario
        new_user = {"name": user.name, "email": user.email, "password": user.password}

        # Encriptar la contraseña
        new_user["password"] = pwd_context.hash(user.password)

        # Usar context manager para manejar la conexión
        with get_db() as db:
            # Ejecutar la inserción del nuevo usuario
            result = db.execute(users.insert().values(new_user))

            # Obtener y retornar el usuario recién creado
            created_user = db.execute(
                users.select().where(users.c.id == result.lastrowid)
            ).first()

            return created_user

    except SQLAlchemyError as e:
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}",
        )
    except Exception as e:
        # Manejar otros errores inesperados
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error inesperado: {str(e)}",
        )


# -------------------------------------------------------------------
# Endpoint para obtener la lista de todos los usuarios registrados
# -------------------------------------------------------------------
@user.get("/users", response_model=list[User])
def get_users():
    try:
        with get_db() as db:
            # Ejecutamos la consulta
            result = db.execute(users.select()).fetchall()
            return result
    except SQLAlchemyError as e:
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los usuarios: {str(e)}",
        )


# -------------------------------------------------------------------
# Endpoint para obtener un usuario por su ID. Devuelve los datos del usuario
# si existe, o un error 404 si no se encuentra
# -------------------------------------------------------------------
@user.get(
    "/users/{id}",
    response_model=User,
    responses={
        404: {"description": "Usuario no encontrado"},
        500: {"description": "Error interno del servidor"},
    },
)
def get_user(id: int):
    try:
        with get_db() as db:
            # Ejecutamos la consulta
            user = db.execute(users.select().where(users.c.id == id)).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con id {id} no encontrado",
                )

            return user

    except SQLAlchemyError as e:
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el usuario: {str(e)}",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID de usuario inválido: {str(e)}",
        )


# -------------------------------------------------------------------
# Endpoint para eliminar un usuario por su ID. Devuelve 204 si la eliminación
# fue exitosa, o 404 si el usuario no existe
# -------------------------------------------------------------------
@user.delete(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Usuario no encontrado"},
        500: {"description": "Error interno del servidor"},
    },
)
def delete_user(id: str):
    try:
        with get_db() as db:
            # Verificamos si existe el usuario
            user = db.execute(users.select().where(users.c.id == id)).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con id {id} no encontrado",
                )

            # Ejecutamos la eliminación
            db.execute(users.delete().where(users.c.id == id))

            return None  # 204 No Content no devuelve body

    except SQLAlchemyError as e:
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el usuario: {str(e)}",
        )


# -------------------------------------------------------------------
# Endpoint para actualizar un usuario por su ID. Actualiza solo los campos
# proporcionados, encripta la contraseña si se proporciona una nueva, y
# devuelve el usuario actualizado o 404 si no existe
# -------------------------------------------------------------------
@user.put(
    "/users/{id}",
    response_model=User,
    responses={404: {"description": "Usuario no encontrado"}},
)
def update_user(id: int, user_update: UserUpdate):
    try:
        with get_db() as db:
            # Verificamos si existe el usuario
            existing_user = db.execute(users.select().where(users.c.id == id)).first()
            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con id {id} no encontrado",
                )

            # Preparamos los datos actualizados
            update_data = user_update.model_dump(
                exclude_unset=True
            )  # Solo incluye campos proporcionados

            # Encriptamos la contraseña si se proporciona
            if "password" in update_data and update_data["password"]:
                update_data["password"] = pwd_context.hash(update_data["password"])

            # Ejecutamos la actualización
            result = db.execute(
                users.update().where(users.c.id == id).values(update_data)
            )

            # Retornamos el usuario actualizado
            return db.execute(users.select().where(users.c.id == id)).first()

    except SQLAlchemyError as e:
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el usuario: {str(e)}",
        )
