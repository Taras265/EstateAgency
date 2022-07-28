from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_cities(db: Session = Depends(get_db)):
    cities = db.query(Cities).all()
    return cities


@router.get("/{start}/{limit}")
async def all_cities_on_page(start: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    cities = db.query(Cities).offset(start).limit(limit).all()
    count = db.query(Cities).count()
    return {"objects": cities, "count": count}


@router.get("/{city_id}")
async def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(Cities).filter(Cities.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return city


@router.post("/")
async def create_city(city: CreateCity, db: Session = Depends(get_db)):
    region = db.query(Regions).filter(Regions.id == city.region).first()
    if not region:
        raise HTTPException(status_code=404, detail="404 Error Not Found Region")
    if city.city_type not in ["село", "смт", "місто"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Type")
    if city.center_type not in ["районний", "обласний"] and not city.center_type:
        raise HTTPException(status_code=404, detail="404 Error Not Found Center Type")
    city_model = Cities()

    city_model.city = city.city
    city_model.region = city.region
    city_model.city_type = city.city_type
    if city_model != 'None':
        city_model.city_type = city.city_type
    else:
        city_model.center_type = None

    db.add(city_model)
    db.commit()

    return "Success"


@router.put("/{city_id}")
async def update_city(city_id: int, city: CreateCity, db: Session = Depends(get_db)):
    city_model = db.query(Cities).filter(Cities.id == city_id).first()
    region = db.query(Regions).filter(Regions.id == city.region).first()
    if not city_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    if not region:
        raise HTTPException(status_code=404, detail="404 Error Not Found Region")
    if city.city_type not in ["село", "смт", "місто"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Type")
    if city.center_type not in ["районний", "обласний"] and city.center_type != "None":
        raise HTTPException(status_code=404, detail="404 Error Not Found Center Type")

    city_model.city = city.city
    city_model.region = city.region
    if city_model != 'None':
        city_model.city_type = city.city_type
    else:
        city_model.center_type = None

    db.add(city_model)
    db.commit()

    return "Success"


@router.delete("/{city_id}")
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    try:
        city_model = db.query(Cities).filter(Cities.id == city_id).first()
        if not city_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Cities).filter(Cities.id == city_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
