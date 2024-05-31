from sqlalchemy.orm import Session
from model.model import User
from scheme.users import UserCreate
from common.utils import get_password_hash, logger
from sqlalchemy.exc import SQLAlchemyError

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(fullname=user.fullname, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise e