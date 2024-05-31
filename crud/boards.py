from sqlalchemy.orm import Session
from model.model import Board
from sqlalchemy import text
from scheme.boards import BoardCreate, BoardOut, BoardOutWithPostCount

def create_board(db:Session, board: BoardCreate, user_sn: int):
    db_board = Board(
        name=board.name, 
        public=board.public, 
        user_sn=user_sn)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

def read_board_by_sn(db: Session, board_sn: int, user_sn: int):
    board = db.query(Board).\
        filter(Board.board_sn == board_sn).\
        filter((Board.public == True) | (Board.user_sn == user_sn)).\
        first()
    
    if board is None:
        return None

    return BoardOut(
        board_sn=board.board_sn,
        name=board.name,
        public=board.public,
        user_sn=board.user_sn,
    )

def remove_board(db: Session, board_sn, user_sn):
    delete_board = db.query(Board).\
        filter(Board.board_sn == board_sn).\
        filter((Board.user_sn == user_sn)).\
        first()

    if not delete_board:
        return False
    
    db.delete(delete_board)
    db.commit()
    return True


def update_board(db: Session, board_sn: int, user_sn: int, name: str, public: bool):
    board = db.query(Board).\
        filter(Board.board_sn == board_sn).\
        filter((Board.user_sn == user_sn)).\
        first()
    
    if not board:
        return None

    board.name = name
    board.public = public
    db.commit()
    db.refresh(board)
    return board

def read_list_boards(db: Session, user_sn: int, sort_flag: bool, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    param = {
        "user_sn": user_sn,
        "skip": skip,
        "limit": limit
    }
    sql_query = """
        SELECT 
            boards.board_sn,
            boards.name,
            boards.public,
            boards.user_sn,
            COUNT(posts.post_sn) AS post_count
        FROM 
            boards
        LEFT OUTER JOIN 
            posts ON posts.board_sn = boards.board_sn
        WHERE 
            1=1
            AND (boards.public = TRUE OR boards.user_sn = :user_sn)
        GROUP BY 
            boards.board_sn
    """
    if sort_flag:
        sql_query += """
            ORDER BY COUNT(posts.post_sn) DESC
        """
    sql_query += """
        OFFSET 
            :skip
        LIMIT 
            :limit;
    """
    
    results = db.execute(text(sql_query), param).fetchall()

    if results is None:
        return None


    return [BoardOutWithPostCount(
        board_sn=result[0],
        name=result[1],
        public=result[2],
        user_sn=result[3],
        post_count=result[4]
    ) for result in results]