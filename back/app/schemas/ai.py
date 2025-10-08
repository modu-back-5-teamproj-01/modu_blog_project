from pydantic import BaseModel

class AIRequest(BaseModel):
    keywords: str
    prompt: str
    max_tokens: int = 100

class AIResponse(BaseModel):
    result: str