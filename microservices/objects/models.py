from typing import Optional
from pydantic.main import BaseModel


class CreateObjType(BaseModel):
    type: str
    slug: str


class CreateObject(BaseModel):
    create_date: str
    date_before_temporarily_removed: Optional[str]
    deposit_date: Optional[str]
    purchase_date: str
    sale_date: Optional[str]
    date_of_next_call: Optional[str]
    inspection_form: Optional[str]
    exclusive: bool
    exclusive_to: Optional[str]
    exclusive_from: Optional[str]
    district: int
    region: int
    city: int
    city_region: int
    street: int
    house: Optional[str]
    apartment: Optional[str]
    on_site: bool
    inspection_flag: bool
    paid_exclusive_flag: bool
    terrace_flag: bool
    sea_flag: bool
    vip: bool
    withdrawal_reason: Optional[str]  # int
    independent: bool
    condition: int
    special: bool
    urgently: bool
    trade: bool
    material: int
    status: str
    object_type: int
    square: int
    price: int
    site_price: int
    square_meter_price: int
    realtor: int
    site_realtor1: int
    site_realtor2: Optional[str]  # int
    realtor_5_5: Optional[str]  # int
    for_trainee: bool
    realtor_notes: Optional[str]
    reference_point: Optional[str]
    author: int
    owner: int
    client: Optional[str]  # int
    owners_number: int
    comment: str
    separation: int
    agency: int
    agency_sales: int
    sale_terms: Optional[str]
    filename_of_exclusive_agreement: Optional[str]
    inspection_file_name: Optional[str]
    document: Optional[str]
    filename_forbid_sale: Optional[str]
    new_building_name: Optional[str]  # int
    new_building: bool
    new_building_type: Optional[str]


class CreateApartment(BaseModel):
    rooms_number: int
    room_types: str
    height: float
    kitchen_square: int
    living_square: int
    gas: bool
    courtyard: bool
    balcony_number: int
    registered_number: int
    child_registered_number: int
    loggias_number: int
    bay_windows_number: int
    commune: bool
    frame: str
    stair: int
    balcony: bool
    heating: int
    office: bool
    penthouse: bool
    redevelopment: str
    layout: int
    construction_number: str
    house_type: int
    two_level_apartment: bool
    loggia: int
    attic: bool
    electric_stove: bool
    floor: int
    storeys_number: int
    object: int
