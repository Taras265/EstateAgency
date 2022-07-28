from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from microservices.auth.models import *
from microservices.models import *

router = APIRouter(
    prefix="/rights",
    tags=["rights"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_rights(db: Session = Depends(get_db)):
    rights = db.query(Rights).all()
    return rights


@router.get("/{slug}")
async def right_by_slug(slug: str, db: Session = Depends(get_db)):
    right = db.query(Rights).filter(Rights.slug == slug).first()
    return right


@router.post("/")
async def create_right(right: CreateRight, db: Session = Depends(get_db)):
    right_model = Rights()

    right_model.right = right.right
    right_model.slug = right.slug

    db.add(right_model)
    db.commit()

    return "Success"


@router.put("/{right_id}")
async def update_right(right_id: int, right: CreateRight, db: Session = Depends(get_db)):
    right_model = db.query(Rights).filter(Rights.id == right_id).first()
    if not right_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    right_model.right = right.right
    right_model.slug = right.slug

    db.add(right_model)
    db.commit()

    return "Success"


@router.delete("/{right_id}")
async def delete_right(right_id: int, db: Session = Depends(get_db)):
    try:
        right_model = db.query(Rights).filter(Rights.id == right_id).first()
        if not right_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Rights).filter(Rights.id == right_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
