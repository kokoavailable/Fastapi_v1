from fastapi import Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from model.model import User
from common.utils import get_db, get_redis, logger
from redis import Redis


def check_valid_session(request: Request, redis: Redis = Depends(get_redis)):
    auth_header = request.headers.get("Authorization")
    logger.debug(f"Received auth: {auth_header}")
    
    if auth_header is None:
        return "Authorization not found in headers"
    
    if not auth_header.startswith("Bearer "):
        return "Invalid authorization header format"
    
    session_id = auth_header[len("Bearer "):]

    if not redis.exists(session_id):
        return "Session not found"
    
    return session_id

def get_user_sn(request: Request, redis: Redis = Depends(get_redis)):
    token = check_valid_session(request, redis)
    if token == "Session not found":
        logger.error(f"Token not found in Redis: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    logger.debug(f"Received token: {token}")
    user_sn = redis.get(token).decode('utf-8')

    return user_sn