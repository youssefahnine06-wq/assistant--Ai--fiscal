
from pathlib import Path
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    
    full_text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            full_text += f"\n--- Page {page_number} ---\n"
            full_text += text

    return full_text


def load_all_pdfs(folder="documents"):
    documents = []
    
    pdf_files = Path(folder).glob("*.pdf")

    for pdf_file in pdf_files:
        print(f"Lecture du document : {pdf_file.name}")
        text = extract_text_from_pdf(pdf_file)

        documents.append({
            "filename": pdf_file.name,
            "content": text
        })

    return documents
                                                            