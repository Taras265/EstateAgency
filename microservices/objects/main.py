from fastapi import FastAPI
from .. import models
from microservices.database import engine
from .routers import types, objects, apartments

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(types.router)
app.include_router(objects.router)
app.include_router(apartments.router)
