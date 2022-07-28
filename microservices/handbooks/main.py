from fastapi import FastAPI, Depends, HTTPException

from .models import GetAddress
from .. import models
from microservices.database import get_db
from microservices.database import engine
from ..models import *
from .routers import districts, regions, cities, city_regions, streets, handbooks, clients, new_building
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(districts.router)
app.include_router(regions.router)
app.include_router(cities.router)
app.include_router(city_regions.router)
app.include_router(streets.router)
app.include_router(handbooks.router)
app.include_router(new_building.router)
app.include_router(clients.router)


@app.post("/address/")
async def get_address(address_form: GetAddress, db: Session = Depends(get_db)):
    district = db.query(Districts).filter(Districts.id == address_form.district).first()
    region = db.query(Regions).filter(Regions.id == address_form.region).first()
    city = db.query(Cities).filter(Cities.id == address_form.city).first()
    city_region = db.query(CityRegions).filter(CityRegions.id == address_form.city_region).first()
    street = db.query(Streets).filter(Streets.id == address_form.street).first()
    if district and region and city and city_region and street:
        if region.district == district.id and city.region == region.id and city_region.city == city.id\
                and street.city_region == city_region.id:
            data = f"{district.district}, {region.region}, {city.city}, {city_region.city_region}, {street.street}"
            if address_form.house:
                data += f", дом {address_form.house}"
            if address_form.apartment:
                data += f", кв. {address_form.apartment}"
            return data
        raise HTTPException(status_code=400, detail="Bad request! Incorrect location!")
    raise HTTPException(status_code=404, detail="Location not found!")
