# schemas/gallery.py

from pydantic import BaseModel
from typing import Optional, List


# Modelo base para galerías que define los campos comunes
class GalleryBase(BaseModel):
    name: str  # Nombre de la galería (requerido)
    description: Optional[str] = None  # Descripción opcional de la galería
    client_id: int  # ID del cliente al que pertenece la galería (requerido)


# Modelo para crear nuevas galerías
# Hereda todos los campos de GalleryBase sin modificaciones
class GalleryCreate(GalleryBase):
    pass


# Modelo para respuestas de galería que incluye el ID
class Gallery(GalleryBase):
    id: int  # ID único de la galería en la base de datos
    photographer_id: int  # ID del fotógrafo (se asigna automáticamente)

    class Config:
        # Permite que Pydantic convierta automáticamente
        # los modelos SQLAlchemy a modelos Pydantic
        from_attributes = True


# Modelo para representar una foto dentro de una galería
class PhotoInGallery(BaseModel):
    gallery_photo_id: int  # ID de la relación gallery_photos
    photo_id: int  # ID de la foto
    description: str  # Descripción de la foto
    path: str  # Ruta de la foto
    selected: bool = False  # Estado de selección
    favorite: bool = False  # Estado de favorito

    class Config:
        from_attributes = True


# Modelo para respuestas de galería que incluye el ID y las fotos
class GalleryWithPhotos(GalleryBase):
    id: int  ## ID único de la galería
    photographer_id: int  # ID del fotógrafo
    photos: List[PhotoInGallery] = []  # Lista de fotos en la galería

    class Config:
        from_attributes = True
