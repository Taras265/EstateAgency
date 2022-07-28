from fastapi import FastAPI
from .. import models
from microservices.database import engine
from .routers import obj_images

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(obj_images.router)
