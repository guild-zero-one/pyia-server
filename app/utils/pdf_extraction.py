"""PDF Extraction"""

import os
import fitz

from fastapi import HTTPException, status, UploadFile

from app.utils import test


def extract_text(pdf_file_path: str):
    if not os.path.exists(pdf_file_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo não foi encontrado",
        )

    try:
        with fitz.open(pdf_file_path) as doc:
            for page in doc:
                blocks = page.get_text("text")
                remove_data = blocks.split("\nIPI\nICMS")
                remove_data = remove_data[1].split("RESERVADO AO FISCO")

            response = test.text_to_dataframe(remove_data[0])
        print(response)
        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar o PDF: {str(e)}",
        )
