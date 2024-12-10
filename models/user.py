# models/user.py

# Importa Table y Column de SQLAlchemy para definir la estructura de tablas y columnas en la base de datos.
# Además, importa tipos de datos como Integer, String y Enum para especificar los tipos de las columnas.
from sqlalchemy import Table, Column, Integer, String, Enum

# Importa 'meta' para la metadata de la base de datos
from config.db import meta

# Importa el módulo enum de Python para crear enumeraciones personalizadas.
import enum

# Definir una clase Enum para los roles de los usuarios
class UserRole(enum.Enum):
    admin = "admin"
    photographer = "photographer"
    client = "client"


# Esquema de la tabla 'users' con sus columnas y restricciones.
users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), unique=True, nullable=False),  # Email debe ser unico
    Column("password", String(255), nullable=False),
    # Column("role", String(50)),  # 'admin', 'photographer' o 'client'
    Column("role", Enum(UserRole), nullable=False, default=UserRole.photographer),  # Usar Enum para role
)
