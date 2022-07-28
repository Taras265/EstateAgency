from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from microservices.auth.models import *
from microservices.models import *

router = APIRouter(
    prefix="/group",
    tags=["groups"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_groups(db: Session = Depends(get_db)):
    groups = db.query(Groups).all()
    return groups


@router.get("/{group_id}")
async def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.id == group_id).first()
    return group


@router.get("/by_name/{group}")
async def get_by_name_group(group: str, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.group == group).first()
    return group


@router.post("/")
async def create_group(group: CreateGroup, db: Session = Depends(get_db)):
    group_model = Groups()

    group_model.group = group.group

    db.add(group_model)
    db.commit()

    return "Success"


@router.put("/{group_id}")
async def update_group(group_id: int, group: CreateGroup, db: Session = Depends(get_db)):
    group_model = db.query(Groups).filter(Groups.id == group_id).first()
    if not group_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    group_model.group = group.group

    db.add(group_model)
    db.commit()

    return "Success"


@router.delete("/{group_id}")
async def delete_group(group_id: int, db: Session = Depends(get_db)):
    try:
        group_model = db.query(Groups).filter(Groups.id == group_id).first()
        if not group_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Groups).filter(Groups.id == group_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
