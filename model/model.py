from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    # sn, idx, uniq
    user_sn = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Board(Base):
    __tablename__ = 'boards'
    board_sn = Column(Integer, Sequence('board_sn_seq'), primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)
    public = Column(Boolean, default=True)
    user_sn = Column(Integer, index=True)

class Post(Base):
    __tablename__ = 'posts'
    post_sn = Column(Integer, Sequence('post_sn_seq'), primary_key=True)
    title = Column(String, index=True)
    content = Column(String, nullable=False)
    board_sn = Column(Integer, index=True)
    user_sn = Column(Integer, index=True)