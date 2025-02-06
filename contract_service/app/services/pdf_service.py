import subprocess
import os
import shutil
from app.schemas.contract import ContractBase
from docxtpl import DocxTemplate

TEMPLATE_DIR = "templates/"
OUTPUT_DIR = "generated_docs/"

async def generate_contract_docx(contract_data: ContractBase, template_name: str) -> str:
    """Generates a contract in DOCX format using a selected template."""
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template {template_name} not found.")

    doc = DocxTemplate(template_path)

    # Render template with contract data
    doc.render(contract_data.model_dump())

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    docx_path = os.path.join(OUTPUT_DIR, f"contract_{contract_data.contract_number}.docx")
    doc.save(docx_path)

    return docx_path

async def convert_docx_to_pdf(docx_path: str) -> str:
    """Converts a DOCX file to PDF using LibreOffice."""
    
    if not shutil.which("libreoffice"):  # ✅ Проверка наличия LibreOffice
        raise FileNotFoundError("LibreOffice is not installed or not in PATH.")

    pdf_path = docx_path.replace(".docx", ".pdf")
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", OUTPUT_DIR, docx_path], check=True)
    return pdf_path
