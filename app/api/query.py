from fastapi import APIRouter, HTTPException
from app.schemas.query import QueryRequest
from app.services.query_service import QueryService

router = APIRouter(
    prefix="/query", 
    tags=["Query"]
)


@router.post("/")
def query_docs(req: QueryRequest):
    try:
        query_service = QueryService(strategy_name=req.strategy)
        result = query_service.answer_question(question=req.question, limit=3)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))