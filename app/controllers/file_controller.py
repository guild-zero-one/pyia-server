"""File Controller"""

from fastapi import HTTPException, UploadFile, status

from app.manager.path_manager import PathManager
from app.utils import pdf_extraction

path_manager = PathManager()


async def create_file(type: str, file: UploadFile):
    try:
        pdf_path = path_manager.create_path(path_manager.path_pdf, file)

        with open(pdf_path, "wb") as p:
            pdf = await file.read()
            p.write(pdf)

        exists_path = path_manager.exists_path(pdf_path)

        if not exists_path:
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
        path_manager.remove_path(pdf_path)
        path_manager.remove_path(path_manager.path_product)
