from fastapi import APIRouter
from api.v1 import users, boards, posts

router = APIRouter()

router.include_router(users.router, prefix="/api/v1/users", tags=["v1-users"])
router.include_router(boards.router, prefix="/api/v1/boards", tags=["v1-boards"])
router.include_router(posts.router, prefix="/api/v1/posts", tags=["v1-posts"])