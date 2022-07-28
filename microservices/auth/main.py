from fastapi import FastAPI
from .. import models
from microservices.database import engine
from .routers import auth, groups, user_groups, rights, group_rights, separations

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(groups.router)
app.include_router(rights.router)
app.include_router(user_groups.router)
app.include_router(group_rights.router)
app.include_router(separations.router)
