from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_clients(db: Session = Depends(get_db)):
    clients = db.query(Clients).all()
    return clients


@router.get("/{client_id}")
async def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return client


@router.get("/{start}/{limit}")
async def all_clients_on_page(start: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    clients = db.query(Clients).offset(start).limit(limit).all()
    count = db.query(Clients).count()
    return {"objects": clients, "count": count}


@router.post("/")
async def create_client(client: CreateClient, db: Session = Depends(get_db)):
    client_model = Clients()

    client_model.email = client.email
    client_model.first_name = client.first_name
    client_model.last_name = client.last_name
    client_model.phone = client.phone

    db.add(client_model)
    db.commit()

    return "Success"


@router.put("/{client_id}")
async def update_client(client_id: int, client: CreateClient, db: Session = Depends(get_db)):
    client_model = db.query(Clients).filter(Clients.id == client_id).first()
    if not client_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    client_model.email = client.email
    client_model.first_name = client.first_name
    client_model.last_name = client.last_name
    client_model.phone = client.phone

    db.add(client_model)
    db.commit()

    return "Success"


@router.delete("/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    try:
        client_model = db.query(Clients).filter(Clients.id == client_id).first()
        if not client_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Clients).filter(Clients.id == client_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
