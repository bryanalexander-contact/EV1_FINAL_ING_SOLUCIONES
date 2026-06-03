import os
from pathlib import Path
from typing import Optional
import pypdf

def extract_text(pdf_path: str) -> str:
    """Extract and return plain text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        The concatenated textual content of all pages.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the PDF cannot be read.
    """
    if not Path(pdf_path).is_file():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    try:
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            text_parts = []
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text_parts.append(page.extract_text() or "")
            return "\n".join(text_parts).strip()
    except Exception as e:
        raise ValueError(f"Failed to read PDF '{pdf_path}': {e}")
