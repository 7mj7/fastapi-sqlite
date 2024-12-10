# schemas/user.py

from typing import Optional
from pydantic import BaseModel, EmailStr

 # Esquema para crear un nuevo usuario. Requiere nombre, correo y contraseña.
class UserCreate(BaseModel):
    name: str
    email: EmailStr # Utiliza EmailStr para validar el correo
    password: str
    
 # Esquema que representa un usuario existente. Incluye un ID opcional.
class User(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    password: str

 # Esquema para actualizar la información de un usuario. Todos los campos son opcionales.
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None