from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import models, schemas, storage
from app.database import get_db

router = APIRouter(tags=["Documents"])


@router.post(
    "/equipment/{equipment_id}/documents",
    response_model=schemas.DocumentOut,
    status_code=201,
)
def upload_document(
    equipment_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    equipment = db.query(models.Equipment).get(equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    object_key = storage.upload_file(file.file, file.content_type)

    document = models.Document(
        equipment_id=equipment_id,
        original_filename=file.filename,
        content_type=file.content_type,
        object_key=object_key,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.get(
    "/equipment/{equipment_id}/documents", response_model=List[schemas.DocumentOut]
)
def list_documents(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).get(equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return (
        db.query(models.Document)
        .filter(models.Document.equipment_id == equipment_id)
        .all()
    )


@router.get("/documents/{document_id}/download")
def download_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    body = storage.download_file(document.object_key)
    return StreamingResponse(
        body,
        media_type=document.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{document.original_filename}"'
        },
    )
