from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from scheme.boards import BoardCreate, BoardOut, BoardUpdate
from scheme.common import ResponseModel
from common.utils import get_db, get_redis, logger
from common.dependencies import check_valid_session, get_user_sn
from fastapi.security import OAuth2PasswordRequestForm
from crud.boards import create_board, read_board_by_sn, remove_board, update_board, read_list_boards
from fastapi.responses import JSONResponse
from model.model import User
from redis import Redis

router = APIRouter()

@router.post("/", response_model=ResponseModel)
def post_board(board: BoardCreate, db: Session = Depends(get_db), redis: Redis = Depends(get_redis), user_sn = Depends(get_user_sn)):
    new_board = create_board(db, board, user_sn)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=ResponseModel(status="success", message="Board created successfully", code=201, data={"board_sn": new_board.board_sn}).dict()
    )

@router.get("/{board_sn}", response_model=ResponseModel)
def get_board(board_sn: int, db: Session = Depends(get_db), user_sn = Depends(get_user_sn)):
    db_board = read_board_by_sn(db, board_sn, user_sn)
    if db_board is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ResponseModel(status="fail", code=404, message="Board not found").dict()
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", code=200, message="Board retrieved successfully", data=db_board).dict()
    )

@router.put("/{board_sn}", response_model=ResponseModel)
def put_board(board_sn: int, board: BoardUpdate, db: Session = Depends(get_db), user_sn = Depends(get_user_sn)):
    db_board = update_board(db, board_sn, user_sn, board.name, board.public)
    logger.debug(f"db_board: {db_board.user_sn}, user_sn: {user_sn}")
    logger.debug(f"db_board.user_sn type: {type(db_board.user_sn)}, user_sn type: {type(user_sn)}")
    if db_board is None or db_board.user_sn != int(user_sn):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ResponseModel(status="fail", code=404, message="Board not found or permission denied").dict()
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", code=200, message="Board updated successfully", data={"name": db_board.name, "public": db_board.public}).dict()
    )

@router.delete("/{board_sn}", response_model=ResponseModel)
def delete_board(board_sn: int, db: Session = Depends(get_db), user_sn = Depends(get_user_sn)):
    success = remove_board(db, board_sn, user_sn)
    
    if not success:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ResponseModel(status="fail", code=404, message="Board not found or permission denied").dict()
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", code=200, message="Board deleted successfully").dict()
    )

@router.get("/", response_model=ResponseModel)
def get_list_boards(page: int = 1, limit: int = 10, sort_flag: bool = False, db: Session = Depends(get_db), user_sn = Depends(get_user_sn)):
    """sort_flog를 파라미터로 받아 총 게시글기준 정렬 여부를 결정한다."""
    logger.info(f"user: {user_sn}")
    boards = read_list_boards(db, user_sn, sort_flag, page=page, limit=limit)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseModel(status="success", code=200, message="Boards retrieved successfully", data=boards).dict()
    )