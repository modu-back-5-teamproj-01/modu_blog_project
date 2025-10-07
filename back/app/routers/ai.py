# back/app/routers/ai.py 파일 전체 내용

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# 요청 스키마 정의: AI에게 질문할 내용 (Prompt)
class AIRequest(BaseModel):
    prompt: str

# 응답 스키마 정의: AI의 응답
class AIResponse(BaseModel):
    response: str
    token_usage: int = 0
    model: str = "Dummy-AI-Model"

router = APIRouter()

# 💡 AI 기능 엔드포인트: POST /ai/generate
@router.post(
    "/generate", 
    response_model=AIResponse, 
    status_code=status.HTTP_200_OK
)
async def generate_ai_response(request: AIRequest):
    """
    사용자의 프롬프트를 받아 AI 응답을 생성합니다.
    (현재는 더미 응답을 반환합니다.)
    """
    
    # 🚨 실제 AI 모델 호출 로직은 여기에 구현됩니다.
    # 예: response = await client.generate(request.prompt)
    
    # 더미 응답 생성
    if not request.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="프롬프트 내용을 입력해주세요."
        )
        
    dummy_response = f"AI 모델의 가상 응답: 당신의 질문 '{request.prompt}'에 대한 훌륭한 답변을 생성했습니다."
    
    return AIResponse(
        response=dummy_response,
        token_usage=len(request.prompt.split()) + 50 # 임의의 토큰 사용량
    )