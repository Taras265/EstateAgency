import requests
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from api.handbooks.handbooks import Locations
from microservices.database import get_db
from ..models import *
from microservices.models import *

router = APIRouter(
    prefix="/objects",
    tags=["objects"],
    responses={404: {"description": "Not found"}}
)

locations_api = Locations()


@router.get("/")
async def all_objects(db: Session = Depends(get_db)):
    objects = db.query(Objects).filter(Objects.on_site == True).all()
    return objects


@router.get("/{object_id}")
async def get_object(object_id: int, db: Session = Depends(get_db)):
    obj = db.query(Objects).filter(Objects.id == object_id).filter(Objects.on_site == True).first()
    if not obj:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return obj


@router.get("/type/{object_type_id}")
async def get_objects_by_type(object_type_id: int, db: Session = Depends(get_db)):
    obj_type = db.query(ObjectTypes).filter(ObjectTypes.id == object_type_id).first()
    if not obj_type:
        raise HTTPException(status_code=404, detail="404 Error Not Found Object Type")
    obj = db.query(Objects).filter(Objects.object_type == object_type_id).filter(Objects.on_site == True).all()
    return obj


@router.post("/")
async def create_object(obj: CreateObject, db: Session = Depends(get_db)):
    object_model = Objects()

    district = db.query(Districts).filter(Districts.id == obj.district).first()
    if not district:
        raise HTTPException(status_code=404, detail="404 Error Not Found District")
    region = db.query(Regions).filter(Regions.id == obj.region).first()
    if not region:
        raise HTTPException(status_code=404, detail="404 Error Not Found Region")
    city = db.query(Cities).filter(Cities.id == obj.city).first()
    if not city:
        raise HTTPException(status_code=404, detail="404 Error Not Found City")
    city_region = db.query(CityRegions).filter(CityRegions.id == obj.city_region).first()
    if not city_region:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Region")
    street = db.query(Streets).filter(Streets.id == obj.street).first()
    if not street:
        raise HTTPException(status_code=404, detail="404 Error Not Found Street")
    if obj.withdrawal_reason == "None":
        obj.withdrawal_reason = None
    elif obj.withdrawal_reason.isdigit():
        withdrawal_reason = db.query(Handbooks).filter(
            Handbooks.id == obj.withdrawal_reason).filter(Handbooks.handbook_type == "withdrawal_reason").first()
        if not withdrawal_reason:
            raise HTTPException(status_code=404, detail="404 Error Not Found Withdrawal Reason")
    condition = db.query(Handbooks).filter(
        Handbooks.id == obj.condition).filter(Handbooks.handbook_type == "condition").first()
    if not condition:
        raise HTTPException(status_code=404, detail="404 Error Not Found Condition")
    material = db.query(Handbooks).filter(
        Handbooks.id == obj.material).filter(Handbooks.handbook_type == "material").first()
    if not material:
        raise HTTPException(status_code=404, detail="404 Error Not Found Material")
    if obj.status not in ["В продаже", "Задаток", "Снята", "Продана", "Снята совсем"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found Status")
    object_type = db.query(ObjectTypes).filter(ObjectTypes.id == obj.object_type).first()
    if not object_type:
        raise HTTPException(status_code=404, detail="404 Error Not Found Object Type")
    realtor = db.query(Users).filter(Users.id == obj.realtor).first()
    site_realtor1 = db.query(Users).filter(Users.id == obj.site_realtor1).first()
    if not realtor:
        raise HTTPException(status_code=404, detail="404 Error Not Found Main Realtor")
    if not site_realtor1:
        raise HTTPException(status_code=404, detail="404 Error Not Found First Site Realtor")
    if obj.site_realtor2 == "None":
        obj.site_realtor2 = None
    elif obj.site_realtor2.isdigit():
        site_realtor2 = db.query(Users).filter(Users.id == obj.site_realtor2).first()
        if not site_realtor2:
            raise HTTPException(status_code=404, detail="404 Error Not Found Second Site Realtor")
    if obj.realtor_5_5 == "None":
        obj.realtor_5_5 = None
    elif obj.realtor_5_5.isdigit():
        realtor_5_5 = db.query(Users).filter(Users.id == obj.realtor_5_5).first()
        if not realtor_5_5:
            raise HTTPException(status_code=404, detail="404 Error Not Found Realtor 5 To 5")
    author = db.query(Users).filter(Users.id == obj.author).first()
    if not author:
        raise HTTPException(status_code=404, detail="404 Error Not Found Author")
    owner = db.query(Clients).filter(Clients.id == obj.owner).first()
    if not owner:
        raise HTTPException(status_code=404, detail="404 Error Not Found Owner")
    if obj.client == "None":
        obj.client = None
    elif obj.client.isdigit():
        client = db.query(Clients).filter(Clients.id == obj.client).first()
        if not client:
            raise HTTPException(status_code=404, detail="404 Error Not Found Client")
    separation = db.query(Separations).filter(Separations.id == obj.separation).first()
    if not separation:
        raise HTTPException(status_code=404, detail="404 Error Not Found Author")
    agency = db.query(Handbooks).filter(
        Handbooks.id == obj.agency).filter(Handbooks.handbook_type == "agency").first()
    if not agency:
        raise HTTPException(status_code=404, detail="404 Error Not Found Agency")
    agency_sales = db.query(Handbooks).filter(
        Handbooks.id == obj.agency_sales).filter(Handbooks.handbook_type == "agency").first()
    if not agency_sales:
        raise HTTPException(status_code=404, detail="404 Error Not Found Agency Sales")
    new_building_name = db.query(NewBuildings).filter(
        NewBuildings.id == obj.new_building_name).first()
    if not new_building_name:
        raise HTTPException(status_code=404, detail="404 Error Not Found New Building Name")
    if obj.new_building_type == "None":
        obj.new_building_type = None
    elif obj.new_building_type not in ["От хозяина", "От строителя"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found New Building Type")
    data_form = {"district": district.id, "region": region.id, "city": city.id, "city_region": city_region.id,
                 "street": street.id, "home": None, "apartment": None}
    message = locations_api.get_address(data_form)

    # if isinstance(message, dict):
    #     raise HTTPException(status_code=400, detail=message.get("detail"))

    object_model.create_date = obj.create_date
    object_model.date_before_temporarily_removed = obj.date_before_temporarily_removed
    object_model.deposit_date = obj.deposit_date
    object_model.purchase_date = obj.purchase_date
    object_model.sale_date = obj.sale_date
    object_model.date_of_next_call = obj.date_of_next_call
    object_model.inspection_form = obj.inspection_form
    object_model.exclusive = obj.exclusive
    object_model.exclusive_to = obj.exclusive_to
    object_model.exclusive_from = obj.exclusive_from
    object_model.district = obj.district
    object_model.region = obj.region
    object_model.city = obj.city
    object_model.city_region = obj.city_region
    object_model.street = obj.street
    object_model.house = obj.house
    object_model.apartment = obj.apartment
    object_model.on_site = obj.on_site
    object_model.inspection_flag = obj.inspection_flag
    object_model.paid_exclusive_flag = obj.paid_exclusive_flag
    object_model.terrace_flag = obj.terrace_flag
    object_model.sea_flag = obj.sea_flag
    object_model.vip = obj.vip
    object_model.withdrawal_reason = obj.withdrawal_reason
    object_model.independent = obj.independent
    object_model.condition = obj.condition
    object_model.special = obj.special
    object_model.urgently = obj.urgently
    object_model.trade = obj.trade
    object_model.material = obj.material
    object_model.status = obj.status
    object_model.object_type = obj.object_type
    object_model.square = obj.square
    object_model.price = obj.price
    object_model.site_price = obj.site_price
    object_model.square_meter_price = obj.square_meter_price
    object_model.realtor = obj.realtor
    object_model.site_realtor1 = obj.site_realtor1
    object_model.site_realtor2 = obj.site_realtor2
    object_model.realtor_5_5 = obj.realtor_5_5
    object_model.for_trainee = obj.for_trainee
    object_model.realtor_notes = obj.realtor_notes
    object_model.reference_point = obj.reference_point
    object_model.author = obj.author
    object_model.owner = obj.owner
    object_model.client = obj.client
    object_model.owners_number = obj.owners_number
    object_model.comment = obj.comment
    object_model.separation = obj.separation
    object_model.agency = obj.agency
    object_model.agency_sales = obj.agency_sales
    object_model.sale_terms = obj.sale_terms
    object_model.filename_of_exclusive_agreement = obj.filename_of_exclusive_agreement
    object_model.inspection_file_name = obj.inspection_file_name
    object_model.document = obj.document
    object_model.filename_forbid_sale = obj.filename_forbid_sale
    object_model.new_building_name = obj.new_building_name
    object_model.new_building = obj.new_building
    object_model.new_building_type = obj.new_building_type

    db.add(object_model)
    db.commit()

    return "Success"


@router.put("/{object_id}")
async def update_object(object_id: int, obj: CreateObject, db: Session = Depends(get_db)):
    object_model = db.query(Objects).filter(Objects.id == object_id).first()
    if not object_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    district = db.query(Districts).filter(Districts.id == obj.district).first()
    if not district:
        raise HTTPException(status_code=404, detail="404 Error Not Found District")
    region = db.query(Regions).filter(Regions.id == obj.region).first()
    if not region:
        raise HTTPException(status_code=404, detail="404 Error Not Found Region")
    city = db.query(Cities).filter(Cities.id == obj.city).first()
    if not city:
        raise HTTPException(status_code=404, detail="404 Error Not Found City")
    city_region = db.query(CityRegions).filter(CityRegions.id == obj.city_region).first()
    if not city_region:
        raise HTTPException(status_code=404, detail="404 Error Not Found City Region")
    street = db.query(Streets).filter(Streets.id == obj.street).first()
    if not street:
        raise HTTPException(status_code=404, detail="404 Error Not Found Street")
    if obj.withdrawal_reason == "None":
        obj.withdrawal_reason = None
    elif obj.withdrawal_reason.isdigit():
        withdrawal_reason = db.query(Handbooks).filter(
            Handbooks.id == obj.withdrawal_reason).filter(Handbooks.handbook_type == "withdrawal_reason").first()
        if not withdrawal_reason:
            raise HTTPException(status_code=404, detail="404 Error Not Found Withdrawal Reason")
    condition = db.query(Handbooks).filter(
        Handbooks.id == obj.condition).filter(Handbooks.handbook_type == "condition").first()
    if not condition:
        raise HTTPException(status_code=404, detail="404 Error Not Found Condition")
    material = db.query(Handbooks).filter(
        Handbooks.id == obj.material).filter(Handbooks.handbook_type == "material").first()
    if not material:
        raise HTTPException(status_code=404, detail="404 Error Not Found Material")
    if obj.status not in ["В продаже", "Задаток", "Снята", "Продана", "Снята совсем"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found Status")
    object_type = db.query(ObjectTypes).filter(ObjectTypes.id == obj.object_type).first()
    if not object_type:
        raise HTTPException(status_code=404, detail="404 Error Not Found Object Type")
    realtor = db.query(Users).filter(Users.id == obj.realtor).first()
    site_realtor1 = db.query(Users).filter(Users.id == obj.site_realtor1).first()
    if not realtor:
        raise HTTPException(status_code=404, detail="404 Error Not Found Main Realtor")
    if not site_realtor1:
        raise HTTPException(status_code=404, detail="404 Error Not Found First Site Realtor")
    if obj.site_realtor2 == "None":
        obj.site_realtor2 = None
    elif obj.site_realtor2.isdigit():
        site_realtor2 = db.query(Users).filter(Users.id == obj.site_realtor2).first()
        if not site_realtor2:
            raise HTTPException(status_code=404, detail="404 Error Not Found Second Site Realtor")
    if obj.realtor_5_5 == "None":
        obj.realtor_5_5 = None
    elif obj.realtor_5_5.isdigit():
        realtor_5_5 = db.query(Users).filter(Users.id == obj.realtor_5_5).first()
        if not realtor_5_5:
            raise HTTPException(status_code=404, detail="404 Error Not Found Realtor 5 To 5")
    author = db.query(Users).filter(Users.id == obj.author).first()
    if not author:
        raise HTTPException(status_code=404, detail="404 Error Not Found Author")
    owner = db.query(Clients).filter(Clients.id == obj.owner).first()
    if not owner:
        raise HTTPException(status_code=404, detail="404 Error Not Found Owner")
    if obj.client == "None":
        obj.client = None
    elif obj.client.isdigit():
        client = db.query(Clients).filter(Clients.id == obj.client).first()
        if not client:
            raise HTTPException(status_code=404, detail="404 Error Not Found Client")
    separation = db.query(Separations).filter(Separations.id == obj.separation).first()
    if not separation:
        raise HTTPException(status_code=404, detail="404 Error Not Found Author")
    agency = db.query(Handbooks).filter(
        Handbooks.id == obj.agency).filter(Handbooks.handbook_type == "agency").first()
    if not agency:
        raise HTTPException(status_code=404, detail="404 Error Not Found Agency")
    agency_sales = db.query(Handbooks).filter(
        Handbooks.id == obj.agency_sales).filter(Handbooks.handbook_type == "agency").first()
    if not agency_sales:
        raise HTTPException(status_code=404, detail="404 Error Not Found Agency Sales")
    new_building_name = db.query(NewBuildings).filter(
        NewBuildings.id == obj.new_building_name).first()
    if not new_building_name:
        raise HTTPException(status_code=404, detail="404 Error Not Found New Building Name")
    if obj.new_building_type == "None":
        obj.new_building_type = None
    elif obj.new_building_type not in ["От хозяина", "От строителя"]:
        raise HTTPException(status_code=404, detail="404 Error Not Found New Building Type")
    data_form = {"district": district.id, "region": region.id, "city": city.id, "city_region": city_region.id,
                 "street": street.id, "home": None, "apartment": None}
    message = locations_api.get_address(data_form)

    # if isinstance(message, dict):
    #     raise HTTPException(status_code=400, detail=message.get("detail"))

    object_model.create_date = obj.create_date
    object_model.date_before_temporarily_removed = obj.date_before_temporarily_removed
    object_model.deposit_date = obj.deposit_date
    object_model.purchase_date = obj.purchase_date
    object_model.sale_date = obj.sale_date
    object_model.date_of_next_call = obj.date_of_next_call
    object_model.inspection_form = obj.inspection_form
    object_model.exclusive = obj.exclusive
    object_model.exclusive_to = obj.exclusive_to
    object_model.exclusive_from = obj.exclusive_from
    object_model.district = obj.district
    object_model.region = obj.region
    object_model.city = obj.city
    object_model.city_region = obj.city_region
    object_model.street = obj.street
    object_model.house = obj.house
    object_model.apartment = obj.apartment
    object_model.on_site = obj.on_site
    object_model.inspection_flag = obj.inspection_flag
    object_model.paid_exclusive_flag = obj.paid_exclusive_flag
    object_model.terrace_flag = obj.terrace_flag
    object_model.sea_flag = obj.sea_flag
    object_model.vip = obj.vip
    object_model.withdrawal_reason = obj.withdrawal_reason
    object_model.independent = obj.independent
    object_model.condition = obj.condition
    object_model.special = obj.special
    object_model.urgently = obj.urgently
    object_model.trade = obj.trade
    object_model.material = obj.material
    object_model.status = obj.status
    object_model.object_type = obj.object_type
    object_model.square = obj.square
    object_model.price = obj.price
    object_model.site_price = obj.site_price
    object_model.square_meter_price = obj.square_meter_price
    object_model.realtor = obj.realtor
    object_model.site_realtor1 = obj.site_realtor1
    object_model.site_realtor2 = obj.site_realtor2
    object_model.realtor_5_5 = obj.realtor_5_5
    object_model.for_trainee = obj.for_trainee
    object_model.realtor_notes = obj.realtor_notes
    object_model.reference_point = obj.reference_point
    object_model.author = obj.author
    object_model.owner = obj.owner
    object_model.client = obj.client
    object_model.owners_number = obj.owners_number
    object_model.comment = obj.comment
    object_model.separation = obj.separation
    object_model.agency = obj.agency
    object_model.agency_sales = obj.agency_sales
    object_model.sale_terms = obj.sale_terms
    object_model.filename_of_exclusive_agreement = obj.filename_of_exclusive_agreement
    object_model.inspection_file_name = obj.inspection_file_name
    object_model.document = obj.document
    object_model.filename_forbid_sale = obj.filename_forbid_sale
    object_model.new_building_name = obj.new_building_name
    object_model.new_building = obj.new_building
    object_model.new_building_type = obj.new_building_type

    db.add(object_model)
    db.commit()

    return "Success"


@router.delete("/{object_id}")
async def delete_object(object_id: int, db: Session = Depends(get_db)):
    try:
        object_model = db.query(Objects).filter(Objects.id == object_id).first()
        if not object_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Objects).filter(Objects.id == object_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
