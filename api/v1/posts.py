from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from scheme.posts import PostCreate, PostOut, PostBase
from scheme.common import ResponseModel
from common.utils import get_db, get_redis, logger
from common.dependencies import get_user_sn
from crud.posts import create_post, read_post_by_sn, remove_post, update_post, read_list_posts
from model.model import User
from fastapi.responses import JSONResponse
from redis import Redis

router = APIRouter()

@router.post("/", response_model=ResponseModel)
def post_post(post: PostCreate, db: Session = Depends(get_db), redis: Redis = Depends(get_redis), user_sn = Depends(get_user_sn)):
    new_post = create_post(db, post, user_sn)

    if new_post is None:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ResponseModel(status="fail", code=403, message="You do not have access to this board").dict()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=ResponseModel(status="success", message="Post created successfully", code=201, data={"post_sn": new_post.post_sn}).dict()
    )

@router.get("/{post_sn}", response_model=ResponseModel)
def get_post(post_sn: int, db: Session = Depends(get_db), user_sn = Depends(get_user_sn)):
    db_post = read_post_by_sn(db, post_sn, user_sn)

    if db_post == "Post not found":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ResponseModel(status="fail", message="Post not found", code=404).dict()
        )
    elif db_post == "You do not have access to this board's posts":
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ResponseModel(status="fail", message="You do not have acess to this board's posts", code=404).dict()
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", message="Post retrieved successfully", code=200, data=db_post).dict()
    )

@router.put("/{post_sn}", response_model=ResponseModel)
def put_post(post_sn: int, post: PostBase, db: Session = Depends(get_db), user_sn = Depends(get_user_sn)):
    updated_post = update_post(db, post_sn, post.title, post.content, user_sn)
    if updated_post is None or updated_post.user_sn != int(user_sn):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ResponseModel(status="fail", message="Post not found or permission denied", code=404).dict()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", message="Post updated successfully", code=200, data={"post_sn": updated_post.post_sn}).dict()
    )

@router.delete("/{post_sn}", response_model=ResponseModel)
def delete_post(post_sn: int, db: Session = Depends(get_db), user_sn = Depends(get_user_sn)):
    success = remove_post(db, post_sn, user_sn)

    if not success:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ResponseModel(status="fail", code=404, message="Board not found or permission denied").dict()
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", message="Post deleted successfully", code=200).dict()
    )
@router.get("/", response_model=ResponseModel)
def get_list_posts(board_sn: int, page: int = 1, limit: int = 10, db: Session = Depends(get_db), user_sn = Depends(get_user_sn)):
    posts = read_list_posts(db, board_sn, user_sn, page=page, limit=limit)


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", message="Posts retrieved successfully", code=200, data={"post_sn": posts.post_sn}).dict()
    )