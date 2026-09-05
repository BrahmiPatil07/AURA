import os
from pypdf import PdfReader
from docx import Document


DOCUMENTS_FOLDER = "documents"
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def read_document(filename):
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(DOCUMENTS_FOLDER, safe_filename)

    if not os.path.isfile(file_path):
        return f"File '{safe_filename}' was not found."

    extension = os.path.splitext(safe_filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return "Unsupported file type. Use TXT, PDF, or DOCX."

    try:
        if extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        elif extension == ".pdf":
            reader = PdfReader(file_path)
            text = []

            for page in reader.pages:
                text.append(page.extract_text() or "")

            return "\n".join(text)

        elif extension == ".docx":
            document = Document(file_path)
            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

    except Exception as error:
        return f"Could not read the file: {error}"