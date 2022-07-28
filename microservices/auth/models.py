from typing import Optional
from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str
    password: str
    second_password: str


class Authorization(BaseModel):
    email: str
    password: str


class UserRight(BaseModel):
    token: Optional[str]
    right: str


class CreateGroup(BaseModel):
    group: str


class CreateRight(BaseModel):
    right: str
    slug: str


class AddUserGroup(BaseModel):
    user: int
    group: int


class AddGroupRight(BaseModel):
    group: int
    right: int


class CreateSeparation(BaseModel):
    separation: str
