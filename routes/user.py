from fastapi import APIRouter, HTTPException, status
from config.db import conn
from models.user import users # users es la tabla de la base de datos
from schemas.user import User # Clase User
from cryptography.fernet import Fernet # Para encriptar la contraseña

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

# -------------------------------------------------------------------
# Endpoint para crear un nuevo usuario. Recibe los datos del usuario,
# encripta la contraseña y devuelve el usuario creado con su ID
# -------------------------------------------------------------------
@user.post("/users/", 
    response_model=User, 
    status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email, "password": user.password}
    # Encriptar la contraseña antes de guardarla en la base de datos
    # Se codifica primero a utf-8 y luego se aplica la encriptación
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
     # Ejecutar la inserción del nuevo usuario en la base de datos
    result = conn.execute(users.insert().values(new_user))
    # Retornar el usuario recién creado
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

# -------------------------------------------------------------------
# Endpoint para obtener la lista de todos los usuarios registrados
# -------------------------------------------------------------------
@user.get("/users", response_model=list[User])
def get_users():
    return  conn.execute(users.select()).fetchall()

# -------------------------------------------------------------------
# Endpoint para obtener un usuario por su ID. Devuelve los datos del usuario
# si existe, o un error 404 si no se encuentra
# -------------------------------------------------------------------
@user.get("/users/{id}", response_model=User, responses={404: {"description": "Usuario no encontrado"}})
def get_user(id: str):
    user = conn.execute(users.select().where(users.c.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
        
# -------------------------------------------------------------------
# Endpoint para eliminar un usuario por su ID. Devuelve 204 si la eliminación
# fue exitosa, o 404 si el usuario no existe
# -------------------------------------------------------------------
@user.delete("/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Usuario no encontrado"}})
def delete_user(id: str):
    # Verificamos si existe el usuario    
    if not conn.execute(users.select().where(users.c.id == id)).first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Ejecutamos la eliminación
    conn.execute(users.delete().where(users.c.id == id))
    return None  # 204 No Content no devuelve body

# -------------------------------------------------------------------
# Endpoint para actualizar un usuario por su ID. Actualiza solo los campos
# proporcionados, encripta la contraseña si se proporciona una nueva, y
# devuelve el usuario actualizado o 404 si no existe
# -------------------------------------------------------------------
@user.put("/users/{id}",
    response_model=User,
    responses={404: {"description": "Usuario no encontrado"}})
def update_user(id: str, user: User):
    # Verificamos si existe el usuario
    if not conn.execute(users.select().where(users.c.id == id)).first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Preparamos los datos actualizados
    update_data = {
        "name": user.name,
        "email": user.email,
        "password": f.encrypt(user.password.encode("utf-8")) if user.password else None
    }
    # Removemos los campos None para no sobrescribir con null
    update_data = {k: v for k, v in update_data.items() if v is not None}
    # Ejecutamos la actualización
    conn.execute(users.update()
                .where(users.c.id == id)
                .values(update_data))
    
    # Retornamos el usuario actualizado
    return conn.execute(users.select().where(users.c.id == id)).first()

    '''
    old_user = get_user(id)
    if not old_user:
        return {"status": "Not Found"}
    new_user = old_user.copy()
    new_user["name"] = user.name or new_user["name"]
    new_user["email"] = user.email or new_user["email"]
    new_user["password"] = f.encrypt(user.password.encode("utf-8")) if user.password else new_user["password"]
    result = conn.execute(users.update().values(new_user).where(users.c.id == id))
    return result
    #return {"status": "Ok"}
    '''
