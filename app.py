from fastapi import FastAPI
from routes.auth import auth
from routes.user import user

app = FastAPI()

app.include_router(auth)
app.include_router(user)

