# 🎯 FastAPI 블로그 프로젝트 - 효율적인 분업 전략

> **핵심 철학**: 도메인 소유권 명확화 + 의존성 최소화 + 병렬 작업 극대화

---

## 📋 목차
1. [분업 전략 개요](#분업-전략-개요)
2. [Phase별 상세 계획](#phase별-상세-계획)
3. [역할별 책임 범위](#역할별-책임-범위)
4. [일정표](#일정표)

---

## 🤔 분업 전략 개요

### 1️⃣ 수직 분할 (Vertical Slicing) 방식
**특징**: 도메인별 완전한 소유권

| 담당자 | 도메인 | 범위 |
|--------|--------|------|
| **Person A** | 🔐 인증(Auth) + 사용자(User) | 회원가입/로그인/JWT<br>프로필 관리<br>권한 체크 로직<br>관련 테스트 |
| **Person B** | 📝 게시글(Post) + 댓글(Comment) | CRUD 전체<br>검색/필터링<br>계층형 댓글<br>관련 테스트 |

**장점**: 
- ✅ 도메인 전문성 확보
- ✅ 코드 충돌 최소화
- ✅ 책임 소재 명확

---

### 2️⃣ 수평 분할 (Horizontal Slicing) 방식
**특징**: 레이어별 전문화

| 담당자 | 레이어 | 범위 |
|--------|--------|------|
| **Person A** | 🏗️ Backend Core | Models (전체)<br>Database 설계<br>API 라우터<br>비즈니스 로직 |
| **Person B** | 🔧 Infrastructure & Quality | 파일 업로드<br>AI 기능<br>테스트 코드<br>보안/성능 최적화 |

**장점**:
- ✅ 전문성에 따른 분업
- ✅ 레이어별 일관성 확보

---

### 3️⃣ 추천 방식: 혼합형 🎯

```
Week 1: 수직 분할 (핵심 기능 구축)
├─ Person A: Auth 도메인 완성 (Day 1-3)
└─ Person B: Blog/Comment 도메인 완성 (Day 1-5)

Week 2: 수평 분할 (고도화)
├─ Person A: 성능 최적화 + 테스트 (인증/게시글)
└─ Person B: 부가 기능 + 테스트 (AI/업로드/댓글)
```

**이유**:
- 초반: 핵심 기능을 빠르게 완성 (MVP)
- 후반: 각자 강점을 살린 고도화

---

## 📅 Phase별 상세 계획

### Phase 1: 기초 세팅 (함께, Day 1)

| 시간 | 작업 내용 | 비고 |
|------|-----------|------|
| **오전 3시간** | • Git 레포지토리 생성<br>• 프로젝트 구조 세팅<br>• FastAPI 초기 설정<br>• requirements.txt 작성 | 페어 프로그래밍 |
| **오후 4시간** | • ERD 설계 완성<br>• database.py 작성<br>• Base Models 생성<br>• 개발 환경 동기화 | 함께 논의 |

**✅ 완료 기준**: 
- [ ] 로컬 개발 환경 실행 가능
- [ ] DB 연결 확인
- [ ] Git 워크플로우 합의

---

### Phase 2: 핵심 도메인 병렬 개발 (Day 2-5)

#### 👤 Person A: 🔐 인증 시스템 완성

##### Day 2-3: 인증 기능 구현
```
📂 작업 파일
├── models/user.py
├── schemas/user.py
├── routers/auth.py
├── utils/security.py
└── utils/dependencies.py

🎯 구현 기능
✅ POST /auth/register (회원가입)
✅ POST /auth/login (로그인, JWT 발급)
✅ GET /auth/me (현재 사용자 정보)
✅ PUT /auth/password (비밀번호 변경)
✅ PUT /auth/profile (프로필 수정)

🔧 유틸리티
✅ 비밀번호 해싱 (bcrypt)
✅ JWT 토큰 생성/검증
✅ get_current_user 의존성
```

##### Day 4: 테스트 & 문서화
```
✅ tests/test_auth.py 작성
✅ 회원가입 테스트 (성공/실패 케이스)
✅ 로그인 테스트 (유효/무효 토큰)
✅ 권한 체크 테스트
✅ API 문서 작성 (docstring)
✅ 에러 핸들링 구현
```

---

#### 👤 Person B: 📝 게시글 시스템 완성

##### Day 2-3: 게시글 CRUD
```
📂 작업 파일
├── models/post.py
├── models/comment.py
├── schemas/post.py
├── schemas/comment.py
└── routers/blog.py

🎯 구현 기능
✅ POST /blog (게시글 작성)
✅ GET /blog (목록 조회 + 페이지네이션)
✅ GET /blog/{post_id} (상세 조회)
✅ PUT /blog/{post_id} (수정)
✅ DELETE /blog/{post_id} (삭제)
✅ GET /blog?search=키워드 (검색)
✅ GET /blog?tag=태그 (필터링)
```

##### Day 4-5: 댓글 시스템
```
📂 작업 파일
└── routers/comment.py

🎯 구현 기능
✅ POST /blog/{post_id}/comments (댓글 작성)
✅ GET /blog/{post_id}/comments (댓글 목록)
✅ POST /comments/{comment_id}/replies (대댓글)
✅ PUT /comments/{comment_id} (댓글 수정)
✅ DELETE /comments/{comment_id} (댓글 삭제)
✅ 계층형 구조 구현 (parent_id)

✅ tests/test_blog.py 작성
✅ tests/test_comment.py 작성
```

---

### Phase 3: 부가 기능 병렬 개발 (Day 6-10)

#### 👤 Person A: 🎨 시스템 고도화

##### Day 6-7: 파일 업로드
```
📂 작업 파일
├── routers/upload.py
└── static/ (폴더 구조)

🎯 구현 기능
✅ POST /upload/images (이미지 업로드)
✅ 파일 유효성 검증 (확장자, 크기)
✅ 파일명 중복 처리 (UUID)
✅ StaticFiles 마운트
✅ 에러 처리 (용량 초과, 잘못된 형식)
```

##### Day 8-9: 성능 & 보안
```
🔧 성능 최적화
✅ DB 인덱스 추가 (post.created_at, user.email)
✅ N+1 쿼리 문제 해결 (joinedload)
✅ 페이지네이션 최적화

🔒 보안 강화
✅ CORS 설정
✅ Rate Limiting (slowapi)
✅ 보안 헤더 추가
✅ SQL Injection 방어 확인
✅ XSS 방어 확인
```

##### Day 10: 문서화
```
✅ README.md 완성
  ├── 프로젝트 소개
  ├── 설치 방법
  ├── 환경 변수 설명
  ├── API 엔드포인트 목록
  └── 실행 방법
✅ /docs 페이지 메타데이터 추가
✅ Postman 컬렉션 작성
```

---

#### 👤 Person B: 🤖 AI 기능

##### Day 6-7: AI 기능 준비
```
📂 작업 파일
└── routers/ai.py

🎯 구현 기능
✅ OpenAI API 키 설정
✅ POST /ai/autocomplete (자동완성)
  └── 제목/내용 자동완성
✅ 프롬프트 엔지니어링
✅ 기본 테스트
```

##### Day 8-9: AI 기능 확장
```
✅ POST /ai/summarize (게시글 요약)
  └── 긴 글을 3줄로 요약
✅ POST /ai/tags (태그 추천)
  └── 내용 기반 태그 자동 생성
✅ 에러 처리 (API 호출 실패, 타임아웃)
✅ tests/test_ai.py 작성
```

##### Day 10: 국제화 (선택)
```
✅ i18n/messages.py 작성
✅ Accept-Language 헤더 처리
✅ 에러 메시지 다국어 지원 (en/ko)
```

---

### Phase 4: 통합 & 마무리 (함께, Day 11-14)

#### Day 11-12: 통합 테스트

| 담당자 | 작업 내용 |
|--------|-----------|
| **Person A** | • 인증 관련 통합 테스트<br>• 게시글 CRUD 통합 테스트<br>• 권한 체크 통합 테스트 |
| **Person B** | • 댓글 시스템 통합 테스트<br>• 파일 업로드 통합 테스트<br>• AI 기능 통합 테스트 |
| **함께** | • E2E 시나리오 테스트<br>• 버그 수정<br>• 코드 리뷰 |

#### Day 13-14: 발표 준비

```
✅ 전체 기능 최종 점검
✅ 발표 자료 준비 (Notion/PPT)
  ├── 프로젝트 소개
  ├── 기술 스택 설명
  ├── 주요 기능 시연
  ├── 트러블슈팅 사례
  └── 느낀 점 / 배운 점
✅ 데모 시나리오 작성
✅ 질의응답 준비
✅ 프로젝트 회고
```

---

## 👥 역할별 책임 범위

### Person A: 🔐 인증 & 시스템 전문가

**핵심 역할**:
- 사용자 인증/인가 시스템 구축
- 보안 관련 모든 기능
- 시스템 아키텍처 최적화
- 파일 업로드 기능

**책임 도메인**:
```
Auth (인증)
├── 회원가입/로그인
├── JWT 토큰 관리
├── 권한 체크
└── 프로필 관리

System (시스템)
├── 성능 최적화
├── 보안 강화
├── 파일 업로드
└── 문서화
```

**기술 스택**:
- JWT, bcrypt
- SQLAlchemy (최적화)
- CORS, Rate Limiting
- FastAPI Security

---

### Person B: 📝 콘텐츠 & AI 전문가

**핵심 역할**:
- 게시글/댓글 시스템 구축
- AI 기능 통합
- 검색/필터링 로직
- 계층형 데이터 구조

**책임 도메인**:
```
Blog (게시글)
├── CRUD 전체
├── 검색/필터링
├── 페이지네이션
└── 조회수 관리

Comment (댓글)
├── 계층형 댓글
├── 대댓글 기능
└── 댓글 권한 체크

AI (인공지능)
├── 자동완성
├── 요약 기능
└── 태그 추천
```

**기술 스택**:
- SQLAlchemy (관계 설정)
- OpenAI API
- 재귀 쿼리 (계층형 댓글)
- 검색 알고리즘

---

## 📊 일정표

### Week 1: 핵심 기능 구축

| Day | Person A (인증/시스템) | Person B (게시글/댓글) | 함께 |
|-----|----------------------|---------------------|------|
| **1** | 🤝 기초 세팅 | 🤝 기초 세팅 | ERD, Git, DB 연결 |
| **2** | 🔐 Auth Models & API | 📝 Post Models & API | - |
| **3** | 🔐 Auth 완성 & 테스트 | 📝 Blog CRUD 완성 | - |
| **4** | 🎨 업로드 시작 | 💬 Comment 시작 | 코드 리뷰 |
| **5** | 🎨 업로드 완성 | 💬 Comment 완성 | 중간 점검 |
| **6-7** | 🔒 보안/성능 | 🤖 AI 시작 | 통합 테스트 |

### Week 2: 고도화 & 마무리

| Day | Person A (최적화) | Person B (AI/부가기능) | 함께 |
|-----|-----------------|---------------------|------|
| **8** | 📈 성능 최적화 | 🤖 AI 자동완성 | - |
| **9** | 🔒 보안 강화 | 🤖 AI 요약/태그 | - |
| **10** | 📝 문서화 | 🌐 국제화 (선택) | - |
| **11** | 🧪 테스트 | 🧪 테스트 | 통합 테스트 |
| **12** | 🐛 버그 수정 | 🐛 버그 수정 | 코드 리뷰 |
| **13-14** | 🎤 발표 준비 | 🎤 발표 준비 | 리허설 & 회고 |

---

## 🎯 마일스톤

### Week 1 마일스톤
- [ ] **Day 3**: 인증 시스템 완성 ✅
- [ ] **Day 5**: 게시글/댓글 CRUD 완성 ✅
- [ ] **Day 7**: 파일 업로드 완성 ✅

### Week 2 마일스톤
- [ ] **Day 10**: AI 기능 완성 ✅
- [ ] **Day 12**: 모든 테스트 통과 ✅
- [ ] **Day 14**: 프로젝트 발표 준비 완료 ✅

---

## 💡 핵심 차이점 (기존 WBS 대비)

### ✅ 개선된 점

1. **명확한 도메인 소유권**
   - 각자 맡은 도메인을 처음부터 끝까지 책임
   - 코드 충돌 최소화

2. **의존성 순서 고려**
   - Auth 먼저 → Blog/Comment는 Auth에 의존
   - 순차적 통합 가능

3. **테스트 동시 진행**
   - 기능 개발 직후 테스트 작성
   - 버그를 초기에 발견

4. **유연한 우선순위**
   - AI, 국제화 같은 부가 기능은 선택적
   - 핵심 기능에 집중

---

## 🚀 시작하기 전 체크리스트

### 개발 환경
- [ ] Python 3.11+ 설치
- [ ] PostgreSQL 또는 MySQL 설치
- [ ] Git 설치 및 계정 설정
- [ ] VS Code + 확장 프로그램 (Python, Pylance)

### 계정 준비
- [ ] GitHub 계정 생성
- [ ] OpenAI API 키 발급 (AI 기능용)
- [ ] 협업 도구 선택 (Notion, Slack 등)

### 사전 학습
- [ ] FastAPI 공식 문서 훑어보기
- [ ] SQLAlchemy 기초 개념
- [ ] JWT 인증 방식 이해
- [ ] Git 협업 워크플로우 (브랜치 전략)

---

## 📞 커뮤니케이션 원칙

1. **매일 스탠드업 (10분)**
   - 어제 한 일
   - 오늘 할 일
   - 막힌 부분

2. **코드 리뷰 (매 3일)**
   - 서로의 코드 리뷰
   - 개선점 논의
   - 지식 공유

3. **페어 프로그래밍 (필요시)**
   - 어려운 문제 함께 해결
   - 복잡한 로직 설계

4. **회고 (주 1회)**
   - 잘한 점
   - 아쉬운 점
   - 다음 주 개선 방향

---