# Blog Project - 협업자 세팅 가이드

이 문서는 신규 협업자가 프로젝트를 로컬 환경에 세팅할 때 따라야 하는 단계별 안내입니다.

---

## 1️⃣ 레포지토리 클론 및 브랜치 확인
```bash
git clone <레포지토리_URL>
cd blog-project
git checkout dev   # 협업 브랜치 기준
git pull origin dev
```

## 2️⃣ 가상환경 생성 및 활성화
Windows
```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3️⃣ Python 의존성 설치
```bash
pip install -r requirements.txt
```

## 4️⃣ 환경 변수 설정

1. `.env.example` 파일을 복사해서 `.env` 생성
```bash
cp .env.example .env   # Windows: copy .env.example .env
```

2. `.env` 내용 수정
```env
DATABASE_URL=sqlite:///./dev_blog.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 5️⃣ FastAPI 실행 확인
```bash
uvicorn back.app.main:app --reload
```

- 브라우저 접속: http://127.0.0.1:8000

- 성공 시: {"message":"Hello, Blog Project!"}


## 6️⃣ DB 연결 테스트
```bash
python -m back.app.init_db
```

- blog.db 파일 생성 확인

- SQLite 브라우저나 VSCode 확장으로 테이블 확인 가능

## 7️⃣ Git push / pull 규칙

- `.gitignore` 기준으로 개인 환경 파일 제외

- 커밋 메시지 예시:
```bash
git add .
git commit -m "초기 세팅 완료"
git push origin dev
```

⚠️ 주의

- OS별 경로 차이 고려 (Windows: \, macOS/Linux: /)

- `.env` 파일은 절대 GitHub에 올리지 말 것