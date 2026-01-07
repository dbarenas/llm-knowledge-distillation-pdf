from __future__ import annotations

import logging
from pathlib import Path

import pdfplumber

from ts_pdf_pipeline.domain.exceptions import LoaderError
from ts_pdf_pipeline.domain.models import Document
from ts_pdf_pipeline.utils.hashing import sha256_text

logger = logging.getLogger(__name__)


class PDFPlumberLoader:
    def load(self, pdf_path: Path) -> Document:
        if not pdf_path.exists():
            raise LoaderError(f"PDF not found: {pdf_path}")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pages_text = [page.extract_text() or "" for page in pdf.pages]
        except Exception as exc:  # pragma: no cover - pdfplumber internal
            raise LoaderError("Failed to read PDF") from exc

        text = "\n".join(pages_text).strip()
        doc_hash = sha256_text(text)
        logger.info("Loaded PDF %s (hash=%s)", pdf_path, doc_hash)
        return Document(pdf_path=pdf_path, text=text, doc_hash=doc_hash)
