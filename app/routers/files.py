"""File Routes"""

from fastapi import APIRouter, UploadFile, File, status

from app.controllers import file_controller

router = APIRouter(prefix="/files")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_file(file: UploadFile):
    """Create File"""
    return await file_controller.create_file(file=file)
