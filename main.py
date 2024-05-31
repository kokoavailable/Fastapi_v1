from fastapi import FastAPI
from common.utils import engine
from model.model import Base
from router.router import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)