Fast api 리팩토링 & 공부 !!

📍 references 
https://github.com/kokoavailable/fastapi-realworld-example-app/blob/master/app/core/settings/app.py

<br>

### 요구사항

#### 계정 API 서비스

- SingUp : 계정 정보(fullname, email, password) 를 입력 받아 계정을 생성합니다.
- Login : email, password 를 입력 받아 계정에 로그인하고, 해당 로그인 세션의 access token 을 반환합니다.
- Logout : 현재 로그인 세션을 로그아웃 합니다.

#### 게시판 API 서비스

- Create : name, public (boolean) 을 입력 받아 게시판을 생성합니다. name 은 unique 해야합니다. public 이 true 이면 전체 로그인 된 유저에게 공개, public 이 false 이면 생성자에게만 공개되는 게시판입니다.
- Update : 게시판 id, name, public 을 입력 받아 해당 게시판의 name, public 을 수정합니다. 타 유저가 생성한 게시판은 수정할 수 없습니다.
- Delete : 게시판 id 를 입력 받아 해당 게시판을 삭제합니다. 타 유저가 생성한 게시판은 삭제할 수 없습니다.
- Get: 게시판 id 를 입력 받아 게시판을 조회합니다. 본인이 생성하거나, 전체 공개된 게시판을 조회할 수 있습니다.
- List : 게시판 목록을 조회합니다. 본인이 생성하거나, 전체 공개된 게시판을 조회할 수 있습니다. 게시판 목록은 **해당 게시판에 작성된 게시글의 갯수** 순으로 정렬 가능해야 합니다.

<br>

#### 게시글 API 서비스

- Create : 게시판 id, title, content 를 입력 받아 게시글을 생성합니다. 본인이 조회할 수 있는 게시판의 id 만 사용이 가능합니다.
- Update : 게시글 id, title, content 을 입력 받아 해당 게시글의 title, content 를 수정합니다. 타 유저가 생성한 게시글은 수정할 수 없습니다.
- Delete : 게시글 id 를 입력 받아 해당 게시글을 삭제합니다. 타 유저가 생성한 게시글은 삭제할 수 없습니다.
- Get: 게시글 id 를 입력 받아 게시글을 조회합니다. 본인이 생성하거나, 전체 공개된 게시판의 게시글을 조회할 수 있습니다.
- List : 게시판 id 을 입력 받아 해당 게시판에 있는 게시글 목록을 조회합니다. 본인이 조회할 수 있는 게시판의 id 만 사용이 가능합니다.b

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

Access 토큰 발행에 uuid4 사용하였다.

swagger, postman 사용하여 성공 실패 테스트 케이스별 api테스트 진행 하였다.

pytest 사용한 테스트 코드 작성하였다. (미완)

개발기(docker)와 로컬 실행환경에서의 설정 참조를 분리하였다.

의존성관련된 모듈과 공통적으로 재사용되는 모듈들을 common 디렉토리에 작성하였다.

api(엔드 포인트), router, crud(db operation), scheme(pydantic), model(sqlalchemy)로 디렉토리 구조를 나누었다.

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

