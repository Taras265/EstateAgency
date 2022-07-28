from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/streets",
    tags=["streets"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_streets(db: Session = Depends(get_db)):
    streets = db.query(Streets).all()
    return streets


@router.get("/{start}/{limit}")
async def all_streets_on_page(start: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    streets = db.query(Streets).offset(start).limit(limit).all()
    count = db.query(Streets).count()
    return {"objects": streets, "count": count}


@router.get("/{street_id}")
async def get_street(street_id: int, db: Session = Depends(get_db)):
    street_model = db.query(Streets).filter(Streets.id == street_id).first()
    if not street_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return street_model


@router.post("/")
async def create_street(street: CreateStreet, db: Session = Depends(get_db)):
    street_model = Streets()

    city_region = db.query(CityRegions).filter(CityRegions.id == street.city_region).first()
    if not city_region:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Region")
    city = db.query(Cities).filter(Cities.id == street.city).first()
    if not city:
        raise HTTPException(status_code=404, detail="404 Error Not Found City")

    street_model.street = street.street
    street_model.city = street.city
    street_model.city_region = street.city_region

    db.add(street_model)
    db.commit()

    return "Success"


@router.put("/{street_id}")
async def update_street(street_id: int, street: CreateStreet, db: Session = Depends(get_db)):
    street_model = db.query(Streets).filter(Streets.id == street_id).first()
    if not street_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    city_region = db.query(CityRegions).filter(CityRegions.id == street.city_region).first()
    if not city_region:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Region")
    city = db.query(Cities).filter(Cities.id == street.city).first()
    if not city:
        raise HTTPException(status_code=404, detail="404 Error Not Found City")

    street_model.street = street.street
    street_model.city = street.city
    street_model.city_region = street.city_region

    db.add(street_model)
    db.commit()

    return "Success"


@router.delete("/{street_id}")
async def delete_street(street_id: int, db: Session = Depends(get_db)):
    try:
        street_model = db.query(Streets).filter(Streets.id == street_id).first()
        if not street_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Streets).filter(Streets.id == street_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
