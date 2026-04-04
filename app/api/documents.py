from fastapi import APIRouter, HTTPException
from app.schemas.document import DocumentCreate
from app.db import get_connection

router = APIRouter(
    prefix="/documents", 
    tags=["Documents"]
)


@router.post("/upload")
def upload_document(doc: DocumentCreate):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO documents (title, content) VALUES (%s, %s) RETURNING id",
            (doc.title, doc.content)
        )

        doc_id = cur.fetchone()[0]
        conn.commit()

        return {"message": "Document uploaded", "document_id": doc_id}

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()