"""File Routes"""

from fastapi import APIRouter, UploadFile, status

from app.controllers import file_controller

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    "/{type}",
    status_code=status.HTTP_200_OK,
)
async def create_file(type: str, file: UploadFile):
    """Create File"""
    return await file_controller.create_file(type=type, file=file)
