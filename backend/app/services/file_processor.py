from docx import Document
from io import BytesIO
import fitz
from typing import Union

def read_docx(content: bytes) -> str:
    """
    Extracts text from a DOCX file.

    Args:
        content (bytes): The byte content of the DOCX file.

    Returns:
        str: The extracted text from the DOCX file.
    """

    doc = Document(BytesIO(content))
    return "\n".join([p.text for p in doc.paragraphs])

def read_txt(content: bytes) -> str:
    """
    Extracts text from a TXT file.

    Args:
        content (bytes): The byte content of the TXT file.

    Returns:
        str: The extracted text from the TXT file.
    """

    return content.decode("utf-8")

def read_pdf(content: bytes) -> str:
    """
    Extracts text from a PDF file.

    Args:
        content (bytes): The byte content of the PDF file.

    Returns:
        str: The extracted text from the PDF file.
    """

    text = ""
    with fitz.open(stream=BytesIO(content), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text")
    return text

def process_file(filename: str, content: bytes) -> Union[str, None]:
    """
    Extracts text from a file based on its extension (DOCX, TXT, PDF).

    Args:
        filename (str): The name of the file, used to determine its extension.
        content (bytes): The byte content of the file.

    Returns:
        Union[str, None]: The extracted text if the file format is supported, 
                           otherwise returns "Unsupported file type".
    """

    ext = filename.lower().split(".")[-1]
    
    if ext == "docx":
        return read_docx(content)
    elif ext == "txt":
        return read_txt(content)
    elif ext == "pdf":
        return read_pdf(content)
    
    return "Unsupported file type"