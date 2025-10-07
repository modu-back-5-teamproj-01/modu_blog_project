# back/app/routers/ai.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import requests
from typing import Annotated

# ⭐ 임포트 경로 정리: 표준적인 상대 경로 적용
from ..core.database import get_db
from ..models.user import User as UserModel
from ..schemas import post as post_schema # 파트너의 스키마 파일

# Auth 모듈에서 정의한 인증 함수를 가져옵니다.
from .auth import get_current_user 

router = APIRouter(prefix="/ai", tags=["AI"])

# [TODO] 실제 AI 서비스의 URL로 변경해야 합니다.
# 현재는 토큰 재활용 테스트를 위해 내부 URL을 사용한다고 가정했습니다.
AI_SERVICE_URL = "http://localhost:8000/ai/external-service" 

# --- AI 서비스 시뮬레이션 엔드포인트 ---
# 외부 AI API를 가정하고, post.py의 토큰 재활용 테스트를 위한 엔드포인트입니다.
# 이 엔드포인트는 실제 외부 AI 서비스가 아닙니다.
@router.post("/external-service")
def simulate_external_ai_service(post: post_schema.PostCreate):
    """
    외부 AI 서비스 시뮬레이션: 
    받은 콘텐츠를 바탕으로 요약과 태그를 생성한다고 가정합니다.
    """
    # 실제 AI 로직 대신 임시 데이터를 반환
    summary = f"[AI 요약] {post.content[:30]}..."
    tags = ["FastAPI", "인증", "AI통합"]
    
    return {
        "summary": summary, 
        "tags": tags
    }

# --- AI 통합 함수 (post.py에서 호출됨) ---
# 이 함수는 post.py 파일에서 직접 호출되므로, 
# 실제 서버의 엔드포인트(URL)는 아닙니다.
def analyze_post_content(
    content: str, 
    current_user: Annotated[UserModel, Depends(get_current_user)], 
    db: Session = Depends(get_db)
):
    """
    게시글 내용(content)을 받아 AI 서비스에 전달하고,
    요약과 태그 목록을 반환합니다.
    """
    
    # 1. AI 서비스에 전달할 데이터 준비
    request_data = {"content": content}

    # 2. AI 서비스 호출
    # 현재는 내부 simulate 엔드포인트를 호출하며, 토큰 인증이 필요 없습니다.
    # 만약 외부 AI가 인증을 요구한다면 'Authorization' 헤더를 추가해야 합니다.
    try:
        # requests 라이브러리 사용
        response = requests.post(AI_SERVICE_URL, json=request_data)
        response.raise_for_status() # HTTP 오류 발생 시 예외 처리
        
        ai_result = response.json()
        
        return {
            "summary": ai_result.get("summary", ""),
            "tags": ai_result.get("tags", [])
        }

    except requests.exceptions.RequestException as e:
        print(f"AI 서비스 호출 실패: {e}")
        # AI 호출 실패 시 기본값 반환 또는 예외 발생
        return {
            "summary": "[AI 요약 실패: 서비스 오류]",
            "tags": ["미분류"]
        }
    
    except Exception as e:
        print(f"예기치 않은 오류 발생: {e}")
        return {
            "summary": "[AI 요약 실패: 내부 오류]",
            "tags": ["오류"]
        }