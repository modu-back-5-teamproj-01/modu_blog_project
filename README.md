# modu_blog_project
모두의연구소 백엔드 5기 블로그 제작 팀 프로젝트

## 📌 목차
- [프로젝트 설명](#-프로젝트-설명)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [폴더 구조](#️-폴더-구조)
- [WBS](#-wbswork-breakdown-structure)
- [와이어프레임](#️-와이어프레임wireframe)
- [API 상세](#-api-상세)
- [ERD](#-erd)
- [설치 및 실행 방법](#-설치-및-실행-방법)
- [개발 담당](#-개발-담당)

## 📝 프로젝트 설명
FastAPI 기반의 개인 블로그 서비스로,
회원가입 및 로그인, 게시글 작성, 댓글, 태그 검색 기능 등을 제공하는 웹 애플리케이션입니다.


## 🚀 주요 기능
- **👤 사용자 (User) 관련 기능**

    - 회원가입 / 로그인 / 로그아웃
    - 비밀번호 해시 및 JWT 토큰 인증
    - 프로필(자기소개) 관리

- **📝 게시글 (Post) 관련 기능**

    - 게시글 작성 / 수정 / 삭제 / 조회
    - 태그 추가 및 태그별 검색
    - 게시글 목록 및 상세 보기

- **💬 댓글 (Comment) 관련 기능**

    - 댓글 작성 / 수정 / 삭제
    - 게시글별 댓글 목록 조회


## 🛠 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | FastAPI, Python, SQLAlchemy |
| Frontend | HTML, CSS, JavaScript |
| DataBase | SQLite |
| Development & Tools | Git, GitHub, Postman |


## 🗂️ 폴더 구조
```
📦 blog-project/
├─ 📂 back/                        # 백엔드 (FastAPI 서버)
│   ├─ 📂 app/
│   │   ├─ 🚀 main.py              # FastAPI 실행 진입점
│   │   ├─ 📂 core/
│   │   │   └─ ⚙️ database.py      # DB 연결 관리
│   │   ├─ 📂 models/              # SQLAlchemy 모델 정의
│   │   │   ├─ 📊 __init__.py
│   │   │   ├─ 📊 base.py
│   │   │   ├─ 📊 user.py
│   │   │   ├─ 📊 post.py
│   │   │   ├─ 📊 comment.py
│   │   │   ├─ 📊 session.py
│   │   │   ├─ 📊 tag.py
│   │   │   ├─ 📊 post_tag.py
│   │   │   └─ 📊 upload.py
│   │   ├─ 📂 schemas/             # Pydantic 스키마
│   │   │   ├─ 📐 user.py
│   │   │   ├─ 📐 session.py
│   │   │   ├─ 📐 post.py
│   │   │   ├─ 📐 comment.py
│   │   │   ├─ 📐 tag.py
│   │   │   └─ 📐 upload.py
│   │   ├─ 📂 utils/               # 여러 유틸 함수들
│   │   │   └─ 🛠️ auth_utils.py
│   │   └─ 📂 routers/             # API 라우터 모듈
│   │       ├─ 🔗 auth.py
│   │       ├─ 🔗 blog.py
│   │       └─ 🔗 comment.py
│   └─ 📂 tests/
├─ 📂 front/                       # 프론트엔드 파트 폴더
│   ├─ 🌐 index.html                 # 로그인 화면
│   ├─ 🌐 signup.html                # 회원가입 화면
│   ├─ 🌐 main.html                  # 블로그 메인 화면
│   ├─ 🌐 post.html                  # 게시글 화면 (상세보기)
│   ├─ 🌐 post_create.html           # 게시글 작성 화면
│   ├─ 🌐 post_edit.html             # 게시글 수정 화면
│   ├─ 🌐 profile.html               # 나의 프로필 화면
│   ├─ 🌐 profile_edit.html          # 프로필 변경 화면
│   ├─ 🌐 password_change.html       # 비밀번호 변경 화면
│   ├─ 🌐 tag_search.html            # 태그 검색 결과 화면
│   ├─ 📂 css/
│   │   └─ 🎨 style.css              # 공용 스타일
│   │   
│   └─ 📂 js/
│       ├─ 📝 auth.js                # 로그인, 회원가입, 토큰 처리
│       ├─ 📝 main.js                # 블로그 메인 화면 관련 JS
│       ├─ 📝 post.js                # 게시글 화면 관련 JS (댓글, 대댓글)
│       ├─ 📝 post_create.js         # 게시글 작성 화면 JS
│       ├─ 📝 post_edit.js           # 게시글 수정 화면 JS
│       ├─ 📝 profile.js             # 프로필 화면 JS
│       ├─ 📝 profile_edit.js        # 프로필 변경 화면 JS
│       ├─ 📝 password_change.js     # 비밀번호 변경 화면 JS
│       └─ 📝 tag_search.js          # 태그 검색 결과 화면 JS
│
├─ 📂 docs/                        # 문서(md 파일 등) 저장
├─ 📂 static/
│   └─ 📂 images/                  # 이미지 (문서/웹 리소스 공용)
├─ 📄 requirements.txt             # Python 의존성 (FastAPI, SQLAlchemy 등)
├─ 📄 .gitignore                   # git에서 제외할 파일/폴더 설정 (venv, __pycache__, .env 등)
├─ 📄 .env.example                 # 환경 변수 예시 파일 (DATABASE_URL, SECRET_KEY)
└─ 📄 README.md                    # 프로젝트 개요 및 실행 방법 문서

```

## 📊 WBS(Work Breakdown Structure)
```mermaid
gantt
    title 블로그 프로젝트 개발 일정
    dateFormat  YYYY-MM-DD
    section 1단계: JWT 인증 및 회원가입
    회원가입 API           :a1, 2025-10-02, 1d
    로그인 API            :a2, 2025-10-02, 1d
    JWT 토큰 검증          :a3, 2025-10-02, 1d
    1단계 테스트            :a4, 2025-10-02, 1d

    section 2단계: 메인페이지 & 블로그 CRUD
    게시글 모델 및 DB       :a5, 2025-10-02, 2d
    게시글 작성 API        :a6, 2025-10-03, 2d
    게시글 목록 및 검색 API :a7, 2025-10-03, 2d
    게시글 태그조회 API     :a8, 2025-10-03, 2d
    게시글 상세보기 API     :a9, 2025-10-03, 2d
    게시글 수정 API        :a10, 2025-10-03, 2d
    게시글 삭제 API        :a11, 2025-10-03, 2d
    2단계 테스트           :a12, 2025-10-03, 6d

    section 3단계: 추가 기능 및 배포
    회원 관련 추가 API      :a13, 2025-10-08, 2d
    댓글 API               :a14, 2025-10-08, 3d
    (선택) 파일 업로드       :a15, 2025-10-08, 2d
    (선택) 부가기능          :a16, 2025-10-08, 3d
    (선택) 클라우드 배포     :a17, 2025-10-08, 4d
    (선택) AI 기능 통합      :a18, 2025-10-08, 4d
    3단계 테스트             :a19, 2025-10-08, 5d
    최종 테스트 및 검증       :a20, 2025-10-13, 3d

```

## 🖼️ 와이어프레임(Wireframe)

![Image](https://github.com/user-attachments/assets/9c7b18e8-3199-45d8-a7dc-53f50d4495f9)

## 📌 API 상세
| 구분                  | Method | Endpoint                                        | 기능 설명                  | JWT 인증 필요  |
| ------------------- | ------ | ----------------------------------------------- | ---------------------- | ------ |
| **Auth (회원 관련)**    | POST   | `/auth/register`                                | 회원가입                   | ❌      |
|                     | POST   | `/auth/login`                                   | 로그인, JWT 발급            | ❌      |
|                     | PUT    | `/auth/password`                                | 비밀번호 변경                | ✅      |
|                     | PUT    | `/auth/profile`                                 | 프로필 수정 (닉네임 등)         | ✅      |
|                     | GET    | `/auth/me`                                      | 내 정보 조회                | ✅      |
|                     | POST    | `/auth/logout`                                      | 로그아웃                | ✅      |
| **Blog (게시글)**      | POST   | `/blog`                                         | 게시글 작성                 | ✅      |
|                     | GET    | `/blog`                                         | 게시글 목록 조회 (검색, 정렬 지원)  | ❌      |
|                     | GET    | `/blog/tag/{tag_name}`                                   | 특정 태그의 게시글 목록 조회       | ❌      |
|                     | GET    | `/blog/{post_id}`                               | 게시글 상세 조회              | ❌      |
|                     | PUT    | `/blog/{post_id}`                               | 게시글 수정 (작성자 본인만 가능)    | ✅      |
|                     | DELETE | `/blog/{post_id}`                               | 게시글 삭제 (작성자 본인만 가능)    | ✅      |
| **Comment (댓글)**    | POST   | `/blog/{post_id}/comments`                      | 댓글 작성                  | ✅      |
|                     | GET    | `/blog/{post_id}/comments`                      | 댓글 목록 조회               | ❌      |
|                     | PUT    | `/blog/{post_id}/comments/{comment_id}`         | 댓글 수정 (작성자 본인만 가능)     | ✅      |
|                     | DELETE | `/blog/{post_id}/comments/{comment_id}`         | 댓글 삭제 (작성자 본인만 가능)     | ✅      |
|                     | POST   | `/blog/{post_id}/comments/{comment_id}/replies` | 대댓글 작성                 | ✅      |



## 📝 ERD
![ERD](./static/images/blog_project_diagram.png)


## ⚡ 설치 및 실행 방법

### 1️⃣ 레포지토리 클론
```bash
git clone https://github.com/modu-back-5-teamproj-01/modu_blog_project.git .
```

### 2️⃣ 가상환경 생성 및 활성화

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 4️⃣ 환경 변수 설정
`.env.example` 파일을 참고하여 `.env` 파일을 생성하고 환경 변수를 설정하세요.

```bash
cp .env.example .env
```

### 5️⃣ 서버 실행
```bash
cd back
uvicorn app.main:app --reload
```

### 6️⃣ 브라우저 접속

`http://127.0.0.1:8000`에 접속하면, 로그인 화면을 확인할 수 있습니다.


## 👥 개발 담당
| 이름 | 주요 담당 |
|------|-------------|
| 천수겸 | API 설계, DB 연동, JWT 인증 구현, HTML/CSS/JS 구성, Pydantic 스키마 설계 |
| 김경환 | SQLAlchemy 모델 설계, API 설계, 테스트 및 QA |