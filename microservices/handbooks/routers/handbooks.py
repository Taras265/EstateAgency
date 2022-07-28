from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/handbooks",
    tags=["handbooks"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{handbook_type}")
async def all_handbooks(handbook_type: str, db: Session = Depends(get_db)):
    handbooks = db.query(Handbooks).filter(Handbooks.handbook_type == handbook_type).all()
    return handbooks


@router.get("/handbook/{handbook_id}")
async def get_handbook(handbook_id: int, db: Session = Depends(get_db)):
    handbook = db.query(Handbooks).filter(Handbooks.id == handbook_id).first()
    if not handbook:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return handbook


@router.get("/{handbook_type}/{handbook_id}")
async def get_checked_handbook(handbook_type: int, handbook_id: int, db: Session = Depends(get_db)):
    handbook = db.query(Handbooks).filter(Handbooks.handbook_type == handbook_type)\
        .filter(Handbooks.id == handbook_id).first()
    if not handbook:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return handbook


@router.get("/{handbook_type}/{start}/{limit}")
async def all_handbooks_on_page(handbook_type: str, start: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    handbooks = db.query(Handbooks).filter(Handbooks.handbook_type == handbook_type).offset(start).limit(limit).all()
    count = db.query(Handbooks).filter(Handbooks.handbook_type == handbook_type).count()
    return {"objects": handbooks, "count": count}


@router.post("/")
async def create_handbook(handbook: CreateHandbook, db: Session = Depends(get_db)):
    if handbook.handbook_type not in ["withdrawal_reason", "condition",
                                      "material", "agency", "stair", "heating",
                                      "layout", "house_type"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found Handbook Type")

    handbook_model = Handbooks()

    handbook_model.handbook = handbook.handbook
    handbook_model.handbook_type = handbook.handbook_type

    db.add(handbook_model)
    db.commit()

    return "Success"


@router.put("/{handbook_id}")
async def update_handbook(handbook_id: int, handbook: CreateHandbook, db: Session = Depends(get_db)):
    if handbook.handbook_type not in ["withdrawal_reason", "condition",
                                      "material", "agency", "stair", "heating",
                                      "layout", "house_type"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found Handbook Type")

    handbook_model = db.query(Handbooks).filter(Handbooks.id == handbook_id).first()
    if not handbook_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    handbook_model.handbook = handbook.handbook
    handbook_model.handbook_type = handbook.handbook_type

    db.add(handbook_model)
    db.commit()

    return "Success"


@router.delete("/{handbook_id}")
async def delete_handbook(handbook_id: int, db: Session = Depends(get_db)):
    try:
        handbook_model = db.query(Handbooks).filter(Handbooks.id == handbook_id).first()
        if not handbook_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Handbooks).filter(Handbooks.id == handbook_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
