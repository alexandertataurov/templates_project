"""
Service for generating and managing PDF documents.
"""

import os
import shutil
import logging
import subprocess
import asyncio
from pathlib import Path
from typing import Optional
from fastapi import HTTPException
from datetime import datetime

from docxtpl import DocxTemplate
from app.schemas.contract import ContractBase
from app.config import settings

logger = logging.getLogger(__name__)


class PDFService:
    """Service for handling PDF document operations."""

    def __init__(self):
        """Initialize service with required directories."""
        self.base_dir = Path(__file__).resolve().parent.parent
        self.templates_dir = self.base_dir / "assets" / "templates"
        self.generated_dir = self.base_dir / "assets" / "generated_docs"

        # Ensure directories exist
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    async def convert_docx_to_pdf(self, docx_path: Path) -> Path:
        """
        Convert DOCX file to PDF using LibreOffice.

        Args:
            docx_path: Path to source DOCX file

        Returns:
            Path to generated PDF file

        Raises:
            HTTPException: If conversion fails
        """
        try:
            pdf_path = docx_path.with_suffix(".pdf")

            # Use LibreOffice for conversion
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
                logger.error(
                    "PDF conversion failed: %s",
                    stderr.decode(),
                    extra={"docx_path": str(docx_path)},
                )
                raise HTTPException(
                    status_code=500, detail="Failed to convert document to PDF"
                )

            logger.info("Successfully converted DOCX to PDF: %s", pdf_path.name)
            return pdf_path

        except Exception as e:
            logger.error(
                "PDF conversion error: %s",
                str(e),
                exc_info=True,
                extra={"docx_path": str(docx_path)},
            )
            raise HTTPException(
                status_code=500, detail=f"PDF conversion failed: {str(e)}"
            )

    async def generate_contract_docx(
        self, contract_data: ContractBase, template_name: str
    ) -> Path:
        """
        Generate a contract document in DOCX format.

        Args:
            contract_data: Contract data for template
            template_name: Name of the template file

        Returns:
            Path to generated document
        """
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Template {template_name} not found"
            )

        try:
            doc = DocxTemplate(template_path)
            doc.render(contract_data.model_dump())

            output_path = (
                self.generated_dir / f"contract_{contract_data.contract_number}.docx"
            )
            doc.save(output_path)

            logger.info(
                "Generated DOCX contract: %s using template: %s",
                output_path.name,
                template_name,
            )
            return output_path

        except Exception as e:
            logger.error("Failed to generate DOCX: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"Failed to generate document: {str(e)}"
            )

    async def convert_to_pdf(self, docx_path: Path) -> Path:
        """
        Convert a DOCX file to PDF using LibreOffice.

        Args:
            docx_path: Path to DOCX file

        Returns:
            Path to generated PDF
        """
        if not shutil.which("libreoffice"):
            raise HTTPException(status_code=500, detail="LibreOffice is not installed")

        try:
            pdf_path = docx_path.with_suffix(".pdf")

            process = await asyncio.create_subprocess_exec(
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(self.generated_dir),
                str(docx_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                logger.error(
                    "PDF conversion failed: %s",
                    stderr.decode() if stderr else "Unknown error",
                )
                raise HTTPException(status_code=500, detail="PDF conversion failed")

            logger.info("Generated PDF: %s", pdf_path.name)
            return pdf_path

        except Exception as e:
            logger.error("Failed to convert to PDF: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"Failed to convert to PDF: {str(e)}"
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
async def generate_contract_docx(
    contract_data: ContractBase, template_name: str
) -> Path:
    return await pdf_service.generate_contract_docx(contract_data, template_name)


async def convert_docx_to_pdf(docx_path: Path) -> Path:
    return await pdf_service.convert_docx_to_pdf(docx_path)
