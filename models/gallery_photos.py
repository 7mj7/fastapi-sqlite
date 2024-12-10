# models/gallery_photos.py

from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from config.db import meta  # Asegúrate de importar correctamente tu metadata o Base

# Tabla de asociación entre galerías y fotografías con atributos adicionales
gallery_photos = Table(
    "gallery_photos",
    meta,
    Column("gallery_id", Integer, ForeignKey("galleries.id"), primary_key=True),
    Column("photo_id", Integer, ForeignKey("photos.id"), primary_key=True),
    Column("selected", Boolean, default=False, nullable=False),
    Column("favorite", Boolean, default=False, nullable=False),
    #Column("added_at", DateTime(timezone=True), server_default=func.now()),
)