# models/gallery.py

from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from config.db import meta

galleries = Table(
    "galleries",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("description", Text),    
    Column("client_id", Integer, ForeignKey("users.id"))
)

