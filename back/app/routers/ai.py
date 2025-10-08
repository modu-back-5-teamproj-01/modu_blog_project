# modu_blog_project/back/app/routers/ai.py

import sys
from pathlib import Path
import os
from openai import OpenAI
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer 
from pydantic import BaseModel

# 🛑 경로 문제 해결 코드: sys.path 주입
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# 💡 이 부분은 인증 의존성 함수가 있는 곳에 따라 다를 수 있습니다.
#    프로젝트 구조상 core.security에서 함수를 임포트해야 할 수 있습니다.
# from core.security import get_current_user_email 


# 스키마 정의 (422 오류 해결에 사용됨)
class AIRequest(BaseModel):
    keywords: str
    prompt: str
    max_tokens: int = 100

class AIResponse(BaseModel):
    result: str

# OpenAI 클라이언트 초기화 (500 오류 해결)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
if not OPENAI_API_KEY:
    # ❌ 실제 프로젝트에서는 오류를 발생시켜야 하지만, 여기서는 임시 로그로 대체
    print("WARNING: OPENAI_API_KEY is not set.")
    # raise ValueError("OPENAI_API_KEY is not set in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)
security = HTTPBearer()


# 💡 라우터 정의 및 인증 의존성 적용 (자물쇠 아이콘 표시 및 401 대비)
router = APIRouter(
    prefix="/api/ai", 
    tags=["AI"],
    # 인증 의존성: 여기에 정확한 인증 함수를 넣어주세요. (예: Depends(get_current_user_email))
    # 현재는 쉬운 테스트를 위해 임시로 [Depends(security)]만 넣습니다.
    dependencies=[Depends(security)] 
)

# modu_blog_project/back/app/routers/ai.py (내용 요약 함수)

# 💡 이 함수가 파일에 있는지, 그리고 주석 처리되어 있지 않은지 확인하세요.

@router.post("/summary", response_model=AIResponse)
async def summarize_content(
    request: AIRequest,
    # current_user_email: str = Depends(get_current_user_email) # 인증 필요 시
):
    try:
        text_to_summarize = request.prompt # 예시: prompt 필드를 요약 텍스트로 사용
        
        prompt = f"다음 내용을 3줄로 간결하게 요약해 주세요: \n\n{text_to_summarize}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 핵심만 추출하는 요약 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        
        summary_text = response.choices[0].message.content
        return {"result": summary_text} # AIResponse 스키마의 필드 이름에 맞게 조정
    
    except Exception as e:
        # ... (에러 처리 로직)
        pass



@router.post("/draft", response_model=AIResponse)
async def generate_draft(
    request: AIRequest,
    # current_user_email: str = Depends(get_current_user_email) # 실제 인증 함수 사용
):
    try:
        # keywords와 prompt를 조합하여 프롬프트를 생성
        full_prompt = (
            f"다음 키워드를 포함하여 기술 블로그 초안을 작성해 주세요: {request.keywords}. "
            f"추가 지시사항: {request.prompt}"
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 전문적인 기술 블로거입니다."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=request.max_tokens 
        )
        
        draft_text = response.choices[0].message.content
        return {"result": draft_text} 
    
    except Exception as e:
        # 터미널에서 상세 오류를 확인해야 함
        print(f"OpenAI API Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI 초안 생성 오류: {e}"
        )