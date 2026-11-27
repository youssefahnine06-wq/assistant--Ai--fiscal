from pathlib import Path
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract

from text_processor import clean_text, split_text


def extract_pages_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "page": page_number,
                "content": text
            })

    if sum(len(page["content"]) for page in pages) < 100:
        print(f"OCR activé pour : {pdf_path.name}")

        images = convert_from_path(str(pdf_path))
        pages = []

        for page_number, image in enumerate(images, start=1):
            text = pytesseract.image_to_string(
                image,
                lang="fra+ara"
            )

            if text.strip():
                pages.append({
                    "page": page_number,
                    "content": text
                })

    return pages


def load_all_pdfs(folder="documents"):
    documents = []

    pdf_files = Path(folder).rglob("*.pdf")

    for pdf_file in pdf_files:
        print(f"\nLecture du document : {pdf_file.name}")

        try:
            pages = extract_pages_from_pdf(pdf_file)

            for page_data in pages:
                cleaned_text = clean_text(page_data["content"])
                chunks = split_text(cleaned_text)

                for chunk_number, chunk in enumerate(chunks, start=1):
                    documents.append({
                        "filename": pdf_file.name,
                        "category": pdf_file.parent.name,
                        "page": page_data["page"],
                        "chunk_id": (
                            f"{pdf_file.stem}_"
                            f"p{page_data['page']}_"
                            f"c{chunk_number}"
                        ),
                        "content": chunk
                    })

            print(f"Nombre de pages lues : {len(pages)}")

        except Exception as error:
            print(f"Erreur avec {pdf_file.name} : {error}")

    print(f"\nNombre total de segments créés : {len(documents)}")

    return documents
