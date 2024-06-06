!!! 트랜잭션 스크립트 패턴을 통해 작성 되었습니다. fast api의 기본 기능만을 사용하여 구현 되었습니다. <br> 
---------------------------

### About

Access 토큰 발행에 uuid4 사용하였다.

swagger, postman 사용하여 성공 실패 테스트 케이스별 api테스트 진행 하였다.

pytest 사용한 테스트 코드 작성하였다. (미완)

개발기(docker)와 로컬 실행환경에서의 설정 참조를 분리하였다.

의존성관련된 모듈과 공통적으로 재사용되는 모듈들을 common 디렉토리에 작성하였다.

api(엔드 포인트), router, crud(db operation), scheme(pydantic), model(sqlalchemy)로 디렉토리 구조를 나누었다.

<br>

### requirements.txt

annotated-types==0.7.0
anyio==4.4.0
asyncpg==0.29.0
bcrypt==4.1.3
certifi==2024.2.2
charset-normalizer==3.3.2
click==8.1.7
dnspython==2.6.1
ecdsa==0.19.0
email_validator==2.1.1
fastapi==0.111.0
fastapi-cli==0.0.4
h11==0.14.0
httpcore==1.0.5
httptools==0.6.1
httpx==0.27.0
idna==3.7
itsdangerous==2.2.0
Jinja2==3.1.4
markdown-it-py==3.0.0
MarkupSafe==2.1.5
mdurl==0.1.2
Naked==0.1.32
orjson==3.10.3
passlib==1.7.4
psycopg2==2.9.9
pyasn1==0.6.0
pycryptodome==3.20.0
pydantic==2.7.1
pydantic-extra-types==2.7.0
pydantic-settings==2.2.1
pydantic_core==2.18.2
Pygments==2.18.0
python-dotenv==1.0.1
python-jose==3.3.0
python-multipart==0.0.9
PyYAML==6.0.1
redis==5.0.4
requests==2.32.2
rich==13.7.1
rsa==4.9
shellescape==3.8.1
shellingham==1.5.4
six==1.16.0
sniffio==1.3.1
SQLAlchemy==2.0.30
starlette==0.37.2
typer==0.12.3
typing_extensions==4.12.0
ujson==5.10.0
urllib3==2.2.1
uvicorn==0.29.0
uvloop==0.19.0
watchfiles==0.22.0
websockets==12.0

<br>

### 디렉토리 트리

```
├── Dockerfile
├── README.md
├── api
│   ├── v1
│   │   ├── __pycache__
│   │   ├── boards.py
│   │   ├── posts.py
│   │   └── users.py
│   └── v2
├── common
│   ├── __pycache__
│   ├── config.ini
│   ├── dependencies.py
│   └── utils.py
├── crud
│   ├── __pycache__
│   ├── boards.py
│   ├── posts.py
│   └── users.py
├── docker-compose.yml
├── main.py
├── model
│   └── model.py
├── requirements.txt
├── router
│   └── router.py
├── scheme
│   ├── __pycache__
│   ├── boards.py
│   ├── common.py
│   ├── posts.py
│   └── users.py
├── test.db
└── tests
    ├── __pycache__
    ├── conftest.py
    ├── test_api
    │   ├── test_board.py
    │   ├── test_post.py
    │   └── test_user.py
    ├── test_common.py
    └── test_db
        └── test_queries
            └── test_tables.py
```

<br>

### 개발 기간

2024.05.27~2024.05.31

<br>

### 실행 방법(local)

```
pip install -r requirements.txt
```

```
uvicorn main:app
```

<br>

### 도커 이미지 생성

```
docker build -t [태그명] [dockerfile의 위치].
docker build -t v.2024.05.31 .
```
