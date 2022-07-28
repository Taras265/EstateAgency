from api.all_api import *
from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from microservices.database import get_db
from microservices.models import *
import shutil
from ..conf import MEDIA_ROOT
import os

from ..models import UpdateObjImages

router = APIRouter(
    prefix="/obj_images",
    tags=["obj_images"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def all_images(db: Session = Depends(get_db)):
    images = db.query(ObjImages).all()
    return images


@router.get("/by_object/{object_id}")
async def images_by_object(object_id: int, db: Session = Depends(get_db)):
    images = db.query(ObjImages).filter(ObjImages.object == object_id)\
        .filter(ObjImages.on_site == True).all()
    return images


@router.get("/all/by_object/{object_id}")
async def all_images_by_object(object_id: int, db: Session = Depends(get_db)):
    images = db.query(ObjImages).filter(ObjImages.object == object_id).all()
    return images


@router.get("/{source}")
async def get_image(source: str, db: Session = Depends(get_db)):
    image_model = db.query(ObjImages).filter(ObjImages.source == source).all()
    if not image_model and source != "default.jpg":
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return FileResponse(f"{MEDIA_ROOT}/objects/{source}")


@router.post("/{obj_id}")
async def save_image(obj_id: int, img: UploadFile = File(...), db: Session = Depends(get_db)):
    if img.filename.split('.')[-1] not in ["jpg", "jpeg"]:
        raise HTTPException(status_code=400, detail="Bad Request")
    image_model = ObjImages()

    if not object_api.get(obj_id):
        raise HTTPException(status_code=404, detail="404 Error Not Found Object")
    image_model.object = obj_id
    image_model.source = f"{image_model.id}.jpg"
    image_model.on_site = True

    db.add(image_model)
    db.commit()

    model_id = image_model.id

    with open(f'{MEDIA_ROOT}/objects/{model_id}.jpg', "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)

    image_model.source = f"{model_id}.jpg"
    db.add(image_model)
    db.commit()

    return "Success"


@router.put("/{image_id}")
async def update_image_info(image_id: int, on_site: UpdateObjImages, db: Session = Depends(get_db)):
    image_model = db.query(ObjImages).filter(ObjImages.id == image_id).first()
    if not image_model:
        raise HTTPException(status_code=404, detail="404 Error Not Found")

    image_model.on_site = on_site.on_site

    db.add(image_model)
    db.commit()

    return "Success"


@router.delete("/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    try:
        image_model = db.query(ObjImages).filter(ObjImages.id == image_id).first()
        if not image_model:
            raise HTTPException(status_code=404, detail="404 Error Not Found")

        os.remove(f'{MEDIA_ROOT}/objects/{image_model.id}.jpg')

        db.query(ObjImages).filter(ObjImages.id == image_id).delete()
        db.commit()

        return "Success"
    except IntegrityError:
        return HTTPException(status_code=400, detail="Bad Request Remove Referencing Objects First")
