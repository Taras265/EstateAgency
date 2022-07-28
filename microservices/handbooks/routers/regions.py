from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/regions",
    tags=["regions"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_regions(db: Session = Depends(get_db)):
    regions = db.query(Regions).all()
    return regions


@router.get("/{start}/{limit}")
async def all_regions_on_page(start: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    regions = db.query(Regions).offset(start).limit(limit).all()
    count = db.query(Regions).count()
    return {"objects": regions, "count": count}


@router.get("/{region_id}")
async def get_region(region_id: int, db: Session = Depends(get_db)):
    region = db.query(Regions).filter(Regions.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return region


@router.post("/")
async def create_region(region: CreateRegion, db: Session = Depends(get_db)):
    district = db.query(Districts).filter(Districts.id == region.district).first()
    if not district:
        raise HTTPException(status_code=404, detail="404 Error Not Found District")
    region_model = Regions()

    region_model.region = region.region
    region_model.district = region.district

    db.add(region_model)
    db.commit()

    return "Success"


@router.put("/{region_id}")
async def update_region(region_id: int, region: CreateRegion, db: Session = Depends(get_db)):
    region_model = db.query(Regions).filter(Regions.id == region_id).first()
    if not region_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    district = db.query(Districts).filter(Districts.id == region.district).first()
    if not district:
        raise HTTPException(status_code=404, detail="404 Error Not Found District")

    region_model.region = region.region
    region_model.district = region.district

    db.add(region_model)
    db.commit()

    return "Success"


@router.delete("/{region_id}")
async def delete_region(region_id: int, db: Session = Depends(get_db)):
    try:
        region_model = db.query(Regions).filter(Regions.id == region_id).first()
        if not region_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Regions).filter(Regions.id == region_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
