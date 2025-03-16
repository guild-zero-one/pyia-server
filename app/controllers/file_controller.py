"""File Controller"""

import os
from fastapi import status, HTTPException, UploadFile

from app.utils import pdf_extraction


async def create_file(type: str, file: UploadFile):
    try:
        path = os.path.join(os.getcwd(), "app", "pdf")

        if not os.path.exists(path):
            os.makedirs(path)

        pdf_path = os.path.join(path, file.filename)

        with open(pdf_path, "wb") as p:
            pdf = await file.read()
            p.write(pdf)

        if not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao salvar o arquivo",
            )

        response = pdf_extraction.extract_text(type, pdf_path)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e)}",
        )
    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
