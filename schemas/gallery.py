# schemas/gallery.py

from pydantic import BaseModel
from typing import Optional

# Modelo base para galerías que define los campos comunes
class GalleryBase(BaseModel):
    name: str                                   # Nombre de la galería (requerido)
    description: Optional[str] = None           # Descripción opcional de la galería
    client_id: int                              # ID del cliente al que pertenece la galería (requerido)

# Modelo para crear nuevas galerías
# Hereda todos los campos de GalleryBase sin modificaciones
class GalleryCreate(GalleryBase):
    pass

# Modelo para respuestas de galería que incluye el ID
class Gallery(GalleryBase):
    id: int                                     # ID único de la galería en la base de datos
    photographer_id: int                        # ID del fotógrafo (se asigna automáticamente)

    class Config:
        # Permite que Pydantic convierta automáticamente 
        # los modelos SQLAlchemy a modelos Pydantic
        from_attributes = True