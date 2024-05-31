from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from redis import Redis
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import configparser
import logging
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
import uuid
import os

app_env = os.getenv('APP_ENV', 'LOCAL')


##### 로컬 환경일 때만 config.ini 읽기

if app_env == 'LOCAL':
    config = configparser.ConfigParser()
    current_dir = Path(__file__).resolve().parent
    config_path = current_dir / 'config.ini'

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")


    config_read = config.read(config_path, encoding='utf-8')
    if not config_read:
        raise FileNotFoundError(f"Configuration file not read: {config_path}")
    
###### 로거


def setup_logging():
    logger = logging.getLogger('main')

    # 로그 레벨 설정
    logger.setLevel(logging.DEBUG)  # 개별 로거 레벨 설정

    # 로그 파일 경로 설정
    log_file_path = os.path.join('..', 'logs', f"{app_env}_{datetime.now().strftime('%Y-%m-%d')}.log")

    # 로그 디렉토리 생성
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # 파일 핸들러 설정
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)  # 파일에는 INFO 이상의 로그만 저장
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # 콘솔 로그 레벨
    console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console_handler.setFormatter(console_formatter)
    logging.getLogger('').addHandler(console_handler)

    return logger

# 로그 설정 함수 호출
logger = setup_logging()

##### ORM 및 REDIS 설정 불러오기
# ORM
if app_env == 'LOCAL':
    rdb_user = config.get(app_env, 'RDB_USER')
    rdb_password = quote(config.get(app_env, 'RDB_PASSWORD'))
    rdb_host = config.get(app_env, 'RDB_HOST')
    rdb_port = config.get(app_env, 'RDB_PORT')
    rdb_name = config.get(app_env, 'RDB_NAME')
elif app_env == 'DEV':
    rdb_user = config.get(app_env, 'RDB_USER')
    rdb_password = config.get(app_env, 'RDB_PASSWORD')
    rdb_host = config.get(app_env, 'RDB_HOST')
    rdb_port = config.get(app_env, 'RDB_PORT')
    rdb_name = config.get(app_env, 'RDB_NAME')

# Redis 설정
if app_env == 'LOCAL':
    redis_host = config.get(app_env, 'REDIS_HOST')
    redis_port = config.get(app_env, 'REDIS_PORT')
else:
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')


##### 동기 ORM session 및 redis
#orm
engine = create_engine(f'postgresql+psycopg2://{rdb_user}:{rdb_password}@{rdb_host}:{rdb_port}/{rdb_name}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 동기 DB 세션 종속성
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


redis_client = Redis(host=redis_host, port=redis_port)

def get_redis():
    return redis_client

##### 비동기 ORM session
#orm
async_engine = create_async_engine(f'postgresql+asyncpg://{rdb_user}:{rdb_password}@{rdb_host}:{rdb_port}/{rdb_name}', echo=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

# 비동기 DB 세션 종속성
async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise

###### 계정 관련 비밀번호 해싱 및 JWT 설정
if app_env == 'LOCAL':
    secret_key = config.get(app_env, 'SECRET_KEY')
else:
    secret_key = os.getenv('SECRET_KEY')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 비밀번호 해싱
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증
def verify_password(plain_password: str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 세션 ID 생성 및 저장 함수
def create_session(user_sn: int, redis: Redis, expires_delta: timedelta = None):
    session_id = str(uuid.uuid4())
    session_expires = expires_delta.total_seconds() if expires_delta else 3600
    redis.set(session_id, user_sn, ex=int(session_expires))
    return session_id