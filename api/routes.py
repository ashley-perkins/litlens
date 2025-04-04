from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from modules import summarizer

router = APIRouter()

class SummarizeRequest(BaseModel):
    goal: str
    content: str

@router.post("/summarize")
def summarize_text(request: SummarizeRequest):
    try:
        summary = summarizer.summarize_inline_text(request.content, request.goal)
        return {
            "goal": request.goal,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")
