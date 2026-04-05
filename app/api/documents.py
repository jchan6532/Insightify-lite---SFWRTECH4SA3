from fastapi import APIRouter, HTTPException
from app.schemas.document import DocumentCreate
from app.db import get_connection
from app.services.ingestion_service import IngestionService

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
            """
            INSERT INTO documents (title, content)
            VALUES (%s, %s)
            RETURNING id
            """,
            (doc.title, doc.content)
        )

        document_id = cur.fetchone()[0]
        conn.commit()

        ingestion_service = IngestionService()
        result = ingestion_service.ingest(document_id=document_id, content=doc.content)

        return {
            "message": "Document uploaded and ingested successfully",
            "document_id": document_id,
            "chunks_created": result.get("stored_chunk_count", 0)
        }

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@router.get("/")
def list_documents():
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, title, created_at
            FROM documents
            ORDER BY id DESC
            """
        )

        rows = cur.fetchall()

        documents = []
        for row in rows:
            documents.append({
                "id": row[0],
                "title": row[1],
                "created_at": str(row[2])
            })

        return {"documents": documents}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()