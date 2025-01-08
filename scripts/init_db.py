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
from models.user import users


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
                # Insertar usuarios de ejemplo

                 # Insertar usuarios de ejemplo con IDs específicos
                usuarios = [
                    {   
                        "id": 1,                     
                        "name": "Admin",
                        "email": "admin@example.com",
                        "password": get_password_hash("admin123"),
                        "role": "admin",
                        "photographer_id": None  # Admin no tiene fotógrafo asignado                      
                    },
                    {
                        "id": 2,
                        "name": "Fotógrafo",
                        "email": "fotografo@example.com",
                        "password": get_password_hash("foto123"),
                        "role": "photographer",
                        "photographer_id": None  # Fotógrafo no tiene fotógrafo asignado
                    },
                    {
                        "id": 3,
                        "name": "Cliente",
                        "email": "cliente@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 2  # Cliente asignado al fotógrafo (ID 2)
                    },
                    {
                        "id": 4,
                        "name": "Cliente 4",
                        "email": "cliente4@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 2  # Cliente asignado al fotógrafo (ID 2)
                    },
                    {
                        "id": 5,
                        "name": "Cliente 5",
                        "email": "cliente5@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 2  # Cliente asignado al fotógrafo (ID 2)
                    },
                    {
                        "id": 6,
                        "name": "Fotógrafo 6",
                        "email": "fotografo6@example.com",
                        "password": get_password_hash("foto123"),
                        "role": "photographer",
                        "photographer_id": None  # Fotógrafo no tiene fotógrafo asignado
                    },
                    {
                        "id": 7,
                        "name": "Cliente 7",
                        "email": "cliente7@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 6  # Cliente asignado al fotógrafo (ID 6)
                    },
                    {
                        "id": 8,
                        "name": "Cliente 8",
                        "email": "cliente8@example.com",
                        "password": get_password_hash("cliente123"),
                        "role": "client",
                        "photographer_id": 6  # Cliente asignado al fotógrafo (ID 6)
                    }
                ]
                
                # Insertar usuarios uno por uno para mantener los IDs específicos
                for usuario in usuarios:
                    conn.execute(users.insert().values(usuario))
                                    
                # No necesitamos hacer commit explícito porque get_db lo maneja
                print("✅ Usuarios de ejemplo creados correctamente")
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