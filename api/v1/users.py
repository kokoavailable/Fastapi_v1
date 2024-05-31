from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from scheme.users import UserCreate, UserOut
from scheme.common import ResponseModel
from crud.users import create_user, get_user_by_email
from common.utils import create_session, verify_password, get_db, get_redis, logger
from common.dependencies import check_valid_session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from redis import Redis
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/signup", response_model=ResponseModel)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ResponseModel(status="fail", code=400, message="Email already registered").dict()
        )
    try:
        create_user(db, user)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=ResponseModel(status="success", code=201, message="User created successfully").dict()
        )
    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseModel(status="fail", code=500, message="Internal server error").dict()
        )

@router.post("/session", response_model=ResponseModel)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db), 
    redis: Redis = Depends(get_redis)
):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ResponseModel(status="fail", code=401, message="Incorret email or password").dict()
        )
    session_expires = timedelta(minutes=30)
    session_id = create_session(user.user_sn, redis, expires_delta=session_expires)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", code=200, message="Login successful", data={"access_token": session_id}).dict()
    )

@router.post("/logout", response_model=ResponseModel)
def logout(token: str = Depends(check_valid_session), redis: Redis = Depends(get_redis)):
    if token == "Authorization not founin headers":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": "fail", "code": 401, "message": token}
        )
    elif token == "Session not found":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": "fail", "code": 404, "message": token}
        )

    redis_key = token
    logger.info(f"{redis_key}")
    redis.delete(redis_key)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", message="Successfully logged out", code=200).dict()
    )
