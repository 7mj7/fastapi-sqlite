# models/photo.py

from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from config.db import meta

photos = Table(
    "photos",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String(255)), 
    Column("path", String(255)),
    Column("session_id", Integer, ForeignKey("sessions.id")),  
)
