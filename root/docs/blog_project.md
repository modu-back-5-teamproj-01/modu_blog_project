# 🎯 FastAPI 블로그 프로젝트: 2주 개발 액션 플랜

제공된 요구사항과 도메인 분업 계획을 바탕으로, 2주간의 개발 일정을 **일일 행동 계획** 형태로 정리했습니다.

---

## 🚀 Week 1: 기초 세팅 및 핵심 기능 구현 (Day 1 ~ Day 7)

### 🗓️ Day 2 (오늘): 시스템/데이터 기초 설정 및 핵심 인증 구현
**오늘의 목표**: FastAPI의 뼈대를 세우고 기본 인증 기능을 작동시키기

#### 👨‍💻 Person A: 인증 (Auth) 및 보안 기초
- **오전 (3시간)**
  1. DB 연결 로직 (`database.py`) 작성
  2. 사용자 모델 (`models/user.py`) 및 스키마 (`schemas/user.py`) 설계
  3. 비밀번호 해싱 및 JWT 토큰 생성 유틸리티 (`utils/security.py`) 작성
- **오후 (4시간)**
  1. 회원가입 API (`POST /auth/register`) 구현
  2. 로그인 API (`POST /auth/login`) 구현 및 JWT 토큰 반환 로직 적용
  3. 회원가입/로그인 기능 End-to-End 테스트 완료

#### 👨‍💻 Person B: 데이터 모델링 및 시스템 의존성
- **오전 (3시간)**
  1. 게시글 모델 (`models/post.py`) 및 스키마 (`schemas/post.py`) 설계
  2. 댓글 모델 (`models/comment.py`) 및 스키마 (`schemas/comment.py`) 설계
- **오후 (4시간)**
  1. JWT 토큰 검증 의존성 함수 (`utils/dependencies.py - get_current_user`) 구현
  2. 정적 파일 서빙을 위한 `static` 폴더 구조 생성 및 `main.py`에 StaticFiles 마운트

---

### 🗓️ Day 3 (수): 인증 완성 및 게시글/댓글 초기 CRUD
🎯 **마일스톤: 인증 시스템 완성!**

#### 👨‍💻 Person A
- **오전 (3시간)**
  1. 인증 라우터 (`routers/auth.py`) 완성: 내 정보 조회, 비밀번호 변경, 프로필 수정 API
  2. 인증 관련 모든 API 기능 및 권한 체크 테스트
- **오후 (4시간)**
  1. 게시글 작성 API (`POST /blog`) 구현 및 작성자 자동 설정 로직 적용

#### 👨‍💻 Person B
- **오전 (3시간)**
  1. 게시글 목록 API (`GET /blog`) 구현 및 페이지네이션 로직 적용
- **오후 (4시간)**
  1. 댓글 작성 API (`POST /blog/{post_id}/comments`) 구현
  2. 댓글 목록 조회 API (`GET /blog/{post_id}/comments`) 구현 및 계층형 댓글 구조 기초 설계

---

### 🗓️ Day 4 (목): 핵심 CRUD 및 댓글 구조 완성
🎯 **마일스톤: 기본 CRUD 완성!**

#### 👨‍💻 Person A
- **오전 (3시간)**
  1. 게시글 상세 API (`GET /blog/{post_id}`) 구현 및 조회수 증가 로직 추가
  2. 게시글 수정 API (`PUT /blog/{post_id}`) 구현
- **오후 (4시간)**
  1. 게시글 삭제 API (`DELETE /blog/{post_id}`) 구현
  2. 작성자 본인만 수정/삭제 가능한 권한 체크 로직 검증 및 테스트

#### 👨‍💻 Person B
- **오전 (3시간)**
  1. 대댓글 작성 API 구현 및 계층형 댓글 조회 로직 최종 완성
- **오후 (4시간)**
  1. 댓글 수정/삭제 API (`PUT/DELETE /comments/{comment_id}`) 구현
  2. 댓글 작성자 권한 체크 로직 적용 및 테스트

---

### 🗓️ Day 5 (금): 검색 기능 및 이미지 업로드
🎯 **마일스톤: 필수 기능 90% 완성!**

#### 👨‍💻 Person A
- **오전 (3시간)**
  1. 게시글 검색 (search), 태그 필터링 (tag), 정렬 (sort) 기능 구현
- **오후 (4시간)**
  1. 게시글 도메인 전체 검색 기능 테스트 및 버그 수정
  2. Person A 담당 코드 전반 리팩토링 및 정리

#### 👨‍💻 Person B
- **오전 (3시간)**
  1. 업로드 라우터 (`routers/upload.py`) 작성 및 이미지 업로드 API 구현
- **오후 (4시간)**
  1. 파일 저장 로직 완성 (로컬 또는 S3) 및 이미지 업로드 테스트
  2. 파일 유효성 검증 및 관련 에러 처리 로직 강화

---

### 🗓️ Day 6-7 (주말): 통합 테스트 및 최종 점검
✅ 전체 API 통합 테스트, Postman 컬렉션 작성, 버그 발견 및 수정, 코드 리뷰, `README.md` 작성 시작  
⚡ 선택적: Week 2 작업 미리 시작 or 충분한 휴식

---

## 🌟 Week 2: 고도화 및 배포 완성 (Day 8 ~ Day 14)

### 🗓️ Day 8 (월): 추가 기능 시작 (AI, 국제화)
- **Person A**
  - 오전 (3시간) ✅ 국제화 (i18n) 구현 및 `Accept-Language` 헤더 처리
  - 오후 (4시간) ✅ 에러 메시지 다국어 적용 및 API 문서화 개선 (`/docs`)
- **Person B**
  - 종일 (7시간) ✅ OpenAI API 키 설정 및 `POST /ai/autocomplete` 구현

---

### 🗓️ Day 9 (화): AI 기능 완성 및 코드 품질 강화
- **Person A** (6시간) ✅ 전체 코드 리팩토링, 에러 처리 강화, 로깅, 주석 작성
- **Person B** (6시간) ✅ `POST /ai/summarize`, `POST /ai/tags` 구현 및 테스트

---

### 🗓️ Day 10 (수): 성능 최적화 + 보안 적용
- **Person A**
  - 오전 (3시간) ✅ DB 최적화 (인덱스, 쿼리 개선, N+1 해결)
  - 오후 (3시간) ✅ CORS, 보안 헤더, Rate Limiting
- **Person B**
  - 오전 (3시간) ✅ 입력 유효성 강화, SQL Injection 방어, XSS 방어
  - 오후 (3시간) ✅ 업로드 보안 강화 (용량 제한, 악성 파일 검증)

---

### 🗓️ Day 11 (목): 테스트 코드 작성
- **Person A** (6시간) ✅ pytest 설정, 인증/게시글 테스트 코드 작성
- **Person B** (6시간) ✅ 댓글/업로드/AI 테스트 코드 작성 및 통합 테스트

---

### 🗓️ Day 12 (금): 문서화 및 배포 준비 (Docker 포함)
- **함께 오전 (3시간)** ✅ `README.md` 작성 (소개, 설치, 실행 방법, API, env 설명)
- **Person A 오후 (3시간)** ✅ Dockerfile, `.dockerignore` 작성 및 빌드 테스트

---

### 🗓️ Day 13-14 (주말): 최종 배포 및 발표 준비
- ✅ Docker 이미지 배포 및 클라우드 환경 테스트 (AWS/GCP)
- ✅ 배포된 환경에서 최종 기능 테스트 및 버그 수정
- ✅ 발표 자료 준비, 데모 시나리오 작성, 프로젝트 회고

---

## 🎯 최종 마일스톤
**배포 완료 및 프로젝트 완성!**
