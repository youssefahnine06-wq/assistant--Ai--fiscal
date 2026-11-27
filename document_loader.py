
from pathlib import Path
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""

    # Première méthode : lecture classique avec pypdf
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            full_text += f"\n--- Page {page_number} ---\n"
            full_text += text

    # Deuxième méthode : OCR si le texte extrait est insuffisant
    if len(full_text.strip()) < 100:
        print(f"OCR activé pour : {pdf_path.name}")

        images = convert_from_path(str(pdf_path))
        full_text = ""

        for page_number, image in enumerate(images, start=1):
            text = pytesseract.image_to_string(
                image,
                lang="fra+ara"
            )

            if text.strip():
                full_text += f"\n--- Page {page_number} ---\n"
                full_text += text

    return full_text


def load_all_pdfs(folder="documents"):
    documents = []
    
    # Recherche des PDF dans les dossiers A, B et C
    pdf_files = Path(folder).rglob("*.pdf")
    
    for pdf_file in pdf_files:
        print(f"\nLecture du document : {pdf_file.name}")

        try:
            text = extract_text_from_pdf(pdf_file)

            documents.append({
                "filename": pdf_file.name,
                "content": text
            })

            print(f"Nombre de caractères extraits : {len(text)}")

        except Exception as error:
            print(f"Erreur avec {pdf_file.name} : {error}")

    return documents
