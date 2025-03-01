"""
Universal service for managing all document types.
"""

from typing import List, Optional, Dict, Any
from datetime import date
import logging
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.services.base_service import BaseService
from app.services.template_manager import TemplateManager

logger = logging.getLogger(__name__)


class DocumentService(BaseService[Document, DocumentCreate, DocumentUpdate]):
    """Service for handling all document operations."""

    def __init__(self, model):
        super().__init__(model)
        self.template_manager = TemplateManager()

    async def create(self, db: AsyncSession, obj_in: DocumentCreate) -> Document:
        """Create a new document with dynamic fields."""
        logger.debug("Creating document: %s", obj_in.model_dump())
        # Validate document_type against templates
        templates = await self.template_manager.list_templates(db)
        template = next(
            (t for t in templates if t["template_type"] == obj_in.document_type), None
        )
        if not template:
            logger.error("Invalid document_type: %s", obj_in.document_type)
            raise HTTPException(
                status_code=400, detail=f"Invalid document_type: {obj_in.document_type}"
            )

        # Validate dynamic fields against template (optional)
        if template["fields"]:
            expected_fields = set(template["fields"])
            provided_fields = set(obj_in.dynamic_fields.keys())
            if not provided_fields.issubset(expected_fields):
                logger.error(
                    "Dynamic fields mismatch: expected %s, got %s",
                    expected_fields,
                    provided_fields,
                )
                raise HTTPException(
                    status_code=400,
                    detail=f"Dynamic fields must match template {obj_in.document_type}: {expected_fields}",
                )

        # Create document
        db_obj = Document(
            document_type=obj_in.document_type,
            reference_number=obj_in.reference_number,
            created_date=obj_in.created_date,
            dynamic_fields=obj_in.dynamic_fields,
            parent_id=obj_in.parent_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        logger.info("Document created: %s (ID: %d)", obj_in.reference_number, db_obj.id)
        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: Document, obj_in: DocumentUpdate
    ) -> Document:
        """Update a document with dynamic fields."""
        logger.debug(
            "Updating document ID: %d with data: %s", db_obj.id, obj_in.model_dump()
        )
        update_data = obj_in.model_dump(exclude_unset=True)
        if "dynamic_fields" in update_data:
            db_obj.dynamic_fields = {
                **db_obj.dynamic_fields,
                **update_data["dynamic_fields"],
            }
            del update_data["dynamic_fields"]
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        await db.commit()
        await db.refresh(db_obj)
        logger.info("Document updated: %s (ID: %d)", db_obj.reference_number, db_obj.id)
        return db_obj

    async def get_by_filters(
        self,
        db: AsyncSession,
        *,
        document_type: Optional[str] = None,
        reference_number: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        dynamic_field_filters: Optional[Dict[str, Any]] = None,
        parent_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Document]:
        """Get documents with optional filters."""
        logger.debug(
            "Fetching documents with filters: type=%s, ref=%s, parent_id=%s",
            document_type,
            reference_number,
            parent_id,
        )
        query = select(Document).offset(skip).limit(limit)
        filters = []

        if document_type:
            filters.append(Document.document_type == document_type)
        if reference_number:
            filters.append(Document.reference_number.ilike(f"%{reference_number}%"))
        if start_date and end_date:
            filters.append(
                and_(
                    Document.created_date >= start_date,
                    Document.created_date <= end_date,
                )
            )
        if parent_id:
            filters.append(Document.parent_id == parent_id)
        if dynamic_field_filters:
            for key, value in dynamic_field_filters.items():
                filters.append(Document.dynamic_fields[key].astext == str(value))

        if filters:
            query = query.where(*filters)

        result = await db.execute(query)
        documents = result.scalars().all()
        logger.info("Retrieved %d documents", len(documents))
        return documents

    async def get_with_relations(
        self, db: AsyncSession, document_id: int
    ) -> Optional[Document]:
        """Get document with all related entities."""
        logger.debug("Fetching document with relations: ID=%d", document_id)
        query = (
            select(Document)
            .options(
                selectinload(Document.children),
                selectinload(Document.parent),
            )
            .filter(Document.id == document_id)
        )
        result = await db.execute(query)
        document = result.scalar_one_or_none()
        if document:
            logger.info(
                "Retrieved document with relations: %s (ID: %d)",
                document.reference_number,
                document_id,
            )
        else:
            logger.warning("Document not found: ID=%d", document_id)
        return document


# Create service instance
document_service = DocumentService(Document)
