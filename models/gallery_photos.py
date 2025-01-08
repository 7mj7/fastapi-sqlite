# models/gallery_photos.py

from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from config.db import meta

# Tabla de asociación entre galerías y fotografías con atributos adicionales
gallery_photos = Table(
    "gallery_photos",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("gallery_id", Integer, ForeignKey("galleries.id"), nullable=False),
    Column("photo_id", Integer, ForeignKey("photos.id"), nullable=False),
    Column("selected", Boolean, default=False, nullable=False),
    Column("favorite", Boolean, default=False, nullable=False),
    #Column("added_at", DateTime(timezone=True), server_default=func.now()),
    
    # Añadir restricción única para gallery_id + photo_id
    UniqueConstraint('gallery_id', 'photo_id', name='uix_gallery_photo')
)