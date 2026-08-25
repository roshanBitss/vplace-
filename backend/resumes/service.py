import pymupdf


def extract_text_from_pdf(file) -> str:
    """
    Extract text from a PDF resume.

    Args:
        file: Django UploadedFile, FieldFile, or file path

    Returns:
        str: Extracted text from all PDF pages
    """
    # If it's a Django file object, reset stream pointer
    if hasattr(file, "seek"):
        file.seek(0)

    # Open PDF document safely
    if isinstance(file, str):
        pdf_document = pymupdf.open(file)
    elif hasattr(file, "path"):
        pdf_document = pymupdf.open(file.path)
    elif hasattr(file, "read"):
        pdf_document = pymupdf.open(stream=file.read(), filetype="pdf")
    else:
        pdf_document = pymupdf.open(file)

    extracted_text = ""
    for page in pdf_document:
        # pyrefly: ignore [unsupported-operation]
        extracted_text += page.get_text()

    pdf_document.close()
    return extracted_text.strip()
