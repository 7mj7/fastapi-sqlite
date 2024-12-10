from fastapi import FastAPI
from routes.auth import auth as authRouter
from routes.user import user as userRouter
from routes.session import session as sessionRouter

app = FastAPI()

app.include_router(authRouter)
app.include_router(userRouter)
app.include_router(sessionRouter)

