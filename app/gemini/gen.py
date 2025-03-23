from fastapi import HTTPException, status
from google import genai

from app.config import GEMINI_API_KEY
from app.manager.path_manager import PathManager
from app.utils import json_transform

path_manager = PathManager()

client = genai.Client(api_key=GEMINI_API_KEY)


def gen_json():
    try:
        prompt_content = path_manager.read_path(path_manager.path_prompt)
        product_content = path_manager.read_path(path_manager.path_product)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{prompt_content}:\n\n{product_content}",
        )

        return json_transform.convert_json(response.text)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e)}",
        )
