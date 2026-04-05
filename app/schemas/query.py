from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    strategy: str = "keyword"