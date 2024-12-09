# config/security.py

# Importaciones necesarias
import os
from datetime import datetime, timedelta,timezone
from typing import Optional
from jose import JWTError, jwt # Para manejo de tokens JWT
from passlib.context import CryptContext # Para hash de contraseñas
from dotenv import load_dotenv # Para variables de entorno

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Clase para manejar la configuración de seguridad.
# Carga valores desde variables de entorno o usa valores por defecto.
class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "my-super-secret-key")  # Lee SECRET_KEY o usa el valor por defecto
    ALGORITHM = os.getenv("ALGORITHM", "HS256")                  # Lee ALGORITHM o usa el valor por defecto
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Convierte a entero

# Instancia de configuración
settings = Settings()


# Configurar contexto de encriptación para contraseñas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verifica si una contraseña coincide con su hash
def verify_password(plain_password: str, hashed_password: str) -> bool:  
    return pwd_context.verify(plain_password, hashed_password)

# Genera un hash de la contraseña
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Crea un token JWT con los datos proporcionados y tiempo de expiración.
# Args:
#   data (dict): Datos a incluir en el token
#     expires_delta (Optional[timedelta]): Tiempo de expiración personalizado
# Returns:
#   str: Token JWT generado
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:        
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# Verifica y decodifica un token JWT.
# Args:
#     token (str): Token JWT a verificar
# Returns:
#     Optional[dict]: Payload del token si es válido, None si no lo es
def verify_token(token: str) -> Optional[dict]:
    """Verifica y decodifica un token JWT."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None