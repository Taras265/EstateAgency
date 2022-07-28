from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/object_types",
    tags=["object_types"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_object_types(db: Session = Depends(get_db)):
    object_types = db.query(ObjectTypes).all()
    return object_types


@router.get("/{object_type_id}")
async def obj_type(object_type_id: int, db: Session = Depends(get_db)):
    object_type = db.query(ObjectTypes).filter(ObjectTypes.id == object_type_id).first()
    if not object_type:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return object_type


@router.post("/")
async def create_object_type(object_type: CreateObjType, db: Session = Depends(get_db)):
    object_type_model = ObjectTypes()

    object_type_model.type = object_type.type
    object_type_model.slug = object_type.slug

    db.add(object_type_model)
    db.commit()

    return "Success"


@router.put("/{object_type_id}")
async def update_object_type(object_type_id: int, object_type: CreateObjType, db: Session = Depends(get_db)):
    object_type_model = db.query(ObjectTypes).filter(ObjectTypes.id == object_type_id).first()
    if not object_type_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    object_type_model.type = object_type.type
    object_type_model.slug = object_type.slug

    db.add(object_type_model)
    db.commit()

    return "Success"


@router.delete("/{object_type_id}")
async def delete_object_type(object_type_id: int, db: Session = Depends(get_db)):
    try:
        object_type_model = db.query(ObjectTypes).filter(ObjectTypes.id == object_type_id).first()
        if not object_type_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(ObjectTypes).filter(ObjectTypes.id == object_type_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
