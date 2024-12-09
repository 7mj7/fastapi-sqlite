# config/db.py

# Importamos los componentes necesarios de SQLAlchemy:
# - create_engine: Crea el motor de base de datos para gestionar conexiones
# - MetaData: Contiene definiciones de tablas y otros elementos del esquema
from sqlalchemy import create_engine, MetaData
from contextlib import contextmanager

# Creación del motor de SQLAlchemy
# - sqlite:///./test.db: URL de conexión a la base de datos SQLite
# - check_same_thread=False: Permite acceso desde múltiples hilos (necesario para FastAPI)
# - isolation_level="AUTOCOMMIT": Comentado, pero permitiría auto-commit en cada operación
engine = create_engine(
    "sqlite:///./data/db/test.db", 
    connect_args={"check_same_thread": False},
    #isolation_level="AUTOCOMMIT"
    )

# Objeto MetaData: Registro central de todos los objetos de la base de datos
# - Almacena definiciones de tablas, índices y constraints
# - Sirve como punto de referencia para el esquema completo de la base de datos
meta = MetaData()

# Gestor de contexto para manejar conexiones a la base de datos
# Proporciona una forma segura de:
# - Obtener una conexión
# - Manejar transacciones (commit/rollback)
# - Cerrar la conexión automáticamente
@contextmanager
def get_db():
     # Establece una nueva conexión
    connection = engine.connect()
    try:
        # Cede la conexión al código que usa este contexto
        yield connection
        # Si no hay excepciones, confirma los cambios
        connection.commit()
    except Exception:
        # Si hay algún error, revierte los cambios
        connection.rollback()
         # Re-lanza la excepción para su manejo superior
        raise
    finally:
         # Garantiza que la conexión se cierre, incluso si hay errores
        connection.close()

'''
# En los endpoints
@user.post("/users/")
def create_user(user: UserCreate):
    with get_db() as db:
        # usar db para operaciones
        result = db.execute(...)
        return result
'''