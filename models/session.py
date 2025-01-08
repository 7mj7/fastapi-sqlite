# models/session.py

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.db import meta

sessions = Table(
    "sessions",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("date", String(255)),
    Column("photographer_id", Integer, ForeignKey("users.id")),
)
