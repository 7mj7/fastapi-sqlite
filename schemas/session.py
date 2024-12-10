# schemas/session.py

#from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    id: int
    name: str
    date: datetime  # Es mejor usar tipos de fecha adecuados
    photographer_id: int
