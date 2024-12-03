from fastapi import APIRouter
from config.db import conn
from models.user import users # users es la tabla de la base de datos
from schemas.user import User # Clase User
from cryptography.fernet import Fernet # Para encriptar la contraseña

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get("/users")
def get_users():
    return  conn.execute(users.select()).fetchall()


@user.post("/users")
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email, "password": user.password}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get("/users")
def helloworld():
    return {"message": "Hello World1"}


@user.get("/users")
def helloworld():
    return {"message": "Hello World1"}


@user.get("/users")
def helloworld():
    return {"message": "Hello World1"}