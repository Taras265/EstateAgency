from typing import Optional
from pydantic.main import BaseModel


class CreateHandbook(BaseModel):
    handbook: str
    handbook_type: str


class CreateNewBuilding(BaseModel):
    new_building: str
    building: bool
    street: int
    house: str
    region: int


class CreateClient(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str


class CreateDistrict(BaseModel):
    district: str


class CreateRegion(BaseModel):
    region: str
    district: int


class CreateCity(BaseModel):
    city: str
    region: int
    city_type: str
    center_type: Optional[str]


class CreateCityRegion(BaseModel):
    city_region: str
    city: int
    description: Optional[str]
    group_on_site: Optional[str]
    region: Optional[int]
    hot_deals_limit: float
    prefix_to_site: Optional[str]
    is_subdistrict: bool
    new_building_region: Optional[str]


class CreateStreet(BaseModel):
    street: str
    city_region: int
    city: int


class GetAddress(BaseModel):
    district: int
    region: int
    city: int
    city_region: int
    street: int
    house: Optional[str]
    apartment: Optional[str]
