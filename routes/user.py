# routes/user.py

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, status, Depends
from config.db import get_db
from models.user import users  # users es la tabla de la base de datos
from models.user import UserRole  # Importar el enum de roles
from schemas.user import User, UserCreate, UserUpdate  # Clase User
from passlib.context import CryptContext  # Para bcrypt
from sqlalchemy.exc import SQLAlchemyError  # Para manejar errores de la base de datos
from middleware.auth import get_current_user  # Middleware


# Configurar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user = APIRouter(tags=["users"])


# -------------------------------------------------------------------
# Endpoint para crear un nuevo usuario. Recibe los datos del usuario,
# encripta la contraseña y devuelve el usuario creado con su ID
# -------------------------------------------------------------------
@user.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, current_user=Depends(get_current_user)):
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
# Endpoint que obtiene el usuario actual autenticado.
# Ruta: GET /users/me
# Response model: User (esquema Pydantic)
# Seguridad: Requiere token JWT válido
# -------------------------------------------------------------------
@user.get(
    "/users/me",
    response_model=User,
    summary="Obtener usuario actual",
    description="Retorna la información del usuario autenticado actual.",
    responses={
        200: {"description": "Usuario autenticado encontrado"},
        401: {"description": "No autenticado"},
    },
)
# Inyecta el usuario actual usando el middleware get_current_user
# Si el token es válido, current_user contendrá los datos del usuario
# Si el token es inválido, get_current_user lanzará una HTTPException
def read_users_me(current_user=Depends(get_current_user)):

    return current_user


# -------------------------------------------------------------------
# Endpoint para obtener la lista de todos los usuarios registrados
# -------------------------------------------------------------------
@user.get("/users", response_model=list[User])
def get_users(current_user=Depends(get_current_user)):
    try:
        with get_db() as db:
            # Si es admin, mostrar todos los usuarios
            if current_user["role"] == UserRole.admin:
                result = db.execute(users.select()).fetchall()
                return result

            # Si es fotógrafo, mostrar solo sus clientes
            elif current_user["role"] == UserRole.photographer:
                result = db.execute(
                    users.select().where(users.c.photographer_id == current_user["id"])
                ).fetchall()
                return result

            # Si es cliente, denegar acceso
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Los clientes no tienen permiso para ver la lista de usuarios",
                )

            """
            result = db.execute(users.select()).fetchall()
            return result
            """

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
        403: {"description": "Acceso denegado"},
        500: {"description": "Error interno del servidor"},
    },
)
def get_user(id: int, current_user=Depends(get_current_user)):
    try:
        with get_db() as db:
            # Si es admin, puede ver cualquier usuario
            if current_user["role"] == UserRole.admin:
                user = db.execute(users.select().where(users.c.id == id)).first()
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Usuario con id {id} no encontrado",
                    )
                return user

            # Si es fotógrafo, solo puede ver sus clientes
            elif current_user["role"] == UserRole.photographer:
                user = db.execute(
                    users.select().where(
                        users.c.id == id, users.c.photographer_id == current_user["id"]
                    )
                ).first()
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permiso para ver este usuario",
                    )
                return user

            # Si es cliente, no tiene acceso a ver otros usuarios
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Los clientes no tienen permiso para ver usuarios",
                )

            """# Ejecutamos la consulta
            user = db.execute(users.select().where(users.c.id == id)).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con id {id} no encontrado",
                )

            return user"""

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
# Endpoint para eliminar un usuario por su ID
# DELETE /users/{id}
#
# Parámetros:
#   - id (int): ID del usuario a eliminar
#
# Respuestas:
#   - 204: Usuario eliminado correctamente (sin contenido)
#   - 404: Usuario no encontrado
#   - 500: Error interno del servidor
#
# Requiere autenticación: Sí
# -------------------------------------------------------------------
@user.delete(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        403: {"description": "Acceso denegado"},
        404: {"description": "Usuario no encontrado"},
        500: {"description": "Error interno del servidor"},
    },
)
def delete_user(id: int, current_user=Depends(get_current_user)):
    try:
        with get_db() as db:
             # Verificamos si existe el usuario a eliminar
            user_to_delete = db.execute(users.select().where(users.c.id == id)).first()

             # Control de acceso basado en roles
            if current_user["role"] == UserRole.admin:
                # Los administradores pueden eliminar cualquier usuario
                if not user_to_delete:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Usuario con id {id} no encontrado"
                    )
                db.execute(users.delete().where(users.c.id == id))
                return None
            
            elif current_user["role"] == UserRole.photographer:
                # Los fotógrafos solo pueden eliminar sus clientes
                if not user_to_delete:
                    print(f"❌ No tienes permiso para eliminar este usuario {id}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="El usuario no existe o no puedes eliminarlo"                        
                    )
                
                if user_to_delete["photographer_id"] != current_user["id"]:
                    print(f"❌ El cliente {id} no pertenede a tu usuario {current_user['id']}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="El usuario no existe o no puedes eliminarlo"                        
                    )
                
                db.execute(users.delete().where(users.c.id == id))
                return None
            
            else:
                # Los clientes no pueden eliminar usuarios
                print(f"❌ Un cliente no puede eliminar usuarios")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para eliminar usuarios"                    
                )



            '''# Verificamos si existe el usuario
            user = db.execute(users.select().where(users.c.id == id)).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con id {id} no encontrado",
                )

            # Ejecutamos la eliminación
            db.execute(users.delete().where(users.c.id == id))

            return None  # 204 No Content no devuelve body'''

    except SQLAlchemyError as e:
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el usuario: {str(e)}",
        )


# -------------------------------------------------------------------
# Endpoint para actualizar un usuario por su ID
# PUT /users/{id}
#
# Parámetros:
#   - id (int): ID del usuario a actualizar
#   - user_update (UserUpdate): Datos a actualizar
#     - email (str, opcional): Nuevo email
#     - password (str, opcional): Nueva contraseña
#     - role (str, opcional): Rol del usuario
#
# Respuestas:
#   - 200: Usuario actualizado correctamente (devuelve usuario actualizado)
#   - 404: Usuario no encontrado
#   - 401: No autorizado
#   - 422: Error de validación en los datos
#   - 500: Error interno del servidor
#
# Requiere autenticación: Sí
# -------------------------------------------------------------------
@user.put(
    "/users/{id}",
    response_model=User,
    responses={404: {"description": "Usuario no encontrado"}},
)
def update_user(
    id: int, user_update: UserUpdate, current_user=Depends(get_current_user)
):
    try:
        with get_db() as db:
            # Verificamos si existe el usuario a actualizar
            existing_user = db.execute(users.select().where(users.c.id == id)).first()
            if not existing_user:
                print(f"❌ Usuario {id} no encontrado")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Control de acceso basado en roles
            if current_user["role"] == UserRole.admin:
                # Los administradores pueden actualizar cualquier usuario
                print(f"✅ Admin con id {current_user['id']}  actualizando usuario con id {id}")
            
            elif current_user["role"] == UserRole.photographer:
                # Los fotógrafos solo pueden actualizar sus clientes
                if existing_user["photographer_id"] != current_user["id"]:
                    print(f"❌ Fotógrafo {current_user['id']} intentó actualizar usuario {id} que no le pertenece")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Solo puedes actualizar tus propios clientes"
                    )
                print(f"✅ Fotógrafo {current_user['id']} actualizando su cliente {id}")
            
            else:
                # Los clientes no pueden actualizar usuarios
                print(f"❌ Cliente {current_user['id']} intentó actualizar usuario {id}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Los clientes no tienen permiso para actualizar usuarios"
                )


            '''# Verificamos si existe el usuario
            existing_user = db.execute(users.select().where(users.c.id == id)).first()
            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con id {id} no encontrado",
                )
            '''
            
             # Preparamos los datos actualizados (Solo incluye campos proporcionados)
            update_data = user_update.model_dump(exclude_unset=True)

            # Encriptamos la contraseña si se proporciona
            if "password" in update_data and update_data["password"]:
                update_data["password"] = pwd_context.hash(update_data["password"])

            # Ejecutamos la actualización
            result = db.execute(
                users.update().where(users.c.id == id).values(update_data)
            )

            # Retornamos el usuario actualizado
            updated_user = db.execute(users.select().where(users.c.id == id)).first()
            return updated_user

    except SQLAlchemyError as e:
        print(f"❌ Error en la base de datos: {str(e)}")
        # Manejar errores específicos de la base de datos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el usuario: {str(e)}",
        )
