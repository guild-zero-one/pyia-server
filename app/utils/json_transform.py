import json
from typing import List


def convert_json(gen_json: str) -> List[dict]:
    """
    Convert a JSON string to a list of dictionaries.

    Parameters:
    - gen_json: JSON string.

    Returns:
    - List of dictionaries.
    """
    json_str = gen_json.strip("```json").strip("```").strip()

    convert_json = json.loads(json_str)

    return convert_json
