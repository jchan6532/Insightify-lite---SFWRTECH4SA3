from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.document import DocumentCreate
from app.db import get_connection
from app.services.ingestion_service import IngestionService
from app.parsers.parser_factory import ParserFactory

router = APIRouter(
    prefix="/documents", 
    tags=["Documents"]
)


@router.post("/upload")
def upload_document(doc: DocumentCreate):
    conn = None
    cur = None

    try:
        parser = ParserFactory.create_parser(f"{doc.title}.txt")
        parsed_content = parser.parse(doc.content.encode("utf-8"))

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO documents (title, content)
            VALUES (%s, %s)
            RETURNING id
            """,
            (doc.title, parsed_content)
        )

        document_id = cur.fetchone()[0]
        conn.commit()

        ingestion_service = IngestionService()
        result = ingestion_service.ingest(document_id=document_id, content=parsed_content)

        return {
            "message": "Document uploaded and ingested successfully",
            "document_id": document_id,
            "file_type": doc.file_type,
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

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    conn = None
    cur = None

    try:
        parser = ParserFactory.create_parser(file.filename)

        raw_content = await file.read()

        try:
            parsed_content = parser.parse(raw_content)
        except NotImplementedError as e:
            raise HTTPException(status_code=400, detail=str(e))

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO documents (title, content)
            VALUES (%s, %s)
            RETURNING id
            """,
            (file.filename, parsed_content)
        )

        document_id = cur.fetchone()[0]
        conn.commit()

        ingestion_service = IngestionService()
        result = ingestion_service.ingest(document_id=document_id, content=parsed_content)

        return {
            "message": "File uploaded and ingested successfully",
            "document_id": document_id,
            "filename": file.filename,
            "chunks_created": result.get("stored_chunk_count", 0)
        }
    
    except NotImplementedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
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


@router.get("/{document_id}/chunks")
def get_document_chunks(document_id: int):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT d.id, d.title
            FROM documents d
            WHERE d.id = %s
            """,
            (document_id,)
        )

        document_row = cur.fetchone()

        if not document_row:
            raise HTTPException(status_code=404, detail="Document not found")

        cur.execute(
            """
            SELECT chunk_index, chunk_text
            FROM chunks
            WHERE document_id = %s
            ORDER BY chunk_index ASC
            """,
            (document_id,)
        )

        chunk_rows = cur.fetchall()

        chunks = []
        for row in chunk_rows:
            chunks.append({
                "chunk_index": row[0],
                "chunk_text": row[1]
            })

        return {
            "document_id": document_row[0],
            "title": document_row[1],
            "chunk_count": len(chunks),
            "chunks": chunks
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()