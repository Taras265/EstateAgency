from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/apartments",
    tags=["apartments"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_apartments(db: Session = Depends(get_db)):
    apartments = db.query(Apartments).all()
    return apartments


@router.get("/{apartment_id}")
async def get_apartment(apartment_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartments).filter(Apartments.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return apartment


@router.get("/objects/{object_id}")
async def get_by_object_apartment(object_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartments).filter(Apartments.object == object_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return apartment


@router.post("/")
async def create_apartment(apartment: CreateApartment, db: Session = Depends(get_db)):
    apartment_model = Apartments()

    if apartment.room_types not in ["Смежные", "Раздельные", "Кухня-студия", "Комната"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found Room Type")
    stair = db.query(Handbooks).filter(
        Handbooks.id == apartment.stair).filter(Handbooks.handbook_type == "stair").first()
    if not stair:
        raise HTTPException(status_code=404, detail="404 Error Not Found Stair")
    heating = db.query(Handbooks).filter(
        Handbooks.id == apartment.heating).filter(Handbooks.handbook_type == "heating").first()
    if not heating:
        raise HTTPException(status_code=404, detail="404 Error Not Found Heating")
    layout = db.query(Handbooks).filter(
        Handbooks.id == apartment.layout).filter(Handbooks.handbook_type == "layout").first()
    if not layout:
        raise HTTPException(status_code=404, detail="404 Error Not Found Layout")
    house_type = db.query(Handbooks).filter(
        Handbooks.id == apartment.house_type).filter(Handbooks.handbook_type == "house_type").first()
    if not house_type:
        raise HTTPException(status_code=404, detail="404 Error Not Found House Type")
    obj = db.query(Objects).filter(Objects.id == apartment.object).first()
    if not obj:
        raise HTTPException(status_code=404, detail="404 Error Not Found Object")

    apartment_model.rooms_number = apartment.rooms_number
    apartment_model.room_types = apartment.room_types
    apartment_model.height = apartment.height
    apartment_model.kitchen_square = apartment.kitchen_square
    apartment_model.living_square = apartment.living_square
    apartment_model.gas = apartment.gas
    apartment_model.courtyard = apartment.courtyard
    apartment_model.balcony_number = apartment.balcony_number
    apartment_model.registered_number = apartment.registered_number
    apartment_model.child_registered_number = apartment.child_registered_number
    apartment_model.loggias_number = apartment.loggias_number
    apartment_model.bay_windows_number = apartment.bay_windows_number
    apartment_model.commune = apartment.commune
    apartment_model.frame = apartment.frame
    apartment_model.stair = apartment.stair
    apartment_model.balcony = apartment.balcony
    apartment_model.heating = apartment.heating
    apartment_model.office = apartment.office
    apartment_model.penthouse = apartment.penthouse
    apartment_model.redevelopment = apartment.redevelopment
    apartment_model.layout = apartment.layout
    apartment_model.construction_number = apartment.construction_number
    apartment_model.house_type = apartment.house_type
    apartment_model.two_level_apartment = apartment.two_level_apartment
    apartment_model.loggia = apartment.loggia
    apartment_model.attic = apartment.attic
    apartment_model.electric_stove = apartment.electric_stove
    apartment_model.floor = apartment.floor
    apartment_model.storeys_number = apartment.storeys_number
    apartment_model.object = apartment.object

    db.add(apartment_model)
    db.commit()

    return "Success"


@router.put("/{apartment_id}")
async def update_apartment(apartment_id: int, apartment: CreateApartment, db: Session = Depends(get_db)):
    apartment_model = db.query(Apartments).filter(Apartments.id == apartment_id).first()
    if not apartment_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    if apartment.room_types not in ["Смежные", "Раздельные", "Кухня-студия", "Комната"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found Room Type")
    stair = db.query(Handbooks).filter(
        Handbooks.id == apartment.stair).filter(Handbooks.handbook_type == "stair").first()
    if not stair:
        raise HTTPException(status_code=404, detail="404 Error Not Found Stair")
    heating = db.query(Handbooks).filter(
        Handbooks.id == apartment.heating).filter(Handbooks.handbook_type == "heating").first()
    if not heating:
        raise HTTPException(status_code=404, detail="404 Error Not Found Heating")
    layout = db.query(Handbooks).filter(
        Handbooks.id == apartment.layout).filter(Handbooks.handbook_type == "layout").first()
    if not layout:
        raise HTTPException(status_code=404, detail="404 Error Not Found Layout")
    house_type = db.query(Handbooks).filter(
        Handbooks.id == apartment.house_type).filter(Handbooks.handbook_type == "house_type").first()
    if not house_type:
        raise HTTPException(status_code=404, detail="404 Error Not Found House Type")
    obj = db.query(Objects).filter(Objects.id == apartment.object).first()
    if not obj:
        raise HTTPException(status_code=404, detail="404 Error Not Found Object")

    apartment_model.rooms_number = apartment.rooms_number
    apartment_model.room_types = apartment.room_types
    apartment_model.height = apartment.height
    apartment_model.kitchen_square = apartment.kitchen_square
    apartment_model.living_square = apartment.living_square
    apartment_model.gas = apartment.gas
    apartment_model.courtyard = apartment.courtyard
    apartment_model.balcony_number = apartment.balcony_number
    apartment_model.registered_number = apartment.registered_number
    apartment_model.child_registered_number = apartment.child_registered_number
    apartment_model.loggias_number = apartment.loggias_number
    apartment_model.bay_windows_number = apartment.bay_windows_number
    apartment_model.commune = apartment.commune
    apartment_model.frame = apartment.frame
    apartment_model.stair = apartment.stair
    apartment_model.balcony = apartment.balcony
    apartment_model.heating = apartment.heating
    apartment_model.office = apartment.office
    apartment_model.penthouse = apartment.penthouse
    apartment_model.redevelopment = apartment.redevelopment
    apartment_model.layout = apartment.layout
    apartment_model.construction_number = apartment.construction_number
    apartment_model.house_type = apartment.house_type
    apartment_model.two_level_apartment = apartment.two_level_apartment
    apartment_model.loggia = apartment.loggia
    apartment_model.attic = apartment.attic
    apartment_model.electric_stove = apartment.electric_stove
    apartment_model.floor = apartment.floor
    apartment_model.storeys_number = apartment.storeys_number
    apartment_model.object = apartment.object

    db.add(apartment_model)
    db.commit()

    return "Success"


@router.delete("/{apartment_id}")
async def delete_apartment(apartment_id: int, db: Session = Depends(get_db)):
    try:
        apartment_model = db.query(Apartments).filter(Apartments.id == apartment_id).first()
        if not apartment_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Apartments).filter(Apartments.id == apartment_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
