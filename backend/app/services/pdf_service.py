"""
Service for generating and managing PDF documents.
"""

import logging
from pathlib import Path
import asyncio
from typing import Optional
from fastapi import HTTPException
from datetime import datetime
from docxtpl import DocxTemplate
from app.schemas.document import DocumentBase
from app.core.config import Settings

logger = logging.getLogger(__name__)


class PDFService:
    """Service for handling PDF document operations."""

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.templates_dir = self.base_dir / "assets" / "templates"
        self.generated_dir = self.base_dir / "assets" / "generated_docs"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    async def generate_document_docx(
        self, document_data: DocumentBase, template_name: str
    ) -> Path:
        """
        Generate a document in DOCX format.

        Args:
            document_data: Document data for template
            template_name: Name of the template file

        Returns:
            Path to generated document
        """
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            logger.error("Template not found: %s", template_name)
            raise HTTPException(
                status_code=404, detail=f"Template {template_name} not found"
            )

        try:
            doc = DocxTemplate(template_path)
            render_data = {
                "document_type": document_data.document_type,
                "reference_number": document_data.reference_number,
                "created_date": document_data.created_date.isoformat(),
                **document_data.dynamic_fields,
            }
            doc.render(render_data)
            output_path = (
                self.generated_dir
                / f"{document_data.document_type}_{document_data.reference_number}.docx"
            )
            doc.save(output_path)
            logger.info(
                "Generated DOCX: %s using template: %s", output_path.name, template_name
            )
            return output_path
        except Exception as e:
            logger.error("Failed to generate DOCX: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"Failed to generate document: {str(e)}"
            )

    async def convert_docx_to_pdf(self, docx_path: Path) -> Path:
        """
        Convert DOCX file to PDF using LibreOffice.

        Args:
            docx_path: Path to source DOCX file

        Returns:
            Path to generated PDF file
        """
        try:
            pdf_path = docx_path.with_suffix(".pdf")
            process = await asyncio.create_subprocess_exec(
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                str(docx_path),
                "--outdir",
                str(self.generated_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                logger.error("PDF conversion failed: %s", stderr.decode())
                raise HTTPException(
                    status_code=500, detail="Failed to convert document to PDF"
                )
            logger.info("Successfully converted DOCX to PDF: %s", pdf_path.name)
            return pdf_path
        except Exception as e:
            logger.error("PDF conversion error: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"PDF conversion failed: {str(e)}"
            )

    async def cleanup_old_files(self, max_age_days: int = 7) -> None:
        """Clean up old generated files."""
        try:
            current_time = datetime.now()
            for file_path in self.generated_dir.glob("*.*"):
                file_age = current_time - datetime.fromtimestamp(
                    file_path.stat().st_mtime
                )
                if file_age.days > max_age_days:
                    file_path.unlink()
                    logger.info("Deleted old file: %s", file_path.name)
        except Exception as e:
            logger.error("Failed to cleanup files: %s", str(e), exc_info=True)


# Create service instance
pdf_service = PDFService()


# Export individual functions for backward compatibility
async def generate_document_docx(
    document_data: DocumentBase, template_name: str
) -> Path:
    return await pdf_service.generate_document_docx(document_data, template_name)


async def convert_docx_to_pdf(docx_path: Path) -> Path:
    return await pdf_service.convert_docx_to_pdf(docx_path)
