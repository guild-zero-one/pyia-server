"""PathManager"""

import os

from fastapi import UploadFile


class PathManager:
    def __init__(self):
        self.path_pdf = os.path.join(os.getcwd(), "app", "pdf")
        self.path_product = os.path.join(
            os.getcwd(), "app", "upload", "products.txt"
        )
        self.path_prompt = os.path.join(
            os.getcwd(), "app", "gemini", "criacao_produtos.txt"
        )

    def read_path(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as path_file:
            return path_file.read()

    def exists_path(self, path: str) -> bool:
        return os.path.exists(path)

    def create_path(self, path: str, file: UploadFile) -> str:
        return os.path.join(path, file.filename)

    def remove_path(self, path: str) -> bool:
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
