from fastapi import APIRouter
from app.schemas.query import QueryRequest
from openai import OpenAI
import os

router = APIRouter(
    prefix="/query", 
    tags=["Query"]
)

@router.post("/")
def query_docs(req: QueryRequest):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Answer this question: {req.question}"
    )

    return {"result": response.output_text}

