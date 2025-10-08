import sys
from pathlib import Path
from fastapi import APIRouter
from schemas.ai import AIRequest, AIResponse  # schemas에서 import

router = APIRouter()

@router.post("/summary", response_model=AIResponse)
async def summarize_content(request: AIRequest):
    """긴 콘텐츠를 요약하여 블로그 글 도입부에 활용"""
    # TODO: OpenAI API 연동 로직 구현
    #  현재는 목업 데이터 변환
    summary = f"[AI 요약 결과] 요청하신 내용의 핵심 내용을 간결하게 정리했습니다."
    return AIResponse(result=summary, type="summary")

@router.post("/draft", response_model=AIResponse)
async def generate_draft(request: AIRequest):
    """주어진 주제로 블로그 게시물 초안 작성"""
    # TODO: OpenAI API 연동 로직 구현
    # 현재는 목업 데이터 반환
    draft = f"[AI 초안 생성] 주제 '{request.prompt}'에 대한 뼈대가 완성되었습니다. 세부 내용을 추가하세요."
    return AIResponse(result=draft, type="draft")