# 블로그 프로젝트 API 명세서

## 📋 프로젝트 개요
- **프로젝트명**: (Modu Blog)
- **Base URL**: `http://127.0.0.1:8000`
- **버전**: 1.0.0
- **프레임워크**: FastAPI
- **데이터베이스**: SQLite
- **인증 방식**: JWT (JSON Web Token)

---

## 🔑 API 엔드포인트 요약표

| HTTP 메서드 | URL | 기능 | 설명 | 인증 필요 |
|------------|-----|------|------|----------|
| **POST** | `/api/auth/signup` | **회원가입** | 새로운 사용자 계정을 생성합니다. 사용자명, 이메일, 비밀번호를 받아 데이터베이스에 저장하고 비밀번호는 암호화하여 보관합니다. | ❌ |
| **POST** | `/api/auth/login` | **로그인** | 사용자 인증을 처리하고 JWT 액세스 토큰을 발급합니다. 발급받은 토큰으로 다른 API를 사용할 수 있습니다. | ❌ |
| **GET** | `/api/posts` | **게시글 목록** | 전체 게시글을 최신순으로 조회합니다. 페이지네이션(skip, limit)과 검색(search) 기능을 지원하여 원하는 게시글을 찾을 수 있습니다. | ❌ |
| **POST** | `/api/posts` | **게시글 작성** | 로그인한 사용자가 새로운 게시글을 작성합니다. 제목과 내용을 입력받아 데이터베이스에 저장하며, 작성자 정보가 자동으로 연결됩니다. | ✅ |
| **GET** | `/api/posts/{post_id}` | **게시글 상세** | 특정 게시글의 전체 내용을 조회합니다. 게시글 정보와 함께 작성자 정보도 함께 반환됩니다. | ❌ |
| **PUT** | `/api/posts/{post_id}` | **게시글 수정** | 기존 게시글의 내용을 수정합니다. 작성자 본인만 수정할 수 있으며, 제목과 내용을 새로운 값으로 업데이트합니다. | ✅ |
| **DELETE** | `/api/posts/{post_id}` | **게시글 삭제** | 게시글을 삭제합니다. 작성자 본인만 삭제할 수 있으며, 삭제된 게시글은 복구할 수 없습니다. | ✅ |
| **GET** | `/api/posts/search` | **게시글 검색** | 검색 키워드로 게시글을 찾습니다. 제목이나 내용에 검색어가 포함된 모든 게시글을 반환합니다. | ❌ |
| **POST** | `/api/posts/{post_id}/comments` | **댓글 작성** | 특정 게시글에 댓글을 작성합니다. 로그인한 사용자만 댓글을 달 수 있으며, 작성자 정보가 자동으로 저장됩니다. | ✅ |
| **DELETE** | `/api/comments/{comment_id}` | **댓글 삭제** | 작성한 댓글을 삭제합니다. 댓글 작성자 본인만 삭제할 수 있습니다. | ✅ |

---

## 📚 API 상세 명세

### 1️⃣ 인증 (Authentication)

#### 1.1 회원가입
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | POST |
| **URL** | `/api/auth/signup` |
| **기능** | 회원가입 |
| **설명** | 새로운 사용자 계정을 생성합니다. 입력받은 비밀번호는 bcrypt로 암호화되어 저장되며, 중복된 사용자명이나 이메일은 거부됩니다. |
| **인증 필요** | ❌ |

**요청 본문**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

**응답 (201 Created)**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2025-10-02T10:00:00.000Z"
}
```

**에러 응답**
| 상태 코드 | 설명 |
|-----------|------|
| 400 | 이미 존재하는 사용자명 또는 이메일 |
| 422 | 유효하지 않은 입력 데이터 |

---

#### 1.2 로그인
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | POST |
| **URL** | `/api/auth/login` |
| **기능** | 로그인 및 토큰 발급 |
| **설명** | 사용자명과 비밀번호로 인증 후 JWT 액세스 토큰을 발급합니다. 발급된 토큰은 30분간 유효하며, 이후 API 요청 시 인증 헤더에 포함하여 사용합니다. |
| **인증 필요** | ❌ |

**요청 본문 (Form Data)**
```
username=testuser
password=password123
```

**응답 (200 OK)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**에러 응답**
| 상태 코드 | 설명 |
|-----------|------|
| 401 | 잘못된 사용자명 또는 비밀번호 |

---

### 2️⃣ 게시글 (Posts)

#### 2.1 게시글 목록 조회
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | GET |
| **URL** | `/api/posts` |
| **기능** | 게시글 목록 조회 (페이지네이션 & 검색) |
| **설명** | 전체 게시글을 최신순으로 조회합니다. `skip`과 `limit`으로 페이지를 나누고, `search` 파라미터로 제목/내용 검색이 가능합니다. 각 게시글은 작성자 정보와 함께 반환됩니다. |
| **인증 필요** | ❌ |

**쿼리 파라미터**
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|--------|------|
| skip | integer | ❌ | 0 | 건너뛸 게시글 수 |
| limit | integer | ❌ | 10 | 조회할 게시글 수 (최대 100) |
| search | string | ❌ | null | 검색 키워드 (제목, 내용) |

**요청 예시**
```
GET /api/posts?skip=0&limit=10&search=fastapi
```

**응답 (200 OK)**
```json
[
  {
    "id": 1,
    "title": "FastAPI 시작하기",
    "content": "FastAPI는 빠르고 현대적인 웹 프레임워크입니다...",
    "author_id": 1,
    "author": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com"
    },
    "created_at": "2025-10-02T11:00:00.000Z",
    "updated_at": "2025-10-02T11:00:00.000Z"
  }
]
```

---

#### 2.2 게시글 작성
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | POST |
| **URL** | `/api/posts` |
| **기능** | 게시글 작성 |
| **설명** | 로그인한 사용자가 새로운 게시글을 작성합니다. 제목(title)과 내용(content)을 입력받아 저장하며, 작성자 ID는 JWT 토큰에서 자동으로 추출됩니다. 작성 시간과 수정 시간이 자동으로 기록됩니다. |
| **인증 필요** | ✅ (Bearer Token) |

**요청 헤더**
```
Authorization: Bearer {access_token}
```

**요청 본문**
```json
{
  "title": "FastAPI 시작하기",
  "content": "FastAPI는 빠르고 현대적인 웹 프레임워크입니다..."
}
```

**응답 (201 Created)**
```json
{
  "id": 1,
  "title": "FastAPI 시작하기",
  "content": "FastAPI는 빠르고 현대적인 웹 프레임워크입니다...",
  "author_id": 1,
  "created_at": "2025-10-02T11:00:00.000Z",
  "updated_at": "2025-10-02T11:00:00.000Z"
}
```

**에러 응답**
| 상태 코드 | 설명 |
|-----------|------|
| 401 | 인증 필요 |
| 422 | 유효하지 않은 입력 |

---

#### 2.3 게시글 상세 조회
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | GET |
| **URL** | `/api/posts/{post_id}` |
| **기능** | 게시글 상세 정보 조회 |
| **설명** | 특정 게시글의 전체 내용을 조회합니다. 게시글 ID를 통해 해당 게시글의 제목, 내용, 작성자 정보, 작성/수정 시간 등 모든 정보를 반환합니다. 존재하지 않는 게시글 조회 시 404 에러를 반환합니다. |
| **인증 필요** | ❌ |

**경로 파라미터**
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| post_id | integer | ✅ | 게시글 ID |

**응답 (200 OK)**
```json
{
  "id": 1,
  "title": "FastAPI 시작하기",
  "content": "FastAPI는 빠르고 현대적인 웹 프레임워크입니다...",
  "author_id": 1,
  "author": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "created_at": "2025-10-02T11:00:00.000Z",
  "updated_at": "2025-10-02T11:00:00.000Z"
}
```

**에러 응답**
| 상태 코드 | 설명 |
|-----------|------|
| 404 | 게시글을 찾을 수 없음 |

---

#### 2.4 게시글 수정
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | PUT |
| **URL** | `/api/posts/{post_id}` |
| **기능** | 게시글 수정 (작성자만) |
| **설명** | 기존 게시글의 제목과 내용을 수정합니다. JWT 토큰으로 로그인한 사용자가 해당 게시글의 작성자인지 확인 후, 일치하면 수정을 허용합니다. 수정 시간(updated_at)이 자동으로 갱신됩니다. |
| **인증 필요** | ✅ (Bearer Token) |

**요청 헤더**
```
Authorization: Bearer {access_token}
```

**경로 파라미터**
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| post_id | integer | ✅ | 게시글 ID |

**요청 본문**
```json
{
  "title": "FastAPI 시작하기 (수정)",
  "content": "FastAPI는 Python 3.7+ 기반의 현대적인 웹 프레임워크입니다..."
}
```

**응답 (200 OK)**
```json
{
  "id": 1,
  "title": "FastAPI 시작하기 (수정)",
  "content": "FastAPI는 Python 3.7+ 기반의 현대적인 웹 프레임워크입니다...",
  "author_id": 1,
  "created_at": "2025-10-02T11:00:00.000Z",
  "updated_at": "2025-10-02T12:00:00.000Z"
}
```

**에러 응답**
| 상태 코드 | 설명 |
|-----------|------|
| 401 | 인증 필요 |
| 403 | 권한 없음 (작성자만 수정 가능) |
| 404 | 게시글을 찾을 수 없음 |

---

#### 2.5 게시글 삭제
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | DELETE |
| **URL** | `/api/posts/{post_id}` |
| **설명** | 특정 게시글을 삭제합니다. 작성자 본인만 가능합니다 |
| **인증 필요** | ✅ (Bearer Token) |

**요청 헤더**
```
Authorization: Bearer {access_token}
```

**경로 파라미터**
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| post_id | integer | ✅ | 게시글 ID |

**응답 (204 No Content)**
```
(응답 본문 없음)
```

**에러 응답**
| 상태 코드 | 설명 |
|-----------|------|
| 401 | 인증 필요 |
| 403 | 권한 없음 (작성자만 삭제 가능) |
| 404 | 게시글을 찾을 수 없음 |

---

#### 2.6 게시글 검색
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | GET |
| **URL** | `/api/posts/search` |
| **설명** | 제목 또는 내용에 검색어가 포함된 게시글을 조회합니다 |
| **인증 필요** | ❌ |

**쿼리 파라미터**
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| q | string | ✅ | 검색 키워드 |
| skip | integer | ❌ | 건너뛸 게시글 수 (기본값: 0) |
| limit | integer | ❌ | 조회할 게시글 수 (기본값: 10) |

**요청 예시**
```
GET /api/posts/search?q=fastapi&skip=0&limit=10
```

**응답 (200 OK)**
```json
[
  {
    "id": 1,
    "title": "FastAPI 시작하기",
    "content": "FastAPI는 빠르고 현대적인 웹 프레임워크입니다...",
    "author_id": 1,
    "author": {
      "id": 1,
      "username": "testuser"
    },
    "created_at": "2025-10-02T11:00:00.000Z"
  }
]
```

---

### 3️⃣ 댓글 (Comments)

#### 3.1 댓글 작성
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | POST |
| **URL** | `/api/posts/{post_id}/comments` |
| **설명** | 특정 게시글에 댓글을 작성합니다 |
| **인증 필요** | ✅ (Bearer Token) |

**요청 헤더**
```
Authorization: Bearer {access_token}
```

**경로 파라미터**
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| post_id | integer | ✅ | 게시글 ID |

**요청 본문**
```json
{
  "content": "유용한 정보 감사합니다!"
}
```

**응답 (201 Created)**
```json
{
  "id": 1,
  "content": "유용한 정보 감사합니다!",
  "post_id": 1,
  "author_id": 2,
  "created_at": "2025-10-02T12:00:00.000Z",
  "updated_at": "2025-10-02T12:00:00.000Z"
}
```

**에러 응답**
| 상태 코드 | 설명 |
|-----------|------|
| 401 | 인증 필요 |
| 404 | 게시글을 찾을 수 없음 |
| 422 | 유효하지 않은 입력 |

---

#### 3.2 댓글 삭제
| 항목 | 내용 |
|------|------|
| **HTTP 메서드** | DELETE |
| **URL** | `/api/comments/{comment_id}` |
| **설명** | 특정 댓글을 삭제합니다. 작성자 본인만 가능합니다 |
| **인증 필요** | ✅ (Bearer Token) |

**요청 헤더**
```
Authorization: Bearer {access_token}
```

**경로 파라미터**
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| comment_id | integer | ✅ | 댓글 ID |

**응답 (204 No Content)**
```
(응답 본문 없음)
```

**에러 응답**
| 상태 코드 | 설명 |
|-----------|------|
| 401 | 인증 필요 |
| 403 | 권한 없음 (작성자만 삭제 가능) |
| 404 | 댓글을 찾을 수 없음 |

---

## 📊 데이터 모델

### User (사용자)
| 필드 | 타입 | 설명 |
|------|------|------|
| id | integer | 사용자 ID (PK) |
| username | string | 사용자명 (unique, 3-50자) |
| email | string | 이메일 (unique) |
| created_at | datetime | 생성 일시 |

### Post (게시글)
| 필드 | 타입 | 설명 |
|------|------|------|
| id | integer | 게시글 ID (PK) |
| title | string | 제목 (1-200자) |
| content | string | 내용 (1-10000자) |
| author_id | integer | 작성자 ID (FK) |
| created_at | datetime | 생성 일시 |
| updated_at | datetime | 수정 일시 |

### Comment (댓글)
| 필드 | 타입 | 설명 |
|------|------|------|
| id | integer | 댓글 ID (PK) |
| content | string | 내용 (1-500자) |
| post_id | integer | 게시글 ID (FK) |
| author_id | integer | 작성자 ID (FK) |
| created_at | datetime | 생성 일시 |
| updated_at | datetime | 수정 일시 |

---

## ⚠️ HTTP 상태 코드

| 코드 | 의미 | 설명 |
|------|------|------|
| 200 | OK | 요청 성공 |
| 201 | Created | 리소스 생성 성공 |
| 204 | No Content | 요청 성공, 응답 본문 없음 |
| 400 | Bad Request | 잘못된 요청 |
| 401 | Unauthorized | 인증 필요 |
| 403 | Forbidden | 권한 없음 |
| 404 | Not Found | 리소스를 찾을 수 없음 |
| 422 | Unprocessable Entity | 유효하지 않은 입력 |
| 500 | Internal Server Error | 서버 내부 오류 |

---

## 🔄 인증 플로우

```
1. 회원가입 (POST /api/auth/signup)
   ↓
2. 로그인 (POST /api/auth/login) → JWT 토큰 발급
   ↓
3. 인증 필요 API 호출 (Authorization: Bearer {token})
   ↓
4. 토큰 만료 시 재로그인 (30분 후)
```

---

## 💻 cURL 사용 예시

### 회원가입
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

### 로그인
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### 게시글 목록 조회
```bash
curl -X GET "http://127.0.0.1:8000/api/posts?skip=0&limit=10"
```

### 게시글 작성
```bash
curl -X POST "http://127.0.0.1:8000/api/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"Content here"}'
```

### 게시글 검색
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/search?q=fastapi"
```

### 댓글 작성
```bash
curl -X POST "http://127.0.0.1:8000/api/posts/1/comments" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Great post!"}'
```

---