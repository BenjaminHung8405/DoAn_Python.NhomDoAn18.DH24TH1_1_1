from fastapi import FastAPI
from .routers import categories, expenses, auth, users
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(users.router, prefix="", tags=["users"])