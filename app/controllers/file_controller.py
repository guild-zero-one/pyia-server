"""File Controller"""

import os
from fastapi import status, HTTPException, UploadFile


async def create_file(file: UploadFile):
    try:
        path = os.path.join(os.getcwd(), "app", "pdf")

        if not os.path.exists(path):
            os.makedirs(path)

        pdf_file = os.path.join(path, file.filename)

        with open(pdf_file, "wb") as p:
            pdf = await file.read()
            p.write(pdf)

        return {"message": "Arquivo salvo com sucesso!", "filename": file.filename}

        if not os.path.exists(pdf_file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao salvar o arquivo.",
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e)}",
        )
