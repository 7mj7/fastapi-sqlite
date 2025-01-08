# routes/gallery.py

from fastapi import APIRouter, HTTPException, status, Depends
from config.db import get_db
from sqlalchemy.exc import SQLAlchemyError
from middleware.auth import get_current_user

from models.user import UserRole  # Importar el enum de roles
from models.gallery import galleries
from models.gallery_photos import gallery_photos
from models.photo import photos

from schemas.gallery import Gallery, GalleryCreate, GalleryWithPhotos

from sqlalchemy import select, join

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
    description="Retorna las galerías según el rol del usuario.",
    responses={
        403: {"description": "Acceso denegado"},
        500: {"description": "Error interno del servidor"},
    },
)
async def get_my_galleries(current_user=Depends(get_current_user)):
    try:
        with get_db() as db:
            # Si es admin, mostrar todas las galerías
            if current_user["role"] == UserRole.admin:
                print(f"👑 Admin consultando todas las galerías")
                galleries_list = db.execute(galleries.select()).fetchall()
                return galleries_list

            # Si es fotógrafo, mostrar solo sus galerías
            elif current_user["role"] == UserRole.photographer:
                print(f"📸 Fotógrafo {current_user['id']} consultando sus galerías")
                galleries_list = db.execute(
                    galleries.select().where(
                        galleries.c.photographer_id == current_user["id"]
                    )
                ).fetchall()
                return galleries_list

            # Si es cliente, mostrar solo las galerías donde es el cliente
            elif current_user["role"] == UserRole.client:
                print(f"👤 Cliente {current_user['id']} consultando sus galerías")
                galleries_list = db.execute(
                    galleries.select().where(
                        galleries.c.client_id == current_user["id"]
                    )
                ).fetchall()
                return galleries_list

            """galleries_list = db.execute(
                galleries.select().where(
                    (galleries.c.photographer_id == current_user["id"])
                    | (galleries.c.client_id == current_user["id"])
                )
            ).fetchall()
            return galleries_list"""

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
    # response_model=Gallery,
    response_model=GalleryWithPhotos,  # Actualizar el modelo de respuesta
    responses={
        403: {"description": "Acceso denegado"},
        404: {"description": "Galería no encontrada"},
        500: {"description": "Error interno del servidor"},
    },
    summary="Obtener galería por ID con sus fotos",
    description="Obtiene una galería específica con sus fotos asociadas. El usuario debe ser el fotógrafo o cliente.",
)
async def get_gallery(id: int, current_user=Depends(get_current_user)):
    try:
        with get_db() as db:
            # Consulta para obtener la galería
            gallery = db.execute(galleries.select().where(galleries.c.id == id)).first()

            if not gallery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Galería con id {id} no encontrada",
                )

            # Control de acceso basado en roles
            if current_user["role"] == UserRole.admin:
                print(f"👑 Admin consultando galería {id}")

            elif current_user["role"] == UserRole.photographer:
                # Verificar que el fotógrafo tenga acceso a la galería
                if gallery.photographer_id != current_user["id"]:
                    print(
                        f"❌ Fotógrafo {current_user['id']} intentó acceder a galería {id} que no le pertenece"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permiso para ver esta galería",
                    )
                print(f"📸 Fotógrafo {current_user['id']} consultando su galería {id}")

            elif current_user["role"] == UserRole.client:
                # Verificar que el cliente tenga acceso a la galería
                if gallery.client_id != current_user["id"]:
                    print(
                        f"❌ Cliente {current_user['id']} intentó acceder a galería {id} no asignada"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permiso para ver esta galería",
                    )
                print(f"👤 Cliente {current_user['id']} consultando su galería {id}")

            # Consulta SQLAlchemy para obtener las fotos de la galería
            query = (
                select(
                    gallery_photos.c.id,  # ID de la relación gallery_photos
                    gallery_photos.c.gallery_id,  # ID de la galería
                    gallery_photos.c.photo_id,  # ID de la foto
                    photos.c.description,  # Descripción de la foto
                    photos.c.path,  # Ruta de la foto
                    gallery_photos.c.selected,  # Estado de selección
                    gallery_photos.c.favorite,  # Estado de favorito
                )
                .select_from(
                    join(
                        photos, gallery_photos, photos.c.id == gallery_photos.c.photo_id
                    )
                )
                .where(gallery_photos.c.gallery_id == id)
            )

            '''print("\n=== SQL Query ===")
            print(str(query))'''

            gallery_photos_result = db.execute(query).fetchall()

            """print("\n=== Resultados de la consulta ===")
            for row in gallery_photos_result:
                print(row)"""

            # Crear el diccionario de respuesta
            response = {
                "id": gallery.id,
                "name": gallery.name,
                "description": gallery.description,
                "photographer_id": gallery.photographer_id,
                "client_id": gallery.client_id,
                "photos": [
                    {
                        "gallery_photo_id": photo.id,
                        "photo_id": photo.photo_id,
                        "description": photo.description,
                        "path": photo.path,
                        "selected": photo.selected,
                        "favorite": photo.favorite
                    }
                    for photo in gallery_photos_result
                ]
            }

            return response

            """
            EQUIVALENTE EN SQL : 
            SELECT 
                gallery_photos.id,         -- ID de la relación gallery_photos
                photos.id as photo_id,     -- ID de la foto
                photos.description,        -- Descripción de la foto
                photos.path,              -- Ruta de la foto
                photos.session_id,        -- ID de la sesión
                gallery_photos.selected,   -- Estado de selección
                gallery_photos.favorite    -- Estado de favorito
            FROM 
                photos
            INNER JOIN 
                gallery_photos
            ON 
                photos.id = gallery_photos.photo_id
            WHERE 
                gallery_photos.gallery_id = [id];
            """

            """gallery = db.execute(galleries.select().where(galleries.c.id == id)).first()

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

            return gallery"""

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
