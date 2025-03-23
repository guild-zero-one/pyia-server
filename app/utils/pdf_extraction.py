"""PDF Extraction"""

import os

import fitz
from fastapi import HTTPException, status

from app import modules


def extract_text(type: str, pdf_path: str):
    if not hasattr(modules, type):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Módulo {type} não encontrado",
        )

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo não foi encontrado",
        )

    try:
        with fitz.open(pdf_path) as doc:
            content = ""

            for page in doc:
                content += page.get_text("text")

            module = getattr(modules, type)

            response = module.create_df(content)

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar o PDF: {str(e)}",
        )
