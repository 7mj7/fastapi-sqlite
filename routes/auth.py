# routes/auth.py

# Importaciones necesarias
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from config.security import verify_password, create_access_token, settings
from config.db import get_db
from models.user import users
from schemas.token import Token

# Crear router con tag para agrupar en la documentación
auth = APIRouter(tags=["authentication"])

# Configurar el esquema OAuth2 para la ruta de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# -------------------------------------------------------------------
# Endpoint de autenticación - Genera token JWT
# POST /token
# Body (form-data):
#   - username: email del usuario
#   - password: contraseña
# -------------------------------------------------------------------
@auth.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    with get_db() as db:
        # Buscar usuario por email (form_data.username contiene el email)
        user = db.execute(
            users.select().where(users.c.email == form_data.username)
        ).first()

        # Verificar que el usuario existe y la contraseña es correcta
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},  # Header requerido por OAuth2
            )

        # Crear token JWT con el email del usuario
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        # Retornar token en formato esperado por OAuth2
        return {
            "access_token": access_token,  # Token JWT
            "token_type": "bearer",  # Tipo de token (siempre "bearer" para JWT)
        }
