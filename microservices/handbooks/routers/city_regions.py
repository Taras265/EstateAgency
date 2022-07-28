from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/city_regions",
    tags=["city_regions"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_city_regions(db: Session = Depends(get_db)):
    city_regions = db.query(CityRegions).all()
    return city_regions


@router.get("/{start}/{limit}")
async def all_city_regions_on_page(start: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    city_regions = db.query(CityRegions).offset(start).limit(limit).all()
    count = db.query(CityRegions).count()
    return {"objects": city_regions, "count": count}


@router.get("/{city_region_id}")
async def get_city_region(city_region_id: int, db: Session = Depends(get_db)):
    city_region = db.query(CityRegions).filter(CityRegions.id == city_region_id).first()

    if not city_region:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return city_region


@router.post("/")
async def create_city_region(city_region: CreateCityRegion, db: Session = Depends(get_db)):
    city_region_model = CityRegions()
    city = db.query(Cities).filter(Cities.id == city_region.city).first()
    if not city:
        raise HTTPException(status_code=404, detail="404 Error Not Found City")
    region = db.query(CityRegions).filter(CityRegions.id == city_region.region).first()
    if not region and city_region.region is not None:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Region")
    if len(str(city_region.hot_deals_limit)) - 1 > 10:
        raise HTTPException(status_code=400, detail="Hot Deals Limit Is To Big")
    if len(city_region.prefix_to_site) > 2:
        raise HTTPException(status_code=400, detail="Prefix Is To Big")
    if city_region.new_building_region not in ["Приморский+Центр",
                                               "Киевский+Малиновский",
                                               "Суворовский"] and city_region.new_building_region != "None":
        raise HTTPException(status_code=404, detail="404 Error Not Found New Building Region")

    city_region_model.city_region = city_region.city_region
    city_region_model.city = city_region.city
    city_region_model.description = city_region.description
    city_region_model.group_on_site = city_region.group_on_site
    city_region_model.region = city_region.region
    city_region_model.hot_deals_limit = city_region.hot_deals_limit
    city_region_model.prefix_to_site = city_region.prefix_to_site
    city_region_model.is_subdistrict = city_region.is_subdistrict
    if city_region.new_building_region != 'None':
        city_region_model.new_building_region = city_region.new_building_region
    else:
        city_region_model.new_building_region = None

    db.add(city_region_model)
    db.commit()

    return "Success"


@router.put("/{city_region_id}")
async def update_city_region(city_region_id: int, city_region: CreateCityRegion, db: Session = Depends(get_db)):
    city_region_model = db.query(CityRegions).filter(CityRegions.id == city_region_id).first()
    city = db.query(Cities).filter(Cities.id == city_region.city).first()
    region = db.query(CityRegions).filter(CityRegions.id == city_region.region).first()
    if not city_region_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    if not city:
        raise HTTPException(status_code=404, detail="404 Error Not Found City")
    if not region and city_region.region is not None:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Region")
    if len(str(city_region.hot_deals_limit)) - 1 > 10:
        raise HTTPException(status_code=400, detail="Hot Deals Limit Is To Big")
    if len(city_region.prefix_to_site) > 2:
        raise HTTPException(status_code=400, detail="Prefix Is To Big")
    if city_region.new_building_region not in ["Приморский+Центр",
                                               "Киевский+Малиновский",
                                               "Суворовский"] and city_region.new_building_region != "None":
        raise HTTPException(status_code=404, detail="404 Error Not Found New Building Region")

    city_region_model.city_region = city_region.city_region
    city_region_model.city = city_region.city
    city_region_model.description = city_region.description
    city_region_model.group_on_site = city_region.group_on_site
    city_region_model.region = city_region.region
    city_region_model.hot_deals_limit = city_region.hot_deals_limit
    city_region_model.prefix_to_site = city_region.prefix_to_site
    city_region_model.is_subdistrict = city_region.is_subdistrict
    if city_region.new_building_region != 'None':
        city_region_model.new_building_region = city_region.new_building_region
    else:
        city_region_model.new_building_region = None

    db.add(city_region_model)
    db.commit()

    return "Success"


@router.delete("/{city_region_id}")
async def delete_city_region(city_region_id: int, db: Session = Depends(get_db)):
    try:
        city_region_model = db.query(CityRegions).filter(CityRegions.id == city_region_id).first()
        if not city_region_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(CityRegions).filter(CityRegions.id == city_region_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
