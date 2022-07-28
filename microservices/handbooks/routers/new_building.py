from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/new_buildings",
    tags=["new_buildings"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_new_buildings(db: Session = Depends(get_db)):
    new_buildings = db.query(NewBuildings).all()
    return new_buildings


@router.get("/{new_building_id}")
async def get_new_building(new_building_id: int, db: Session = Depends(get_db)):
    new_building = db.query(NewBuildings).filter(NewBuildings.id == new_building_id).first()
    if not new_building:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return new_building


@router.get("/{start}/{limit}")
async def all_new_buildings_on_page(start: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    new_buildings = db.query(NewBuildings).offset(start).limit(limit).all()
    count = db.query(NewBuildings).count()
    return {"objects": new_buildings, "count": count}


@router.post("/")
async def create_new_building(new_building: CreateNewBuilding, db: Session = Depends(get_db)):
    street = db.query(Streets).filter(Streets.id == new_building.street).first()
    if not street:
        raise HTTPException(status_code=404, detail="404 Error Not Found Street")
    region = db.query(CityRegions).filter(CityRegions.id == new_building.region).first()
    if not region:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Region")
    new_building_model = NewBuildings()

    new_building_model.new_building = new_building.new_building
    new_building_model.building = new_building.building
    new_building_model.street = new_building.street
    new_building_model.house = new_building.house
    new_building_model.region = new_building.region

    db.add(new_building_model)
    db.commit()

    return "Success"


@router.put("/{new_building_id}")
async def update_new_building(new_building_id: int, new_building: CreateNewBuilding, db: Session = Depends(get_db)):
    street = db.query(Streets).filter(Streets.id == new_building.street).first()
    if not street:
        raise HTTPException(status_code=404, detail="404 Error Not Found Street")
    region = db.query(CityRegions).filter(CityRegions.id == new_building.region).first()
    if not region:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Region")
    new_building_model = db.query(NewBuildings).filter(NewBuildings.id == new_building_id).first()
    if not new_building_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    new_building_model.new_building = new_building.new_building
    new_building_model.building = new_building.building
    new_building_model.street = new_building.street
    new_building_model.house = new_building.house
    new_building_model.region = new_building.region

    db.add(new_building_model)
    db.commit()

    return "Success"


@router.delete("/{new_building_id}")
async def delete_new_building(new_building_id: int, db: Session = Depends(get_db)):
    try:
        new_building_model = db.query(NewBuildings).filter(NewBuildings.id == new_building_id).first()
        if not new_building_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(NewBuildings).filter(NewBuildings.id == new_building_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
