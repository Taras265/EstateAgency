from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/districts",
    tags=["districts"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_districts(db: Session = Depends(get_db)):
    districts = db.query(Districts).all()
    return districts


@router.get("/{district_id}")
async def get_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(Districts).filter(Districts.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return district


@router.post("/")
async def create_district(district: CreateDistrict, db: Session = Depends(get_db)):
    district_model = Districts()

    district_model.district = district.district

    db.add(district_model)
    db.commit()

    return "Success"


@router.put("/{district_id}")
async def update_district(district_id: int, district: CreateDistrict, db: Session = Depends(get_db)):
    district_model = db.query(Districts).filter(Districts.id == district_id).first()
    if not district_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    district_model.district = district.district

    db.add(district_model)
    db.commit()

    return "Success"


@router.delete("/{district_id}")
async def delete_district(district_id: int, db: Session = Depends(get_db)):
    try:
        district_model = db.query(Districts).filter(Districts.id == district_id).first()
        if not district_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Districts).filter(Districts.id == district_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
