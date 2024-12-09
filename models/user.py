# models/user.py

from sqlalchemy import Table, Column
from sqlalchemy import Integer, String
from config.db import meta, engine

users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("email", String(255)),
    Column("password", String(255)),
    Column("role", String(50)),  # 'photographer' o 'client'
)
