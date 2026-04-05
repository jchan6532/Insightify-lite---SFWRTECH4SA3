from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    content: str
    file_type: str = "txt"