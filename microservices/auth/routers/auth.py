from fastapi import APIRouter, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session
from microservices.auth.functions import *
from microservices.auth.models import CreateUser, Authorization, UserRight
from microservices.database import get_db
from microservices.models import *

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 Error Not Found")
    return user


@router.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = Users()
    user_model = db.query(Users).filter(Users.email == create_user.email).first()
    if user_model:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    elif create_user.password != create_user.second_password:
        raise HTTPException(status_code=400, detail="Incorrect second password")
    if len(create_user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be more than 8 characters")

    create_user_model.email = create_user.email
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.phone = create_user.phone

    hash_password = get_password_hash(create_user.password)
    create_user_model.hashed_password = hash_password

    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()

    return create_user_model.id


@router.post("/login")
async def login_for_access_token(form_data: Authorization, db: Session = Depends(get_db)):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="User email or password incorrect")
    token_expires = timedelta(minutes=120)
    token = create_access_token(user.email, user.id, expires_delta=token_expires)
    return {"token": token}


@router.get("/user/{token}")
async def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could Not Validate Credentials")
    user = db.query(Users).filter(Users.id == user_id).filter(Users.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 Error Not Found User")
    return {"email": email, "id": user_id}


@router.post("/user/right")
async def get_user_rights(user_right: UserRight, db: Session = Depends(get_db)):
    if user_right.token:
        try:
            payload = jwt.decode(user_right.token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("id")
            user_groups = db.query(UserGroup).filter(UserGroup.user == user_id).all()
            for user_group in user_groups:
                group = db.query(Groups).filter(Groups.id == user_group.group).first()
                return check_right_by_group(group.id, user_right.right, db)
            return payload
        except JWTError:
            group = db.query(Groups).filter(Groups.group == "user").first()
            return check_right_by_group(group.id, user_right.right, db)
    else:
        group = db.query(Groups).filter(Groups.group == "user").first()
        return check_right_by_group(group.id, user_right.right, db)


def check_right_by_group(group_id, right, db):
    group_rights = db.query(GroupRight).filter(GroupRight.group == group_id).all()
    for group_right in group_rights:
        user_right = db.query(Rights).filter(Rights.id == group_right.right).filter(Rights.slug == right).first()
        if user_right:
            return True
    return False
