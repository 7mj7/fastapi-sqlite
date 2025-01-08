# scripts/init_db.py

"""
Instrucciones de Ejecución:

Este script debe ejecutarse desde el directorio raíz del proyecto usando el módulo Python.

1. Para inicialización normal (crea tablas y datos solo si no existen):
   python -m scripts.init_db

2. Para reiniciar la base de datos (elimina todo y recrea desde cero):
   python -m scripts.init_db --reset

Ejemplos de uso:
    # Estando en el directorio raíz del proyecto:
    > python -m scripts.init_db         # Inicialización segura
    > python -m scripts.init_db --reset # Reinicio completo (¡Cuidado! Elimina datos existentes)

Notas:
- La opción --reset eliminará TODOS los datos existentes
- Asegúrese de tener respaldo antes de usar --reset
- El script creará usuarios de ejemplo por defecto
"""

# Importaciones necesarias
from config.db import get_db, engine, meta
from config.security import get_password_hash
from models.user import users  # Importar la tabla de usuarios
from models.gallery import galleries  # Importar la tabla de galerías
from models.session import sessions  # Importar la tabla de sesiones
from models.photo import photos  # Importar la tabla de fotografías
from models.gallery_photos import (
    gallery_photos,
)  # Importar la tabla de fotografías en galerías


# Función para inicializar la base de datos
def init_db():
    """
    Inicializa la base de datos y crea datos de ejemplo.
    Usa la configuración existente del archivo config/db.py
    """
    try:
        print("🚀 Iniciando creación de base de datos...")

        # Crear todas las tablas definidas en el metadata
        meta.create_all(engine)
        print("✅ Tablas creadas correctamente")

        # Usar el context manager get_db para manejar la conexión
        with get_db() as conn:
            # Verificar si ya existen usuarios
            result = conn.execute(users.select()).first()

            if not result:
                print("📝 Insertando usuarios de ejemplo...")

                # Insertar usuarios de ejemplo con IDs específicos
                usuarios = [
                    {
                        "id": 1,
                        "name": "Admin",
                        "email": "admin@example.com",
                        "password": get_password_hash("admin123"),
                        "role": "admin",
                        "photographer_id": None,  # Admin no tiene fotógrafo asignado
                    },
                    {
                        "id": 2,
                        "name": "Fotógrafo",
                        "email": "fotografo@example.com",
                        "password": get_password_hash("foto123"),
                        "role": "photographer",
                        "photographer_id": None,  # Fotógrafo no tiene fotógrafo asignado
                    },
                    {
                        "id": 3,
                        "name": "Cliente",
                        "email": "cliente@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 2,  # Cliente asignado al fotógrafo (ID 2)
                    },
                    {
                        "id": 4,
                        "name": "Cliente 4",
                        "email": "cliente4@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 2,  # Cliente asignado al fotógrafo (ID 2)
                    },
                    {
                        "id": 5,
                        "name": "Cliente 5",
                        "email": "cliente5@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 2,  # Cliente asignado al fotógrafo (ID 2)
                    },
                    {
                        "id": 6,
                        "name": "Fotógrafo 6",
                        "email": "fotografo6@example.com",
                        "password": get_password_hash("foto123"),
                        "role": "photographer",
                        "photographer_id": None,  # Fotógrafo no tiene fotógrafo asignado
                    },
                    {
                        "id": 7,
                        "name": "Cliente 7",
                        "email": "cliente7@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 6,  # Cliente asignado al fotógrafo (ID 6)
                    },
                    {
                        "id": 8,
                        "name": "Cliente 8",
                        "email": "cliente8@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 6,  # Cliente asignado al fotógrafo (ID 6)
                    },
                ]

                # Insertar usuarios uno por uno para mantener los IDs específicos
                for usuario in usuarios:
                    conn.execute(users.insert().values(usuario))
                print("✅ Usuarios de ejemplo creados correctamente")

                # Insertar sesiones de ejemplo
                print("📸 Insertando sesiones fotográficas de ejemplo...")
                sesiones = [
                    {
                        "id": 1,
                        "name": "Boda María y Juan",
                        "date": "2025-02-15",
                        "photographer_id": 2,
                    },
                    {
                        "id": 2,
                        "name": "Sesión Familiar López",
                        "date": "2025-02-20",
                        "photographer_id": 2,
                    },
                    {
                        "id": 3,
                        "name": "Evento Corporativo XYZ",
                        "date": "2025-03-01",
                        "photographer_id": 6,
                    },
                ]

                # Insertar sesiones
                for sesion in sesiones:
                    conn.execute(sessions.insert().values(sesion))
                print("✅ Sesiones de ejemplo creadas correctamente")

                # Insertar fotos de ejemplo
                print("📷 Insertando fotos de ejemplo...")
                fotos = [
                    {
                        "id": 1,
                        "description": "Ceremonia de boda - Primer beso de los novios",
                        "path": "/uploads/sessions/1/boda_001.jpg",
                        "session_id": 1,
                    },
                    {
                        "id": 2,
                        "description": "Ceremonia de boda - Intercambio de anillos",
                        "path": "/uploads/sessions/1/boda_002.jpg",
                        "session_id": 1,
                    },
                    {
                        "id": 3,
                        "description": "Sesión familiar - Grupo completo en el parque",
                        "path": "/uploads/sessions/2/familia_001.jpg",
                        "session_id": 2,
                    },
                    {
                        "id": 4,
                        "description": "Evento corporativo - Presentación principal",
                        "path": "/uploads/sessions/3/evento_001.jpg",
                        "session_id": 3,
                    },
                ]

                for foto in fotos:
                    conn.execute(photos.insert().values(foto))
                print("✅ Fotos de ejemplo creadas correctamente")

                # Insertar galerías de ejemplo
                print("📸 Insertando galerías de ejemplo...")
                galerias = [
                    {
                        "id": 1,
                        "name": "Boda María y Juan - Selección Final",
                        "description": "Fotos seleccionadas de la boda",
                        "photographer_id": 2,
                        "client_id": 3,
                    },
                    {
                        "id": 2,
                        "name": "Familia López - Sesión Completa",
                        "description": "Todas las fotos de la sesión familiar",
                        "photographer_id": 2,
                        "client_id": 4,
                    },
                    {
                        "id": 3,
                        "name": "Evento XYZ - Highlights",
                        "description": "Mejores momentos del evento",
                        "photographer_id": 6,
                        "client_id": 7,
                    },
                ]

                # Insertar galerías
                for galeria in galerias:
                    conn.execute(galleries.insert().values(galeria))
                print("✅ Galerías de ejemplo creadas correctamente")

                # Insertar relaciones entre galerías y fotos
                print("🔗 Insertando relaciones entre galerías y fotos...")
                galeria_fotos = [
                    {
                        "id": 1,
                        "gallery_id": 1,  # Galería "Boda María y Juan"
                        "photo_id": 1,  # Foto "boda_001.jpg"
                        "selected": True,
                        "favorite": True,
                    },
                    {
                        "id": 2,
                        "gallery_id": 1,  # Galería "Boda María y Juan"
                        "photo_id": 2,  # Foto "boda_002.jpg"
                        "selected": True,
                        "favorite": False,
                    },
                    {
                        "id": 3,
                        "gallery_id": 2,  # Galería "Sesión Familiar López"
                        "photo_id": 3,  # Foto "familia_001.jpg"
                        "selected": False,
                        "favorite": True,
                    },
                    {
                        "id": 4,
                        "gallery_id": 3,  # Galería "Evento Corporativo XYZ"
                        "photo_id": 4,  # Foto "evento_001.jpg"
                        "selected": False,
                        "favorite": False,
                    },
                ]

                # Insertar relaciones
                for galeria_foto in galeria_fotos:
                    conn.execute(gallery_photos.insert().values(galeria_foto))
                print("✅ Relaciones entre galerías y fotos creadas correctamente")

                # No necesitamos hacer commit explícito porque get_db lo maneja

            else:
                print("ℹ️ La base de datos ya contiene usuarios")

    except Exception as e:
        print(f"❌ Error durante la inicialización: {str(e)}")
        raise e


def reset_db():
    """
    Elimina todas las tablas y las vuelve a crear con datos de ejemplo
    """
    try:
        print("🗑️ Eliminando tablas existentes...")
        meta.drop_all(engine)
        print("✅ Tablas eliminadas correctamente")

        # Volver a crear las tablas
        init_db()

    except Exception as e:
        print(f"❌ Error durante el reset: {str(e)}")
        raise e


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("⚠️ Reiniciando la base de datos...")
        reset_db()
    else:
        init_db()
