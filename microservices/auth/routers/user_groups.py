from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from microservices.auth.models import *
from microservices.models import *

router = APIRouter(
    prefix="/user",
    tags=["user_groups"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{user_id}")
async def user_groups(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    groups = db.query(UserGroup).filter(UserGroup.user == user.id).all()
    return groups


@router.get("/groups/{group_id}")
async def by_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    groups = db.query(UserGroup).filter(UserGroup.group == group.id).all()
    return groups


@router.post("/")
async def add_group_for_user(user_group: AddUserGroup, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_group.user).first()
    group = db.query(Groups).filter(Groups.id == user_group.group).first()
    if not group or not user:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    user_group = UserGroup()
    user_group.group = group.id
    user_group.user = user.id

    db.add(user_group)
    db.commit()

    return "Success"


@router.put("/{user_group_id}")
async def update_user_group(user_group_id: int, user_group_form: AddUserGroup, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_group_form.user).first()
    group = db.query(Groups).filter(Groups.id == user_group_form.group).first()
    if not group or not user:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    user_group = db.query(UserGroup).filter(UserGroup.id == user_group_id).first()

    user_group.group = user_group_form.group
    user_group.user = user_group_form.user

    db.add(user_group)
    db.commit()

    return "Success"


@router.delete("/{user_group_id}")
async def delete_user_group(user_group_id: int, db: Session = Depends(get_db)):
    try:
        user_group = db.query(UserGroup).filter(UserGroup.id == user_group_id).first()
        if not user_group:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(UserGroup).filter(UserGroup.id == user_group_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
