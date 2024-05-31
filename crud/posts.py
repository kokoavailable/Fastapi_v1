from sqlalchemy.orm import Session
from model.model import Post, Board
from scheme.posts import PostCreate, PostOut

def create_post(db: Session, post: PostCreate, user_sn: int):
    board = db.query(Board).filter(
        Board.board_sn == post.board_sn,
        (Board.public == True) | (Board.user_sn == user_sn)
    ).first()

    if not board:
        return None
    
    db_post = Post(
        title=post.title,
        content=post.content,
        board_sn=post.board_sn,
        user_sn=user_sn
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post

def read_post_by_sn(db: Session, post_sn: int, user_sn: int):
    post = db.query(Post).filter(Post.post_sn == post_sn).first()
    if not post:
        return "Post not found"
    
    board = db.query(Board).\
        filter(Board.board_sn == post.board_sn).\
        filter((Board.public == True) | (Board.user_sn == user_sn)).\
        first()
    
    if board is None:
        return "You do not have access to this board's posts"
    
    return PostOut(
        post_sn=post.post_sn,
        board_sn=post.board_sn,
        user_sn=post.user_sn,
        title=post.title,
        content=post.content
    )

def remove_post(db: Session, post_sn: int, user_sn: int):
    delete_post = db.query(Post).\
    filter(Post.post_sn == post_sn).\
    filter((Post.user_sn == user_sn)).\
    first()

    if not delete_post:
        return False
    
    db.delete(delete_post)
    db.commit()
    return True

def update_post(db: Session, post_sn, title: str, content: str, user_sn: int):
    update_post = db.query(Post).\
        filter(Post.post_sn == post_sn).\
        filter((Post.user_sn == user_sn)).\
        first()
    
    if not update_post:
        return None


    update_post.title = title
    update_post.content = content
    db.commit()
    db.refresh(update_post)
    return update_post

def read_list_posts(db: Session, board_sn: int, user_sn: int, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    board = db.query(Board).filter(
            Board.board_sn == board_sn,
            (Board.public == True) | (Board.user_sn == user_sn)
        ).first()
    
    if not board:
        return None
    
    posts = db.query(Post).filter(
        Post.board_sn == board_sn
    ).offset(skip).limit(limit).all()
    
    return [PostOut(
        post_sn=post.post_sn,
        board_sn=post.board_sn,
        user_sn=post.user_sn,
        title=post.title,
        content=post.content
    ) for post in posts]