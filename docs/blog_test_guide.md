
# 🧪 Blog API 테스트 가이드

## 📌 1. 개요
이 문서는 `/blog` 라우터의 주요 API를 Postman 혹은 curl을 통해 테스트하기 위한 가이드입니다.  
JWT 인증이 필요한 엔드포인트와, 테스트에 필요한 Header / Body 형식을 함께 제공합니다.

---

## ⚙️ 2. 사전 준비

### (1) Base URL
```
http://127.0.0.1:8000
```

### (2) 공통 Header
| Key | Value | 설명 |
|-----|--------|------|
| `Content-Type` | `application/json` | JSON 요청 필수 |
| `Authorization` | `Bearer <ACCESS_TOKEN>` | 로그인 후 발급된 JWT 토큰 |

> ⚠️ `Authorization`은 로그인(`/auth/login`) 후 받은 토큰으로 교체해야 합니다.

---

## 🧾 3. API별 테스트 시나리오

### ✅ (1) 게시글 생성 – `POST /blog/`
**설명:** 새 게시글을 작성합니다.  
**인증 필요:** ✅ Yes

#### Body 예시
```json
{
  "title": "두 번째 테스트 글",
  "content": "FastAPI 블로그 글 작성 테스트 중입니다.",
  "summary": "테스트용 요약입니다.",
  "tags": ["fastapi", "backend"]
}
```

#### 예상 Response
```json
{
  "id": 1,
  "title": "두 번째 테스트 글",
  "content": "FastAPI 블로그 글 작성 테스트 중입니다.",
  "summary": "테스트용 요약입니다.",
  "author": {
    "id": 1,
    "username": "test_user"
  },
  "tags": [
    {"id": 1, "name": "fastapi"},
    {"id": 2, "name": "backend"}
  ],
  "view_count": 0,
  "created_at": "2025-10-10T10:30:00",
  "updated_at": "2025-10-10T10:30:00"
}
```

---

### 📚 (2) 게시글 목록 조회 – `GET /blog/`
**설명:** 전체 게시글 목록을 조회합니다.  
**인증 필요:** ❌ No

#### Query Parameters (선택)
| Key | Type | Default | 설명 |
|-----|------|----------|------|
| `skip` | int | 0 | 시작 인덱스 |
| `limit` | int | 10 | 최대 조회 수 |

#### 예상 Response
```json
[
  {
    "id": 1,
    "title": "두 번째 테스트 글",
    "summary": "테스트용 요약입니다.",
    "author": {"id": 1, "username": "test_user"},
    "view_count": 0,
    "created_at": "2025-10-10T10:30:00"
  }
]
```

---

### 🔍 (3) 단일 게시글 조회 – `GET /blog/{post_id}`
**설명:** 특정 게시글을 ID로 조회합니다.  
**인증 필요:** ❌ No

#### 예상 Response
```json
{
  "id": 1,
  "title": "두 번째 테스트 글",
  "content": "FastAPI 블로그 글 작성 테스트 중입니다.",
  "author": {"id": 1, "username": "test_user"},
  "tags": [{"id": 1, "name": "fastapi"}],
  "view_count": 1
}
```

---

### ✏️ (4) 게시글 수정 – `PUT /blog/{post_id}`
**설명:** 사용자가 작성한 게시글을 수정합니다.  
**인증 필요:** ✅ Yes

#### Body 예시
```json
{
  "title": "수정된 테스트 글",
  "content": "수정된 본문 내용입니다.",
  "summary": "요약도 수정함",
  "tags": ["backend", "api"]
}
```

#### 예상 Response
수정된 게시글 객체가 반환됩니다.

---

### ❌ (5) 게시글 삭제 – `DELETE /blog/{post_id}`
**설명:** 사용자가 작성한 게시글을 삭제합니다.  
**인증 필요:** ✅ Yes

#### 예상 Response
```json
{"message": "Post deleted successfully"}
```

---

### 🏷️ (6) 태그 목록 조회 – `GET /blog/tag/`
**설명:** 현재 등록된 모든 태그를 조회합니다.  
**인증 필요:** ❌ No

#### 예상 Response
```json
[
  {"id": 1, "name": "fastapi"},
  {"id": 2, "name": "backend"}
]
```

---

## 🧩 4. 테스트 팁
- Postman에서 **환경 변수**를 이용해 `{{ACCESS_TOKEN}}` 변수를 사용하면 편리합니다.  
- `Authorization` 헤더는 로그인 후 응답에서 `"access_token"`을 복사해 붙여넣습니다.  
- 테스트 순서 추천:  
  1️⃣ `/auth/register` → 2️⃣ `/auth/login` → 3️⃣ `/blog/` → 4️⃣ `/blog/{id}` → 5️⃣ `/blog/{id}` 수정/삭제

---
