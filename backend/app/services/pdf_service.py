import os
import shutil
import subprocess
from pathlib import Path

from docxtpl import DocxTemplate
from app.schemas.contract import ContractBase

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
GENERATED_DIR = BASE_DIR / "assets" / "generated_docs"


async def generate_contract_docx(
    contract_data: ContractBase, template_name: str
) -> str:
    """Generates a contract in DOCX format using a selected template."""
    template_path = os.path.join(TEMPLATES_DIR, template_name)

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template {template_name} not found.")

    doc = DocxTemplate(template_path)

    # Render template with contract data
    doc.render(contract_data.model_dump())

    os.makedirs(GENERATED_DIR, exist_ok=True)

    docx_path = os.path.join(
        GENERATED_DIR, f"contract_{contract_data.contract_number}.docx"
    )
    doc.save(docx_path)

    return docx_path


async def convert_docx_to_pdf(docx_path: str) -> str:
    """Converts a DOCX file to PDF using LibreOffice."""

    if not shutil.which("libreoffice"):  # ✅ Проверка наличия LibreOffice
        raise FileNotFoundError("LibreOffice is not installed or not in PATH.")

    pdf_path = docx_path.replace(".docx", ".pdf")
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            GENERATED_DIR,
            docx_path,
        ],
        check=True,
    )
    return pdf_path
