import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.security import HTTPBearer

# 프로젝트 루트를 Python 경로에 추가 (import 전에 실행)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # back의 상위 디렉토리
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 이제 절대 경로 임포트
from back.app.routers import auth
from back.app.routers import ai
from back.app.routers import post

security = HTTPBearer()

# 3. FastAPI 앱 정의 및 보안 스키마 직접 정의 (Value 입력란 생성)
app = FastAPI(
    title="AI Blog API",
    openapi_extra={
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": { 
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization", 
                }
            }
        },
        "security": [{"ApiKeyAuth": []}], 
    }
)

# 4. 라우터 등록
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(post.router)

# 5. 기본 루트 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Blog API!"}