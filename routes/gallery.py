# routes/gallery.py

from fastapi import APIRouter, HTTPException, status, Depends
from config.db import get_db
from models.gallery import galleries
from models.user import UserRole  # Importar el enum de roles
from schemas.gallery import Gallery, GalleryCreate
from sqlalchemy.exc import SQLAlchemyError
from middleware.auth import get_current_user

# Crear router con tag para la documentación
gallery = APIRouter(tags=["galleries"])


# -------------------------------------------------------------------
# Endpoint para crear una nueva galería
# POST /galleries/
# El usuario autenticado será automáticamente asignado como fotógrafo
#
# Ruta protegida por las siguientes razones:
# 1. Solo usuarios autenticados pueden crear galerías (usa get_current_user)
# 2. Solo fotógrafos pueden crear galerías (verifica rol)
# 3. Asigna automáticamente el fotógrafo actual como propietario
# -------------------------------------------------------------------
@gallery.post(
    "/galleries/",
    response_model=Gallery,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva galería",
    # description="Crea una nueva galería asignando al usuario actual como fotógrafo."
    description="Crea una nueva galería. Solo disponible para fotógrafos.",
)
async def create_gallery(
    gallery: GalleryCreate, current_user=Depends(get_current_user)
):
    try:
        # Imprimir información del usuario actual para debugging
        print(f"Usuario actual: {current_user['email']}")
        print(f"Rol del usuario: {current_user['role']}")

        # Verificar que el usuario tiene rol de fotógrafo
        if current_user["role"] != UserRole.photographer:
            print(f"Acceso denegado - Rol del usuario: {current_user['role']}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los fotógrafos pueden crear galerías",
            )

        # Asignar automáticamente el usuario actual como fotógrafo
        new_gallery = gallery.model_dump()
        new_gallery["photographer_id"] = current_user["id"]

        with get_db() as db:
            result = db.execute(galleries.insert().values(new_gallery))

            created_gallery = db.execute(
                galleries.select().where(galleries.c.id == result.lastrowid)
            ).first()

            return created_gallery

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la galería: {str(e)}",
        )


# -------------------------------------------------------------------
# Endpoint para obtener las galerías del usuario actual
# GET /galleries/me/
# Retorna galerías donde el usuario es fotógrafo o cliente
# -------------------------------------------------------------------
@gallery.get(
    "/galleries/me/",
    response_model=list[Gallery],
    summary="Obtener mis galerías",
    description="Retorna las galerías donde el usuario es fotógrafo o cliente.",
)
async def get_my_galleries(current_user=Depends(get_current_user)):
    try:
        with get_db() as db:
            galleries_list = db.execute(
                galleries.select().where(
                    (galleries.c.photographer_id == current_user["id"])
                    | (galleries.c.client_id == current_user["id"])
                )
            ).fetchall()
            return galleries_list

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las galerías: {str(e)}",
        )


# -------------------------------------------------------------------
# Endpoint para obtener una galería específica por ID
# GET /galleries/{id}
# Verifica que el usuario tenga acceso a la galería
# -------------------------------------------------------------------
@gallery.get(
    "/galleries/{id}",
    response_model=Gallery,
    responses={404: {"description": "Galería no encontrada"}},
    summary="Obtener galería por ID",
    description="Obtiene una galería específica. El usuario debe ser el fotógrafo o cliente.",
)
async def get_gallery(id: int, current_user=Depends(get_current_user)):
    try:
        with get_db() as db:
            gallery = db.execute(galleries.select().where(galleries.c.id == id)).first()

            if not gallery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Galería con id {id} no encontrada",
                )

            # Verificar que el usuario tiene acceso a la galería
            if (
                gallery.client_id != current_user["id"]
                and gallery.photographer_id != current_user["id"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permiso para ver esta galería",
                )

            return gallery

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la galería: {str(e)}",
        )


# -------------------------------------------------------------------
# Endpoint para eliminar una galería
# DELETE /galleries/{id}
# Solo el fotógrafo puede eliminar sus galerías
# -------------------------------------------------------------------
@gallery.delete(
    "/galleries/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Galería no encontrada"}},
    summary="Eliminar galería",
    description="Elimina una galería. Solo el fotógrafo puede eliminar sus galerías.",
)
async def delete_gallery(id: int, current_user=Depends(get_current_user)):
    try:
        with get_db() as db:
            gallery = db.execute(galleries.select().where(galleries.c.id == id)).first()

            if not gallery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Galería con id {id} no encontrada",
                )

            # Verificar que el usuario es el fotógrafo de la galería
            if gallery.photographer_id != current_user["id"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo el fotógrafo puede eliminar la galería",
                )

            db.execute(galleries.delete().where(galleries.c.id == id))
            return None

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la galería: {str(e)}",
        )
