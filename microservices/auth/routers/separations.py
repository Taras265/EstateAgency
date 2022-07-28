from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from microservices.auth.models import *
from microservices.models import *

router = APIRouter(
    prefix="/separations",
    tags=["separations"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_separations(db: Session = Depends(get_db)):
    separations = db.query(Separations).all()
    return separations


@router.get("/{separation_id}")
async def get_separation(separation_id: int, db: Session = Depends(get_db)):
    separation = db.query(Separations).filter(Separations.id == separation_id).first()
    if not separation:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return separation


@router.get("/{start}/{limit}")
async def all_separations_on_page(start: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    separations = db.query(Separations).offset(start).limit(limit).all()
    count = db.query(Separations).count()
    return {"objects": separations, "count": count}


@router.post("/")
async def create_separation(separation: CreateSeparation, db: Session = Depends(get_db)):
    separation_model = Separations()

    separation_model.separation = separation.separation

    db.add(separation_model)
    db.commit()

    return "Success"


@router.put("/{separation_id}")
async def update_separation(separation_id: int, separation: CreateSeparation, db: Session = Depends(get_db)):
    separation_model = db.query(Separations).filter(Separations.id == separation_id).first()
    if not separation_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    separation_model.separation = separation.separation

    db.add(separation_model)
    db.commit()

    return "Success"


@router.delete("/{separation_id}")
async def delete_separation(separation_id: int, db: Session = Depends(get_db)):
    try:
        separation_model = db.query(Separations).filter(Separations.id == separation_id).first()
        if not separation_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        db.query(Separations).filter(Separations.id == separation_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing objects first")
