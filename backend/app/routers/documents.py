"""
Universal document management endpoints.
"""

from typing import List, Optional, Dict, Any
import logging
from fastapi import APIRouter, HTTPException, Query
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.services.document_service import document_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/{document_id}")
async def get_document(document_id: int):
    logger.debug("Fetching document ID: %d", document_id)
    return {"document_id": document_id}


@router.post(
    "/",
    response_model=DocumentResponse,
    summary="Create new document",
    description="Creates a new document of any type with dynamic fields",
)
async def create_document(document: DocumentCreate) -> DocumentResponse:
    logger.debug("Creating document with data: %s", document)
    async with AsyncSessionLocal() as db:
        try:
            return await document_service.create(db, document)
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error("Error creating document: %s", str(e), exc_info=True)
            raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Get document details",
    description="Retrieves details of a specific document",
)
async def get_document(
    document_id: int,
    include_related: bool = Query(False, description="Include related documents"),
) -> DocumentResponse:
    logger.debug(
        "Fetching document ID: %d, include_related: %s", document_id, include_related
    )
    async with AsyncSessionLocal() as db:
        if include_related:
            document = await document_service.get_with_relations(db, document_id)
        else:
            document = await document_service.get(db, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document


@router.get(
    "/",
    response_model=List[DocumentResponse],
    summary="List documents",
    description="Get a list of documents with optional filtering",
)
async def list_documents(
    skip: int = Query(0, ge=0, description="Number of documents to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of documents"),
    document_type: Optional[str] = Query(None, description="Filter by document type"),
    reference_number: Optional[str] = Query(
        None, description="Filter by reference number"
    ),
    dynamic_field_filters: Optional[Dict[str, Any]] = Query(
        None, description="Filter by dynamic fields"
    ),
    parent_id: Optional[int] = Query(None, description="Filter by parent document ID"),
) -> List[DocumentResponse]:
    logger.debug("Listing documents with filters: skip=%d, limit=%d", skip, limit)
    async with AsyncSessionLocal() as db:
        return await document_service.get_by_filters(
            db,
            document_type=document_type,
            reference_number=reference_number,
            dynamic_field_filters=dynamic_field_filters,
            parent_id=parent_id,
            skip=skip,
            limit=limit,
        )


@router.put(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Update document",
    description="Updates an existing document",
)
async def update_document(
    document_id: int, document: DocumentUpdate
) -> DocumentResponse:
    async with AsyncSessionLocal() as db:
        db_obj = await document_service.get(db, document_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Document not found")
        return await document_service.update(db, db_obj, document)


@router.delete(
    "/{document_id}",
    summary="Delete document",
    description="Deletes a specific document",
)
async def delete_document(document_id: int) -> dict:
    async with AsyncSessionLocal() as db:
        db_obj = await document_service.get(db, document_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Document not found")
        await document_service.delete(db, db_obj)
        return {"message": "Document deleted"}
