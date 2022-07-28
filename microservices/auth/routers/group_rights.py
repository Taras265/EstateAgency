from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from microservices.auth.models import *
from microservices.models import *

router = APIRouter(
    prefix="/group/right",
    tags=["group_rights"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{group_id}")
async def group_rights(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="404 Error Not Found Group")
    groups = db.query(GroupRight).filter(GroupRight.group == group.id).all()
    return groups


@router.post("/")
async def add_group_rights(group_right: AddGroupRight, db: Session = Depends(get_db)):
    right = db.query(Rights).filter(Rights.id == group_right.right).first()
    group = db.query(Groups).filter(Groups.id == group_right.group).first()
    if not right:
        raise HTTPException(status_code=404, detail="404 Error Not Found Right")
    if not group:
        raise HTTPException(status_code=404, detail="404 Error Not Found Group")

    group_right = GroupRight()
    group_right.group = group.id
    group_right.right = right.id

    db.add(group_right)
    db.commit()

    return "Success"


@router.put("/{group_right_id}")
async def update_group_rights(group_right_id: int, group_right_form: AddGroupRight, db: Session = Depends(get_db)):
    right = db.query(Rights).filter(Rights.id == group_right_form.right).first()
    group = db.query(Groups).filter(Groups.id == group_right_form.group).first()
    if not right:
        raise HTTPException(status_code=404, detail="404 Error Not Found Right")
    if not group:
        raise HTTPException(status_code=404, detail="404 Error Not Found Group")
    group_right = db.query(GroupRight).filter(GroupRight.id == group_right_id).first()
    if not group_right:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    group_right.group = group_right_form.group
    group_right.right = group_right_form.right

    db.add(group_right)
    db.commit()

    return "Success"


@router.delete("/{group_right_id}")
async def delete_group_rights(group_right_id: int, db: Session = Depends(get_db)):
    try:
        group_right = db.query(GroupRight).filter(GroupRight.id == group_right_id).first()
        if not group_right:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(GroupRight).filter(GroupRight.id == group_right_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
