# models/__init__.py
"""
Módulo de inicialización de modelos para la base de datos

Este módulo inicializa todos los modelos de la base de datos y establece
las relaciones entre las tablas. Proporciona un punto central para la 
importación de todos los modelos de la aplicación.

Modelos incluidos:
- users: Gestión de usuarios (fotógrafos y clientes)
- sessions: Sesiones fotográficas
- galleries: Galerías de fotos
- photos: Fotografías individuales

Ejemplo de uso:
    from models import users, sessions, galleries, photos
"""

from .user import users
from .session import sessions
from .gallery import galleries
from .photo import photos

# Importación de dependencias para crear las tablas
from config.db import engine, meta

# Creación de todas las tablas en la base de datos
# Este proceso verifica si las tablas existen y las crea si es necesario
meta.create_all(engine)

# Exportar los modelos para facilitar su importación
__all__ = ['users', 'sessions', 'galleries', 'photos']